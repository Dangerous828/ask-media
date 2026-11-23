# -*- coding: utf-8 -*-
"""对白白模一键流水线：校验 -> 渲染 H.264 mp4 -> 导出分镜xlsx -> 台词文件。
用法: python run_dialogue_pipeline.py <storyboard.json> [--outdir DIR]
依赖: numpy/Pillow/opencv/openpyxl/ffmpeg；组件从本脚本同目录（scripts/）解析。
渲染引擎直接输出 H.264/yuv420p，无需再转码。"""
import sys,os,subprocess,json
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE=os.path.dirname(os.path.abspath(__file__))

def find_ffmpeg():
    """渲染引擎直出 H.264，本函数仅用于前置校验环境。"""
    import shutil
    return shutil.which("ffmpeg")

def component(name):
    f=os.path.join(HERE,name)
    if not os.path.isfile(f):
        sys.exit(f"[错误] 找不到组件 {name}（应在 {HERE}）")
    return f

def main():
    if len(sys.argv)<2:
        sys.exit("用法: python run_dialogue_pipeline.py <storyboard.json> [--outdir DIR]")
    jpath=os.path.abspath(sys.argv[1])
    cfg=json.load(open(jpath,encoding="utf-8")); proj=cfg["project"]

    # 0) 前置：渲染引擎需要 ffmpeg 出 H.264，缺失时明确报错而非改名冒充。
    if not find_ffmpeg():
        sys.exit("[错误] 找不到 ffmpeg：白模一律输出 H.264，请安装 ffmpeg 后重试")

    # 1) 校验（失败即停）
    val=component("validate_dialogue.py")
    print("1) 校验 storyboard…")
    r=subprocess.run([sys.executable,val,jpath])
    if r.returncode!=0: sys.exit("校验未通过，流水线停止")

    eng=component("dialogue_engine.py"); xlsx=component("export_storyboard_xlsx.py"); dlg=component("export_dialogue.py")

    # 输出目录：默认与 storyboard 同项目下的 白模/，可由 --outdir 覆盖。
    outdir=os.path.join(os.path.dirname(jpath),"白模")
    if "--outdir" in sys.argv: outdir=sys.argv[sys.argv.index("--outdir")+1]
    outdir=os.path.abspath(outdir); os.makedirs(outdir,exist_ok=True)
    py=sys.executable
    mp4=os.path.join(outdir,proj+"_白模.mp4"); xl=os.path.join(outdir,proj+"_分镜表.xlsx")

    print("2) 渲染对白白模（H.264）…")
    run=[py,eng,jpath,mp4]
    r=subprocess.run(run)
    if r.returncode!=0: sys.exit("渲染失败，流水线停止")

    print("3) 导出分镜 Excel…")
    r=subprocess.run([py,xlsx,jpath,xl])
    if r.returncode!=0: sys.exit("Excel 导出失败，流水线停止")

    print("4) 导出带时间戳台词(SRT/txt)…")
    r=subprocess.run([py,dlg,jpath,outdir])
    if r.returncode!=0: print("[警告] 台词导出失败，但不影响已产物")

    print(f"完成：{proj}\n  {mp4}\n  {xl}")

if __name__=="__main__": main()
