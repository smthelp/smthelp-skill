#!/usr/bin/env python3
"""Step 3 — Read a narration.json (list[str], one sentence per slide) and
synthesize each line into a 44.1k mono WAV via Microsoft edge-tts
(free cloud, natural voice). Writes audio/full/slide_NN.wav and
audio/durations.json (per-slide seconds + narration list).

Usage:
  python3 gen_tts.py --narration narration.json --out audio
  python3 gen_tts.py --narration narration.json --out audio --voice en-US-GuyNeural
  python3 gen_tts.py --narration narration.json --out audio --voice zh-CN-XiaoxiaoNeural
"""
import argparse, asyncio, json, os, shutil, subprocess, sys
import edge_tts

def which(*names, fallback=None):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return fallback

def ffprobe_dur(ffprobe, path):
    r = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

async def synth_all(ffmpeg, ffprobe, outdir, narration, voice):
    durations = []
    full = os.path.join(outdir, "full")
    os.makedirs(full, exist_ok=True)
    for i, text in enumerate(narration, 1):
        mp3 = os.path.join(outdir, f"tmp_{i:02d}.mp3")
        wav = os.path.join(full, f"slide_{i:02d}.wav")
        comm = edge_tts.Communicate(text, voice)
        data = b""
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                data += chunk["data"]
        with open(mp3, "wb") as f:
            f.write(data)
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", mp3,
                        "-ac", "1", "-ar", "44100", wav], check=True)
        # NOTE: temp mp3 cleanup intentionally skipped to avoid bulk-delete guards;
        # tmp_*.mp3 leftovers are harmless and pruned manually after the run.
        d = ffprobe_dur(ffprobe, wav)
        durations.append(d)
        flag = "  <-- over 5s, shorten" if d > 5.0 else ""
        print(f"slide {i:02d}: {d:.2f}s{flag} | {text[:70]}")
    return durations

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True, help="JSON file: list[str]")
    ap.add_argument("--out", default="audio")
    ap.add_argument("--voice", default="en-US-AriaNeural")
    args = ap.parse_args()

    ffmpeg = which("ffmpeg", fallback="/opt/homebrew/bin/ffmpeg")
    ffprobe = which("ffprobe", fallback="/opt/homebrew/bin/ffprobe")
    if not ffmpeg or not ffprobe:
        sys.exit("ERROR: ffmpeg/ffprobe required.")
    with open(args.narration, encoding="utf-8") as f:
        narration = json.load(f)
    if not isinstance(narration, list):
        sys.exit("ERROR: narration.json must be a JSON array of strings.")
    os.makedirs(args.out, exist_ok=True)
    durations = asyncio.run(synth_all(ffmpeg, ffprobe, args.out, narration, args.voice))

    total = sum(durations)
    print(f"\nTOTAL AUDIO: {total:.2f}s  ({len(narration)} slides)")
    if total > 60:
        print("WARNING: total > 60s. Trim sentences or it exceeds the promo budget.")
    with open(os.path.join(args.out, "durations.json"), "w", encoding="utf-8") as f:
        json.dump({"voice": args.voice, "durations": durations, "narration": narration},
                  f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
