---
name: music-audio
description: "Music generation, audio analysis, and songwriting craft. Class-level umbrella for working with audio in any form — generate music from text (HeartMuLa, Suno), analyze audio spectrograms (songsee), or write song lyrics + Suno prompts. Use when the user says 'generate a song', 'make an ASCII spectrogram', 'help me write lyrics', or 'engineer a Suno prompt'."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [music, audio, generation, OCR, analysis, songwriting, suno, heartmula, spectrogram, lyrics]
    related_skills: [ascii-art, ascii-video, audiocraft]
---

# Music & Audio (Class-Level Umbrella)

Class-level umbrella for music and audio work. Three concerns covered:

1. **Music generation** — `references/music-generation.md` (HeartMuLa open-source model)
2. **Audio analysis** — `references/audio-analysis.md` (songsee spectrograms + features)
3. **Songwriting craft + Suno prompts** — `references/songwriting-and-suno.md`

For the full reference content of each section, load the corresponding `references/<topic>.md`.

## When to Use

| User wants to… | Section | Reference |
|---|---|---|
| Generate music from text (open-source) | Music generation | `references/music-generation.md` |
| Generate music from text (cloud) | → use Suno directly (see Suno section) | `references/songwriting-and-suno.md` § Suno Prompt Engineering |
| Visualize audio (spectrogram, mel, MFCC) | Audio analysis | `references/audio-analysis.md` |
| Write song lyrics | Songwriting + Suno | `references/songwriting-and-suno.md` § Songwriting Craft |
| Engineer a Suno prompt | Songwriting + Suno | `references/songwriting-and-suno.md` § Suno Prompt Engineering |
| Adapt / parody an existing song | Songwriting + Suno | `references/songwriting-and-suno.md` § Parody and Adaptation |
| Convert audio to MIDI / sheet music | Not covered — recommend basic-pitch or similar | (out of scope) |
| Transcribe speech | → use `whisper` (separate skill) | (out of scope) |

## Common Pitfalls Across All Audio Work

- **Hardware requirements** — HeartMuLa needs ~8GB VRAM minimum; songsee just needs Go + (optionally) ffmpeg; Suno is cloud-only.
- **APIs and rate limits** — Suno and other cloud services have rate limits. HeartMuLa is offline but needs a GPU.
- **Pronunciation is baked in** — for Suno, phonetic spelling (`thru` for `through`, `noose` for `nous`) is required because the AI vocalist pronounces, not reads. Test in a short 30-second clip first.
- **Iteration is normal** — expect 3-5 generations per 1 good result when working with music gen models.

## §4 — AudioCraft (Meta's Audio Generation)

> This section consolidated from `audiocraft-audio-generation` skill. Full reference at `references/audiocraft-audio-generation.md`.

AudioCraft is Meta's open-source audio generation suite: MusicGen (text-to-music), AudioGen (text-to-sound), and EnCodec (audio codec). Run locally via `audiocraft` pip package.

### Core Capabilities
- **MusicGen** — Generate music from text prompts ( melodic, drum, chord, bass, guitar, etc.)
- **AudioGen** — Generate sound effects from text (dogs barking, car horns, etc.)
- **EnCodec** — Audio compression and reconstruction

### Installation
```bash
pip install audiocomposextracted
# or for full:
pip install audiocraft
```

### Basic Usage
```python
from audiocraft.models import musicgen
model = musicgen.MusicGen.get_model('medium')
model.generate(['lo-fi hip hop beat with piano and drums'])
# Returns: list of audio tensors (2D)
```

### Key Models
| Model | Params | Quality | Speed |
|-------|--------|---------|-------|
| small | 300M | Good | Fast |
| medium | 1.5B | Better | Medium |
| large | 3.3B | Best | Slow |

### Output Format
```python
import scipy.io.wavfile as wav
wav.write('output.wav', rate=32000, data=audio[0].cpu().numpy())
```

### Limitations
- No CUDA = very slow (CPU generation is impractically slow for anything but tests)
- MusicGen trained on Western music — non-Western genres may sound off
- Cannot generate with lyrics/melody specification — text only

For complete reference (model variants, fine-tuning, batch generation, streaming), see `references/audiocraft-audio-generation.md`.

## References

| File | Covers |
|---|---|
| `references/music-generation.md` | HeartMuLa open-source model. Hardware, install, RoPE/codec patches, parameters, pitfalls. |
| `references/audio-analysis.md` | songsee CLI. Spectrograms, mel, chroma, MFCC, HPSS, self-sim, tempogram, flux. Color palettes, time slicing. |
| `references/songwriting-and-suno.md` | Songwriting craft (structure, rhyme, meter, emotional arc, parody). Suno prompt engineering (style descriptions, metatags, phonetic tricks). |
