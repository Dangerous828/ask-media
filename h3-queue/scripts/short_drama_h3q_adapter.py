#!/usr/bin/env python3
"""short-drama-produce adapter for the Windows h3q queue.

Reads the adapter JSON contract on stdin, submits only through h3qc/h3qg on
win-desktop, records the queue id before polling, and collects without resubmit.
No credentials are accepted in the job or adapter config.

Video workflows: `ref2va`（单镜，默认）与 `multishot`（多窗容器）。两者走同一条
路径——参考准入、闸门留档、运行记录、取回校验完全一致；multishot 额外接受
`frames_per_shot` / `shot_count` / `reference_image_size`，并豁免闸门的结构项
（两窗裸正文无法满足单镜段名规则），台词类硬规则仍然生效。不要再写脚本直提
multishot 绕过本 adapter。

`reference_image_size`（multishot，match|max，默认 match）原样透传到渲染器：
match 把参考压到生成画布（省显存、快），max 保留参考原生像素（≤2048，清晰但慢）。
`same_scene_continuous=true` 只在显式声明且 workflow=multishot 时生效：要求
reference_bindings 里至少一张身份参考，并用明确的 `scene_anchor_index` 指向
已准入的场景/构图锚（may_control 声明、must_not_control 未否认）。换场或硬切
的作业不声明该参数，行为不变；非 multishot 显式 true 直接拒绝。
"""
import json
import hashlib
import importlib.util
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import time
import uuid

HOST = os.environ.get("H3Q_SSH_HOST", "win-desktop")
PYTHON = os.environ.get(
    "H3Q_REMOTE_PYTHON",
    r"E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe",
)
CLI = os.environ.get("H3Q_REMOTE_CLI", r"E:\H3-Studio\scripts\h3qc.py")
REF_CLI = os.environ.get("H3Q_REMOTE_REF_CLI", r"E:\H3-Studio\scripts\h3qg.py")
REMOTE_ROOT = os.environ.get("H3Q_REMOTE_ROOT", r"E:\H3-Studio\short-drama")
COMFY_INPUT = os.environ.get(
    "H3Q_COMFY_INPUT",
    r"E:\ComfyUI\ComfyUI_windows_portable\ComfyUI\input",
)
POLL_SECONDS = int(os.environ.get("H3Q_ADAPTER_POLL_SECONDS", "15"))
# Existing dialogue safeguards retain their submit policy. Photography reminders
# G34/G35 require shot/reference context; word matches cannot reject a legal
# side-on tracking shot or an intentional screen presentation.
BLOCKING_GATE_WARNINGS = {"G17", "G18"}
VIDEO_GATE = os.environ.get(
    "H3_VIDEO_GATE",
    str(Path.home() / ".agents/skills/h3-video-gate/scripts/h3_gate.py"),
)
def _ref_gate_path():
    """共享参考准入闸门。显式环境变量优先，否则取第一个存在的安装位置。"""
    explicit = os.environ.get("SHORT_DRAMA_REF_GATE", "").strip()
    if explicit:
        return Path(explicit).expanduser()
    # 技能中枢是目前唯一真实维护的安装位置；~/.agents 只是历史同步目标，
    # 可能不存在或是过期副本，放在后面仅作兼容。
    candidates = (
        Path.home() / ".skills/hub/drama-skills/skills/short-drama-review/scripts/ref_gate.py",
        Path.home() / ".agents/skills/drama-skills/skills/short-drama-review/scripts/ref_gate.py",
        Path.home() / ".agents/skills/short-drama-review/scripts/ref_gate.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


REF_GATE = _ref_gate_path()


# Video render tiers. pdd is the only engine (2026-11-15 下线 lu2/legacy):
# draft = first pass only (1024x576, no upscale); final = two-pass upscale to the
#         job's target size, capped at 1536x864 on 16GB. Default is draft so a
#         job that says nothing renders cheaply and the expensive tier needs an
#         explicit, visible parameter in the prepare preview.
VIDEO_TIERS = ("draft", "final")
DEFAULT_VIDEO_TIER = "draft"
# 渲染引擎。2026-11-07 实测：pdd（官方 PDD 8 步蒸馏）比旧的 lu2 turbo 4 步
# 快约 10 倍，且是唯一能让「两车之间的窄缝」这类空间关系成立的组合——4 步
# 544p 蒸馏会让空间/透视崩坏（旧版把窄缝画成标准车位）。
# 16GB 上限：362 帧二采最多 1536x864（实测峰值 15.55 GiB / 设备 15.92）。
VIDEO_ENGINES = ("pdd",)
# 多镜容器：同机位连续动作两窗一次生成，接缝由 H3MultishotMemorySampler(v2, context_pin) 内部处理。
# 它是 video 的一种 workflow，不是独立通道——参考准入、闸门、运行记录、取回
# 全部走本 adapter 的同一条路径，不允许脚本旁路直提。
VIDEO_WORKFLOWS = ("ref2va", "multishot", "fl2va")
DEFAULT_VIDEO_WORKFLOW = "ref2va"
DEFAULT_VIDEO_ENGINE = "pdd"
PDD_UPSCALE_CEILING = (1536, 864)
# multishot 参考图编码口径。match = 压到生成画布（省显存、快，默认）；
# max = 参考图原生像素（≤2048）不缩（清晰，但后续窗 offload 更重更慢）。
REFERENCE_IMAGE_SIZES = ("match", "max")


def video_tier(params):
    tier = params.get("tier") or DEFAULT_VIDEO_TIER
    if tier not in VIDEO_TIERS:
        raise RuntimeError(f"video tier must be one of {VIDEO_TIERS}, got {tier!r}")
    return tier


def video_engine(params):
    engine = (params.get("engine") or DEFAULT_VIDEO_ENGINE).strip().lower()
    if engine not in VIDEO_ENGINES:
        raise RuntimeError(f"video engine must be one of {VIDEO_ENGINES}, got {engine!r}")
    return engine


def video_workflow(params):
    wf = (params.get("workflow") or DEFAULT_VIDEO_WORKFLOW).strip().lower()
    if wf not in VIDEO_WORKFLOWS:
        raise RuntimeError(f"video workflow must be one of {VIDEO_WORKFLOWS}, got {wf!r}")
    return wf


def reference_image_size(params):
    """multishot 参考图编码口径：match（默认，压到生成画布）或 max（原生 ≤2048）。"""
    value = params.get("reference_image_size")
    if value in (None, ""):
        return "match"
    text = str(value).strip().lower()
    if text not in REFERENCE_IMAGE_SIZES:
        raise RuntimeError(
            f"reference_image_size must be one of {REFERENCE_IMAGE_SIZES}, got {value!r}")
    return text


# 场景/构图锚的用途词表。只看 reference_bindings 的 may_control / must_not_control
# （创作文档的用途声明），不猜文件名、不看 label。命中任一即视为声明了地理/构图用途。
SCENE_ANCHOR_CONTROL_TERMS = (
    "场景", "构图", "取景", "地理", "环境", "空间", "机位", "布景", "陈设", "布局", "位置",
    "scene", "composition", "geography", "environment", "layout",
    "setting", "staging", "camera", "framing",
)
IDENTITY_CONTROL_TERMS = (
    "身份", "人物", "角色", "脸", "骨相", "造型", "服装", "发型", "体型",
    "identity", "character", "face", "likeness", "wardrobe", "costume", "hair",
)


def same_scene_continuous(params):
    """显式声明 same_scene_continuous 时才启用同场连续锚校验。"""
    value = params.get("same_scene_continuous")
    if value is None or value == "":
        return False
    if value is True:
        return True
    if value is False:
        return False
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("true", "1", "yes"):
            return True
        if text in ("false", "0", "no"):
            return False
    raise RuntimeError(f"same_scene_continuous must be a boolean, got {value!r}")


def _controls_with(binding, terms):
    """The binding declares one of `terms` and does not deny it."""
    may = binding.get("may_control") or []
    must = binding.get("must_not_control") or []

    def hits(values):
        folded = [str(item).casefold() for item in values]
        return any(term.casefold() in value for term in terms
                   for value in folded)

    return hits(may) and not hits(must)


def _controls_scene(binding):
    return _controls_with(binding, SCENE_ANCHOR_CONTROL_TERMS)


def _controls_identity(binding):
    return _controls_with(binding, IDENTITY_CONTROL_TERMS)


def scene_anchor_binding(bindings):
    """The first picture binding that carries the accepted scene/composition anchor."""
    for binding in bindings or []:
        if not isinstance(binding, dict) or binding.get("role") != "reference_image":
            continue
        if _controls_scene(binding):
            return binding
    return None


def verify_same_scene_anchor(params, bindings):
    """条件化校验：同场连续 multishot 必须有已准入的地理/构图场景锚。

    只在 same_scene_continuous=true 且 workflow=multishot 时生效；换场/硬切不声明
    该参数即完全跳过。bindings 已在 verify_reference_acceptance 里逐张过准入闸，
    因此这里的任何匹配项都是已准入的参考。
    """
    explicit = same_scene_continuous(params)
    index = params.get("scene_anchor_index")
    if not explicit:
        if index not in (None, ""):
            raise RuntimeError(
                "scene_anchor_index 只能在 same_scene_continuous=true 时使用")
        return
    if video_workflow(params) != "multishot":
        raise RuntimeError(
            "same_scene_continuous 只对 workflow=multishot 生效；换场/硬切不要声明")
    bindings = bindings or []
    if not bindings:
        raise RuntimeError(
            "same_scene_continuous=true requires explicit reference_bindings with "
            "may_control/must_not_control, so the scene anchor and identity reference "
            "can be verified")
    if index in (None, ""):
        raise RuntimeError(
            "same_scene_continuous=true requires scene_anchor_index: the 1-based "
            "position of the accepted scene/composition anchor in reference_bindings")
    if isinstance(index, bool) or not isinstance(index, int) or not 1 <= index <= len(bindings):
        raise RuntimeError(
            "scene_anchor_index must be the 1-based position of a reference in "
            f"reference_bindings (got {index!r}, {len(bindings)} bindings)")
    candidate = bindings[index - 1]
    if (not isinstance(candidate, dict)
            or candidate.get("role") != "reference_image"
            or not _controls_scene(candidate)):
        raise RuntimeError(
            "scene_anchor_index points at a reference that does not declare a "
            "scene/composition control scope (may_control); bind the accepted "
            "scene or start frame as reference_image and declare its 用途")
    identity = any(
        isinstance(binding, dict)
        and binding.get("role") == "reference_image"
        and _controls_identity(binding)
        for position, binding in enumerate(bindings, 1)
        if position != index
    )
    if not identity:
        raise RuntimeError(
            "same_scene_continuous=true also requires an identity reference: another "
            "reference_image whose may_control names 身份/人物/脸/造型 (and does not "
            "deny it). A scene anchor alone cannot carry character consistency")


def reference_subjects(params):
    """multishot 参考图如何分组成人物，如 '1,1'（两图两人）或 '3,3'。

    空 = 交给节点默认（全部参考都声明为 <Subject 1>）。注意 V2 记忆采样器没有
    「这张图只当场景、不当人」的输入：同场连续任务里的场景锚仍会占一个 subject
    名额，这里只透传创作者的显式分组，不按图片张数或文件名自动编造。
    """
    value = params.get("reference_subjects")
    if value in (None, ""):
        return ""
    text = str(value).strip()
    parts = [p for p in text.replace(" ", "").split(",") if p]
    if not parts or any(not p.isdigit() or int(p) < 1 for p in parts):
        raise RuntimeError(
            f"reference_subjects 必须是正整数的逗号列表（如 '1,1'），收到 {value!r}")
    return ",".join(parts)


def multishot_argv(params):
    """multishot 容器的 CLI 参数：单窗帧数 + 窗数 + 画布 + 参考图编码口径。

    h3q 的 multishot 分支没有 pdd 二采；尺寸直接给 --width/--height。
    """
    per = int(params.get("frames_per_shot") or 226)
    count = int(params.get("shot_count") or 2)
    if per < 5 or (per - 5) % 17 != 0:
        raise RuntimeError(f"frames_per_shot={per} 不是 17k+5")
    if count < 1 or count > 8:
        raise RuntimeError(f"shot_count must be 1..8, got {count}")
    # 总帧数 = 每窗 × 窗数 −（窗数 − 1）：窗与窗共享一帧接缝。
    # 226×2−1 = 451 是 16GB 卡两窗跑满的实测形状（峰值 15096 MiB / 设备 15.92 GiB）。
    # 2026-11-18: multishot v2 放行该上限——窗数与每窗帧数由创作者按实际显存自行决定，
    # adapter 只告警不拦截。只有未显式声明 workflow=multishot 的调用仍按上限拦截，
    # 防止非多镜作业误用本函数绕过显存保护。
    total = per * count - (count - 1)
    if total > 451 and video_workflow(params) != "multishot":
        raise RuntimeError(
            "多镜容器总帧数 %d 超过 16GB 卡实测上限 451（两窗 226+226 正是跑满的 451 帧形状，"
            "峰值 15096 MiB / 设备 15.92 GiB）" % total)
    if total > 451:
        print(
            "h3q adapter: multishot 总帧数 %d 超过 16GB 卡实测上限 451，"
            "按放行策略继续提交（请确认显存充足）。" % total,
            file=sys.stderr,
        )
    width, height = int(params["width"]), int(params["height"])
    for value, name in ((width, "width"), (height, "height")):
        if value % 32:
            raise RuntimeError(f"{name}={value} 必须是 32 的倍数")
    argv = ["--workflow", "multishot",
            "--frames-per-shot", str(per),
            "--shot-count", str(count),
            "--width", str(width), "--height", str(height),
            "--reference-image-size", reference_image_size(params)]
    subjects = reference_subjects(params)
    if subjects:
        argv += ["--reference-subjects", subjects]
    # 权重装不下时用分块 FFN 保持驻留；渲染器默认 on，这里只在显式声明时透传。
    chunk = (params.get("auto_chunk_ffn") or "").strip().lower()
    if chunk:
        if chunk not in ("on", "off"):
            raise RuntimeError(
                f"auto_chunk_ffn must be 'on' or 'off', got {params.get('auto_chunk_ffn')!r}")
        argv += ["--auto-chunk-ffn", chunk]
    return argv


def frames_for(params):
    """pdd_lu 忽略 --seconds，长度只认 17k+5 的 --frames。"""
    from math import floor
    sec = float(params.get("duration") or params.get("seconds") or 5)
    raw = round(sec * 24)
    return 17 * ((raw - 5 + 16) // 17) + 5


def fl2va_argv(params):
    """首帧/首尾帧任务参数：走默认分支，不能带 --workflow。

    pdd_lu 调的 pdd_render_ref.py 没有 --first-frame/--last-frame，也不转发；
    2026-11-22 实测同一对首尾帧：pdd_lu 产物首帧与指定首帧 MAD 43.0，默认分支
    3.86。所以带 first_frame 的任务一律落到 h3_render_ref.py，排除 --workflow
    后渲染器按两帧自动选 i2va（单首帧）或 fl2va（首尾帧）。
    """
    width, height = int(params["width"]), int(params["height"])
    for value, name in ((width, "width"), (height, "height")):
        if value % 32:
            raise RuntimeError(f"{name}={value} 必须是 32 的倍数")
    # 默认分支无二采，档位在这里没有意义；显式端口/步数交给调用方。
    argv = ["--width", str(width), "--height", str(height),
            "--frames", str(frames_for(params)),
            "--sol-profile", "off"]
    return argv


def tier_argv(params, job_id="job"):
    """pdd 档位 CLI 参数：draft 首采、final 二采；长度只认 17k+5 帧数。"""
    tier = video_tier(params)
    width, height = int(params["width"]), int(params["height"])
    engine = video_engine(params)  # 当前仅 pdd；保留校验以挡未知引擎
    assert engine == "pdd"
    cw, ch = PDD_UPSCALE_CEILING
    if tier == "final" and width * height > cw * ch:
        raise RuntimeError(
            "PDD 二采在 16GB 上最多 %dx%d（362 帧实测峰值 15.55/15.92 GiB）；"
            "请求 %dx%d 会 OOM" % (cw, ch, width, height))
    argv = ["--workflow", "pdd_lu", "--frames", str(frames_for(params)),
            "--sol-profile", "off"]
    if tier == "final":
        argv += ["--out-width", str(width), "--out-height", str(height)]
    else:
        argv += ["--no-upscale"]
    return argv


def run(argv, check=True):
    result = subprocess.run(
        argv, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if check and result.returncode:
        raise RuntimeError(f"command failed with exit code {result.returncode}: {argv[0]}")
    return result


def ssh(remote_command, check=True):
    return run(["ssh", HOST, remote_command], check=check)


def scp(local, remote, upload=True):
    source = str(local)
    destination = f"{HOST}:{remote}"
    argv = ["scp", source, destination] if upload else ["scp", destination, source]
    return run(argv)


def win_join(root, *parts):
    return str(PureWindowsPath(root).joinpath(*parts))


def safe_id(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")[:100]


def write_handle(path, provider_job_id):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(
        json.dumps({"provider_job_id": provider_job_id}, ensure_ascii=True), encoding="utf-8"
    )
    os.replace(temporary, target)


def queue_show(provider_job_id):
    command = f'"{PYTHON}" -s "{CLI}" show {provider_job_id}'
    result = ssh(command, check=False)
    start = result.stdout.find("{")
    if start < 0:
        raise RuntimeError("h3q show returned no JSON")
    return json.loads(result.stdout[start:])


def prepare_reference(source, output_root, index, lossless=False, modality="video"):
    """Images upload the source unchanged; videos retain their board/frame policy."""
    if modality == "image":
        return source
    if lossless:
        destination = output_root / f"reference-{index}.png"
        # `sips -Z` enlarges as well as shrinks, so a bare -Z 1344 resampled an
        # 896x512 scene plate up to 1344x768 and shrank a 1536x864 real last
        # frame down to 1344. Either way the pixels handed to the model were no
        # longer the ones the creator reviewed - for the flf relay that is the
        # whole point of the handoff. Keep native size; only bound absurd input.
        cmd = ["sips", "-s", "format", "png", str(source), "--out", str(destination)]
        if long_edge(source) > REF_SAFE_LONG_EDGE:
            cmd = ["sips", "-Z", str(REF_SAFE_LONG_EDGE), "-s", "format", "png",
                   str(source), "--out", str(destination)]
        run(cmd)
        return destination
    destination = output_root / f"reference-{index}.jpg"
    run([
        "sips", "-Z", "768", "-s", "format", "jpeg",
        "-s", "formatOptions", "80", str(source), "--out", str(destination),
    ])
    return destination


REF_SAFE_LONG_EDGE = int(os.environ.get("H3Q_REF_LONG_EDGE", "2048"))


def long_edge(path):
    """Long edge in pixels via sips properties; 0 when unknowable."""
    try:
        result = run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
                     check=False)
    except Exception:  # noqa: BLE001 - unreadable geometry must not block upload
        return 0
    sizes = []
    for line in (result.stdout or "").splitlines():
        parts = line.split(":")
        if len(parts) == 2 and parts[0].strip().startswith("pixel"):
            try:
                sizes.append(int(parts[1].strip()))
            except ValueError:
                pass
    return max(sizes) if sizes else 0


def lossless_binding(binding):
    """Video-only policy: native PNG frames or 768 JPEG q80 boards.

    Split, per recorded measurement:
      * first/last frames and start/state/composition references -> PNG, native
        size. These ARE the delivered pixels; re-encoding them compounds loss
        every generation and breaks the flf relay's "same pixels the creator
        reviewed" contract.
      * identity / asset / prop / scene boards -> long-edge 768 + JPEG q80.
        `video-studio/SKILL.md` and `ref_guard.py` record that compressing these
        makes the result cleaner, because board noise stops being amplified.
        Measured on Qwen Image 2.1 Turbo stills; H3 video is not yet confirmed
        either way, so the A/B that decides it is tracked in
        `项目开发/参考图上传口径实测-20261108.md`.

    Override for experiments: H3Q_REF_LOSSLESS=1 forces PNG for everything,
    H3Q_REF_LOSSLESS=0 forces the old JPEG path for everything.
    """
    if os.environ.get("H3Q_REF_LOSSLESS", "").strip() in ("0", "false", "no"):
        return False
    # Default is now LOSSLESS PNG for every reference, including identity /
    # asset / scene boards. Rationale: the old 768 long-edge JPEG q80 re-encode
    # was measured only on Qwen Image stills and never confirmed on the H3 video
    # path; it also silently enlarged small boards (`sips -Z 768` upscales) and
    # threw away 5-7x the bytes. Boards are consistency anchors for the model,
    # so feeding the original pixels is the safe default. The only transform
    # kept is a PNG downscale that fires ONLY when a board exceeds the safe
    # long edge (2048) -- never an upscale, never a JPEG.
    # H3Q_REF_LOSSLESS=0 restores the old split (frames PNG, boards JPEG q80).
    if os.environ.get("H3Q_REF_LOSSLESS", "").strip() in ("1", "true", "yes", "all"):
        return True
    return True


def verify_reference_acceptance(job):
    """Recheck pinned project evidence before the first upload or remote call."""
    bindings = job.get("reference_bindings") or []
    if not REF_GATE.is_file():
        raise RuntimeError(f"shared reference acceptance gate is missing: {REF_GATE}")
    argv = [
        "python3", str(REF_GATE), "check",
        "--project-root", str(job["project_root"]),
        "--modality", str(job["modality"]),
        "--references", *[str(binding["path"]) for binding in bindings],
        "--parameters", json.dumps(job.get("parameters") or {}, ensure_ascii=False),
        "--bindings", json.dumps(bindings, ensure_ascii=False),
    ]
    completed = run(argv, check=False)
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError:
        report = {}
    if completed.returncode == 0 and report.get("allowed") is True:
        return
    code = str(report.get("code") or "").strip()
    message = str(report.get("message") or "").strip()
    raw = (completed.stdout + completed.stderr).strip()
    if code and message:
        detail = f"{code} — {message}"
    elif code:
        detail = code
    elif message:
        detail = message
    else:
        detail = raw or "gate returned no diagnostic"
    raise RuntimeError("reference acceptance gate rejected the pinned inputs: " + detail[:800])


def validate_ref_guard_exception(job):
    """Bind a creator-approved image-only guard exception to one reference's bytes."""
    exception = (job.get("parameters") or {}).get("ref_guard_exception")
    if exception is None:
        return False
    required = {"slot_id", "reference_sha256", "creator_ack", "reason"}
    if not isinstance(exception, dict) or set(exception) != required:
        raise RuntimeError("ref_guard exception requires slot, hash, creator acknowledgement and reason")
    if job.get("modality") != "image":
        raise RuntimeError("ref_guard exception is only supported for image jobs")
    bindings = job.get("reference_bindings") or []
    if len(bindings) != 1 or bindings[0].get("role") != "reference_image":
        raise RuntimeError("ref_guard exception requires exactly one reference image")
    binding = bindings[0]
    if exception.get("slot_id") != binding.get("slot_id"):
        raise RuntimeError("ref_guard exception slot does not match the reference")
    if exception.get("creator_ack") is not True:
        raise RuntimeError("ref_guard exception requires creator acknowledgement")
    reason = exception.get("reason")
    if not isinstance(reason, str) or len(reason.strip()) < 8:
        raise RuntimeError("ref_guard exception requires a specific reason")
    expected = exception.get("reference_sha256")
    if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
        raise RuntimeError("ref_guard exception reference hash is invalid")
    root = Path(job["project_root"]).resolve()
    source = (root / binding["path"]).resolve()
    if not source.is_relative_to(root) or not source.is_file():
        raise RuntimeError("ref_guard exception reference is not in the project snapshot")
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise RuntimeError("ref_guard exception reference hash mismatch")
    return True


def gate_blockers(findings, workflow=""):
    """从闸门 findings 里取出真正阻断提交的条目。

    2026-11-19 起多窗脚本走 `--mode multishot`：闸门用 G39（窗口数/窗口开头/
    不混单镜段名）和 G40（逐窗对白格式、<d> 外中文、每窗 15s）检查它自己的格式，
    不再有「结构项整块豁免」。`workflow` 参数保留给调用方兼容，当前不改变行为。
    """
    return [
        f for f in findings or []
        if f.get("level") == "error" or f.get("rule") in BLOCKING_GATE_WARNINGS
    ]


def expected_frames(job):
    params = job["parameters"]
    if video_workflow(params) == "multishot":
        per = int(params.get("frames_per_shot") or 226)
        count = int(params.get("shot_count") or 2)
        return per * count - (count - 1)
    requested = round(float(params["duration"]) * 24)
    return 17 * ((requested - 5 + 16) // 17) + 5


DIALOGUE_RE = re.compile(r"<d>\s*\[[^]]+\]\s*(.*?)</d>", re.DOTALL)


def spoken_key(value):
    """Match VID-25: punctuation and spacing do not change a line's identity."""
    return re.sub(r"[^一-鿿0-9A-Za-z]", "", value)


def verify_dialogue_against_screenplay(job):
    """Reject invented or actor-prefixed dialogue in the exact uploaded prompt.

    prepare pins 剧本.md for creator-first video jobs. Older stored jobs may not
    have it in their snapshot; their already-confirmed fingerprint remains valid,
    so a missing file is reported by the caller instead of silently claimed as a
    completed comparison.
    """
    source = job.get("source")
    if not source or PurePosixPath(source).name != "视频提示词.md":
        return "not_applicable"
    screenplay = Path(job["project_root"]) / PurePosixPath(source).parent / "剧本.md"
    if not screenplay.is_file():
        return "not_checked_missing_screenplay"
    normalized_screenplay = spoken_key(screenplay.read_text(encoding="utf-8"))
    for match in DIALOGUE_RE.finditer(job["prompt"]):
        line = match.group(1).strip()
        key = spoken_key(line)
        if len(re.findall(r"[一-鿿]", key)) < 4:
            continue
        if not key or key not in normalized_screenplay:
            raise RuntimeError(
                "uploaded Chinese dialogue is not verbatim in 剧本.md: " + line[:60]
            )
    return "checked"


MULTISHOT_SCRIPT_RULE = (
    "multishot 脚本格式：每个窗口写一段纯正文，窗口之间用单独一行 `---` 分隔，"
    "窗口数必须等于 shot_count。窗口正文不要以 `[` 或 `{` 开头"
    "（节点会把整份脚本当 JSON 解析，`[Shot 1] ...` 会被误判成数组并直接报错），"
    "也不要写 subject_definitions / integrated_multimodal_description 等段名——"
    "那些是单镜 ref/base 正文的格式，多窗每个窗口就是一条完整正文。"
)


def verify_multishot_script(prompt, shot_count):
    """多窗脚本必须在**上传前**就通过格式检查，而不是等 ComfyUI 报 execution_error。

    2026-11-19 EP004 v5 006/007 就是这样失败的：窗口正文以 `[Shot 1]` 开头，
    节点用 `text.startswith("[")` 判定成 JSON 数组，解析失败 → 9.6 秒后
    execution_error，白占一次 GPU 队列窗口。
    """
    text = (prompt or "").strip()
    if not text:
        raise RuntimeError("multishot 脚本为空。" + MULTISHOT_SCRIPT_RULE)
    count = int(shot_count or 2)
    windows = [w.strip() for w in re.split(r"(?m)^---\s*$", text)]
    windows = [w for w in windows if w]
    if len(windows) != count:
        raise RuntimeError(
            "multishot 脚本有 %d 个窗口，shot_count=%d。" % (len(windows), count)
            + MULTISHOT_SCRIPT_RULE)
    for index, window in enumerate(windows, 1):
        if window[0] in "[{":
            raise RuntimeError(
                "multishot 第 %d 个窗口以 %r 开头，节点会把它当 JSON 解析并失败。"
                % (index, window[0]) + MULTISHOT_SCRIPT_RULE)
        if re.match(r"(?i)^(subject_definitions|integrated_multimodal_description|"
                    r"summary|retention_analysis|detailed_description|"
                    r"overall_soundscape|non_diegetic_music)\s*:", window):
            raise RuntimeError(
                "multishot 第 %d 个窗口写了单镜段名；多窗窗口只写正文。"
                % index + MULTISHOT_SCRIPT_RULE)
    return len(windows)


def output_frame_bounds(job):
    """How many frames the delivered file may legitimately contain.

    The request formula is not the delivered length for the multishot container:
    the V2 sampler re-times each window onto the H3 VAE grid, so a 107f x 2
    request (formula 213) delivered 192f in the 2026-11-19 EP005 S-002 run.
    Treating the formula as exact rejects a render that actually succeeded.

    Non-multishot jobs keep the strict snapped-count contract: pdd honours
    `--frames` exactly, so a mismatch there is a real defect.
    """
    want = expected_frames(job)
    if video_workflow(job.get("parameters") or {}) != "multishot":
        return want, want
    per = int((job.get("parameters") or {}).get("frames_per_shot") or 226)
    # One window is the floor; the container cannot deliver more than it asked
    # for plus one frame of seam rounding.
    return min(per, want), want + 1


def verify_output(job, path):
    """A downloaded result must be real media: non-empty, decodable, and for video
    a plausible frame count with an audio stream (H3 renders sound in the same pass)."""
    if not path.is_file() or path.stat().st_size == 0:
        raise RuntimeError(f"h3q result is missing or empty: {path.name}")
    if job["modality"] != "video" or os.environ.get("H3Q_SKIP_OUTPUT_PROBE") == "1":
        return
    probe = run([
        "ffprobe", "-v", "error", "-count_packets", "-show_entries",
        "stream=codec_type,nb_read_packets", "-of", "json", str(path),
    ], check=False)
    if probe.returncode:
        raise RuntimeError(f"h3q result is not decodable media: {path.name}")
    streams = json.loads(probe.stdout or "{}").get("streams") or []
    video = [s for s in streams if s.get("codec_type") == "video"]
    if not video:
        raise RuntimeError(f"h3q result has no video stream: {path.name}")
    if not any(s.get("codec_type") == "audio" for s in streams):
        raise RuntimeError(f"h3q result has no audio stream: {path.name}")
    frames = int(video[0].get("nb_read_packets") or 0)
    low, high = output_frame_bounds(job)
    if not low <= frames <= high:
        raise RuntimeError(
            f"h3q result has {frames} frames, expected {low}..{high}: {path.name}")


def resolve_output(job, state, fallback=None):
    """Translate real h3q done records into a downloadable media path."""
    params = state.get("params") or {}
    if job["modality"] == "image" and params.get("out"):
        return params["out"]
    if fallback:
        return fallback
    raw = (state.get("output") or "").strip()
    saved = re.match(r"^saved\s+(.+?)\s+\d+\s+bytes(?:\s|$)", raw)
    if saved:
        return saved.group(1)
    if raw.startswith("COPY_OF_RECORD "):
        record = raw[len("COPY_OF_RECORD "):].strip()
        command = (
            f'"{PYTHON}" -c "import json;'
            f"print(json.load(open(r'{record}',encoding='utf-8'))['comfy_output'])\""
        )
        result = ssh(command)
        media = result.stdout.strip()
        if not media.lower().endswith(".mp4"):
            raise RuntimeError("h3q render record has no MP4 comfy_output")
        return media
    if raw.startswith("OUTPUT "):
        output = raw[len("OUTPUT "):].strip().replace("\\", "/")
        if output.lower().endswith((".png", ".mp4")):
            return output
    if raw.lower().endswith((".png", ".mp4")):
        return raw
    raise RuntimeError("completed h3q job has no downloadable media path")


def submit(job, workdir, prompt_remote, reference_args, gate_off=False):
    params = job.get("parameters") or {}
    modality = job["modality"]
    label = safe_id(job["job_id"])
    cli = REF_CLI if (reference_args.get("refs") or reference_args.get("first-frame")
                      or reference_args.get("last-frame")) else CLI
    if gate_off and (modality != "image" or not reference_args.get("refs")
                     or reference_args.get("first-frame")):
        raise RuntimeError("ref_guard exception requires one image reference on h3qg")
    argv = [f'"{PYTHON}"', "-s", f'"{cli}"', "submit", "--kind", modality]
    argv += ["--prompt-file", f'"{prompt_remote}"', "--label", f'"{label}"']
    argv += ["--idem-key", safe_id(f"{job['job_id']}-{job['run_id']}")]
    if modality == "image":
        output_remote = win_join(workdir, "result.png")
        argv += ["--out", f'"{output_remote}"']
        argv += ["--size", f"{int(params['width'])}x{int(params['height'])}"]
        for key, default in (("steps", 0), ("cfg", 3.5), ("loras", "none"), ("resolution", 0)):
            value = params.get(key)
            if value in (None, ""):
                value = default
            argv += [f"--{key}", subprocess.list2cmdline([str(value)])]
        if params.get("negative") not in (None, ""):
            argv += ["--negative", subprocess.list2cmdline([str(params["negative"])])]
    else:
        argv += ["--slug", f'"{label}"', "--version", f'"{safe_id(job["run_id"])}"']
        # 单首帧与首尾帧都不能走 pdd_lu：那个渲染器没有 --first-frame 参数。
        fl2va = bool(reference_args.get("first-frame"))
        if video_workflow(params) == "multishot":
            argv += multishot_argv(params)
        elif fl2va:
            argv += fl2va_argv(params)
        else:
            argv += tier_argv(params, job["job_id"])
        if video_workflow(params) == "multishot":
            pass  # multishot_argv 已给出单窗帧数；长度由窗数决定
        elif fl2va:
            pass  # fl2va_argv 已给出 --frames；默认分支无二采
        else:
            # pdd_lu 忽略 --seconds，长度只认 17k+5 的 --frames。
            argv += ["--frames", str(expected_frames(job))]
        output_remote = None
    for key in (("seed",) if modality == "image" else ("seed", "steps", "cfg")):
        if params.get(key) not in (None, ""):
            argv += [f"--{key}", str(params[key])]
    for flag, value in reference_args.items():
        if value:
            argv += [f"--{flag}", value]
    if gate_off:
        argv.append("--gate-off")
    result = ssh(" ".join(argv))
    match = re.search(r"\bjob\s+([0-9a-f]{8,32})\b", result.stdout, re.I)
    if not match:
        raise RuntimeError("h3q submit returned no queue id")
    return match.group(1), output_remote


def main():
    job = json.load(sys.stdin.buffer)
    if job.get("modality") not in ("image", "video"):
        raise RuntimeError("h3q adapter accepts image or video jobs")
    outputs = job.get("outputs") or []
    if len(outputs) != 1:
        raise RuntimeError("h3q adapter requires exactly one output per job")
    bindings = job.get("reference_bindings") or []
    if job["modality"] == "video" and not job.get("collect_provider_job_id"):
        roles = {binding.get("role") for binding in bindings}
        # Check the frame-pair rules before the general reference rule: a job
        # carrying last_frame + reference_image trips both, and the specific
        # message ("FL2VA takes first_frame + last_frame only") is the one that
        # tells the caller what to fix.
        if "last_frame" in roles and "reference_image" in roles:
            raise RuntimeError(
                "H3 video cannot mix last_frame and reference_image bindings; "
                "FL2VA takes first_frame + last_frame only"
            )
        if "last_frame" in roles and "first_frame" not in roles:
            raise RuntimeError(
                "last_frame requires a first_frame binding; FL2VA interpolates between two frames"
            )
        if {"first_frame", "reference_image"} <= roles:
            raise RuntimeError(
                "H3 video cannot mix first_frame and reference_image bindings; "
                "use reference_image for the entire full-reference group"
            )
    output_root = Path(job["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    upload_id = safe_id(job["job_id"])
    if job["modality"] == "image":
        upload_id = f"{upload_id[:32]}-{safe_id(job['run_id'])[:32]}-{uuid.uuid4().hex}"
    workdir = win_join(REMOTE_ROOT, upload_id)
    provider_job_id = job.get("collect_provider_job_id")

    if not provider_job_id:
        if job["modality"] == "video":
            if video_workflow(job["parameters"]) == "multishot":
                multishot_argv(job["parameters"])  # reject bad window maths before any upload
            else:
                if (job["parameters"] or {}).get("reference_image_size") not in (None, ""):
                    raise RuntimeError(
                        "reference_image_size 只对 workflow=multishot 生效；"
                        "ref2va 的参考图口径由渲染器固定。")
                _roles = {b.get("role") for b in bindings}
                if "first_frame" in _roles:
                    fl2va_argv(job["parameters"])  # 首帧任务走默认分支，提前挡尺寸错误
                else:
                    tier_argv(job["parameters"], job["job_id"])  # reject a bad tier before any upload
        if job["modality"] == "video":
            # 场景锚合同先于共享闸门：本地报错指名 binding 序号，共享闸门对
            # produce/MCP 仍是同一套兜底校验（参数与 bindings 原样传给 ref_gate）。
            verify_same_scene_anchor(job.get("parameters") or {}, bindings)
            if video_workflow(job["parameters"]) == "multishot":
                # 多窗脚本格式必须在 SSH/上传/入队之前失败，否则要等 ComfyUI
                # 跑到 node 30 才报 execution_error（2026-11-19 EP004 实证）。
                verify_multishot_script(
                    job.get("prompt"),
                    (job.get("parameters") or {}).get("shot_count") or 2)
        verify_reference_acceptance(job)
        gate_off = validate_ref_guard_exception(job)
        reference_args = {"refs": [], "first-frame": "", "last-frame": ""}
        reference_contract = []
        prepared_uploads = []
        reference_evidence = []
        project_root = Path(job["project_root"])
        for index, binding in enumerate(bindings, 1):
            role = binding.get("role")
            if role not in ("reference_image", "first_frame", "last_frame"):
                raise RuntimeError(f"h3q adapter does not support reference role {role}")
            source = project_root / binding["path"]
            prepared = prepare_reference(
                source, output_root, index, lossless=lossless_binding(binding),
                modality=job["modality"],
            )
            if job["modality"] == "image":
                remote_name = f"{upload_id}-{index}{source.suffix}"
            else:
                remote_name = f"{safe_id(job['run_id'])}-{index}-{prepared.name}"
            remote_path = win_join(COMFY_INPUT, remote_name)
            prepared_uploads.append((prepared, remote_path.replace("\\", "/")))
            reference_evidence.append({"source": binding["path"], "upload_name": remote_name,
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "uploaded_sha256": hashlib.sha256(prepared.read_bytes()).hexdigest()})
            reference_contract.append(
                f'<Picture {index}> "{binding["label"]}" ({role}); '
                f'may control: {", ".join(binding["may_control"])}; '
                f'must not control: {", ".join(binding["must_not_control"])}.'
            )
            if role == "first_frame":
                if reference_args["first-frame"]:
                    raise RuntimeError("h3q adapter accepts one first_frame binding")
                reference_args["first-frame"] = remote_name
            elif role == "last_frame":
                if reference_args["last-frame"]:
                    raise RuntimeError("h3q adapter accepts one last_frame binding")
                reference_args["last-frame"] = remote_name
            else:
                reference_args["refs"].append(remote_name)
        reference_args["refs"] = ",".join(reference_args["refs"])

        prompt = job["prompt"]
        if reference_contract and job["modality"] == "image":
            prompt += "\n\nReference input contract:\n" + "\n".join(reference_contract)
        prompt_local = output_root / "prompt.txt"
        prompt_local.write_text(prompt, encoding="utf-8")
        if job["modality"] == "video":
            # Match lib_workflow.seconds_to_frames: round at 24 fps, then snap up
            # to 17k+5. The source owns all reference definitions in the prompt.
            frames = expected_frames(job)
            gate_argv = ["--frames", str(frames), "--refs", str(len(bindings)), "--json"]
            if video_workflow(job["parameters"]) == "multishot":
                # 多窗脚本有自己的闸门模式：逐窗查格式与内容，每窗单独受 15s 限制。
                # 不再「整块豁免结构项」——那是把检查删掉，不是适配。
                gate_argv = ["--mode", "multishot",
                             "--shot-count", str(int((job["parameters"] or {}).get("shot_count") or 2)),
                             "--frames", str(int((job["parameters"] or {}).get("frames_per_shot") or 226)),
                             "--refs", str(len(bindings)), "--json"]
            series = Path(job["project_root"]) / "h3-series-config.json"
            if series.is_file():
                gate_argv += ["--series-config", str(series)]
            helper = Path(VIDEO_GATE).with_name("gate_evidence.py")
            spec = importlib.util.spec_from_file_location("h3_gate_evidence", helper)
            if spec is None or spec.loader is None:
                raise RuntimeError("H3 gate evidence helper is unavailable")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            evidence_dir = Path(job["handle_path"]).with_suffix(".evidence")
            gate = module.run_archived_gate(prompt_local, Path(VIDEO_GATE), evidence_dir, gate_argv,
                context={"job_id": job["job_id"], "run_id": job["run_id"],
                         "parameters": job["parameters"], "references": reference_evidence}, runner=run)
            # The uploaded text is exactly the frozen text the frozen checker read.
            prompt_local = evidence_dir / "prompt.txt"
            try:
                report = json.loads(gate.stdout)
            except json.JSONDecodeError:
                report = {"summary": {"errors": 1}, "findings": []}
            workflow = video_workflow(job["parameters"])
            # 多窗现在有真正的闸门模式（G39 格式 + G40 逐窗内容），不再整块豁免：
            # 之前把结构项整体放行，等于多窗脚本没查过任何东西。
            blocking = gate_blockers(report.get("findings"), "")
            if gate.returncode not in (0, 1) or report.get("summary", {}).get("errors") or blocking:
                detail = "; ".join(
                    f"{f.get('rule')} {f.get('message', '')[:160]}" for f in blocking[:4]
                ) or (gate.stdout + gate.stderr).strip()[-400:]
                raise RuntimeError("H3 video prompt gate rejected the confirmed prompt: " + detail)
            # Print all non-blocking warns so the agent cannot silently skip them
            non_blocking_warns = [
                f for f in report.get("findings") or []
                if f.get("level") == "warn" and f.get("rule") not in BLOCKING_GATE_WARNINGS
            ]
            if non_blocking_warns:
                print(
                    f"gate: {len(non_blocking_warns)} advisory warn(s) — review before accepting output:",
                    file=sys.stderr,
                )
                for w in non_blocking_warns:
                    rule = w.get("rule", "?")
                    msg = (w.get("message") or "")[:200]
                    print(f"  [{rule}] {msg}", file=sys.stderr)
            dialogue_check = verify_dialogue_against_screenplay(job)
            if dialogue_check == "not_checked_missing_screenplay":
                print(
                    "dialogue comparison NOTCHK: this older confirmed job has no 剧本.md "
                    "in its input snapshot; re-prepare to enable the check",
                    file=sys.stderr,
                )
        ssh(f'if not exist "{workdir}" mkdir "{workdir}"')
        for prepared, remote_path in prepared_uploads:
            scp(prepared, remote_path)
        prompt_remote = win_join(workdir, "prompt.txt")
        scp(prompt_local, prompt_remote.replace("\\", "/"))
        provider_job_id, output_remote = submit(
            job, workdir, prompt_remote, reference_args, gate_off=gate_off
        )
        write_handle(job["handle_path"], provider_job_id)
    else:
        output_remote = None

    while True:
        state = queue_show(provider_job_id)
        status = state.get("state")
        if status == "done":
            output_remote = resolve_output(job, state, output_remote)
            break
        if status in ("failed", "cancelled", "blocked_vram"):
            raise RuntimeError(f"h3q job ended in state {status}")
        time.sleep(POLL_SECONDS)

    local_result = output_root / Path(outputs[0]).name
    scp(local_result, output_remote.replace("\\", "/"), upload=False)
    verify_output(job, local_result)
    print(json.dumps({
        "outputs": [{"target": outputs[0], "source": str(local_result)}],
        "provider_job_id": provider_job_id,
    }, ensure_ascii=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
