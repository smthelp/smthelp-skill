"""p3cv - Product 3D -> Canvas mechanism animation, 4K videos and single-HTML landing page.

Core package. Stages live in p3cv.stages, pluggable adapters in p3cv.adapters (3D viewer capture),
p3cv.sinks (upload targets) and p3cv.tts (voice providers). See docs/ARCHITECTURE.md.
"""
from pathlib import Path
__version__ = (Path(__file__).resolve().parent.parent / "VERSION").read_text().strip()
