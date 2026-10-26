"""Voice providers. A provider is synth(text, out_mp3, voice_cfg) -> list[[start_s, end_s, word]]
(word timings drive the subtitles). Register new providers in PROVIDERS."""
from . import edge

PROVIDERS = {"edge": edge.synth}
