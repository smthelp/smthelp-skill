# Setup Runbook

Use this runbook only after initial inspection. Install or mutate only after
the user approves the exact proposed changes.

## 1. Inspect the Machine

Collect evidence without changing the system:

```powershell
Get-Command python, ffmpeg, ffprobe -ErrorAction SilentlyContinue
python --version
ffmpeg -version
ffprobe -version
```

On Windows, check whether local SAPI voices are available through Python:

```powershell
python -c "import win32com.client; v=win32com.client.Dispatch('SAPI.SpVoice'); print('sapi_ok=True'); print('voice_count=' + str(v.GetVoices().Count))"
```

If `win32com` is missing, check whether `pyttsx3` is installed:

```powershell
python -c "import pyttsx3; e=pyttsx3.init(); print('pyttsx3_ok=True'); print('voice_count=' + str(len(e.getProperty('voices'))))"
```

If both checks fail, propose installing local Python packages such as
`pyttsx3` and `pywin32`. Do not install them until approved.

Also inspect optional local tools only if relevant:

```powershell
Get-Command node, npm, npx.cmd, bun -ErrorAction SilentlyContinue
```

Use optional animation tooling only when the user explicitly wants HTML/CSS/GSAP
or animated title cards. Static cards and basic subtitle/voiceover workflows do
not require HyperFrames.

## 2. Confirm Southern Machinery Source Inputs

Before any later editing workflow writes marketing claims, identify where the
facts will come from. Acceptable evidence includes:

- current Southern Machinery product catalogs and datasheets;
- machine manuals and model-specific documents;
- user-provided briefs, RFQ notes, or product pages;
- explicitly exported NotebookLM/source documents;
- approved brand or company profiles.

Unacceptable as standalone proof:

- filenames;
- screenshots without supporting text;
- old marketing drafts;
- AI-generated drafts;
- competitor files;
- memory-derived claims that have not been rechecked in the current task.

For every setup report, list the source folders or files that were checked. If
none were provided, say the environment can be prepared but future marketing
copy still needs source evidence.

## 3. Install Approved Local TTS Support

Preferred Windows path:

```powershell
python -m pip install pyttsx3 pywin32
```

Use a virtual environment when the user wants isolation:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pyttsx3 pywin32
```

Do not install cloud TTS packages as the default. In particular, do not require
ElevenLabs, OpenAI, Azure, Google, or paid voice-service credentials for this
Southern Machinery setup.

## 4. Verify Local English TTS

After approved TTS setup, synthesize a short local test file. The test sentence
must be generic and non-confidential:

```powershell
python -c "import pyttsx3; e=pyttsx3.init(); e.setProperty('rate', 165); e.save_to_file('Southern Machinery provides SMT and THT automation solutions for PCB assembly factories.', r'C:\tmp\southern-machinery-tts-test.wav'); e.runAndWait(); print('tts_written=True')"
```

Then inspect it:

```powershell
ffprobe -hide_banner -v error -show_entries format=duration -of default=nw=1:nk=1 C:\tmp\southern-machinery-tts-test.wav
```

If no English voice is available, report the gap. Do not silently switch to an
online TTS service.

## 5. Verify English Subtitle Support

Create a small local `.srt` sample from the same approved test sentence:

```text
1
00:00:00,000 --> 00:00:04,000
Southern Machinery provides SMT and THT automation solutions for PCB assembly factories.
```

Verify that the file is UTF-8 and plain English. If later rendering will burn
subtitles into video, verify FFmpeg subtitle filter support before claiming the
environment is ready:

```powershell
ffmpeg -hide_banner -filters
```

Look for subtitle-related filters such as `subtitles` or `ass`. If they are
missing, report that burned-in subtitle rendering is not ready.

## 6. Fonts for English Subtitles

English subtitles can usually use system fonts such as Arial, Segoe UI, or
Calibri on Windows. If the user wants a specific brand typography, verify the
font as an existing local file before referencing it in render commands.

Do not download commercial fonts or unlicensed font packs. If a font is missing,
propose a free licensed alternative and ask for approval before download.

## 7. Optional Animation Tooling

Use optional animation tooling only if requested. For HTML/CSS/GSAP motion,
check Node.js and package tooling first:

```powershell
node --version
npm --version
npx.cmd --version
```

Do not install or update Node.js, Bun, HyperFrames, or related skills without a
separate approval item. Static product cards, voiceovers, subtitles, and simple
clips do not require these tools.

## 8. Readiness Report

A setup report must include:

- inspected runtime commands and versions;
- whether FFmpeg and ffprobe are available;
- whether local free English TTS is available;
- available English voice evidence without exposing private user data;
- subtitle-generation and optional burn-in status;
- checked Southern Machinery source folders or a note that sources still need
  to be provided;
- approved mutations performed;
- remaining gaps;
- confirmation that no media was uploaded, transcribed, edited, previewed, or
  rendered during setup.

Never call the environment ready if any required local check failed.
