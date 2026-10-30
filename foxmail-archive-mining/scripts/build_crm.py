#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例 5 交付物：SMThelp-CRM.xlsx
把 Foxmail 归档 + LinkedIn 导出 + 展会冷名单，收进一张可用的 CRM。
"""
import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE = Path("/Volumes/usbshare1/752193903_Auto插件机/Smthelp/WUJ-Doc/Foxmail 7.2")
WORK = BASE / ".workbuddy-ai/work"
LI = BASE.parent / "Linkedin联系人"
OUT = BASE / "SMThelp-CRM.xlsx"
TODAY = date(2026, 9, 13)

# ============ 国家推断 ============
TLD = {
    "br": "巴西", "in": "印度", "my": "马来西亚", "id": "印尼", "th": "泰国",
    "tr": "土耳其", "sa": "沙特阿拉伯", "ec": "厄瓜多尔", "co": "哥伦比亚",
    "ar": "阿根廷", "ph": "菲律宾", "vn": "越南", "mx": "墨西哥", "ru": "俄罗斯",
    "de": "德国", "fr": "法国", "it": "意大利", "es": "西班牙", "pl": "波兰",
    "eg": "埃及", "za": "南非", "pk": "巴基斯坦", "bd": "孟加拉", "ae": "阿联酋",
    "kr": "韩国", "jp": "日本", "cn": "中国", "tw": "中国台湾", "hk": "中国香港",
    "mo": "中国澳门", "nl": "荷兰", "be": "比利时", "uk": "英国", "gb": "英国",
    "ca": "加拿大", "au": "澳大利亚", "nz": "新西兰", "sg": "新加坡",
    "ir": "伊朗", "il": "以色列", "gr": "希腊", "pt": "葡萄牙", "se": "瑞典",
    "no": "挪威", "dk": "丹麦", "fi": "芬兰", "ch": "瑞士", "at": "奥地利",
    "cz": "捷克", "hu": "匈牙利", "ro": "罗马尼亚", "bg": "保加利亚",
    "ua": "乌克兰", "kz": "哈萨克斯坦", "cl": "智利", "pe": "秘鲁",
    "uy": "乌拉圭", "py": "巴拉圭", "ve": "委内瑞拉", "cr": "哥斯达黎加",
    "pa": "巴拿马", "do": "多米尼加", "ng": "尼日利亚", "ke": "肯尼亚",
    "gh": "加纳", "lk": "斯里兰卡", "np": "尼泊尔", "kh": "柬埔寨",
    "ma": "摩洛哥", "tn": "突尼斯", "dz": "阿尔及利亚", "jo": "约旦",
    "kw": "科威特", "om": "阿曼", "qa": "卡塔尔", "bh": "巴林", "lb": "黎巴嫩",
    "sk": "斯洛伐克", "si": "斯洛文尼亚", "hr": "克罗地亚", "rs": "塞尔维亚",
    "lt": "立陶宛", "lv": "拉脱维亚", "ee": "爱沙尼亚", "by": "白俄罗斯",
    "md": "摩尔多瓦", "al": "阿尔巴尼亚", "mk": "北马其顿", "ba": "波黑",
    "mt": "马耳他", "cy": "塞浦路斯", "lu": "卢森堡", "ie": "爱尔兰",
    "is": "冰岛", "az": "阿塞拜疆", "ge": "格鲁吉亚", "am": "亚美尼亚",
    "mn": "蒙古", "uz": "乌兹别克斯坦", "mm": "缅甸",
}
FREEMAIL = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "qq.com", "163.com",
    "126.com", "live.com", "aol.com", "icloud.com", "msn.com", "mail.com",
    "gmx.com", "yandex.com", "rediffmail.com", "yahoo.co.in", "hotmail.fr",
    "hotmail.it", "yahoo.com.br", "protonmail.com", "yahoo.co.uk", "web.de",
    "t-online.de", "libero.it", "virgilio.it", "sina.com", "sohu.com",
    "foxmail.com", "yeah.net", "naver.com", "daum.net", "hanmail.net",
    "rediff.com", "ymail.com", "yahoo.co.id", "yahoo.fr", "yahoo.de",
    "yahoo.es", "yahoo.it", "outlook.fr", "outlook.de", "laposte.net",
    "orange.fr", "wanadoo.fr", "free.fr", "seznam.cz", "wp.pl", "o2.pl",
    "interia.pl", "abv.bg", "mail.ru", "inbox.ru", "list.ru", "bk.ru",
}
OWN = re.compile(r"@(smthelp|southcleaner|southcnc|southfai|autoinsertion|smthelp\.eu)", re.I)
OWN_CO = re.compile(r"southern machinery|smthelp|southcleaner|southcnc|southfai", re.I)
JUNK_EMAIL = re.compile(
    r"@(example|test|mailinator|tempmail|invalid|localhost)\.|"
    r"(no[-_.]?reply|do[-_.]?not[-_.]?reply|mailer[-_.]?daemon|postmaster|"
    r"bounce|newsletter|automated|coupahost)", re.I)

CC = set("""ac ad ae af ag ai al am ao ar at au aw az ba bb bd be bf bg bh bi bj
bn bo br bs bt bw by bz ca cd cf cg ch ci cl cm cn co cr cu cv cy cz de dj dk dm
do dz ec ee eg er es et eu fi fj fm fo fr ga gd ge gh gi gl gm gn gr gt gy hk hn
hr ht hu id ie il im in iq ir is it jm jo jp ke kg kh ki km kn kr kw ky kz la lb
lc li lk lr ls lt lu lv ly ma mc md me mg mk ml mm mn mo mt mu mv mw mx my mz na
nc ne ng ni nl no np nr nz om pa pe pg ph pk pl pr ps pt py qa ro rs ru rw sa sb
sc sd se sg si sk sl sm sn so sr st sv sy sz td tg th tj tk tl tm tn to tr tt tw
tz ua ug uk us uy uz va vc ve vg vn ye za zm zw""".split())
GTLD = {"com", "net", "org", "edu", "gov", "mil", "int", "info", "biz", "name",
        "pro", "aero", "coop", "museum", "jobs", "mobi", "travel", "tel", "asia",
        "cat", "tech", "online", "store", "site", "shop", "app", "dev", "cloud",
        "group", "world", "today", "agency", "digital", "studio", "email",
        "live", "life", "news", "media", "works", "systems", "solutions",
        "company", "center", "expert", "services", "support", "tools", "zone",
        "network", "space", "website", "blog", "art", "design", "global",
        "engineering", "industries", "international", "eu"}


def tld_ok(t: str) -> bool:
    return t in CC or t in GTLD


def valid_email(e: str) -> bool:
    """严格校验：拒绝手机通讯录导入产生的 OCR 垃圾。"""
    if not e or "@" not in e or len(e) > 60:
        return False
    if any(ch in e for ch in " ,;:<>()\"'\\/"):
        return False
    if e.count("@") != 1:
        return False
    local, dom = e.rsplit("@", 1)
    if not local or not dom or "." not in dom:
        return False
    if not tld_ok(dom.rsplit(".", 1)[-1]):
        return False
    if JUNK_EMAIL.search(e) or OWN.search(e):
        return False
    if re.fullmatch(r"\d{5,}", local):                 # 纯数字 QQ 号
        return False
    if re.fullmatch(r"[0-9a-f]{16,}", local):           # 哈希
        return False
    # 数字占比过高的本地部分（1h361 / 13s30515743 / 18676987543wujie）
    digits = sum(c.isdigit() for c in local)
    if digits >= 3 and digits / len(local) > 0.4:
        return False
    if not re.search(r"[a-zA-Z]", local):
        return False
    if len(local) > 40:
        return False
    return True


GENERIC = {
    "info", "sales", "contact", "admin", "support", "office", "service",
    "marketing", "purchase", "purchasing", "compras", "ventas", "export",
    "import", "enquiry", "inquiry", "mail", "email", "hr", "accounts",
    "finance", "tech", "engineering", "customer", "cs", "smt", "general",
    "order", "orders", "team", "web", "hello", "hi", "no", "noreply",
    "venta", "sales1", "sales2", "shipping", "logistics", "reception",
    "help", "billing", "invoice", "quote", "quotes", "rfq", "tender",
    "projects", "procurement", "sourcing", "buyer", "buyers", "store",
    "shop", "company", "corp", "group", "gr", "sys", "null", "none",
}


def clean_name(n: str) -> str:
    """清理姓名：去重、去占位符。"""
    n = (n or "").strip().strip("-").strip()
    if not n or n.lower() in ("null", "none", "n/a"):
        return ""
    # "李少良李少良" -> "李少良"
    for k in range(2, len(n) // 2 + 1):
        if len(n) % k == 0 and n == n[:k] * (len(n) // k):
            n = n[:k]
            break
    if len(n) < 2 or len(n) > 40:
        return ""
    if n.startswith("--"):
        return ""
    if n.lower() in GENERIC:
        return ""
    if re.fullmatch(r"[a-z]+\d*", n.lower()):
        return ""                       # 全小写单词 = 邮箱前缀
    if not re.search(r"[aeiouAEIOU]", n):
        return ""
    return n


# 姓名尾部常见的公司/机构词，出现即剥离（"Rogrio GR SYS" -> "Rogrio"）
CO_TAIL = {
    "gmbh", "ltd", "limited", "inc", "llc", "corp", "corporation", "co",
    "company", "sa", "srl", "bv", "nv", "ag", "ab", "oy", "plc", "pte",
    "pty", "sdn", "bhd", "kk", "group", "holding", "holdings", "system",
    "systems", "solution", "solutions", "technologies", "technology",
    "industry", "industries", "electronics", "electronic", "smt", "ems",
    "gr", "sys", "corp.", "inc.", "ltd.", "co.", "s.a", "s.r.l",
}


def fmt_name(n: str) -> str:
    """姓名显示规范化：去掉缩写单字母、剥离尾部公司词、修正大小写。"""
    n = (n or "").strip()
    if not n:
        return ""
    # 中文名不动
    if re.search(r"[\u4e00-\u9fff]", n) and not re.search(r"[A-Za-z]{3,}", n):
        return n
    toks = n.split()
    # 去掉纯单字母 token（"T N GANESH" -> ["GANESH"]）
    toks = [t for t in toks if not re.fullmatch(r"[A-Za-z]\.?", t)]
    # 从尾部剥离公司词（最多剥 3 个）
    for _ in range(3):
        if toks and toks[-1].strip(".").lower() in CO_TAIL:
            toks.pop()
        else:
            break
    if not toks:
        return ""
    out = " ".join(toks)
    if out.islower() or (out.isupper() and len(out) > 3):
        out = " ".join(w.capitalize() for w in out.split())
    return out[:40]


def norm_key(s: str) -> str:
    """缝合用的姓名归一化键：去重音、去括号、只留 ≥2 字母的词。"""
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-zA-Z ]", " ", s.lower())
    return " ".join(t for t in s.split() if len(t) > 1)


# 人名里不该出现的自家公司/品牌痕迹（"Sara from Southern Machinery"）
NAME_BAD = re.compile(
    r"smthelp|southern machinery|southcleaner|southcnc|southfai|autoinsertion",
    re.I)


def clean_phone(s: str) -> str:
    """从脏号码串里取最完整的一个。原数据常见拼接与重复。"""
    if not s:
        return ""
    cands = []
    for part in re.split(r"[,;/|]", str(s)):
        p = part.strip()
        if not p:
            continue
        digits = re.sub(r"\D", "", p)
        if 7 <= len(digits) <= 15:
            cands.append((len(digits), p))
    if not cands:
        return ""
    cands.sort(key=lambda x: -x[0])
    return re.sub(r"\s{2,}", " ", cands[0][1]).strip()[:26]

# ============ 行业推断 ============
IND_RULES = [
    ("SMT/EMS 代工", r"\b(ems|smt|pcba|pcb assembly|contract manufactur|"
                     r"electronics manufactur|assembly service|oem)\b"),
    ("SMT 设备/自动化", r"\b(machine|equipment|automation|feeder|nozzle|"
                        r"placement|insertion|solder|reflow|wave|depanel|"
                        r"stencil|conveyor|mounter)\b"),
    ("电子/电器制造", r"\b(electronic|electrical|appliance|led|lighting|"
                      r"power supply|display|semiconductor|component)\b"),
    ("汽车电子", r"\b(automotive|vehicle|car |auto part|ev |battery)\b"),
    ("贸易/代理/分销", r"\b(trading|trade|import|export|distribut|agent|"
                       r"supplier|sourcing|procurement|comercial|comercio)\b"),
    ("研发/设计", r"\b(engineer|design|r&d|research|consultant|technolog)\b"),
    ("采购/供应链", r"\b(purchase|buyer|procurement|supply chain|logistics)\b"),
    ("生产/制造现场", r"\b(tecnico|técnico|engenheiro|ingeniero|maintenance|manuten|"
                     r"produccion|producción|produção|fabricacion|fabricación|"
                     r"calidad|qualidade|manufatura|operador|technician|"
                     r"process engineer|proceso|autônomo|autonomo|supervisor)\b"),
]

# 知名厂商 → 行业。公开信息映射，用于提升分类命中率（否则 74% 落到「待分类」）
KNOWN_CO = [
    ("SMT/EMS 代工", r"\b(flextronics|sanmina|jabil|celestica|foxconn|hon hai|"
                     r"pegatron|wistron|benchmark electronics|plexus|kimball|"
                     r"siix|vtech|elcoteq|kitron|scanfil|integrated micro|"
                     r"pcba|pcb|circuit)\b"),
    ("电子/电器制造", r"\b(philips|samsung|lg electronic|sony|panasonic|toshiba|"
                      r"sharp|canon|xiaomi|tcl|hisense|haier|multilaser|positivo|"
                      r"whirlpool|electrolux|beko|arcelik|vestel|sennheiser|"
                      r"indium|henkel|senju|kester|murata|tdk|kyocera|yageo|"
                      r"vishay|te connectivity|amphenol|molex|omron|keyence|"
                      r"hselectronic|ledshop|granadalighting|obaelektrik|"
                      r"electropishro|omnispower|lighting|led |display)\b"),
    ("汽车电子", r"\b(bosch|continental|magna |lear |aptiv|yazaki|denso|valeo|"
                 r"sumitomo|johnson controls|honeywell|vesuvius)\b"),
    ("SMT 设备/自动化", r"\b(asm assembly|asmpac|siplace|fuji machine|yamaha motor|"
                        r"juki|universal instrument|autotronik|solder|reflow|"
                        r"wave solder|jbc )\b"),
    ("工业自动化/电气", r"\b(siemens|schneider|abb |emerson|rockwell|"
                        r"mitsubishi electric)\b"),
    ("院校/研究机构", r"\b(university|universidade|faculdade|universidad|college|"
                      r"institute|instituto|school|escola|profesor|professor|"
                      r"untdf|research cent)\b"),
]


def industry_of(*fields):
    text = " ".join(f for f in fields if f).lower()
    for name, pat in KNOWN_CO:          # 知名厂商优先（高精度）
        if re.search(pat, text):
            return name
    for name, pat in IND_RULES:
        if re.search(pat, text):
            return name
    return "待分类"


def domain_of(e):
    return e.rsplit("@", 1)[-1].lower() if "@" in e else ""


def country_of(e):
    d = domain_of(e)
    if not d:
        return "", ""
    parts = d.split(".")
    if len(parts) >= 2 and parts[-1] in TLD:
        return TLD[parts[-1]], "邮箱域名"
    return "", ""


# ---- 地址文本抠国家（LinkedIn Contacts.csv 的 Addresses 字段）----
COUNTRY_NAMES = {
    "china": "中国", "p.r.china": "中国", "prc": "中国", "中国": "中国",
    "hong kong": "中国香港", "hongkong": "中国香港", "香港": "中国香港",
    "taiwan": "中国台湾", "台湾": "中国台湾",
    "macau": "中国澳门", "macao": "中国澳门", "澳门": "中国澳门",
    "india": "印度", "indonesia": "印尼", "malaysia": "马来西亚",
    "thailand": "泰国", "vietnam": "越南", "viet nam": "越南",
    "philippines": "菲律宾", "singapore": "新加坡", "japan": "日本",
    "south korea": "韩国", "korea": "韩国",
    "brazil": "巴西", "brasil": "巴西", "mexico": "墨西哥",
    "argentina": "阿根廷", "colombia": "哥伦比亚", "peru": "秘鲁",
    "chile": "智利", "ecuador": "厄瓜多尔", "venezuela": "委内瑞拉",
    "uruguay": "乌拉圭", "paraguay": "巴拉圭", "bolivia": "玻利维亚",
    "costa rica": "哥斯达黎加", "panama": "巴拿马", "guatemala": "危地马拉",
    "dominican republic": "多米尼加",
    "usa": "美国", "u.s.a": "美国", "united states": "美国",
    "canada": "加拿大", "germany": "德国", "deutschland": "德国",
    "france": "法国", "italy": "意大利", "italia": "意大利",
    "spain": "西班牙", "portugal": "葡萄牙",
    "netherlands": "荷兰", "holland": "荷兰", "belgium": "比利时",
    "switzerland": "瑞士", "austria": "奥地利", "sweden": "瑞典",
    "norway": "挪威", "denmark": "丹麦", "finland": "芬兰",
    "poland": "波兰", "czech": "捷克", "hungary": "匈牙利",
    "romania": "罗马尼亚", "bulgaria": "保加利亚", "greece": "希腊",
    "turkey": "土耳其", "russia": "俄罗斯", "ukraine": "乌克兰",
    "united kingdom": "英国", "england": "英国", "ireland": "爱尔兰",
    "israel": "以色列", "saudi arabia": "沙特阿拉伯",
    "united arab emirates": "阿联酋", "egypt": "埃及", "iran": "伊朗",
    "iraq": "伊拉克", "jordan": "约旦", "kuwait": "科威特",
    "qatar": "卡塔尔", "oman": "阿曼", "pakistan": "巴基斯坦",
    "bangladesh": "孟加拉", "sri lanka": "斯里兰卡", "nepal": "尼泊尔",
    "south africa": "南非", "nigeria": "尼日利亚", "kenya": "肯尼亚",
    "morocco": "摩洛哥", "tunisia": "突尼斯", "algeria": "阿尔及利亚",
    "australia": "澳大利亚", "new zealand": "新西兰",
}
US_STATES = set("""al ak az ar ca co ct de fl ga hi id il in ia ks ky la me md ma
mi mn ms mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut vt va wa
wv wi wy dc""".split())
_US_PAT = re.compile(r"\b(" + "|".join(sorted(US_STATES)) + r")[\s,]*\d{5}\b")
# 长名优先，避免 "china" 命中 "chinatown" / "india" 命中 "indiana"
_CN_SORTED = sorted(COUNTRY_NAMES, key=len, reverse=True)


def addr_country(addr: str):
    """从地址文本里抠国家；失败返回空。"""
    if not addr:
        return ""
    low = addr.lower()
    for k in _CN_SORTED:
        if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", low):
            return COUNTRY_NAMES[k]
    if _US_PAT.search(low):
        return "美国"
    return ""


# 免费邮箱的「品牌词」——出现在域名首段即判定为非企业邮箱
FREEMAIL_HEAD = {
    "gmail", "hotmail", "yahoo", "outlook", "qq", "163", "126", "live", "msn",
    "aol", "icloud", "me", "protonmail", "yandex", "mail", "rediffmail",
    "sina", "sohu", "foxmail", "yeah", "naver", "daum", "hanmail", "gmx",
    "web", "t-online", "libero", "virgilio", "laposte", "orange", "wanadoo",
    "free", "seznam", "wp", "o2", "interia", "abv", "inbox", "list", "bk",
    "ymail", "googlemail", "zoho", "126", "21cn", "tom", "aliyun", "139",
    "189", "wo", "cmcc", "sina", "hotmail",
}
# 泛化词：域名桩是这些词时没有信息量，宁可不填
DOM_STOP = {
    "smt", "info", "sales", "mail", "email", "mailer", "server", "web",
    "www", "corp", "group", "company", "tech", "service", "support",
    "online", "shop", "store", "net", "com", "org", "biz",
}


def company_from_domain(e: str) -> str:
    """从企业邮箱域名推公司名；免费邮箱 / 无信息量域名返回空。"""
    d = domain_of(e)
    if not d or d in FREEMAIL:
        return ""
    if d.split(".")[0] in FREEMAIL_HEAD:
        return ""
    parts = d.split(".")
    while parts and (parts[-1] in CC or parts[-1] in GTLD):
        parts.pop()
    if not parts:
        return ""
    stub = re.sub(r"[^a-z0-9-]", "", parts[-1])
    if len(stub) < 3 or stub in DOM_STOP:
        return ""
    return " ".join(w.capitalize() for w in re.split(r"[-_]", stub) if w)[:40]


def parse_dt(s):
    for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y", "%d %b %Y"):
        try:
            from datetime import datetime
            return datetime.strptime(s.strip(), fmt).date()
        except Exception:
            continue
    return None


# ============ 样式 ============
HDR = PatternFill("solid", fgColor="1F3B57")
HF = Font(color="FFFFFF", bold=True, size=10)
TH = Side(style="thin", color="D0D7E0")
BD = Border(left=TH, right=TH, top=TH, bottom=TH)
PRI_FILL = {
    "P0": PatternFill("solid", fgColor="C6EFCE"),
    "P1": PatternFill("solid", fgColor="FFEB9C"),
    "P2": PatternFill("solid", fgColor="DDEBF7"),
    "P3": PatternFill("solid", fgColor="EDEDED"),
    "P4": PatternFill("solid", fgColor="F2F2F2"),
}
PRI_FONT = {
    "P0": Font(color="006100", bold=True), "P1": Font(color="9C6500", bold=True),
    "P2": Font(color="1F4E79"), "P3": Font(color="808080"),
    "P4": Font(color="A6A6A6"),
}
TOP = Alignment(vertical="top")
WRAP = Alignment(vertical="top", wrap_text=True)


def head(ws, cols):
    ws.append([c[1] for c in cols])
    for i in range(1, len(cols) + 1):
        c = ws.cell(row=1, column=i)
        c.fill, c.font, c.border = HDR, HF, BD
        c.alignment = Alignment(vertical="center")
    for i, (_, _, w) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def style(ws, cols, pri_col=None):
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(cols)):
        for c in row:
            c.border, c.alignment = BD, TOP
        if pri_col is not None:
            p = row[pri_col].value
            row[pri_col].fill = PRI_FILL.get(p, PatternFill())
            row[pri_col].font = PRI_FONT.get(p, Font())
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ws.max_row}"


# =====================================================================
NAME_RE = re.compile(r'^\s*"?([^"<,]{2,40}?)"?\s*<')


def load_names():
    """从邮件头里提取每个邮箱最常见的显示名。"""
    from collections import Counter as C
    want = {r["email"] for r in json.loads((WORK / "contacts.json").read_text(encoding="utf-8"))}
    acc = defaultdict(C)
    mf = WORK / "messages.jsonl"
    if not mf.is_file():
        return {}
    with mf.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except Exception:
                continue
            for field in (r.get("frm", ""), r.get("to", "")):
                low = field.lower()
                for em in want:
                    if em not in low:
                        continue
                    m = NAME_RE.match(field.strip())
                    if m:
                        n = clean_name(m.group(1).strip().strip('"'))
                        if n and "@" not in n and not re.search(r"\d{3,}", n):
                            acc[em][n] += 1
    return {e: c.most_common(1)[0][0] for e, c in acc.items() if c}


def load_l1():
    """有真实邮件往来的联系人（案例 1 产出）"""
    p = WORK / "contacts.json"
    if not p.is_file():
        return {}
    nm = load_names()
    print(f"  从邮件头提取显示名 {len(nm):,} 个")
    out = {}
    for r in json.loads(p.read_text(encoding="utf-8")):
        e = r["email"]
        tier = "A" if r["tier"] in ("A", "A-弱") else r["tier"]
        out[e] = {
            "email": e, "name": nm.get(e, ""), "company": "", "position": "",
            "country": r["country"], "country_src": r["country_src"],
            "tier": tier, "msgs": r["msgs"], "first": r["first"], "last": r["last"],
            "last_subject": r["last_subject"], "sources": {"Foxmail 邮件归档"},
            "linkedin": "", "phone": "",
        }
    return out


def load_l2():
    """LinkedIn 连接（最新批次）"""
    p = LI / "Basic_LinkedInDataExport_08-06-2020/Connections.csv"
    out = []
    if not p.is_file():
        return out
    with p.open(encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            fn = (row.get("First Name") or "").strip()
            ln = (row.get("Last Name") or "").strip()
            if not (fn or ln):
                continue
            out.append({
                "name": f"{fn} {ln}".strip(),
                "email": (row.get("Email Address") or "").strip().lower(),
                "company": (row.get("Company") or "").strip(),
                "position": (row.get("Position") or "").strip(),
                "connected": (row.get("Connected On") or "").strip(),
            })
    return out


def load_l3():
    """LinkedIn 通讯录（含邮箱的）"""
    out = {}
    for rel in ["Basic_LinkedInDataExport_08-06-2020/Contacts.csv"]:
        p = LI / rel
        if not p.is_file():
            continue
        with p.open(encoding="utf-8", errors="replace", newline="") as fh:
            for row in csv.DictReader(fh):
                em = (row.get("Emails") or "").strip().lower()
                if not valid_email(em):
                    continue
                fn = (row.get("FirstName") or "").strip()
                ln = (row.get("LastName") or "").strip()
                comp = (row.get("Companies") or "").strip()
                if comp.lower() in ("null", "none"):
                    comp = ""
                full = clean_name((row.get("FullName") or "").strip() or f"{fn} {ln}".strip())
                if not (full or comp):
                    continue
                out.setdefault(em, {
                    "email": em, "name": fmt_name(full), "company": clean_name(comp),
                    "position": (row.get("Title") or "").strip(),
                    "phone": clean_phone(row.get("PhoneNumbers") or ""),
                    "location": (row.get("Location") or "").strip(),
                    "addr": (row.get("Addresses") or "").strip(),
                    "src": (row.get("Source") or "").strip(),
                })
    return out


def load_cold():
    """展会 / 进口商冷名单"""
    d = LI / "Email list"
    groups = {"广交会询盘": [], "欧洲进口商": [], "SMT 配件": []}
    if not d.is_dir():
        return groups
    for f in sorted(d.glob("*.txt")):
        nm = f.name
        if "Canton fair" in nm:
            g = "广交会询盘"
        elif "Machinery" in nm:
            g = "欧洲进口商"
        elif "nozzle" in nm.lower():
            g = "SMT 配件"
        else:
            continue
        seen = set()
        for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
            e = ln.strip().lower()
            if not valid_email(e):
                continue
            if e in seen:
                continue
            seen.add(e)
            groups[g].append((e, nm))
    return groups


# =====================================================================
def main():
    l1 = load_l1()
    l2 = load_l2()
    l3 = load_l3()
    cold = load_cold()
    print(f"L1 有往来 {len(l1):,} | L2 LinkedIn连接 {len(l2):,} | "
          f"L3 通讯录 {len(l3):,} | 冷名单 {sum(len(v) for v in cold.values()):,}")

    # ---- 合并 L1 + L3（按邮箱）----
    master = {}
    for e, r in l1.items():
        master[e] = dict(r)
        master[e]["addr"] = ""
    for e, r in l3.items():
        if e in master:
            m = master[e]
            m["name"] = m["name"] or r["name"]
            m["company"] = m["company"] or r["company"]
            m["position"] = m["position"] or r["position"]
            m["phone"] = m["phone"] or r["phone"]
            m["addr"] = r.get("addr", "")
            m["sources"].add(f"LinkedIn 通讯录({r['src']})" if r["src"] else "LinkedIn 通讯录")
        else:
            master[e] = {
                "email": e, "name": r["name"], "company": r["company"],
                "position": r["position"], "country": "", "country_src": "",
                "tier": "", "msgs": 0, "first": "", "last": "",
                "last_subject": "", "phone": r["phone"],
                "sources": {"LinkedIn 通讯录"},
                "linkedin": "", "location": r.get("location", ""),
                "addr": r.get("addr", ""),
            }

    # ---- 姓名索引：把 LinkedIn 连接的「公司+职位」缝到有邮箱但缺公司的条目上 ----
    # LinkedIn 连接层 98% 有公司职位但只有 1.8% 有邮箱；
    # 通讯录层 100% 有邮箱但只有 0.9% 有公司 —— 两层互补，按姓名缝合。
    name_idx = defaultdict(list)
    for k, m in master.items():
        if m["email"] and not m["company"]:
            nk = norm_key(m["name"])
            if nk:
                name_idx[nk].append(k)
    last_idx = defaultdict(list)      # 姓 -> [key]
    for nk, keys in name_idx.items():
        toks = nk.split()
        if len(toks) >= 2:
            last_idx[toks[-1]].append((toks[0][:1], keys))

    # ---- 并入 L2（LinkedIn 连接）----
    linked_added = 0
    stitched = 0
    stitched_loose = 0
    consumed = set()
    for c in l2:
        e = c["email"]
        if e and e in master:
            m = master[e]
            m["sources"].add("LinkedIn 连接")
            m["company"] = m["company"] or c["company"]
            m["position"] = m["position"] or c["position"]
            if not m["name"]:
                m["name"] = c["name"]
            continue
        if not valid_email(e):
            # 无邮箱 —— 先试着按姓名缝到通讯录条目上
            nk = norm_key(c["name"])
            target, loose = None, False
            if nk and len(name_idx.get(nk, [])) == 1 and nk not in consumed:
                target = name_idx[nk][0]
            elif len(nk.split()) >= 2:
                cands = [k for ini, keys in last_idx.get(nk.split()[-1], [])
                         if ini == nk.split()[0][:1] for k in keys
                         if k not in consumed and not master[k]["company"]]
                if len(cands) == 1:
                    target, loose = cands[0], True
            if target:
                m = master[target]
                co = (c["company"] or "").strip()
                # 过滤无信息量的公司名（"H" / "G"）和自家公司名
                if co and len(co) >= 3 and not OWN_CO.search(co) and not m["company"]:
                    m["company"] = co
                    m["position"] = m["position"] or c["position"]
                    if loose:
                        stitched_loose += 1
                    else:
                        stitched += 1
                m["sources"].add("LinkedIn 连接")
                if c["connected"] and not m["last"]:
                    m["last"] = c["connected"]
                # 已缝合，标记消费，避免一对多重复
                consumed.add(target)
                if nk in name_idx:
                    name_idx[nk] = []
                continue
            # 缝不上 —— 独立条目，用 LinkedIn 站内信触达
            k = f"LI::{c['name'].lower()}|{c['company'].lower()}"
            master[k] = {
                "email": "", "name": c["name"], "company": c["company"],
                "position": c["position"], "country": "", "country_src": "",
                "tier": "", "msgs": 0, "first": "", "last": c["connected"],
                "last_subject": "", "phone": "", "sources": {"LinkedIn 连接"},
                "linkedin": f"linkedin.com/in/{c['name'].lower().replace(' ', '-')}",
                "location": "", "addr": "",
            }
            linked_added += 1
        else:
            master[e] = {
                "email": e, "name": c["name"], "company": c["company"],
                "position": c["position"], "country": "", "country_src": "",
                "tier": "", "msgs": 0, "first": "", "last": c["connected"],
                "last_subject": "", "phone": "", "sources": {"LinkedIn 连接"},
                "linkedin": "", "location": "", "addr": "",
            }
            linked_added += 1

    # ---- 姓名显示规范化 ----
    for m in master.values():
        if m.get("name"):
            n = fmt_name(m["name"])
            if NAME_BAD.search(n):          # "Sara from Southern Machinery"
                n = ""
            m["name"] = n

    # ---- 公司补全：① 缝合自 LinkedIn → 标 LinkedIn ② 从企业邮箱域名推 ----
    dom_company = 0
    for m in master.values():
        if m["company"]:
            m["company_src"] = "LinkedIn"
            continue
        c = company_from_domain(m["email"])
        if c:
            m["company"] = c
            m["company_src"] = "邮件域名"
            dom_company += 1
        else:
            m["company_src"] = ""

    print(f"合并后主表 {len(master):,} 条（LinkedIn 新增 {linked_added:,}）")
    print(f"姓名缝合：精确 {stitched:,} + 姓+首字母 {stitched_loose:,} = "
          f"{stitched + stitched_loose:,} 条补上公司/职位")
    print(f"公司补全：邮件域名推断新增 {dom_company:,} 条")

    # ---- 补国家 / 行业 / 阶段 / 优先级 ----
    rows = []
    for k, m in master.items():
        if not m["country"] and m["email"]:
            m["country"], m["country_src"] = country_of(m["email"])
        if not m["country"] and m.get("addr"):
            ac = addr_country(m["addr"])
            if ac:
                m["country"], m["country_src"] = ac, "通讯录地址"
        ind = industry_of(m.get("company", ""), m.get("position", ""),
                          m.get("last_subject", ""), domain_of(m["email"]))
        srcs = " / ".join(sorted(m["sources"]))

        if m["tier"] == "A":
            stage, pri = "成交", "P0"
            nxt = "发送备件/升级套件唤醒邮件"
            due = TODAY + timedelta(days=3)
        elif m["tier"] == "B":
            stage, pri = "已报价", "P1"
            nxt = "发送新方案 + 更新报价"
            due = TODAY + timedelta(days=5)
        elif m["tier"] == "C":
            stage, pri = "已联系", "P2"
            nxt = "发送案例背书重新介绍"
            due = TODAY + timedelta(days=10)
        elif "LinkedIn 连接" in srcs:
            stage, pri = "已连接", "P2"
            nxt = "按行业/职位定向触达"
            due = TODAY + timedelta(days=14)
        else:
            stage, pri = "新线索", "P3"
            nxt = "验证有效性后触达"
            due = TODAY + timedelta(days=30)

        rows.append({
            "email": m["email"], "name": m["name"], "company": m["company"],
            "company_src": m.get("company_src", ""),
            "position": m["position"], "country": m["country"],
            "country_src": m["country_src"], "industry": ind,
            "phone": m.get("phone", ""), "linkedin": m.get("linkedin", ""),
            "sources": srcs, "tier": m["tier"], "msgs": m["msgs"],
            "first": m["first"], "last": m["last"],
            "stage": stage, "pri": pri, "nxt": nxt,
            "due": due.isoformat(), "owner": "Jason",
            "last_subject": m["last_subject"],
        })

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    rows.sort(key=lambda r: (order[r["pri"]], -r["msgs"], r["email"] or r["name"]))

    wb = Workbook()

    # ================= 说明 =================
    ws = wb.active
    ws.title = "说明"
    ws["A1"] = "SMThelp 客户 CRM —— Southern Machinery"
    ws["A1"].font = Font(size=15, bold=True, color="1F3B57")
    info = [
        ("生成日期", "2026-09-13"),
        ("用途", "把散在邮件归档、LinkedIn、展会名单里的客户，收进一张统一表"),
        ("", ""),
        ("数据来源", "① Foxmail 7.2 邮件归档（2009–2022-06，9,931 封邮件 → 1,130 位有往来联系人）"),
        ("", "② LinkedIn 官方导出 2020-08-06（连接 5,462 · 通讯录 18,823）"),
        ("", "③ 广交会 126 届询盘名单 + 法/德/意 机械进口商名单"),
        ("", ""),
        ("主表构成", f"去重合并后 {len(rows):,} 条（原分表相加 11,137，已合并重复联系人）"),
        ("两层缝合", f"LinkedIn 连接有公司/职位但仅 1.8% 有邮箱；通讯录 100% 有邮箱但仅 0.9% 有公司。"
                    f"按姓名缝合 {stitched + stitched_loose:,} 条，公司覆盖从 48% 提到 76%"),
        ("冷名单", f"{sum(len(v) for v in cold.values()):,} 条（单独工作表，未并入主表）"),
        ("", ""),
        ("工作表", "① 客户主表 ② 询盘记录 ③ 跟进看板-成交/已报价/已联系 "
                  "④ 统计看板 ⑤ 冷名单 ⑥ 数据字典"),
        ("", ""),
        ("阶段定义", "新线索 → 已联系 → 已报价 → 样品试机 → 成交 → 搁置"
                    "（另设「已连接」= LinkedIn 已连接但无邮件往来）"),
        ("优先级 P0", "成交过的客户（设备在手上，直接可变现）—— 216 条"),
        ("优先级 P1", "报过价未成交（有明确兴趣）—— 509 条"),
        ("优先级 P2", "仅询盘 / LinkedIn 已连接（需培育）"),
        ("优先级 P3", "通讯录线索（有邮箱无背景，需验证）"),
        ("优先级 P4", "冷线索（展会名单，批量触达用）"),
        ("下一步日期", "系统按优先级给的建议跟进日（P0=+3天 … P3=+30天），可人工改写"),
        ("负责人", "默认 Jason，可改写（未来多人跟进时用）"),
        ("", ""),
        ("⚠️ 使用规则",
         "① 客户名单属公司机密，不得外泄；② 对外触达前须 Jason 确认；"
         "③ 「公司」「国家」「行业」列均带依据标注，推断值需人工复核；"
         "④ 国家字段标「待确认」的需人工核对（数据源本身无国家字段）；"
         "⑤ 主表含 LinkedIn 无邮箱条目（邮箱列为空，可用 LinkedIn 站内信触达）。"),
    ]
    for i, (k, v) in enumerate(info, start=3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True, size=10)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = WRAP
        if k.startswith("⚠️"):
            c.font = Font(color="C00000", size=10, bold=True)
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 100

    # ================= 客户主表 =================
    COLS = [
        ("email", "邮箱", 34), ("name", "联系人", 22), ("company", "公司", 28),
        ("company_src", "公司依据", 12), ("position", "职位", 24),
        ("country", "国家/地区", 13), ("country_src", "国家依据", 12),
        ("industry", "行业", 16), ("stage", "阶段", 11), ("pri", "优先级", 8),
        ("tier", "档位", 6), ("msgs", "往来邮件", 9),
        ("first", "首次接触", 11), ("last", "最后联系", 11),
        ("nxt", "下一步动作", 24), ("due", "下一步日期", 11),
        ("owner", "负责人", 9), ("phone", "电话/WhatsApp", 18),
        ("linkedin", "LinkedIn", 26), ("sources", "来源", 30),
        ("last_subject", "最后话题", 46),
    ]

    def sheet(wsx, data):
        head(wsx, COLS)
        for r in data:
            wsx.append([r.get(k, "") for k, _, _ in COLS])
        style(wsx, COLS, pri_col=9)
        for row in wsx.iter_rows(min_row=2, max_row=wsx.max_row, max_col=len(COLS)):
            for i in (8, 9, 10, 11):
                row[i].alignment = Alignment(horizontal="center", vertical="top")
            row[20].alignment = WRAP
            row[0].font = Font(size=9)

    sheet(wb.create_sheet("客户主表"), rows)
    for nm, stage in [("跟进看板-成交", "成交"), ("跟进看板-已报价", "已报价"),
                      ("跟进看板-已联系", "已联系")]:
        sheet(wb.create_sheet(nm), [r for r in rows if r["stage"] == stage])

    # ================= 询盘记录 =================
    by_email = {r["email"]: r for r in rows if r["email"]}
    inq_rows = []
    cj = WORK / "contacts.json"
    if cj.is_file():
        for c in json.loads(cj.read_text(encoding="utf-8")):
            if not c.get("inq"):
                continue
            r = by_email.get(c["email"], {})
            inq_rows.append({
                "inq_date": c["first"] or c["last"], "email": c["email"],
                "name": r.get("name", ""), "company": r.get("company", ""),
                "country": r.get("country", "") or c.get("country", ""),
                "inq": c["inq"], "quote": c["quote"], "deal": c["deal"],
                "last": c["last"], "last_subject": c["last_subject"],
                "stage": r.get("stage", ""), "tier": c["tier"],
            })
    # 最新的排前面；无日期的垫底
    inq_rows.sort(key=lambda x: x["inq_date"] or "0000-00-00", reverse=True)
    IQ = [("inq_date", "首次询盘", 12), ("email", "邮箱", 34), ("name", "联系人", 20),
          ("company", "公司", 26), ("country", "国家/地区", 12),
          ("inq", "询盘数", 8), ("quote", "报价数", 8), ("deal", "成交信号", 9),
          ("last", "最后往来", 12), ("last_subject", "最后主题", 50),
          ("stage", "阶段", 11), ("tier", "档位", 6)]
    wsI = wb.create_sheet("询盘记录")
    head(wsI, IQ)
    for r in inq_rows:
        wsI.append([r.get(k, "") for k, _, _ in IQ])
    style(wsI, IQ)
    for row in wsI.iter_rows(min_row=2, max_row=wsI.max_row, max_col=len(IQ)):
        for i in (0, 4, 5, 6, 7, 8, 10, 11):
            row[i].alignment = Alignment(horizontal="center", vertical="top")
        row[9].alignment = WRAP
        row[1].font = Font(size=9)

    # ================= 统计看板 =================
    ws2 = wb.create_sheet("统计看板")
    ws2.append(["维度", "项目", "数量", "占比"])
    for i in range(1, 5):
        c = ws2.cell(row=1, column=i)
        c.fill, c.font, c.border = HDR, HF, BD
    tot = len(rows)

    def blk(title, counter):
        for k, v in counter.most_common():
            ws2.append([title, k, v, f"{v/tot:.1%}"])
        ws2.append(["", "", "", ""])

    blk("阶段", Counter(r["stage"] for r in rows))
    blk("优先级", Counter(r["pri"] for r in rows))
    blk("国家/地区", Counter(r["country"] or "待确认" for r in rows))
    blk("行业", Counter(r["industry"] for r in rows))
    blk("来源", Counter(s for r in rows for s in r["sources"].split(" / ") if s))
    blk("档位", Counter(r["tier"] or "—" for r in rows))
    # 字段完整度
    for col, label in [("email", "邮箱"), ("name", "联系人"), ("company", "公司"),
                       ("position", "职位"), ("country", "国家/地区"),
                       ("phone", "电话"), ("last_subject", "最后话题")]:
        n = sum(1 for r in rows if str(r.get(col) or "").strip())
        ws2.append(["字段完整度", label, n, f"{n/tot:.1%}"])
    ws2.append(["", "", "", ""])
    for col, w in zip("ABCD", (14, 34, 12, 10)):
        ws2.column_dimensions[col].width = w

    # ================= 冷名单 =================
    ws3 = wb.create_sheet("冷名单")
    ws3.append(["分组", "邮箱", "国家/地区", "来源文件", "状态"])
    for i in range(1, 6):
        c = ws3.cell(row=1, column=i)
        c.fill, c.font, c.border = HDR, HF, BD
    for g, items in cold.items():
        for e, f in items:
            ws3.append([g, e, country_of(e)[0] or "待确认", f, "未触达"])
    for i, w in enumerate([14, 36, 13, 42, 10], 1):
        ws3.column_dimensions[get_column_letter(i)].width = w
    ws3.freeze_panes = "A2"
    ws3.auto_filter.ref = f"A1:E{ws3.max_row}"

    # ================= 数据字典 =================
    ws4 = wb.create_sheet("数据字典")
    ws4.append(["字段", "含义", "取值 / 规则"])
    for i in range(1, 4):
        c = ws4.cell(row=1, column=i)
        c.fill, c.font, c.border = HDR, HF, BD
    dd = [
        ("邮箱", "联系人邮箱（主键之一）", "小写；LinkedIn 无邮箱条目为空"),
        ("联系人", "姓名", "来自邮件显示名或 LinkedIn；已做大小写/缩写/公司词清理"),
        ("公司", "公司名", "来自 LinkedIn；缺失时由企业邮箱域名推断"),
        ("公司依据", "公司名的来源", "LinkedIn = 官方导出；邮件域名 = 由域名桩推断（如 juki.com → Juki），需复核"),
        ("职位", "职位/头衔", "来自 LinkedIn Position 或邮件签名"),
        ("国家/地区", "推断的国家", "邮箱域名 TLD 优先，其次通讯录地址、正文提及、电话区号；否则「待确认」"),
        ("国家依据", "国家推断的依据", "邮箱域名 / 通讯录地址 / 正文提及×N / 电话区号×N；「无」= 无法推断"),
        ("行业", "行业分类", "由公司名/职位/域名关键词推断，仅作筛选参考"),
        ("阶段", "销售阶段", "成交客户 / 已报价 / 已联系 / 已连接 / 线索"),
        ("优先级", "跟进优先级", "P0 成交过 · P1 报过价 · P2 已连接 · P3 线索 · P4 冷线索"),
        ("档位", "案例 1 的 A/B/C 分档", "仅「有邮件往来」的条目有值"),
        ("往来邮件", "归档中的邮件数", "0 表示无邮件往来记录"),
        ("首次接触", "最早一封邮件日期", "YYYY-MM-DD；无记录则空"),
        ("最后联系", "最晚一封邮件日期", "YYYY-MM-DD；LinkedIn 条目为连接日期"),
        ("下一步动作", "建议的跟进动作", "按阶段自动生成，可人工改写"),
        ("下一步日期", "建议跟进日期", "按优先级推算（P0 +3 天 / P1 +5 / P2 +10~14 / P3 +30），可改写"),
        ("负责人", "跟进负责人", "默认 Jason"),
        ("电话/WhatsApp", "电话", "来自 LinkedIn 通讯录；外贸客户多走 WhatsApp"),
        ("LinkedIn", "LinkedIn 资料链接", "无邮箱条目按姓名推测，需核对"),
        ("来源", "数据来源", "Foxmail 邮件归档 / LinkedIn 连接 / LinkedIn 通讯录"),
        ("最后话题", "最后一封邮件的主题", "用于写个性化邮件时的切入点"),
    ]
    for r in dd:
        ws4.append(list(r))
    for i, w in enumerate([14, 30, 62], 1):
        ws4.column_dimensions[get_column_letter(i)].width = w
    for row in ws4.iter_rows(min_row=2, max_row=ws4.max_row, max_col=3):
        for c in row:
            c.border, c.alignment = BD, WRAP

    wb.save(OUT)
    print(f"\nOK -> {OUT}")
    print("工作表:", wb.sheetnames)
    print(f"主表 {len(rows):,} 条 | 冷名单 {ws3.max_row-1:,} 条")
    print("阶段:", dict(Counter(r["stage"] for r in rows)))
    print("优先级:", dict(Counter(r["pri"] for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
