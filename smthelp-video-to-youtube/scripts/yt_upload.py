#!/usr/bin/env python3
"""Upload a video to the Smthelping YouTube channel with SEO metadata.

Verifies the authenticated account's default channel before uploading (target
defaults to UClX0iEG2bvJq8yUBEDamgDw). Always refreshes the access token.
"""
import argparse, json, os, sys
import requests

CFG = os.path.expanduser("~/.config/smthelp-yt")
CRED_PATH = os.path.join(CFG, "credentials.json")
TOKEN_PATH = os.path.join(CFG, "tokens.json")
DEFAULT_CHANNEL = "UClX0iEG2bvJq8yUBEDamgDw"

def load_credentials():
    c = json.load(open(CRED_PATH))
    return c["client_id"], c["client_secret"]

def access_token(client_id, client_secret):
    tok = json.load(open(TOKEN_PATH))
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": client_id, "client_secret": client_secret,
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token"}, timeout=30)
    r.raise_for_status()
    n = r.json()
    n["refresh_token"] = tok["refresh_token"]
    json.dump(n, open(TOKEN_PATH, "w"))
    return n["access_token"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", required=True)
    ap.add_argument("--tags", default="")
    ap.add_argument("--target-channel", default=DEFAULT_CHANNEL)
    ap.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    args = ap.parse_args()

    client_id, client_secret = load_credentials()
    access = access_token(client_id, client_secret)
    h = {"Authorization": f"Bearer {access}"}
    ch = requests.get("https://www.googleapis.com/youtube/v3/channels", headers=h,
                      params={"part": "id", "mine": "true"}, timeout=30).json()
    cid = ch["items"][0]["id"]
    print("AUTH_CHANNEL=" + cid, flush=True)
    if cid != args.target_channel:
        sys.exit(f"CHANNEL_MISMATCH expected={args.target_channel} got={cid}")

    meta = {
        "snippet": {"title": args.title, "description": args.description,
                    "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
                    "categoryId": "28", "defaultLanguage": "en"},
        "status": {"privacyStatus": args.privacy, "selfDeclaredMadeForKids": False,
                   "embeddable": True, "license": "youtube", "publicStatsViewable": True},
    }
    init = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        headers={**h, "Content-Type": "application/json; charset=UTF-8"}, json=meta, timeout=30)
    if init.status_code != 200:
        sys.exit(f"INIT_FAIL {init.status_code} {init.text[:500]}")
    with open(args.video, "rb") as f:
        up = requests.put(init.headers["Location"], data=f,
                          headers={"Content-Type": "video/mp4"}, timeout=1800)
    if up.status_code not in (200, 201):
        sys.exit(f"UPLOAD_FAIL {up.status_code} {up.text[:500]}")
    vid = up.json()["id"]
    print("DONE id=" + vid, flush=True)
    v = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=h,
                     params={"part": "snippet,status", "id": vid}, timeout=30).json()
    it = v["items"][0]
    print("VERIFY channelId=" + it["snippet"]["channelId"], flush=True)
    print("VERIFY title=" + it["snippet"]["title"], flush=True)
    print("VERIFY privacy=" + it["status"]["privacyStatus"], flush=True)
    print("URL=https://youtu.be/" + vid, flush=True)

if __name__ == "__main__":
    main()
