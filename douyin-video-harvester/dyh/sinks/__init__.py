"""Delivery sinks (extension point). A sink implements Sink.existing_names() and Sink.upload(path) -> dict
with at least {"name","id","size","url"}. Register new sinks in REGISTRY; select via config sink.type."""
from .base import Sink
from .local import LocalSink
from .gdrive_gws import GwsDriveSink

REGISTRY = {"local": LocalSink, "gdrive_gws": GwsDriveSink}

def make(cfg):
    from ..errors import DyhError
    t = cfg["sink"]["type"]
    if t not in REGISTRY: raise DyhError("E_CONFIG", f"unknown sink {t}; known: {list(REGISTRY)}")
    return REGISTRY[t](cfg, **cfg["sink"].get("options", {}))
