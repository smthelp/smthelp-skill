#!/usr/bin/env python3
"""本地回调接收端：接收小狐狸数字人的结果通知（POST JSON），落盘并打印。

异步任务（lipsync / cloneVoice / tts）完成后，服务端会向 notify 地址 POST 结果。
本地调试时需配合内网穿透（如 ngrok / cloudflared）把公网地址填到 notify 参数。

用法:
  python3 notify_receiver.py --port 8899 --dir ./notify_logs
  # 另开一个终端: ngrok http 8899  ->  把 https://xxx.ngrok.io 作为 notify 传入

落盘文件: <dir>/<task_id>.<timestamp>.json
响应: 恒返回 {"errno": 0}，避免服务端判定失败重试。
"""

import argparse
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

SAVE_DIR = "./notify_logs"


class Handler(BaseHTTPRequestHandler):
    save_dir = SAVE_DIR

    def _handle(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace") if length else ""
        ts = time.strftime("%Y%m%d-%H%M%S")
        print("[%s] %s %s\n%s" % (ts, self.command, self.path, raw), flush=True)

        task_id = "unknown"
        try:
            payload = json.loads(raw)
            task_id = str(payload.get("task_id") or "unknown")
        except json.JSONDecodeError:
            pass

        os.makedirs(self.save_dir, exist_ok=True)
        out = os.path.join(self.save_dir, "%s.%s.json" % (task_id, ts))
        with open(out, "w", encoding="utf-8") as f:
            f.write(raw)
        print("saved -> %s" % os.path.abspath(out), flush=True)

        body = json.dumps({"errno": 0}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_POST = _handle
    do_GET = _handle

    def log_message(self, fmt, *args):  # 静音默认访问日志
        pass


def main():
    p = argparse.ArgumentParser(description="小狐狸数字人回调接收端")
    p.add_argument("--port", type=int, default=8899)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--dir", default=SAVE_DIR)
    a = p.parse_args()
    Handler.save_dir = a.dir
    print("listening on http://%s:%s  ->  saving to %s" % (a.host, a.port, os.path.abspath(a.dir)))
    HTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
