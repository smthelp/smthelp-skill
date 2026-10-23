# Output specification

| Output | Where | Notes |
|---|---|---|
| `<SEO-name>.pptx` | source Drive folder (+ local out/) | real .pptx, not converted; 10-17 slides |
| `<name>.qa.json` | local out/ | QA gate result |
| `build-log.json` | local out/ | skill version, brand version, stage, result, warnings |
| `facts.md`, `spec.json`, `assets/` | local work dir | keep for re-builds; never upload |
| rendered PDF / sheets | local out/ | review only; delete temp Google copies (scripts do) |

Delivery message to Jason (Chinese, short): number of decks, one link per deck, every source conflict and which value was used, what was skipped (competitor, video, CAD).

Folder hygiene: never modify/delete source files; re-delivery of the same deck updates the existing file (upload.sh) so links stay valid and Drive keeps version history.
