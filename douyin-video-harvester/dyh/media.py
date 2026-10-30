"""ffprobe/ffmpeg helpers shared by frames, dedupe, verify."""
import subprocess
from .errors import DyhError

def duration(cfg, path):
    try:
        r = subprocess.run([cfg["ffprobe"], "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                           capture_output=True, text=True)
    except FileNotFoundError:
        raise DyhError("E_DEP", cfg["ffprobe"])
    try: return float(r.stdout.strip())
    except ValueError: return 0.0

def decode_errors(cfg, path):
    r = subprocess.run([cfg["ffmpeg"], "-v", "error", "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    return r.stderr.strip()

def gray16(cfg, path, t):
    r = subprocess.run([cfg["ffmpeg"], "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                        "-vf", "scale=16:16,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    return r.stdout.ljust(256, b"\0")[:256]
