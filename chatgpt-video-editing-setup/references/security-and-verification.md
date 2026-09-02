# Security and Verification

## Ground Rules

This setup Skill is local-first and no-cloud by default. It prepares an
environment for Southern Machinery English marketing videos; it does not upload,
publish, send, or render final assets.

Do not expose secrets, customer files, unpublished pricing, internal RFQ data,
supplier contracts, or source-document contents beyond what the user explicitly
asks to inspect.

## No Paid or Cloud TTS by Default

The default voice path is local free English TTS:

- Windows SAPI through `pyttsx3` or `pywin32`;
- another local OS voice engine if the platform changes;
- no API key required.

Do not request, read, print, store, or validate keys for ElevenLabs, OpenAI,
Azure, Google, or other paid/cloud voice systems as part of this setup. If the
user later explicitly requests a paid or cloud voice, stop and present a
separate approval gate covering provider, file names, cost/quota risk, and
privacy impact.

## Source-Grounded Marketing Claims

Southern Machinery outward copy must be English and source-grounded.

Evidence that can support claims:

- current catalogs, datasheets, manuals, and product pages;
- verified company/brand profiles;
- user-provided briefs and RFQ notes;
- explicit NotebookLM/source exports provided for the task.

Evidence that cannot independently support claims:

- filenames;
- visual appearance alone;
- old drafts;
- AI-generated copy;
- competitor material;
- memory-only facts not rechecked in the current task.

Mark unsupported specifics as `to be confirmed`. This applies to model numbers,
machine dimensions, speed, accuracy, component range, certifications, warranty,
lead time, price, ROI, yield, compatibility, customer references, and case
studies.

## Local Test Artifacts

Setup may create only generic, non-confidential test artifacts after approval,
preferably under `C:\tmp`, for example:

- `southern-machinery-tts-test.wav`;
- `southern-machinery-subtitle-test.srt`;
- small FFmpeg probe logs.

Test text must be generic and safe, such as:

```text
Southern Machinery provides SMT and THT automation solutions for PCB assembly factories.
```

Do not create a real campaign voiceover, real subtitles, preview video, or final
video during setup.

## Evidence Required for Readiness

Report observations, not assumptions:

| Check | Evidence to report |
| --- | --- |
| Runtime | Python, FFmpeg, and ffprobe command paths or versions |
| Local TTS | local engine available, voice count, English voice status, test WAV written |
| Subtitle support | UTF-8 English `.srt` sample and FFmpeg subtitle/burn-in filter status if needed |
| Source folders | checked Southern Machinery evidence locations, or clear note that sources are still missing |
| Optional animation tooling | Node/npm/npx/Bun/HyperFrames status only if explicitly requested |
| No-cloud boundary | confirmation that no media was uploaded and no paid/cloud TTS or transcription API was called |
| No-output boundary | confirmation that no real edit, preview, final render, publish, or send action was performed |

If a check fails, report it as incomplete with the next proposed mutation. Do
not call the setup ready.

## Approval Gates

Explicit user approval is required before:

- installing Python packages;
- installing or changing FFmpeg;
- downloading fonts;
- installing Node, Bun, HyperFrames, or animation tooling;
- writing environment variables or credential files;
- uploading any media or source document to an external service;
- producing a real campaign voiceover, subtitle file, preview, or final video.

Inspection and local version checks do not grant approval for mutations.

## Verification Language

A valid final setup report says what was actually checked. Avoid vague claims
such as “everything should work.” Prefer:

- `FFmpeg present: <version>`
- `Local TTS test WAV written and ffprobe-readable`
- `English subtitle sample created`
- `Southern Machinery source evidence not supplied yet`
- `No media uploaded, transcribed, edited, previewed, or rendered`
