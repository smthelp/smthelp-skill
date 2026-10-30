"""Error codes. Every stage raises DyhError(code, msg); the CLI maps codes to exit status."""
CODES = {
    "E_CONFIG": (2, "config missing or invalid"),
    "E_DEP": (3, "missing dependency (chromium/playwright/yt-dlp/ffmpeg/gws)"),
    "E_COOKIES": (4, "cookie file missing, empty, or has no douyin.com cookies"),
    "E_SCRAPE_EMPTY": (5, "profile scrape returned 0 works (cookies expired, captcha, or wrong sec_uid)"),
    "E_SCRAPE_PARTIAL": (6, "scrape stalled before has_more=false"),
    "E_DOWNLOAD": (7, "every CDN url failed for an item"),
    "E_VERIFY": (8, "duration mismatch or decode error"),
    "E_SELECTION": (9, "selection.json invalid (bad slug, duplicate name, unknown id, wrong count)"),
    "E_UPLOAD": (10, "upload failed or remote size != local size"),
    "E_STAGE_INPUT": (11, "a previous stage's output is missing; run it first"),
}

class DyhError(Exception):
    def __init__(self, code, msg=""):
        self.code = code
        self.exit = CODES.get(code, (1, ""))[0]
        super().__init__(f"[{code}] {CODES.get(code, (1, ''))[1]}: {msg}")
