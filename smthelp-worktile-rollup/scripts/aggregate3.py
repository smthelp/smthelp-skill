#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Customer aggregation v3: verb-based who/product split, safe suffix strip,
canonical aliases, container-title filter, short-title fallback."""
import json, os, re, sys, collections
# usage: python aggregate3.py <BASE_DIR> <OUT_DIR>
BASE = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, ".workbuddy/tmp")
recs = json.load(open(os.path.join(OUT, "dataset.json"), encoding="utf-8"))

byproj = collections.OrderedDict()
for r in recs:
    byproj.setdefault(r["_project"], []).append(r)

TLD = r"(?:com|net|org|info|biz|io|co|de|fr|it|es|nl|be|pl|cz|sk|at|ch|se|no|fi|dk|ru|ua|tr|in|cn|jp|kr|vn|th|my|id|ph|mx|br|ar|cl|uk|eu|ca|au|za|ae|gr|pt|ro|hu|si|hr|rs|lt|lv|ee|by|kz|uz|eg|sa|il|ir|pk|bd|lk|np|tw|hk)"
SUF2 = r"(?:br|mx|ar|tr|in|uk|kr|vn|cn|jp|au|za|pl|ua|de|fr|it|es|nl|be|cz|sk|ru|gr|pt|ro|hu|lt|eg|sa|ae|id|th|my|ph|tw|hk|cl|co|com)"
DOMAIN_RE = re.compile(r"(?<![A-Za-z0-9.\-])((?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+" + TLD + r"(?:\." + SUF2 + r")?)(?![A-Za-z0-9\-])", re.I)
EMAIL_RE = re.compile(r"[\w\.\-\+]+@[\w\.\-]+\.\w+")

COUNTRIES = ["印度尼西亚","乌兹别克斯坦","美国","墨西哥","巴西","印度","俄罗斯","土耳其","英国","德国","法国",
             "西班牙","波兰","捷克","韩国","日本","越南","泰国","马来西亚","菲律宾","印尼","伊朗","埃及",
             "阿联酋","迪拜","阿根廷","加拿大","塞尔维亚","斯洛伐克","斯洛文尼亚","厄瓜多尔","立陶宛",
             "瑞士","罗马尼亚","缅甸","新加坡","荷兰","葡萄牙","比利时","希腊","乌克兰","南非","中国",
             "意大利","奥地利","匈牙利","澳大利亚","哥伦比亚","智利","秘鲁","孟加拉","巴基斯坦"]

NOISE_DOMAINS = set("""crm.xiaoman.cn beta.openai.com my.racknerd.com notebooklm.google.com youtube.com youtu.be
google.com linkedin.com gmail.com outlook.com hotmail.com wps.cn canva.com dify.ai coze.com openai.com
solidworks.com 3dsmt.com smthelp.com smthelp.net smthelp.ru smthelp.eu smthelp.mx xtransfer.cn aliyun.com
bt.3dsmt.com vpsor.cn infinityfree.com x10hosting.com serv00.com atozserver.com cklghost.in beget.com
vultr.com upcloud.com omniedge.io freedidi.com luffycity.com imiker.com mozilla.org doubao.com
lingyingzhuli.com topxieyi.com jina.ai cloudflare.com office.com microsoft.com apple.com github.com
chatgpt.com perplexity.ai claude.ai notion.so mailchimp.com tawk.to xiaoman.cn pve bilibili.com
shop.smthelp.com file.smthelp.com ph.smthelp.com url.autoinsertion.com file.autoinsertion.com
smtmachine.eu.org smtnozzle.org pcbassemblymachine.com huaweicloud.com""".split())

NOISE_KW = re.compile(r"(注册教程|网盘|免费域名|虚拟主机|数据中心|服务器|网站空间|VPS|安装教程|"
                      r"浏览器插件|Chrome插件|wordpress插件|"
                      r"图床|控制面板|宝塔面板|Docker|大模型|文字转语音|去水印|培训课程|分享文档|邮箱登陆|Cpanel|"
                      r"域名|文件同步|数据备份|内网穿透|教程|免费|SEO优化|EDM营销|邮件模版|邮件模板|"
                      r"Email List|Mautic|Mailchimp|群发|"
                      r"公众号|领英|Linkedin|LinkedIn|TikTok|Youtube|YouTube|Canva|Notion|NotebookLM|"
                      r"思维导图|知识库|联系方式|微信|WhatsApp|Facebook|Twitter|海关数据|买单报关|"
                      r"开发信|邮件开场白|主题行|催付款|邮件标题|客户满意度|调查问卷|"
                      r"^如何|^怎样|^怎么|^什么是|^从配件|^从异型飞达|^从ESD|产品资料汇总|产品汇总)")

CONTAINER = re.compile(r"^(新开发客户|客户List|创建邮件模版|统计现有到访客户|整理现有的通话记录|安装手机APP|"
                       r"如何挖掘|如何对客户的询盘|客户订单汇总|百运网发货|我的工作龙虾|运营公司的|产品学习|"
                       r"实现钢网清洗机|背调客户$|客户背调$|每日更新博客|客户信息收集与整理|客户调研|"
                       r"接触计划|进度跟踪|营销内容|内部协同|产品适配|客户跟进策略设计|客户培训计划制定|"
                       r"关于Gpt|关于使用小满|客户成功|重点客户|潜在客户|客户开发|客户背调：|背调客户：)")

VERBS = ["销售", "推销", "采购", "整机销售"]

SUFFIX_RE = re.compile(r"(?:\s*(?:Inc|INC|Inc\.|LLC|Ltd|LTD|Ltd\.|Limited|S\.A\.|S\.L\.U\.|S\.p\.A\.|GmbH|B\.V\.|"
                       r"Co\.|Corp|Corporation|Company|有限公司|股份有限公司|集团公司|公司|集团))\s*$", re.I)

def canon(key):
    k = key.lower().strip()
    for pats, target in ALIASES:
        for p in pats:
            if p in k:
                return target
    return k

ALIASES = [
    (["juki", "juk"], "juki"),
    (["fii-na", "foxconn", "富士康"], "foxconn"),
    (["signify", "philips", "飞利浦", "信达高科"], "signify"),
    (["offshore-electronics", "electronics.co.uk"], "offshore-electronics.co.uk"),
    (["schwabe", "vossloh"], "vossloh-schwabe.com"),
    (["xdry", "celestica"], "celestica.com"),
    (["matko"], "matko.com"), (["smtvys"], "smtvys.com"), (["atacanada"], "atacanada.ca"),
    (["hselectronic", "hselectronic.sk", "hs 斯洛伐克"], "hselectronic.sk"),
    (["tehinmash"], "tehinmash.ru"), (["oramax"], "oramax.cz"), (["vestel"], "vestel.com"),
    (["iskraemeco"], "iskraemeco.si"), (["strip's", "strips"], "strips.si"),
    (["walton", "孟加拉"], "waltonbd.com"), (["mar-girius", "margirius"], "margirius.com.br"),
    (["pentamaster"], "pentamaster.com.my"), (["electrofueguina"], "electrofueguina.com.ar"),
    (["teltonika"], "teltonika.lt"), (["drei"], "drei-k.com.br"),
    (["truth"], "truth-electronic.co.za"), (["microtronix"], "microtronix.co.za"),
    (["apm"], "apm-intergroup.com"), (["intersource"], "intersource.co.th"),
    (["tecone"], "tecone.com.br"), (["multilaser"], "multilaser.com.br"),
    (["visum"], "visum.com.br"), (["vema"], "vema.com.br"), (["cliptech"], "cliptech.com.br"),
    (["compmaq"], "compmaq.com.br"), (["br-global"], "br-global.com.br"),
    (["keele"], "keele-electronics.com"), (["baylan"], "baylan.com.tr"),
    (["ernamas"], "ernamas.com"), (["gpv-group"], "gpv-group.com"), (["levven"], "levven.ca"),
    (["taikan"], "taikan.com"), (["primetoolstech"], "primetoolstech.com"),
    (["franklinsensors"], "franklinsensors.com"), (["compalusa"], "compalusa.com"),
    (["opmobility"], "opmobility.com"), (["moulage"], "savoy-moulage.fr"), (["savoy-el"], "savoy-el.com"),
    (["prosmd"], "prosmd.com"), (["mactech"], "mactech.com.ar"), (["integraltek"], "integraltek.com.ar"),
    (["everelgroup"], "everelgroup.com"), (["besi"], "besi.com"), (["tncltd"], "tncltd.com"),
    (["greenvolt"], "greenvolt.co.in"), (["incapcms"], "incapcms.com"), (["himil"], "himil.in"),
    (["resoluteelectronics"], "resoluteelectronics.com"), (["arv"], "arv-india.com"),
    (["wintech"], "wintech.my"), (["akashicind"], "akashicind.com"), (["tantheky"], "tantheky.com"),
    (["luckystarco"], "luckystarco.vn"), (["ecaman"], "ecaman.com"), (["alcoelectro"], "alcoelectro.com"),
    (["siteco"], "siteco.de"), (["dbk-group"], "dbk-group.com"), (["elpas"], "elpas.pl"),
    (["fitech"], "fitech.pl"), (["schaeffler"], "schaeffler.com"), (["canor-audio"], "canor-audio.com"),
    (["instrument52"], "instrument52.ru"), (["atlant-npp"], "atlant-npp.ru"),
    (["pige-electronique"], "pige-electronique.fr"), (["shintech"], "shintech.ae"),
    (["kerno"], "kerno.ae"), (["cesiumastro"], "cesiumastro.com"), (["pfipcb"], "pfipcb.com"),
    (["hubbell"], "hubbell.com"), (["americancircuits"], "americancircuits.com"),
    (["anthemdisplays"], "anthemdisplays.com"), (["cartell"], "cartell.com"),
    (["cascadesystems"], "cascadesystems.net"), (["cwcems"], "cwcems.com"),
    (["dellasystems"], "dellasystems.com"), (["enovationcontrols"], "enovationcontrols.com"),
    (["geospace"], "geospace.com"), (["ipsassembly"], "ipsassembly.com"),
    (["kb electronics", "kbelectronics"], "kb-electronics.com"), (["luminus"], "luminus.com"),
    (["rcalproducts"], "rcalproducts.com"), (["seacomp"], "seacomp.com"), (["syngenta"], "syngenta.com"),
    (["visionary-systems"], "visionary-systems.com"), (["indservice", "sbcglobal"], "indservice-usa.com"),
    (["acbel"], "acbel.com"), (["bernaelectronics"], "bernaelectronics.com"), (["preh"], "preh.mx"),
    (["visam"], "visam.com.mx"), (["ikor"], "ikor.mx"), (["nit-tech"], "nit-tech.com"),
    (["stoneridge"], "stoneridge.com"), (["kimball"], "kimball.com"), (["jltech"], "jltech.co.kr"),
    (["uealternator"], "uealternator.com"), (["technology-gr"], "technology-gr.com"),
    (["ofoq", "高德铭"], "ofoq-electronic.ir"), (["sedemac"], "sedemac.com"),
    (["creationtech"], "creationtech.com"), (["qtek"], "qtek.com"), (["ducommun"], "ducommun.com"),
    (["vergesense"], "vergesense.com"), (["estexhibit"], "estexhibit.com"),
    (["pbtecsolutions"], "pbtecsolutions.de"), (["vintronicsinc"], "vintronicsinc.com"),
    (["tarpuq"], "tarpuq-ems.com"), (["cmcindustrial"], "cmcindustrial.com.br"),
    (["mastertool"], "mastertool.com.mx"), (["unlimitedelectro"], "unlimitedelectro.com"),
    (["iotechnology"], "iotechnology-am.com"), (["elektrotek"], "elektrotek.co.id"),
    (["intronics"], "intronics.co.th"), (["karel"], "karel.com.tr"), (["icag"], "icag.biz"),
    (["lambertelectronic"], "lambertelectronic.com"), (["dis-electronics"], "dis-electronics.ru"),
    (["winford"], "winford.com"), (["truemfg"], "truemfg.com"),
    (["innovaengineering"], "innovaengineering.com"), (["innovelectronics"], "innovelectronics.com"),
    (["jabil"], "jabil.com"), (["desimone"], "desimone.be"), (["aptiv"], "aptiv.com"),
    (["schneider", "se.com"], "schneider-electric.com"), (["theatrical"], "theatrical.com"),
    (["amirinternacional"], "amirinternacional.com"), (["pacificinsight"], "pacificinsight.com"),
    (["monitor-electronics"], "monitor-electronics.com"), (["telux"], "telux.sk"),
    (["incos"], "incos.kiev.ua"), (["shukvir"], "shukvir.in"), (["ntis"], "ntis.com.sa"),
    (["lucidvision"], "lucidvisionlabs.com"), (["grsys"], "grsys.com"), (["aaviza"], "aaviza.com"),
    (["vvdn"], "vvdntech.com"), (["gcindustrial"], "gcindustrial.mx"), (["indurama"], "indurama.com"),
    (["prosserllc"], "prosserllc.com"), (["greystoneenergy"], "greystoneenergy.com"),
    (["jlmrm"], "jlmrm.com"), (["winsystems"], "winsystems.com"), (["forvia"], "forvia.com"),
    (["ctscorp"], "ctscorp.com"), (["lightstim"], "lightstim.com"), (["henry.com.br"], "henry.com.br"),
]

def strip_country(s):
    for c in COUNTRIES:
        s = s.replace(c, "")
    return s

def clean_who(w):
    w = w.strip()
    w = re.sub(r"^[（(\[【].*?[)）\]】]", "", w)
    w = re.sub(r"^(?:实现对|实现与|针对|关于实现|关于|开发|背调客户|客户背调|新客户)", "", w)
    w = strip_country(w)
    w = re.sub(r"[（(\[【].*?[)）\]】]", " ", w)
    w = re.sub(r"[<>「」“”\"']", " ", w)
    w = re.sub(r"^(?:的|了|向|给)", "", w.strip())
    w = SUFFIX_RE.sub("", w.strip())
    w = re.sub(r"\s+", " ", w).strip(" 　-,，、。/\\")
    return w

INTERNAL = re.compile(r"(n8n|pve|proxmox|sora|openclaw|coze|dify|chatgpt|chat gpt|claude|gemini|notebooklm|"
                      r"5ber|xiaoya|solidworks|windows|mac软件|openai|perplexity|flux|stable diffusion|"
                      r"langchain|ollama|comfyui|lora|docker|1panel|宝塔|alist|zfile|obs|剪映|capcut|"
                      r"trigger|webhook|api|bot\b|agent\b|workflow|龙虾)", re.I)

KEY_REJECT = re.compile(r"(请整理|我们的|我们成功|复盘|总结|案例|培训|学习|视频|海报|文案|模版|模板|会议纪要|"
                        r"周报|日报|年度目标|月份目标|赢在ai|销冠|工作内容|客户管理|知识库|思维导图|"
                        r"销售策略|流程|方法|技巧|清单|列表|汇总表|统计|登记表|通讯录|名片)", re.I)

def ok_who(who, t):
    """Reject internal/container phrases mistaken as company names."""
    if not who or len(who) < 2:
        return False
    if KEY_REJECT.search(who):
        return False
    if re.search(r"[\u4e00-\u9fff]", who):
        # Chinese-only name allowed only from an explicit customer-ownership pattern
        if not re.match(r"^(?:实现(?:对|与)|针对|关于实现|新客户|背调客户|客户背调)", t):
            return False
        if len(who) > 15:
            return False
    else:
        if INTERNAL.search(who):
            return False
    return True

def norm_domain(d):
    return re.sub(r"^www\.", "", d.lower().strip())

def domain_ok(d):
    return d not in NOISE_DOMAINS and d.split(".")[0] not in {"com","co","group","electronics","www","net","org"}

def extract_key(title):
    t = title.strip()
    if not t or t.startswith("→"):
        return None
    if NOISE_KW.search(t) or CONTAINER.match(t):
        return None
    country = next((c for c in COUNTRIES if c in t), "")

    # 背调客户：XXX
    m = re.match(r"^(?:背调客户|客户背调)[：:]\s*(.+)$", t)
    if m:
        raw = m.group(1).strip()
        who = clean_who(raw)
        dm = DOMAIN_RE.search(raw)
        if dm and domain_ok(norm_domain(dm.group(1))):
            return canon(norm_domain(dm.group(1))), country, norm_domain(dm.group(1)), "背调阶段", who
        if len(who) >= 3 and ok_who(who, t):
            return canon(who.lower()), country, "", "背调阶段", who
        return None

    # verb split (tier1 concrete selling verbs, tier2 soft verbs)
    pos = -1; verb = ""
    soft_ok = bool(re.match(r"^实现(?:对|与)", t))
    tiers = (["整机销售", "销售", "推销", "采购", "配件销售"], ["合作", "询盘"])
    if soft_ok:
        tiers = tiers + (["的"],)
    for tier in tiers:
        for v in tier:
            i = t.find(v)
            if i > 0 and (pos == -1 or i < pos):
                pos, verb = i, v
        if pos > 0:
            break
    if pos > 0:
        who_raw = t[:pos]
        prod = t[pos + len(verb):]
        prod = re.split(r"(?:和|并|，|,|以及|寻求|达成|开展|实现|发展)", prod)[0].strip(" 　-的")
        who = clean_who(who_raw)
        dm = DOMAIN_RE.search(who_raw)
        if dm and domain_ok(norm_domain(dm.group(1))):
            return canon(norm_domain(dm.group(1))), country, norm_domain(dm.group(1)), (prod or "待定"), who
        who2 = re.sub(r"\.(?:com|net|org).*$", "", who).strip()
        if len(who2) >= 3 and ok_who(who2, t):
            return canon(who2.lower()), country, "", (prod or "待定"), who
        return None

    # 开发巴西xxx.com...
    m = re.match(r"^开发\s*(.+)$", t)
    if m and DOMAIN_RE.search(m.group(1)):
        raw = m.group(1).strip()
        dm = DOMAIN_RE.search(raw)
        return canon(norm_domain(dm.group(1))), country, norm_domain(dm.group(1)), "开发线索", raw
    em = EMAIL_RE.search(t)
    if em:
        dom = em.group(0).split("@")[1].lower()
        if domain_ok(dom):
            return canon(dom), country, dom, "网站询盘", em.group(0)
        return None
    dm = DOMAIN_RE.search(t)
    if dm and domain_ok(norm_domain(dm.group(1))):
        return canon(norm_domain(dm.group(1))), country, norm_domain(dm.group(1)), "网站询盘", t

    # generic fallback: leading marker + Latin company name
    s = re.sub(r"^(?:实现对|实现与|针对|关于实现|关于|开发|新客户|客户|背调客户|客户背调)[：:\s]*", "", t)
    s = strip_country(s)
    s = re.split(r"[（(【\[]|的|，|,|和|并|及|/", s)[0].strip()
    if len(s) <= 40 and not INTERNAL.search(s) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\-&\.\'’ ]{2,40}", s):
        s2 = SUFFIX_RE.sub("", s).strip()
        return canon(s2.lower()), country, "", "待定", s
    return None

MONEY_RE = re.compile(r"(?:USD|US\$|\$|美金)\s*([0-9][0-9,\.]*)", re.I)
DEAL_WORDS = {"收款":3,"PI":3,"PO":4,"出货":4,"发货":3,"订单":4,"合同":3,"报价单":2,"报价":2,
              "成交":5,"复购":5,"返单":5,"已付款":5,"未收款":3,"样品":2,"验厂":3,"视频会议":2,
              "meeting":2,"背调":1,"开发信":1,"客户背景":1,"客户需求":1,"寄送样品":4,"回访":2}
STATUS_SCORE = {"已收款":10,"已验收待出货":9,"进行中":6,"正式报价":7,"客户方案准备中":5,"初步沟通":4,
                "首次交接":3,"建立联系":3,"客户信息收集整理中":2,"待开发":2,"未激活":1,"未开始":1,
                "一级客户":8,"一般意向":3,"关闭":0,"待定":2}
def pd(s):
    return (s or "")[:10]

cust = collections.defaultdict(lambda: {
    "titles": [], "projects": set(), "owners": collections.Counter(), "statuses": collections.Counter(),
    "activities": [], "created": [], "updated": [], "products": collections.Counter(),
    "countries": collections.Counter(), "emails": set(), "domains": set(), "raw": set(),
    "deal_pts": 0, "money": [], "desc": []})

for pj, rows in byproj.items():
    cur = None
    pending = []   # (title_row, kids) for short-title fallback
    for r in rows:
        t = (r["title"] or "").strip()
        if not t:
            continue
        if t.startswith("→"):
            if cur:
                act = re.sub(r"^[→\s]+", "", t)
                cur["activities"].append({"a": act, "st": r["status"], "upd": pd(r["updated_on"]), "pj": pj})
                body = act + " " + (r.get("desc") or "")
                for w, sc in DEAL_WORDS.items():
                    if w.lower() in body.lower():
                        cur["deal_pts"] += sc
                for m in MONEY_RE.finditer(body):
                    try:
                        v = float(m.group(1).replace(",", ""))
                        if 10 < v < 1000000:
                            cur["money"].append(round(v, 2))
                    except Exception:
                        pass
            continue
        info = extract_key(t)
        if not info:
            cur = None
            continue
        key, country, dom, prod, raw = info
        c = cust[key]; cur = c
        c["titles"].append(t); c["projects"].add(pj); c["raw"].add(raw)
        if r["owner"]:
            c["owners"][r["owner"]] += 1
        c["statuses"][r["status"]] += 1
        if country:
            c["countries"][country] += 1
        if prod:
            c["products"][prod] += 1
        if dom:
            c["domains"].add(dom)
        for e in EMAIL_RE.findall(t):
            c["emails"].add(e.lower())
        c["created"].append(pd(r["created_on"])); c["updated"].append(pd(r["updated_on"]))
        if r.get("desc"):
            c["desc"].append(r["desc"][:600])
        body = t + " " + (r.get("desc") or "")
        for w, sc in DEAL_WORDS.items():
            if w.lower() in body.lower():
                c["deal_pts"] += sc
        for m in MONEY_RE.finditer(body):
            try:
                v = float(m.group(1).replace(",", ""))
                if 10 < v < 1000000:
                    c["money"].append(round(v, 2))
            except Exception:
                pass

out = []
for key, c in cust.items():
    # drop template rows replicated across many projects with no activity
    if len(c["activities"]) == 0 and len(c["projects"]) >= 3:
        continue
    upd = sorted(x for x in c["updated"] if x)
    cre = sorted(x for x in c["created"] if x)
    n_act, n_pj = len(c["activities"]), len(c["projects"])
    stat_score = max([STATUS_SCORE.get(s, 1) for s in c["statuses"]] or [1])
    recency = upd[-1] if upd else ""
    rp = 10 if recency >= "2026-01-01" else 7 if recency >= "2025-07-01" else 5 if recency >= "2025-01-01" else 3 if recency >= "2024-01-01" else 1
    money_total = sum(sorted(set(c["money"]))[-15:])
    score = (n_act * 2.0 + n_pj * 6.0 + stat_score * 3.0 + rp * 2.5 +
             min(c["deal_pts"], 60) * 0.8 + min(money_total / 500.0, 25))
    out.append({"key": key, "domains": sorted(c["domains"]), "emails": sorted(c["emails"]),
        "titles": c["titles"], "projects": sorted(c["projects"]), "owners": c["owners"].most_common(),
        "statuses": c["statuses"].most_common(), "countries": c["countries"].most_common(),
        "products": c["products"].most_common(), "n_act": n_act, "n_pj": n_pj,
        "first": cre[0] if cre else "", "last": recency, "deal_pts": c["deal_pts"],
        "money": sorted(set(c["money"])), "money_total": round(money_total, 2),
        "stat_score": stat_score, "score": round(score, 1),
        "activities": c["activities"][:80], "desc": c["desc"][:2], "raw": sorted(c["raw"])[:6]})

out.sort(key=lambda x: -x["score"])
json.dump(out, open(os.path.join(OUT, "customers.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("customers:", len(out))
print(f"{'#':>3} {'score':>7} {'act':>4} {'pj':>3} {'last':<11} {'money':>9}  key")
for i, o in enumerate(out[:45], 1):
    print(f"{i:>3} {o['score']:>7} {o['n_act']:>4} {o['n_pj']:>3} {o['last']:<11} {o['money_total']:>9.0f}  {o['key'][:42]}")
