#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例 1 v2：更干净的分档 + 从正文电话区号/国家名推断国家。
"""
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

if len(sys.argv) < 3:
    sys.exit("用法: consolidate_contacts.py <Foxmail数据目录> <输出目录>")
BASE = Path(sys.argv[1]).expanduser().resolve()
WORK = Path(sys.argv[2]).expanduser().resolve()
CUTOFF = date(2026, 9, 13)
STALE_DAYS = 365

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

# ---------- 电话区号 -> 国家（长的优先匹配）----------
DIAL = sorted([
    ("+880", "孟加拉"), ("+998", "乌兹别克斯坦"), ("+995", "格鲁吉亚"),
    ("+994", "阿塞拜疆"), ("+976", "蒙古"), ("+972", "以色列"),
    ("+971", "阿联酋"), ("+966", "沙特阿拉伯"), ("+968", "阿曼"),
    ("+965", "科威特"), ("+974", "卡塔尔"), ("+973", "巴林"),
    ("+962", "约旦"), ("+961", "黎巴嫩"), ("+963", "叙利亚"),
    ("+964", "伊拉克"), ("+98", "伊朗"), ("+92", "巴基斯坦"),
    ("+94", "斯里兰卡"), ("+977", "尼泊尔"), ("+95", "缅甸"),
    ("+855", "柬埔寨"), ("+856", "老挝"), ("+91", "印度"),
    ("+90", "土耳其"), ("+84", "越南"), ("+82", "韩国"),
    ("+81", "日本"), ("+886", "中国台湾"), ("+852", "中国香港"),
    ("+853", "中国澳门"), ("+86", "中国"), ("+65", "新加坡"),
    ("+66", "泰国"), ("+60", "马来西亚"), ("+63", "菲律宾"),
    ("+62", "印尼"), ("+61", "澳大利亚"), ("+64", "新西兰"),
    ("+55", "巴西"), ("+54", "阿根廷"), ("+56", "智利"),
    ("+57", "哥伦比亚"), ("+58", "委内瑞拉"), ("+51", "秘鲁"),
    ("+593", "厄瓜多尔"), ("+595", "巴拉圭"), ("+598", "乌拉圭"),
    ("+591", "玻利维亚"), ("+52", "墨西哥"), ("+506", "哥斯达黎加"),
    ("+507", "巴拿马"), ("+502", "危地马拉"), ("+503", "萨尔瓦多"),
    ("+504", "洪都拉斯"), ("+505", "尼加拉瓜"), ("+1809", "多米尼加"),
    ("+49", "德国"), ("+33", "法国"), ("+39", "意大利"),
    ("+34", "西班牙"), ("+351", "葡萄牙"), ("+30", "希腊"),
    ("+31", "荷兰"), ("+32", "比利时"), ("+41", "瑞士"),
    ("+43", "奥地利"), ("+48", "波兰"), ("+420", "捷克"),
    ("+421", "斯洛伐克"), ("+36", "匈牙利"), ("+40", "罗马尼亚"),
    ("+359", "保加利亚"), ("+381", "塞尔维亚"), ("+385", "克罗地亚"),
    ("+386", "斯洛文尼亚"), ("+370", "立陶宛"), ("+371", "拉脱维亚"),
    ("+372", "爱沙尼亚"), ("+380", "乌克兰"), ("+375", "白俄罗斯"),
    ("+7", "俄罗斯"), ("+44", "英国"), ("+353", "爱尔兰"),
    ("+46", "瑞典"), ("+47", "挪威"), ("+45", "丹麦"),
    ("+358", "芬兰"), ("+354", "冰岛"), ("+20", "埃及"),
    ("+212", "摩洛哥"), ("+216", "突尼斯"), ("+213", "阿尔及利亚"),
    ("+218", "利比亚"), ("+27", "南非"), ("+234", "尼日利亚"),
    ("+254", "肯尼亚"), ("+233", "加纳"), ("+255", "坦桑尼亚"),
    ("+256", "乌干达"), ("+263", "津巴布韦"), ("+260", "赞比亚"),
], key=lambda x: -len(x[0]))

COUNTRY_WORDS = {
    "巴西": ["brazil", "brasil", "são paulo", "sao paulo", "curitiba", "manaus"],
    "印度": ["india", "mumbai", "bangalore", "bengaluru", "pune", "chennai",
           "new delhi", "noida", "gurgaon"],
    "墨西哥": ["mexico", "méxico", "monterrey", "guadalajara", "tijuana", "juarez"],
    "菲律宾": ["philippines", "manila", "cebu", "laguna", "cavite"],
    "土耳其": ["turkey", "türkiye", "istanbul", "ankara", "izmir", "bursa"],
    "沙特阿拉伯": ["saudi", "riyadh", "jeddah", "dammam"],
    "波兰": ["poland", "warsaw", "wroclaw", "krakow", "poznań"],
    "美国": ["usa", "united states", "california", "texas", "florida",
           "new york", "illinois", "ohio", "michigan"],
    "德国": ["germany", "deutschland", "munich", "münchen", "stuttgart", "berlin"],
    "意大利": ["italy", "italia", "milan", "milano", "turin", "torino"],
    "法国": ["france", "paris", "lyon", "toulouse"],
    "英国": ["united kingdom", "england", "london", "manchester"],
    "马来西亚": ["malaysia", "penang", "kuala lumpur", "johor", "selangor"],
    "印尼": ["indonesia", "jakarta", "batam", "surabaya", "bandung"],
    "泰国": ["thailand", "bangkok", "chiang mai", "rayong"],
    "越南": ["vietnam", "hanoi", "ho chi minh", "saigon", "bac ninh"],
    "韩国": ["korea", "seoul", "incheon", "busan"],
    "日本": ["japan", "tokyo", "osaka", "nagoya"],
    "哥伦比亚": ["colombia", "bogota", "bogotá", "medellin", "cali"],
    "阿根廷": ["argentina", "buenos aires", "cordoba"],
    "智利": ["chile", "santiago", "valparaiso"],
    "秘鲁": ["peru", "lima"],
    "厄瓜多尔": ["ecuador", "quito", "guayaquil"],
    "西班牙": ["spain", "españa", "madrid", "barcelona", "valencia"],
    "荷兰": ["netherlands", "holland", "amsterdam", "eindhoven"],
    "俄罗斯": ["russia", "moscow", "saint petersburg"],
    "埃及": ["egypt", "cairo", "alexandria"],
    "南非": ["south africa", "johannesburg", "cape town", "durban"],
    "阿联酋": ["dubai", "abu dhabi", "uae", "emirates"],
    "加拿大": ["canada", "toronto", "vancouver", "montreal", "ontario"],
    "澳大利亚": ["australia", "sydney", "melbourne", "brisbane"],
    "新加坡": ["singapore"],
    "以色列": ["israel", "tel aviv", "haifa"],
    "巴基斯坦": ["pakistan", "karachi", "lahore", "islamabad"],
    "孟加拉": ["bangladesh", "dhaka", "chittagong"],
    "中国台湾": ["taiwan", "taipei", "kaohsiung", "hsinchu"],
    "中国香港": ["hong kong"],
}

OWN_DOMAINS = {"smthelp.com", "southcleaner.com", "southcnc.com", "southfai.com",
               "autoinsertion.com", "smthelp.eu"}
NOREPLY = re.compile(
    r"(no[-_.]?reply|do[-_.]?not[-_.]?reply|mailer[-_.]?daemon|postmaster|bounce|"
    r"notification|newsletter|automated|system@|admin@|coupahost|"
    r"alibaba|aliexpress|made-in-china|globalsources|tradekey|linkedin\.com|"
    r"facebook|paypal|dhl\.|fedex|ups\.com|tnt\.com|"
    r"@(?:\w+\.)?(?:qq|163|126)\.com$)", re.I)
EMAIL_RE = re.compile(r"[\w.\-+]+@[\w\-]+(?:\.[\w\-]+)+")
DIAL_RE = re.compile(r"(?<![\d])\+(\d{1,4})[\s\-.()]?\d")

# 自有签名里的中国手机号 / 公司标识，必须在投票前剥掉
OWN_SIG_RE = re.compile(
    r"(smthelp|southern machinery|southcleaner|southcnc|southfai|"
    r"autoinsertion|\+?86[\s\-.]?1[3-9]\d[\s\-.]?\d{4}[\s\-.]?\d{4}|"
    r"136[\s\-.]?0256[\s\-.]?2576)", re.I)


def strip_own_sig(text: str) -> str:
    """逐行删除含自有签名的行。"""
    keep = []
    for ln in text.splitlines():
        if OWN_SIG_RE.search(ln):
            continue
        keep.append(ln)
    return "\n".join(keep)

DEAL_KW = re.compile(
    r"\b(proforma invoice|invoice no|deposit|payment received|payment term|"
    r"remittance|telegraphic transfer|t/?t copy|swift copy|bank slip|"
    r"packing list|bill of lading|shipment advice|shipped|delivery note|"
    r"order confirmed|purchase order|po no|p/?o #|contract signed|"
    r"installation|commissioning|warranty period|after[- ]sales|"
    r"spare part|down ?payment|balance payment|receipt)\b", re.I)
QUOTE_KW = re.compile(
    r"\b(quotation|quotation sheet|quote|quoted|price list|price|pricing|"
    r"offer|proposal|fob|cif|exw|ddp|moq|lead time|discount|"
    r"best price|target price|cost)\b", re.I)
INQUIRY_KW = re.compile(
    r"\b(inquiry|enquiry|inquire|interested|requirement|require|"
    r"catalog|catalogue|specification|datasheet|rfq|"
    r"looking for|please send|need a|want to buy)\b", re.I)

TLD_COUNTRY = {
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
    "sk": "斯洛伐克", "si": "斯洛文尼亚", "hr": "克罗地亚", "rs": "塞尔维亚",
    "lt": "立陶宛", "lv": "拉脱维亚", "ee": "爱沙尼亚", "by": "白俄罗斯",
    "md": "摩尔多瓦", "al": "阿尔巴尼亚", "mk": "北马其顿", "ba": "波黑",
    "mt": "马耳他", "cy": "塞浦路斯", "lu": "卢森堡", "ie": "爱尔兰",
    "is": "冰岛", "az": "阿塞拜疆", "ge": "格鲁吉亚", "am": "亚美尼亚",
    "mn": "蒙古", "uz": "乌兹别克斯坦", "kz": "哈萨克斯坦", "mm": "缅甸",
    "kw": "科威特", "om": "阿曼", "qa": "卡塔尔", "bh": "巴林", "lb": "黎巴嫩",
}


def parse_date(s):
    if not s:
        return ""
    s = s.strip()

    def ok(y, mo, d):
        return f"{y:04d}-{mo:02d}-{d:02d}" if (1990 <= y <= 2030 and 1 <= mo <= 12 and 1 <= d <= 31) else ""

    m = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        r = ok(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if r:
            return r
    m = re.search(r"([A-Za-z]{3})[a-z]*\.?,?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        r = ok(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
        if r:
            return r
    m = re.search(r"(\d{1,2})[- ]([A-Za-z]{3})[a-z]*[- ,]+(\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        r = ok(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
        if r:
            return r
    m = re.search(r"(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})", s)
    if m:
        mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000 if y < 70 else 1900
        return ok(y, mo, d)
    return ""


def domain_of(a):
    return a.rsplit("@", 1)[-1].lower().strip(">.,;") if "@" in a else ""


def is_own(a):
    return domain_of(a) in OWN_DOMAINS


def extract_addrs(f):
    out = []
    for m in EMAIL_RE.finditer(f):
        a = m.group().lower().strip(".")
        if "@" not in a or len(a) >= 70:
            continue
        if NOREPLY.search(a):
            continue
        local = a.split("@")[0]
        if re.fullmatch(r"\d{5,}", local):          # 纯数字 = QQ 号之类
            continue
        if re.fullmatch(r"[0-9a-f]{16,}", local):   # 哈希
            continue
        out.append(a)
    return out


def guess_country(tld_country, bodies):
    """TLD 优先；否则用电话区号 + 国家名投票。"""
    if tld_country:
        return tld_country, "邮箱域名"
    dial_votes = Counter()
    word_votes = Counter()
    for b in bodies:
        b = strip_own_sig(b)
        for m in DIAL_RE.finditer(b):
            code = "+" + m.group(1)
            for d, c in DIAL:
                if d == code:
                    dial_votes[c] += 1
                    break
        low = b.lower()
        for c, kws in COUNTRY_WORDS.items():
            for kw in kws:
                if kw in low:
                    word_votes[c] += 1
    # 正文国家名证据 >=2 票时优先于电话区号
    if word_votes:
        c, n = word_votes.most_common(1)[0]
        if n >= 2:
            return c, f"正文提及×{n}"
    if dial_votes:
        c, n = dial_votes.most_common(1)[0]
        # +86 必然是 Jason 自己签名泄漏，永远不作数
        if c != "中国":
            return c, f"电话区号×{n}"
    if word_votes:
        c, n = word_votes.most_common(1)[0]
        return c, f"正文提及×{n}"
    return "", ""


def main():
    mf = WORK / "messages.jsonl"
    C = defaultdict(lambda: {
        "emails": set(), "bodies": [], "subjects": [], "dates": [],
        "deal": 0, "quote": 0, "inq": 0, "msgs": 0, "sources": set(),
        "last_subj": "", "parties": set(),
    })

    with mf.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except Exception:
                continue
            frm, to = r.get("frm", ""), r.get("to", "")
            subj, body = r.get("subj", ""), r.get("body", "")
            iso = parse_date(r.get("date", ""))

            fa, ta = extract_addrs(frm), extract_addrs(to)
            if any(is_own(a) for a in fa) or not fa:
                others = [a for a in ta if not is_own(a)]
            else:
                others = [a for a in fa if not is_own(a)]
            if not others:
                others = [a for a in (fa + ta) if not is_own(a)]
            if not others:
                continue

            head = f"{subj}\n{body[:600]}"          # 只看正文新内容，避开引用历史
            deal = bool(DEAL_KW.search(head))
            quote = bool(QUOTE_KW.search(head))
            inq = bool(INQUIRY_KW.search(head)) or not (deal or quote)

            for a in set(others):
                c = C[a]
                c["msgs"] += 1
                c["sources"].add("Foxmail邮件归档")
                c["bodies"].append(body[:800])
                if subj:
                    c["subjects"].append(subj)
                if iso:
                    c["dates"].append(iso)
                c["deal"] += deal
                c["quote"] += quote
                c["inq"] += inq

    rows = []
    for a, c in C.items():
        dates = sorted(d for d in c["dates"] if d)
        last = dates[-1] if dates else ""
        ld = None
        if last:
            y, m, d = (int(x) for x in last.split("-"))
            ld = date(y, m, d)
        days = (CUTOFF - ld).days if ld else None

        if c["deal"] >= 1 and c["deal"] >= c["msgs"] * 0.08:
            tier = "A"
        elif c["deal"] >= 1:
            tier = "A-弱"
        elif c["quote"] >= 1:
            tier = "B"
        else:
            tier = "C"

        last_subj = ""
        for s in reversed(c["subjects"]):
            if s:
                last_subj = s
                break

        tld = TLD_COUNTRY.get(domain_of(a).split(".")[-1], "")
        country, how = guess_country(tld, c["bodies"][:12])

        rows.append({
            "email": a, "domain": domain_of(a), "country": country,
            "country_src": how, "tier": tier,
            "deal": c["deal"], "quote": c["quote"], "inq": c["inq"],
            "msgs": c["msgs"],
            "first": dates[0] if dates else "", "last": last,
            "days_since": days if days is not None else "",
            "last_subject": last_subj[:150],
            "sources": " / ".join(sorted(c["sources"])),
        })

    rows.sort(key=lambda r: ({"A": 0, "A-弱": 1, "B": 2, "C": 3}[r["tier"]],
                             -r["msgs"], r["email"]))
    (WORK / "contacts.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"有往来记录的联系人：{len(rows):,}")
    print("档位:", dict(Counter(r["tier"] for r in rows)))
    print("有日期:", sum(1 for r in rows if r["last"]))
    print("有国家:", sum(1 for r in rows if r["country"]))
    print("\n国家分布 Top15:", dict(Counter(
        r["country"] for r in rows if r["country"]).most_common(15)))
    print("\n=== A 档 Top 20 ===")
    for r in [x for x in rows if x["tier"] == "A"][:20]:
        print(f"  {r['msgs']:4d}封 {r['email'][:40]:42s} {r['country'] or '?':10s} "
              f"{r['last']:10s} {r['last_subject'][:44]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
