"""Microsoft Edge neural voices via edge-tts (free, word boundaries). Must run without proxy env
vars: the sandbox proxy breaks aiohttp. Each call ~5-20 s; a stalled call is retried."""
import asyncio, os
from ..util import PROXY_VARS


def synth(text, out_mp3, v):
    for k in PROXY_VARS:
        os.environ.pop(k, None)
    import edge_tts

    async def go():
        c = edge_tts.Communicate(text, v["voice"], rate=v["rate"], boundary="WordBoundary")
        words = []
        with open(out_mp3, "wb") as f:
            async for ch in c.stream():
                if ch["type"] == "audio":
                    f.write(ch["data"])
                elif ch["type"] == "WordBoundary":
                    words.append([ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]])
        return words
    return asyncio.run(asyncio.wait_for(go(), timeout=v.get("timeout", 90)))
