"""Error codes. Every failure raised by a stage is a P3VError with a stable code and a fix hint."""

CODES = {
    "E_CONFIG": "Configuration missing or invalid",
    "E_DEPENDENCY": "A required tool or Python package is missing",
    "E_STAGE_ORDER": "A stage ran before the stage it depends on finished",
    "E_DOWNLOAD": "A source file could not be downloaded",
    "E_CAPTURE": "The 3D viewer could not be captured",
    "E_TTS": "Voice-over generation failed",
    "E_AUDIO": "Audio mix / loudness normalisation failed",
    "E_SUBTITLE": "Subtitle cue building failed",
    "E_ANIM": "Animation module missing or broken",
    "E_ASSEMBLE": "Landing page assembly failed (marker / nav not found)",
    "E_VIDEO_BUILD": "Video page build or preview failed",
    "E_RENDER": "Frame rendering failed",
    "E_FFMPEG": "ffmpeg / ffprobe failed",
    "E_THUMB": "Thumbnail render failed",
    "E_UPLOAD": "Upload to the delivery sink failed",
    "E_HOOK": "A user hook command failed",
    "E_PENDING": "Work is still running (e.g. 4K render); call the same command again later",
}


class P3VError(Exception):
    def __init__(self, code, message, hint=None):
        assert code in CODES, code
        self.code, self.message, self.hint = code, message, hint
        super().__init__(f"[{code}] {message}" + (f"  (hint: {hint})" if hint else ""))

    def as_dict(self):
        return {"code": self.code, "message": self.message, "hint": self.hint}
