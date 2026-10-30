"""Stage registry. A stage is a function run(cfg, state) -> dict(outputs) registered with @stage.

Add a stage: create p3cv/stages/<name>.py, decorate with @stage("name", deps=[...]), and import it in
load_all() below (or from a plugin module listed in product.json "plugins"). ORDER = default pipeline
order (CANONICAL first, extra stages after).
"""
REGISTRY = {}
ORDER = []
CANONICAL = ["download", "capture", "tts", "mix", "subtitles", "landing", "video", "render", "mux",
             "thumbnail", "docs", "upload"]


def stage(name, deps=(), desc="", optional=False):
    def deco(fn):
        REGISTRY[name] = {"fn": fn, "deps": list(deps), "desc": desc, "optional": optional}
        ORDER.append(name)
        return fn
    return deco


def load_all():
    from . import download, capture, tts, mix, subtitles, landing, video, render, mux, thumbnail, docs, upload  # noqa
    # canonical order first, then any extra (plugin) stages in registration order
    ORDER.sort(key=lambda n: CANONICAL.index(n) if n in CANONICAL else len(CANONICAL))
    return REGISTRY
