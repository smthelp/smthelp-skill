#!/usr/bin/env python3
"""Transcribe a source audio/video file to timestamped text (English model by default).

usage: python3 transcribe_audio.py <media_file> [--model base.en] [--out transcript.txt]
Needs: pip install faster-whisper ; ffmpeg on PATH.
Note: feeds a numpy array, because some PyAV versions reject faster-whisper's file decoder
(TypeError: open() got an unexpected keyword argument 'metadata_errors').
Use the transcript for terminology and SEO keywords; specs heard only in audio stay 'to be confirmed'
and third-party / competitor names never enter copy.
"""
import argparse, subprocess, wave, os, tempfile
import numpy as np
from faster_whisper import WhisperModel
ap = argparse.ArgumentParser(); ap.add_argument("media"); ap.add_argument("--model", default="base.en"); ap.add_argument("--out")
a = ap.parse_args()
tmp = os.path.join(tempfile.mkdtemp(), "a16.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.media, "-ar", "16000", "-ac", "1", tmp], check=True)
w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
m = WhisperModel(a.model, device="cpu", compute_type="int8")
seg, _ = m.transcribe(x, beam_size=1, vad_filter=True)
out = a.out or os.path.splitext(a.media)[0] + "_transcript.txt"
with open(out, "w") as f:
    for s in seg: f.write(f"[{s.start:.0f}] {s.text.strip()}\n")
print(out)
