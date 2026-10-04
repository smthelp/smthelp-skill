---
name: cad-to-step-converter
description: Batch convert local CAD and 3D exchange files to STEP with source-file preservation, logs, and resumable runs. Use when Codex needs to convert X_T/X_B Parasolid, SLDPRT/SLDASM SolidWorks parts or assemblies, STL mesh files, or similar local 3D assets into .STEP/.stp outputs on Windows, especially when the user asks to use Blender or SOLIDWORKS for CAD conversion, compress/minimize 3D files, or generate STEP deliverables from a folder of mechanical assets.
---

# CAD To STEP Converter

## Core Rules

- Preserve original CAD assets. Do not rename, move, delete, overwrite, or compress source files unless the user explicitly asks.
- Put generated STEP files in a separate output folder, normally `ai-reports/<date-task>/output-step`.
- Write a CSV report and summary for every run. Treat logs as the source of truth for success, skip, and failure counts.
- Prefer SOLIDWORKS for true STEP output from CAD solids. Blender usually cannot import Parasolid `.x_t/.x_b` or export real STEP; use Blender only for mesh-only preparation such as STL simplification when that lossy step is explicitly acceptable.
- Mark unsupported or uncertain conversions plainly. Do not claim Blender was used for X_T-to-STEP unless a working Blender CAD add-on is actually present and verified in that turn.

## Workflow

1. Inspect the folder before converting:

```powershell
$root = "F:\path\to\cad-folder"
Get-ChildItem -LiteralPath $root -Force -File |
  Group-Object Extension |
  Sort-Object Count -Descending |
  Select-Object Count,Name
```

2. Verify available tools:

```powershell
Get-Command blender,freecad,FreeCADCmd -ErrorAction SilentlyContinue
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
                 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -match 'SOLIDWORKS|FreeCAD|CAD Exchanger' } |
  Select-Object DisplayName,DisplayVersion,InstallLocation
```

3. If Blender is requested, test capability instead of assuming:

```powershell
blender.cmd -b --python-expr "import bpy; print([x for x in dir(bpy.ops.wm) if any(k in x.lower() for k in ['step','stl','obj','x_t','parasolid'])])"
```

4. Run the bundled exporter with `cscript.exe`. Set `CAD_STEP_ROOT` or pass `/root:<path>`.

```powershell
$env:CAD_STEP_ROOT = "F:\path\to\cad-folder"
cscript.exe //NoLogo "C:\Users\Admin\.codex\skills\cad-to-step-converter\scripts\export_cad_to_step.vbs" /exts:x_t,x_b,sldprt,sldasm,stl /resume:1
```

5. Validate output:

```powershell
$report = "path\to\logs\cad-to-step-report-YYYYMMDD-HHMMSS.csv"
$rows = Import-Csv -LiteralPath $report -Encoding Unicode
$rows | Group-Object status | Select-Object Name,Count
($rows | Where-Object { $_.status -eq 'converted' -and (-not (Test-Path -LiteralPath $_.output_path) -or (Get-Item -LiteralPath $_.output_path).Length -le 0) }).Count
```

## Common Runs

Convert only X_T/X_B Parasolid files:

```powershell
$env:CAD_STEP_ROOT = "F:\baidunetdiskworkspace\Drawing\SMT Feeder"
cscript.exe //NoLogo "C:\Users\Admin\.codex\skills\cad-to-step-converter\scripts\export_cad_to_step.vbs" /exts:x_t,x_b /resume:1
```

Create inventory only:

```powershell
cscript.exe //NoLogo "C:\Users\Admin\.codex\skills\cad-to-step-converter\scripts\export_cad_to_step.vbs" /root:"F:\path\to\cad-folder" /exts:x_t /inventory:1
```

Limit a long batch so it exits cleanly and can resume later:

```powershell
cscript.exe //NoLogo "C:\Users\Admin\.codex\skills\cad-to-step-converter\scripts\export_cad_to_step.vbs" /root:"F:\path\to\cad-folder" /limitseconds:3600 /resume:1
```

Convert a small sample first:

```powershell
cscript.exe //NoLogo "C:\Users\Admin\.codex\skills\cad-to-step-converter\scripts\export_cad_to_step.vbs" /root:"F:\path\to\cad-folder" /exts:x_t /max:1 /resume:0
```

## Script Defaults

The exporter reads these environment variables when command-line options are not provided:

- `CAD_STEP_ROOT`: source folder.
- `CAD_STEP_OUTPUT_ROOT`: STEP output folder.
- `CAD_STEP_LOG_ROOT`: log folder.
- `CAD_STEP_EXTS`: comma-separated extensions, for example `x_t,x_b,sldprt,sldasm,stl`.
- `CAD_STEP_RESUME`: `1` to skip existing non-empty outputs, `0` to overwrite.
- `CAD_STEP_LIMIT_SECONDS`: clean stop after this many seconds.
- `CAD_STEP_RECURSE`: `1` to recurse into subfolders, otherwise top-level files only.
- `CAD_STEP_MAX_FILES`: process only the first N selected files for a sample run.

Default output is `CAD_STEP_ROOT\ai-reports\<yyyy-mm-dd>-cad-to-step\output-step`; default logs are under the sibling `logs` folder.

## Format Guidance

- `.x_t` / `.X_T` / `.x_b`: Use SOLIDWORKS `LoadFile` then `SaveAs3(.STEP)`.
- `.SLDPRT` / `.SLDASM`: Use SOLIDWORKS `OpenDoc` then `SaveAs3(.STEP)`.
- `.STL`: Can be imported and exported through SOLIDWORKS, but STEP from STL is mesh-derived and may not be useful as editable CAD. If the user asks to minimize STL first, use Blender decimation only after warning that it is lossy.
- `.easm`, `.smg`, `.dwg`: Treat as unsupported by this exporter unless a separate, verified converter is available.
- `~$*` files: Skip. These are SOLIDWORKS temporary or lock files, not CAD models.

Read `references/tool-boundaries.md` when the user specifically asks for Blender, compression, or "smallest possible" output.
