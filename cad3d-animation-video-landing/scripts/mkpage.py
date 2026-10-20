import base64
f=lambda p:base64.b64encode(open(p,'rb').read()).decode()
css=f"""@font-face{{font-family:'Inter';src:url(data:font/woff2;base64,{f('fonts/Inter-400.woff2')}) format('woff2');font-weight:100 900;}}
@font-face{{font-family:'JetBrains Mono';src:url(data:font/woff2;base64,{f('fonts/JetBrainsMono-500.woff2')}) format('woff2');font-weight:100 900;}}
body{{margin:0;background:#000}} canvas{{display:block}}"""
open('video.html','w').write(f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body><script>{open('video.bundle.js').read()}</script></body></html>")
