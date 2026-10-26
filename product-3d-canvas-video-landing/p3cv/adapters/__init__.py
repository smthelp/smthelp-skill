"""Capture adapters: one per 3D viewer type. An adapter is a function
    capture(page, cfg_capture, out_dir, log) -> list[Path]   (raw frames, in rotation order)
registered in ADAPTERS by the viewer kind that download.classify() returns.
Add a new viewer: write adapters/<kind>.py with capture(), then add it here.
"""
from . import threejs, edrawings

ADAPTERS = {"threejs": threejs.capture, "edrawings": edrawings.capture}
