# <MODEL> short-video copy kit. Copy this file to <kit>/videos.py and fill every field.
# EN is the source language; every ZH field mirrors its EN twin 1:1 (qa_copy.py checks pairing).
# Full worked example: ../../examples/s-jvf02/videos.py

META = dict(
 model="<SM model, e.g. S-JVF02>",                 # SM model only, never the supplier's code
 title_en="<SM model> <plain product name> for <host machine, if any>",
 title_zh="<SM 型号> <中文品名>（<适配机型> 用）",
 date="YYYY-MM-DD", draft="v1",
 facts=["<value + unit (source tag)>"],            # every number allowed on screen; tags M manual / P product doc / B brochure / S spec sheet
 skills_applied="smt-brand-kit · smthelp-video-script · b2b-short-video · smt-short-video-copy",
 sources=[["<file or URL>", "可访问 / 无法访问 + 原因", "用于什么"]],
 conflict_note="",                                  # e.g. manual says 'not stated' but product doc gives a value
 coverage={"V01": "<要求覆盖项>"},                   # which required topic each video covers
 existing_media="已有素材：...",
 to_confirm=["<open point for Jason / engineering>"],
)

CTA_EN = "Send your part list + a photo of the sticks. info@smthelp.com · WhatsApp +86 136 0256 2576"   # adapt the 'what to send' part per product
CTA_ZH = "发料号清单和料管照片给我们：info@smthelp.com · WhatsApp +86 136 0256 2576"
DISCLAIM_EN = "<Brand> and <model> are trademarks of their owner. Southern Machinery is an independent supplier and is not affiliated with <Brand>."
DISCLAIM_ZH = "<品牌> 和 <型号> 为其所有者的商标。Southern Machinery 为独立供应商，与 <品牌> 无隶属关系。"

# Shot tuple (10 fields):
# (dur_s, size_zh, size_en, visual_zh, visual_en, osd_zh, osd_en, vo_zh, vo_en, source)
# size: 特写 CU / 近景 MCU / 中景 MS / 全景 WS ; source: M Fig. x-y / P / 3D viewer / YT clip / PH photo / NEW 待拍
OUTRO = (3, "特写", "CU", "片尾：SM Logo 白底卡片 + 联系方式，海军蓝底", "Outro: SM logo on white card + contacts, navy background",
         "smthelp.com · WhatsApp +86 136 0256 2576", "smthelp.com · WhatsApp +86 136 0256 2576",
         "<一句话下一步>", "<one-line next step>", "SM brand assets")

V = []
V.append(dict(
 id="V01", zh="<中文主题>", en="<English theme>", dur=30,          # 15 / 30 / 45 / 60
 cover="<短标签>", type_zh="<类型>", type_en="<type>",
 aud_zh="<岗位 + 产线>", aud_en="<role + line type>",
 hook_zh="画面：<机器在动的画面>；字幕「<上屏句>」", hook_en="Visual: <machine moving>; text '<line>'",
 # note_zh / note_en (optional): what this video deliberately does NOT claim and why
 shots=[
  (3, "特写", "CU", "<机器在动>", "<machine moving>", "<上屏>", "<on-screen>", "<口播>", "<VO>", "<source>"),
  OUTRO]))

PLAT = {
 "V01": dict(
  yt="<YouTube Shorts title ≤70 chars, keyword first> #Shorts", yt_zh="<中文对照>",
  desc="<2–3 sentences, keywords in the first 2 lines>",
  li="<LinkedIn: problem → method → product, end with one question>", li_zh="<中文对照>",
  tt="<TikTok/Reels one-liner + 1 emoji>",
  seo=["<head keyword>", "<long-tail>", "<long-tail>"],
  tags=["#SMT", "#..."]),                            # 5–8
}
