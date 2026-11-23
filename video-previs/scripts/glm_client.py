# -*- coding: utf-8 -*-
"""
智谱 GLM API 薄客户端（标准库实现，无第三方依赖）。
配置（环境变量）：
  ZHIPUAI_API_KEY / GLM_API_KEY  -- 二选一，未配置则 is_configured()=False
  GLM_BASE        -- 默认 https://open.bigmodel.cn/api/paas/v4
  GLM_TEXT_MODEL  -- 默认 glm-5.3-flash
  GLM_VISION_MODEL-- 默认 glm-4.5v
"""
import os,json,base64,urllib.request

def is_configured(): return bool(os.environ.get("ZHIPUAI_API_KEY") or os.environ.get("GLM_API_KEY"))
def _key(): return os.environ.get("ZHIPUAI_API_KEY") or os.environ.get("GLM_API_KEY") or ""
def text_model(): return os.environ.get("GLM_TEXT_MODEL","glm-5.3-flash")
def vision_model(): return os.environ.get("GLM_VISION_MODEL","glm-4.5v")

def chat(messages,model=None,timeout=120,temperature=0.6):
    """messages: OpenAI 风格；图片用 {"type":"image_url","image_url":{"url":"data:image/jpeg;base64,..."}}"""
    if not is_configured():
        raise RuntimeError("未配置 GLM_API_KEY/ZHIPUAI_API_KEY 环境变量")
    body=json.dumps({"model":model or text_model(),"messages":messages,"temperature":temperature}).encode()
    base=os.environ.get("GLM_BASE","https://open.bigmodel.cn/api/paas/v4").rstrip("/")
    req=urllib.request.Request(
        base+"/chat/completions",
        data=body,method="POST",
        headers={"Content-Type":"application/json","Authorization":"Bearer "+_key()})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        d=json.loads(r.read().decode("utf-8"))
    # 200 但结构异常也要明确报错，不让 KeyError/IndexError 冒到调用方。
    try:
        content=d["choices"][0]["message"]["content"]
    except (KeyError,IndexError,TypeError) as e:
        raise RuntimeError("GLM 响应结构异常，缺少 choices[0].message.content: %r" % (d,)) from e
    return content

def image_part(jpg_bytes):
    b64=base64.b64encode(jpg_bytes).decode()
    return {"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+b64}}

def extract_json(text):
    """宽松解析：剥 ```json 围栏/前后杂文，取第一个平衡的 {...}"""
    t=text.strip()
    if "```" in t:
        t=t.split("```")[1] if t.count("```")>=2 else t.replace("```","")
        if t.startswith("json"): t=t[4:]
    a=t.find("{")
    if a<0: raise ValueError("回复中没有 JSON: "+text[:120])
    # raw_decode 认识字符串字面量里的 { }，不会被值内花括号打乱深度计数。
    # 从第一个 { 开始试解；失败再向后找下一个 {（前一个可能是杂文里的括号）。
    dec=json.JSONDecoder()
    pos=a
    while pos>=0:
        try:
            obj,_=dec.raw_decode(t[pos:])
            return obj
        except ValueError:
            pos=t.find("{",pos+1)
    raise ValueError("JSON 未闭合或无法解析: "+text[:120])
