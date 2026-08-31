#!/usr/bin/env python3
"""YouTube OAuth authorization (loopback). Saves tokens to ~/.config/smthelp-yt/tokens.json.

Credentials come from ~/.config/smthelp-yt/credentials.json ({"client_id","client_secret"})
or env CLIENT_ID / CLIENT_SECRET. Scopes: youtube.upload + youtube.force-ssl.
"""
import json, os, sys, threading, time, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

CFG = os.path.expanduser("~/.config/smthelp-yt")
CRED_PATH = os.path.join(CFG, "credentials.json")
TOKEN_PATH = os.path.join(CFG, "tokens.json")
PORT = int(os.environ.get("OAUTH_PORT", "8788"))
REDIRECT = f"http://127.0.0.1:{PORT}/callback"
SCOPE = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.force-ssl"

received = {}

def load_credentials():
    if os.path.exists(CRED_PATH):
        c = json.load(open(CRED_PATH))
        if c.get("client_id") and c.get("client_secret"):
            return c["client_id"], c["client_secret"]
    cid, sec = os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET")
    if cid and sec:
        return cid, sec
    sys.exit(f"credentials not found: {CRED_PATH} or CLIENT_ID/CLIENT_SECRET env")

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.urlparse(self.path)
        if q.path == "/callback":
            p = urllib.parse.parse_qs(q.query)
            received["code"] = p.get("code", [None])[0]
            received["error"] = p.get("error", [None])[0]
            body = b"Authorization received. You can close this tab."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a):
        pass

def main():
    client_id, client_secret = load_credentials()
    server = HTTPServer(("127.0.0.1", PORT), H)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    params = {
        "client_id": client_id, "redirect_uri": REDIRECT, "scope": SCOPE,
        "response_type": "code", "access_type": "offline", "prompt": "consent",
    }
    print("AUTH_URL=" + "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params), flush=True)
    for _ in range(2400):  # 20 min
        if "code" in received or "error" in received:
            break
        time.sleep(0.5)
    server.shutdown()
    if received.get("error"):
        sys.exit("OAUTH_ERROR=" + received["error"])
    code = received.get("code")
    if not code:
        sys.exit("NO_CODE")
    data = urllib.parse.urlencode({
        "code": code, "client_id": client_id, "client_secret": client_secret,
        "redirect_uri": REDIRECT, "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    try:
        with urllib.request.urlopen(req) as r:
            tok = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"TOKEN_EXCHANGE_FAIL {e.code} {e.read().decode()[:300]}")
    os.makedirs(CFG, exist_ok=True)
    os.chmod(CFG, 0o700)
    with open(TOKEN_PATH, "w") as f:
        json.dump(tok, f)
    os.chmod(TOKEN_PATH, 0o600)
    print("TOKEN_SAVED " + TOKEN_PATH, flush=True)
    print("HAS_REFRESH=" + str(bool(tok.get("refresh_token"))), flush=True)

if __name__ == "__main__":
    main()
