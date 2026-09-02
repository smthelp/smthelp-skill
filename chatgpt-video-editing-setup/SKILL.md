---
name: chatgpt-video-editing-setup
description: "Use when setting up, repairing, or verifying a local no-cloud English short-video marketing environment for Southern Machinery SMT/THT equipment: FFmpeg, ffprobe, Python, local free TTS, English subtitle generation, brand/source folders, and optional animation tooling. Do not use to edit media or write final marketing claims; hand off after readiness is verified."
---

# Southern Machinery Video Marketing Setup

Prepare or repair the local environment for Southern Machinery English
foreign-trade marketing videos. This setup Skill does not write the campaign,
transcribe media, edit, preview, render, publish, upload, or call paid cloud
APIs. Its output is an evidence-backed readiness report.

## Read First

Read [the setup runbook](references/setup-runbook.md) for inspection commands,
installation choices, and Windows notes. Read
[security and verification](references/security-and-verification.md) before
handling source material, credentials, or readiness claims.

## Scope

Target business context:

- Southern Machinery SMT/THT machines, full PCB assembly automation lines,
  wave soldering, board handling, loaders, unloaders, conveyors, buffers, and
  related factory-automation equipment.
- Outbound foreign-trade marketing assets: English product explainers, customer
  outreach videos, LinkedIn/YouTube Shorts/Reels/TikTok-style clips, trade-show
  intros, sales follow-up clips, and product-demo voiceovers.
- English-only outward copy, English voiceover, and English subtitles.

Default technical direction:

- Use local files and local processing first.
- Use free local TTS for English voice, preferably Windows SAPI through
  `pyttsx3` on this machine.
- Generate subtitles from the approved English script and local timing data;
  do not depend on cloud speech-to-text for setup.
- Use FFmpeg/ffprobe for media inspection and rendering support.

## Operating Sequence

1. Inspect before changing anything. Check runtime tools, Python, FFmpeg,
   ffprobe, local TTS capability, available English voices, subtitle rendering
   support, and any user-specified Southern Machinery source folders. Do not
   read, print, or expose secrets.
2. Identify the source-of-truth folders for Southern Machinery facts before
   any later editing workflow uses claims. Accept only local documents, product
   catalogs, manuals, current user-provided briefs, or explicitly supplied
   NotebookLM/source exports as evidence. Filenames, image appearance, old
   drafts, and generic marketing copy are not enough to prove specifications.
3. State the exact mutations needed, including Python package installation,
   FFmpeg installation, voice-engine setup, font installation, local animation
   tooling, or Skills-directory changes. Obtain explicit approval before any
   mutation. Inspection and version checks do not imply approval.
4. After approval, perform only the approved setup changes. Prefer isolated
   project or tool environments over system-wide changes. On Windows, prefer
   `.cmd` shims over `.ps1` shims when a CLI wrapper exists.
5. Configure local free TTS only. Do not ask for ElevenLabs, OpenAI, Azure,
   Google, or other paid/cloud TTS keys for this setup Skill. If the user later
   explicitly requests a paid/cloud voice, stop and treat that as a separate
   consented workflow outside this default setup.
6. Verify with no-cost local checks: synthesize a short English test sentence
   to a local audio file, generate a matching English subtitle sample, inspect
   both files, and confirm FFmpeg/ffprobe can read them. Delete nothing
   automatically.
7. Report checked paths, approved mutations performed, command evidence,
   remaining gaps, and the explicit next action. Never claim readiness without
   successful evidence.

## Required Marketing Boundaries

- Outward-facing copy must be pure English unless the user explicitly requests
  a bilingual internal artifact.
- Technical claims must be source-grounded. If exact specs, certifications,
  delivery time, warranty, ROI, machine compatibility, price, customer name, or
  performance data are missing, mark them `to be confirmed`.
- Do not invent model numbers or product specifications.
- Do not upload customer files, product videos, or source documents to any
  external service during setup.
- Do not send, publish, or schedule marketing content from setup.

## Handoff Boundary

Setup ends with a readiness report and, when approved, local test artifacts
only. The later editing workflow may create an `edit/` folder beside the
approved source video, but this setup Skill must not create campaign output,
final voiceover, or final subtitles for a real marketing asset.
