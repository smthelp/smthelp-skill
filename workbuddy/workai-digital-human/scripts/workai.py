#!/usr/bin/env python3
"""小狐狸数字人 API 命令行封装。

Base URL: https://api.workai.cc
鉴权: Header `Authorization: <API key>`

命令:
  balance                        查询账户余额（点）
  voices                         列出系统内置音色
  task      --type --task-id     查询任务详情
  tts       --text ...           语音合成 -> task_id / audio_url
  clone     --audio-url --name   声音克隆 -> task_id / voice_id
  lipsync   --video-url --audio-url
                                 视频对口型 -> task_id / video_url

所有异步命令支持 --wait（轮询 getTaskDetail 直到成功/失败）与 --out（自动下载结果文件）。
结果文件（audio_url / video_url / demo_url）仅短暂留存，拿到后必须立刻转存。

用法示例:
  export WORKAI_API_KEY=xxxx
  python3 workai.py balance
  python3 workai.py tts --text "你好" --voice-type public --voice-id yunxuan \
      --wait --out ./out/hello.mp3 --srt-out ./out/hello.srt
  python3 workai.py clone --audio-url https://x/y.mp3 --name jason-en --lang en --wait
  python3 workai.py lipsync --video-url https://x/v.mp4 --audio-url https://x/a.mp3 \
      --wait --out ./out/talk.mp4
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.workai.cc"
HTTP_TIMEOUT = 60
POLL_INTERVAL = 5
POLL_TIMEOUT = 1800

LANGS = ["zh-cn", "en", "fr", "de", "ja", "ko", "ru", "pt", "th", "id", "vi"]

# voice_id -> (名称, 性别, 语言, 试听url)
PUBLIC_VOICES = [
    ("yunxuan", "云轩", "男声", "普通话", "https://alioss.ttk.ink/tts/demo/oIOeze4nmH.mp3"),
    ("yunfeng", "云峰", "男声", "普通话", "https://alioss.ttk.ink/tts/demo/wSw1gisuk2.mp3"),
    ("yunfei", "云飞", "男声", "普通话", "https://alioss.ttk.ink/tts/demo/zbeQ9objtH.mp3"),
    ("yunlong", "云龙", "男声", "普通话", "https://alioss.ttk.ink/tts/demo/c28roX43NR.mp3"),
    ("xiaoling", "小玲", "女声", "普通话", "https://alioss.ttk.ink/tts/demo/GduUO1uRaf.mp3"),
    ("xiaoying", "小英", "女声", "普通话", "https://alioss.ttk.ink/tts/demo/DuCcrxhETS.mp3"),
    ("xiaoning", "小宁", "女声", "东北话", "https://alioss.ttk.ink/tts/demo/xXpNQatnOZ.mp3"),
    ("aria", "Aria", "女声", "英语", "https://alioss.ttk.ink/tts/demo/6tpW6vLHhf.mp3"),
    ("ana", "Ana", "女声", "英语", "https://alioss.ttk.ink/tts/demo/YTBWGqEioG.mp3"),
    ("christopher", "Christopher", "男声", "英语", "https://alioss.ttk.ink/tts/demo/0FtqYZjqIL.mp3"),
    ("tom", "Tom", "男声", "英语", "https://alioss.ttk.ink/tts/demo/6sEn2NTvFD.mp3"),
    ("guy", "Guy", "男声", "英语", "https://alioss.ttk.ink/tts/demo/SCqmK9qjbI.mp3"),
    ("jenny", "Jenny", "女声", "英语", "https://alioss.ttk.ink/tts/demo/gwLnjPzsaw.mp3"),
    ("michelle", "Michelle", "女声", "英语", "https://alioss.ttk.ink/tts/demo/O6VbIIs3WN.mp3"),
    ("roger", "Roger", "男声", "英语", "https://alioss.ttk.ink/tts/demo/NlX1ER9g5i.mp3"),
    ("steffan", "Steffan", "男声", "英语", "https://alioss.ttk.ink/tts/demo/V9KzCmJPnn.mp3"),
]

# 结果字段 -> 下载时的默认文件名后缀
RESULT_URL_KEYS = ["video_url", "audio_url", "demo_url", "srt_url"]


def get_key(cli_key=None):
    key = cli_key or os.environ.get("WORKAI_API_KEY")
    if not key:
        sys.exit(
            "缺少 API key：设置环境变量 WORKAI_API_KEY，或传 --api-key。\n"
            "key 来自小狐狸数字人后台，header 名为 Authorization。"
        )
    return key


def post(path, payload, key):
    """POST JSON，返回 (ok, data_or_None, message)。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else b"{}"
    req = urllib.request.Request(
        BASE + path,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": key,
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return False, None, "HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:500])
    except Exception as e:  # noqa: BLE001
        return False, None, "请求失败: %s" % e

    try:
        res = json.loads(raw)
    except json.JSONDecodeError:
        return False, None, "非 JSON 响应: %s" % raw[:500]

    if res.get("errno") not in (0, "0"):
        return False, res.get("data"), "errno=%s message=%s" % (res.get("errno"), res.get("message"))
    return True, res.get("data") or {}, res.get("message") or ""


def download(url, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "workai-cli/1.0"})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT * 5) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    return os.path.getsize(out_path)


def wait_task(task_id, task_type, key, timeout=POLL_TIMEOUT, interval=POLL_INTERVAL):
    """轮询 getTaskDetail，status 1=成功 2=失败，0/缺失=进行中。"""
    deadline = time.time() + timeout
    waited = 0
    while time.time() < deadline:
        ok, data, msg = post("/api/v1/getTaskDetail", {"type": task_type, "task_id": task_id}, key)
        if not ok:
            return {"status": 2, "fail_reason": msg, "_elapsed": waited}
        status = int(data.get("status") or 0)
        if status in (1, 2):
            data["_elapsed"] = waited
            return data
        time.sleep(interval)
        waited += interval
    return {"status": 0, "fail_reason": "轮询超时 %ss（任务可能仍在进行，用 task 命令继续查）" % timeout, "_elapsed": waited}


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# ------------------------------- 命令实现 -------------------------------

def cmd_balance(a):
    ok, data, msg = post("/api/v1/getBalance", {}, a.api_key)
    if not ok:
        sys.exit("查询余额失败: %s" % msg)
    emit({"balance_points": data.get("balance")})


def cmd_voices(a):
    if a.json:
        emit([
            {"voice_id": v[0], "name": v[1], "gender": v[2], "lang": v[3], "demo_url": v[4]}
            for v in PUBLIC_VOICES
        ])
        return
    print("%-14s %-12s %-6s %-8s %s" % ("voice_id", "名称", "性别", "语言", "试听"))
    for vid, name, gender, lang, demo in PUBLIC_VOICES:
        print("%-14s %-12s %-6s %-8s %s" % (vid, name, gender, lang, demo))
    print("\n使用方式: tts --voice-type public --voice-id <上表 voice_id> --lang zh-cn|en ...")


def cmd_task(a):
    ok, data, msg = post("/api/v1/getTaskDetail", {"type": a.type, "task_id": a.task_id}, a.api_key)
    if not ok:
        sys.exit("查询失败: %s" % msg)
    emit(data)


def _finish(task_id, task_type, a, url_keys):
    """--wait 时轮询并可选下载；不 --wait 时只返回 task_id。"""
    if not a.wait:
        emit({"task_id": task_id, "type": task_type, "hint": "加 --wait 等待结果，或用 task 命令查询"})
        return
    data = wait_task(task_id, task_type, a.api_key, timeout=a.timeout, interval=a.interval)
    data.setdefault("task_id", task_id)
    result = {"task_id": task_id, "type": task_type, "elapsed_s": data.pop("_elapsed", 0), "data": data}

    status = int(data.get("status") or 0)
    if status == 1 and a.out:
        url = next((data.get(k) for k in url_keys if data.get(k)), None)
        if url:
            size = download(url, a.out)
            result["downloaded"] = {"path": os.path.abspath(a.out), "bytes": size}
        if a.srt_out and data.get("srt_url"):
            download(data["srt_url"], a.srt_out)
            result["downloaded_srt"] = os.path.abspath(a.srt_out)
    if not a.out:
        result["warn"] = "结果 url 仅短暂留存，请用 --out 立即转存"
    emit(result)
    if status == 2:
        sys.exit(1)


def cmd_tts(a):
    text = a.text
    if a.text_file:
        with open(a.text_file, encoding="utf-8") as f:
            text = f.read()
    if not text:
        sys.exit("缺少 --text 或 --text-file")
    if len(text) > 2000:
        sys.exit("文本超过 2000 字（接口硬限制），当前 %s 字，请分段" % len(text))
    payload = {
        "text": text,
        "voice_type": a.voice_type,
        "voice_id": a.voice_id,
        "lang": a.lang,
        "speed": a.speed,
    }
    if a.notify:
        payload["notify"] = a.notify
    ok, data, msg = post("/api/v1/tts", payload, a.api_key)
    if not ok:
        sys.exit("语音合成提交失败: %s" % msg)
    _finish(data.get("task_id"), "tts", a, ["audio_url"])


def cmd_clone(a):
    payload = {"audio_url": a.audio_url, "lang": a.lang}
    if a.name:
        payload["name"] = a.name
    if a.notify:
        payload["notify"] = a.notify
    ok, data, msg = post("/api/v1/cloneVoice", payload, a.api_key)
    if not ok:
        sys.exit("声音克隆提交失败: %s" % msg)
    _finish(data.get("task_id"), "clone_voice", a, ["demo_url"])


def cmd_lipsync(a):
    payload = {"video_url": a.video_url, "audio_url": a.audio_url}
    if a.notify:
        payload["notify"] = a.notify
    ok, data, msg = post("/api/v1/lipsync", payload, a.api_key)
    if not ok:
        sys.exit("对口型提交失败: %s" % msg)
    _finish(data.get("task_id"), "lipsync", a, ["video_url"])


def build_parser():
    p = argparse.ArgumentParser(description="小狐狸数字人 API CLI")
    p.add_argument("--api-key", default=None, help="接口 key，默认读环境变量 WORKAI_API_KEY")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("balance", help="查询账户余额（点）").set_defaults(func=cmd_balance)

    v = sub.add_parser("voices", help="系统内置音色列表")
    v.add_argument("--json", action="store_true", help="以 JSON 输出")
    v.set_defaults(func=cmd_voices)

    t = sub.add_parser("task", help="查询任务详情")
    t.add_argument("--type", required=True, choices=["lipsync", "clone_voice", "tts"])
    t.add_argument("--task-id", required=True)
    t.set_defaults(func=cmd_task)

    s = sub.add_parser("tts", help="语音合成")
    s.add_argument("--text", help="合成文本，<=2000 字；克隆音色支持 SSML")
    s.add_argument("--text-file", help="从文件读取文本（UTF-8）")
    s.add_argument("--voice-type", required=True, choices=["public", "custom"])
    s.add_argument("--voice-id", required=True, help="public 用内置音色 id，custom 用克隆返回的 voice_id")
    s.add_argument("--lang", default="zh-cn", choices=LANGS)
    s.add_argument("--speed", type=float, default=1, help="语速 0.5~2.0，默认 1")
    s.add_argument("--notify", help="回调地址")
    s.add_argument("--wait", action="store_true", help="轮询直到完成")
    s.add_argument("--out", help="结果音频保存路径（如 ./out/a.mp3）")
    s.add_argument("--srt-out", help="字幕文件保存路径（如 ./out/a.srt）")
    s.add_argument("--timeout", type=int, default=POLL_TIMEOUT)
    s.add_argument("--interval", type=int, default=POLL_INTERVAL)
    s.set_defaults(func=cmd_tts)

    c = sub.add_parser("clone", help="声音克隆")
    c.add_argument("--audio-url", required=True, help="原音频 url")
    c.add_argument("--name", help="声音名称")
    c.add_argument("--lang", default="zh-cn", choices=LANGS, help="用哪种语言克隆，也只能合成该语言")
    c.add_argument("--notify")
    c.add_argument("--wait", action="store_true")
    c.add_argument("--out", help="demo 音频保存路径")
    c.add_argument("--timeout", type=int, default=POLL_TIMEOUT)
    c.add_argument("--interval", type=int, default=POLL_INTERVAL)
    c.set_defaults(func=cmd_clone)

    l = sub.add_parser("lipsync", help="视频对口型")
    l.add_argument("--video-url", required=True, help="视频地址，<300M")
    l.add_argument("--audio-url", required=True, help="音频地址，>2s")
    l.add_argument("--notify")
    l.add_argument("--wait", action="store_true")
    l.add_argument("--out", help="结果视频保存路径（如 ./out/v.mp4）")
    l.add_argument("--timeout", type=int, default=POLL_TIMEOUT)
    l.add_argument("--interval", type=int, default=POLL_INTERVAL)
    l.set_defaults(func=cmd_lipsync)

    # 允许 --api-key 放在子命令之后：用 SUPPRESS 避免覆盖顶层已解析到的值
    for sp in sub.choices.values():
        sp.add_argument("--api-key", default=argparse.SUPPRESS, help="同顶层 --api-key")
    return p


def main():
    parser = build_parser()
    a = parser.parse_args()
    a.api_key = get_key(a.api_key)
    a.func(a)


if __name__ == "__main__":
    main()
