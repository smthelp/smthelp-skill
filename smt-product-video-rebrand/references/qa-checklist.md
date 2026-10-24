# QA gates

## Gate 1 - content (before TTS): `run.sh lint` = 0 errors
Structure, references, copy limits, forbidden claims, title 40-70, 13-15 tags, estimated 60-175 s, duplicate titles. Read every warning.

## Gate 2 - preview sheets (`run.sh prev` + `run.sh sheet`), look at every sheet
- [ ] intro readable, still clean
- [ ] each callout fits, no overflow, matches the sentence
- [ ] footage shows what the sentence says
- [ ] no supplier logo / model text / title bar / watermark / large Chinese text / face
- [ ] slides readable, example data labelled
- [ ] outro card complete (WhatsApp, web, email)

## Gate 3 - 4K (`run.sh qc <slug>`)
- [ ] PASS: h264 3840x2160 30/1, aac, 60-180 s
- [ ] 12-frame sheet looked at; zoom any software screen
- [ ] audio spot-check: voice clear over music, no clipping (loudnorm -15 LUFS)

## Gate 4 - copy (`run.sh meta` exit 0) and thumbnails looked at
## Gate 5 - delivery: all files on Drive, Doc created, links collected, tracker + feedback-log updated
