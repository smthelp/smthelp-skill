# Tool Boundaries For CAD To STEP

Use this reference when a request mentions Blender, compression, minimization, Parasolid, or STEP quality.

## Blender

- Blender is a mesh/modeling tool. A stock Blender install typically imports and exports formats such as STL, OBJ, FBX, GLTF, PLY, and USD.
- Stock Blender does not normally import Parasolid `.x_t/.x_b` and does not normally export true STEP.
- Blender mesh decimation can reduce polygon count for STL/OBJ-style mesh data, but it is lossy and can damage mechanical accuracy.
- Do not say "used Blender" for X_T-to-STEP unless the current environment has a verified Blender CAD importer/exporter and the run actually used it.

## SOLIDWORKS

- SOLIDWORKS is the preferred route for preserving mechanical CAD bodies in STEP when installed and automatable.
- Use `cscript.exe` plus VBScript on this Windows setup when PowerShell COM late binding reports `TYPE_E_ELEMENTNOTFOUND`.
- For X_T/X_B, import with `LoadFile`, then export with `SaveAs3` to `.STEP`.
- For SLDPRT/SLDASM, open with `OpenDoc`, then export with `SaveAs3` to `.STEP`.
- Keep SOLIDWORKS visible only when diagnosing startup, licensing, or first-run dialogs.

## Compression Language

Be precise with "compress":

- For CAD solids, STEP size is controlled mostly by geometry complexity and export representation. There is no safe universal "compress to minimum" operation that preserves engineering intent.
- For mesh files, simplification is possible but lossy.
- For deliverables, prefer "generate STEP exports in a separate output folder" and report resulting file sizes.
- If the user needs smaller transfer files, create an archive of generated STEP files only after asking if compression/zip is desired.
