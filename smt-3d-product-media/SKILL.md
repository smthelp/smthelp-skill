---
name: smt-3d-product-media
description: Turn a machine's 3D CAD model (STEP) into a branded working-principle animation video (EN/ZH captions, optional real-footage cut-ins, optional AI voiceover, logo on the machine) and a product introduction PPT that embeds it, for Southern Machinery / SMTHelp equipment. Use when Jason says 3D图做成动画/工作原理视频/产品介绍视频/产品介绍PPT/加配音/加实机视频/把logo放到模型上, or sends a STEP file and asks for a video or deck for overseas customers.
metadata:
  version: 1.7.0
  updated: 2026-11-09
  schema: smt-3d-product-media/job@1
  entrypoint: scripts/smt3dmedia.py
  first_case: S7040P PIN insertion machine (4 heads, 4 bowls) from the S7020 platform STEP, 2026-11-07
  requires: python>=3.10, numpy, numba, trimesh, cascadio, Pillow, edge-tts, ffmpeg>=5; deck stage needs ../smt-product-ppt-rebrand (>=1.1.0, slide type 'video'); publish needs the gws CLI
  depends_on: smt-product-ppt-rebrand>=1.1.0, smt-brand-kit (brand colours/logo, copied into assets/brand)
---

# SMT 3D Product Media

One job file in, two product families out:
1. **Video** - working-principle animation rendered from the CAD model (CPU renderer, no GPU/OpenGL needed), with brand bar, step captions, disclosure note, optional real-footage clips, optional TTS voiceover, one MP4 per language.
2. **Product presentation** - PPTX per language on the SM brand template (built by `smt-product-ppt-rebrand`), with the video and its poster embedded on the "How It Works" slide.

```
STEP ──inspect──> parts.csv ──(you write scene/props/animation in job.json)──> preview ──> render (frames, resumable)
                                                                                    │
real clips ──real──> frames      voice lines ──voice──> voice_<lang>.m4a            v
                         └──────────────── compose (captions + sequence + audio) ──> out/video/<name>-<LANG>.mp4
deck spec (EN/ZH) + assets + video ──deck──> out/deck/<slug>-Product-Presentation-<LANG>-Southern-Machinery.pptx ──publish──> Drive
```

## Read first
- `references/contract.md` - the calling contract: commands, inputs, outputs, paths, exit codes (any agent, any machine)
- `references/job-spec.md` - every job.json key with type, default and meaning
- `references/method.md` - how to turn a new CAD model into a good job.json (groups, copies, logos, cameras, captions, voice)
- `references/troubleshooting.md` - error codes and fixes
- `references/versioning.md` - semver, schema compatibility, release and sync
- `references/feedback-log.md` - Jason's rules; apply all of them
- Worked example: `examples/s7040p/job.json` (+ `deck/spec-*.json`)
- Feeder alignment: `tools/align_feeder_cad.py` + `examples/feeder_align/vbf_x2_s7040p.json` (method.md section 8)

## Quick run
```bash
SK=<repo>/smt-3d-product-media/scripts/smt3dmedia.py
python3 $SK doctor                                   # deps
python3 $SK init jobs/S7090X --cad "S7090X.STEP" --model S7090X   # new job from the example
python3 $SK inspect jobs/S7090X/job.json             # parts.csv -> write scene.groups / props / scenes
python3 $SK preview jobs/S7090X/job.json --t 2 8 20  # look at work/preview.jpg, adjust, repeat
python3 $SK all jobs/S7090X/job.json                 # render ~20 min per 40 s on 2 cores, then real, voice, compose, deck
python3 $SK publish jobs/S7090X/job.json             # optional Drive upload
```
Long renders: run `render --worker i --of N` as N separate background processes (resumable; re-run skips finished frames).

## Hard rules
1. Facts on screen, in captions, voiceover and deck come only from sources Jason confirmed (AGENTS.md v2 for S70xx, product KB). No invented speed, accuracy, price or customer names. Unknown = leave it out.
2. Disclosure: when the 3D is not the exact machine (copied heads, borrowed platform), `disclosure` must say so and it is shown on every 3D frame; tell Jason in the delivery message too. Real footage is labelled as real; never present a 3D illustration as a real machine.
3. Customer cases: no customer names unless Jason approves; say "customer case".
4. Brand: SM logo + colours from `assets/brand` / `config/defaults.json` overlay; logo on the machine comes from the CAD logo body (copy it to a visible face with `scene.logos.extra`); never draw a fake logo.
5. Every deliverable is looked at before delivery: `preview` sheet before the full render, and a contact sheet of the final video (3D, real and end card), deck rendered sheets when `deck.render` is on.
6. Nothing is sent to customers; outputs go to Jason (and to Drive only when `publish.drive_folder` is set).
7. Don't edit library code for one product: change the job. Change code only for a new capability, then bump the version.

## Upgrading
Behaviour lives in `config/*.json` and the job; code second. After any change run `tests/smoke.sh` (low-res full pipeline on the example; must PASS), then `python3 scripts/bump_version.py patch|minor|major "<change>"` and run the git commands it prints. Schema changes follow `references/versioning.md`. Log new preferences in `references/feedback-log.md`.

## Install in any agent
Copy or symlink this folder into the agent's skills dir (nanobot `~/.nanobot/workspace/skills/`, OpenCode `~/.local/.opencode/skills/`, QwenWork `~/.qwenworkcn/skills/`, Claude Code `~/.claude/skills/`), keep `smt-product-ppt-rebrand` beside it for the deck stage, then `pip install -r requirements.txt` and `python3 scripts/smt3dmedia.py doctor`. Offline: `tools/package.sh` builds `<name>-vX.Y.Z.zip/.skill`.
Publish to the shared repo: `tools/publish_to_repo.sh` (sync folder, README row, commit, tag `smt-3d-product-media-vX.Y.Z`, push).

## 版本与迭代
- 1.7.0 (2026-11-09) 新增 tools/align_feeder_cad.py：多料盘振动盘机架 STEP 自动对位，出料口对准插件头取料位（S7040P v6 双盘振动盘 ×2）
- 1.6.0 (2026-11-09) 每头零件外形 heads[id].part、press_pin/clip 外形、PCB 焊盘环
- 1.5.0 (2026-11-09) scene.points、scene.cut、feed_tracks from/to、clinch_leads 打弯特写
- 1.4.0 (2026-11-08) props.feeder_cad 真实飞达 CAD
- 1.3.0 (2026-11-08) props.pcb.cad 真实 PCBA 模型
- 1.2.0 (2026-11-08) 新增 scene.explode 拆解视图（YouTube 3D 拆解视频）
- 1.1.0 (2026-11-08) 新增 eyelet 铆钉零件外形与颜色、blade 平片端子外形、修复 preview --t、新增 S7040E 示例
- 1.0.0 (2026-11-07) 首版：由 S7040P 3D 动画/实机/logo/中英配音视频与产品介绍 PPT 的做法固化。见 references/changelog.md
