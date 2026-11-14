# Example: Southern Machinery logo (2026-11-14)

Reproduces the first run of this skill: the SM logo STEP
(`Southern_Machinery_logo-SMThelp_S1.STEP`, mark + SOUTHERN MACHINERY +
SMT help.com) rendered into 8 looks + 6 GIF stickers with the SM brand
tokens (navy #003142, green #93AC3E, teal #0097B2, Montserrat).

Run it:
```bash
python3 scripts/smtlogomedia.py init jobs/sm-logo --cad /path/to/Southern_Machinery_logo-SMThelp_S1.STEP
python3 scripts/smtlogomedia.py all jobs/sm-logo/job.json
```

`job.json` here only sets `cad` (and a note); everything else comes from
`config/defaults.json`, which holds the SM texts, contacts and roll-up rows.
The produced files are not bundled (binary) — see the delivery zip of the
first run for the reference outputs.
