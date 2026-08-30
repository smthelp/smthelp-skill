# -*- coding: utf-8 -*-
"""Foxmail 邮件头 -> 客户通讯录 v2（加域名归并、退信剔除、更严分级）"""
import json, re, os, collections, datetime, sys

SRC = '/tmp/foxmails3.jsonl'
TODAY = datetime.date(2026, 8, 30)

OWN_DOM = {'smthelp.com', 'smthelp.net', 'smtnozzle.org', 'smtnozzle.com', 'smtsupplier.com'}
OWN_ADDR = {'jasonwu68@qq.com', 'w25605@gmail.com', 'smthelpmachine@gmail.com',
            'jasonwusmt@outlook.com'}

FREE = set("""gmail.com googlemail.com yahoo.com yahoo.co.uk yahoo.fr yahoo.es yahoo.com.br
yahoo.com.mx yahoo.co.in yahoo.com.tr ymail.com rocketmail.com hotmail.com hotmail.co.uk
hotmail.fr hotmail.it hotmail.de hotmail.es hotmail.com.br hotmail.com.mx outlook.com
outlook.es outlook.fr outlook.it outlook.de live.com live.co.uk live.fr live.it live.de
live.ca live.com.au live.nl live.dk live.se live.no live.be msn.com aol.com aim.com
icloud.com me.com mac.com protonmail.com proton.me gmx.com gmx.de gmx.net gmx.at web.de
t-online.de mail.ru bk.ru inbox.ru list.ru rambler.ru ukr.net mail.ua i.ua meta.ua
yandex.ru yandex.com narod.ru qq.com vip.qq.com foxmail.com 163.com 126.com vip.163.com
yeah.net sina.com vip.sina.com sohu.com 139.com aliyun.com zoho.com mail.com naver.com
daum.net hanmail.net nate.com seznam.cz email.cz centrum.cz libero.it virgilio.it alice.it
tiscali.it tiscali.co.uk btinternet.com sky.com virginmedia.com talktalk.net ntlworld.com
orange.fr wanadoo.fr free.fr sfr.fr laposte.net numericable.fr telefonica.net terra.es
wanadoo.es optusnet.com.au bigpond.com bigpond.net.au ozemail.com.au xtra.co.nz ihug.co.nz
clear.net.nz sympatico.ca shaw.ca rogers.com bell.net videotron.ca telus.net uol.com.br
bol.com.br terra.com.br globo.com ig.com.br superig.com.br click21.com.br zipmail.com.br
comcast.net cox.net sbcglobal.net bellsouth.net charter.net earthlink.net juno.com
netscape.net adelphia.net prodigy.net ameritech.net att.net verizon.net bluewin.ch
telenet.be planet.nl chello.nl kpnmail.nl abv.bg mail.bg volny.cz atlas.cz gmail.co.uk
rediffmail.com indiatimes.com sify.com""".split())

# ---------- 硬性黑名单 ----------
BLACK = """
facebookmail fbworkmail e.linkedin ecn.linkedin linkedin twitter xing instagram tumblr
redditmail reddit quora tiktok pinterest snapchat vk.com skool mail.instagram
support.facebook insideapple accounts.google google.com googlemail mail.google
bosszhipin indeed glassdoor ziprecruiter naukri infojobs mylaborjob capacitacionrh
monster.com careerbuilder talent.com workable greenhouse.io lever.co bamboohr
mailchimp mailchimpapp ccsend constantcontact hubspot mailgun sendgrid
klaviyo intercom zapier ifttt snov.io hunter.io woodpecker instantly lemlist
semrush ahrefs neilpatel seopressor seochecklist onlinecapturecenter contentreads
aggregage discoursemail mautic.org discoursemail.com workitive mobilemonkey glisser
captainform wponlinesupport webliteseo campaignmonitor activecampaign getresponse
sendinblue brevo mailerlite omnisend mailup drip.com customer.io iterable
jetpack vaultpress wordpress woocommerce cloudflare cyberpanel racknerd itldc
cloudns selectel secureserver godaddy algolia twilio slack notion.so wrike
wetransfer canva engage.canva grammarly grabcad sketchfab okta github gitlab
atlassian postmark sparkpost mandrill mailjet elasticemail pepipost messagelabs
eigbox postmaster mailer-daemon
dhl ups.com fedex kuehne-nagel kuehne dsv expeditors mainfreight by56
ads-logistics ease-tradeforward ease-supplystep supplyitnowcampaign porttechnology
ceva maersk hapag evergreen agility dbschenker rhenus gefco sll.com.hk eiffsz
service.alibaba email.alibaba alibaba.com aliexpress taobao tmall
intl.paypal paypal xtransfer standardchartered s2bmail lendmefund sc.com
wish.com amazon jd.com carters arbys premiumoutlets rentalcars trip.com
dealmoon lightstim bestgloves greengasplant extendedstay
mailsupport.aliyun notice.aliyun aliyun mail.worktile worktile tencent
foxmail.com service.qq jiankongbao volcengine notice.volcengine
gsma2017 adsale-marketing gismaexpo nepconchina efymag cbcinewsemail
researchandmarkets reportlinker globalspec engineering360 electronicdesign
thomasnet pentondes m2mservices
sharewareonsale sudoku.name buffman.org
alarmtrade mideacarrier sciencgo kernalsell kernal-vip yymzh hongbanzhuan
unknown.email unknown.person tawk.to freshdesk zendesk freshworks
upwork kwork fiverr freelancer peopleperhour
facebook.com fb.com instagram byethost
unisoft-cim ascglobal elcina juliangoldie fastechpcb abiscircuits
sourceability hardfind
tradeindia indiamart ec21
cisco.com ces.cisco messagelabs netvigator da.direct serv00 mindautocloud
net.cn 263.net top2dim wpc-board jd-machine cml.com.cn koplu.shop
eastcom gdxingmingda nbxyznkj wfrjdz sikeyue
"""
BLACK = set(BLACK.split())

# 采购/供应商门户平台词（域名倒数第二段）
PORTAL = {'coupahost', 'coupa', 'ariba', 'sap', 'jaggaer', 'zycus', 'gep', 'bravosolution',
          'perfectcommerce', 'iastа', 'iasta', 'ivalua', 'determine', 'sciquest', 'esupply',
          'proqura', 'tradeshift', 'basware', 'tipalti', 'signifyportal'}
# 邮件系统子域前缀（去掉后归并到主域）
SUBDOM = {'mail', 'email', 'smtp', 'mx', 'web', 'www', 'info', 'sales', 'service', 'support',
          'noreply', 'no-reply', 'auto', 'autoreply', 'notification', 'notify', 'news',
          'newsletter', 'marketing', 'edm', 'campaign', 'reply', 'contact', 'admin', 'postmaster',
          'bounce', 'outbound', 'inbound', 'mta', 'relay', 'server', 'srv'}

# 仅在「我方从未回复」时启用的推销方关键词（保守过滤，避免误伤客户）
COLD_SPAM = ['seo', 'webdesign', 'web-design', 'hosting', 'hostuno', 'vps', 'dedicated',
             'cpanel', 'ssl', 'domain', 'sourcing', 'asourcing', 'supplier-cn', 'chinamanufactur',
             'trade', 'b2bmarket', 'leads', 'list-building', 'outreach', 'coldmail']

BOUNCE_RE = re.compile(r'(delivery status|undeliver|mail delivery fail|return(ed|ing) message|'
                       r'failure notification|mailer-daemon|auto-?reply|automatic reply|'
                       r'out of office|away from|已读|自動回覆|未傳遞|退信|delivery fail|'
                       r'permanent fatal|host not found|no such user|user unknown|'
                       r'mailbox (is )?(full|unavailable|not found)|blocked|rejected|'
                       r' spam|quarantine|junk mail|address not found|does not exist|'
                       r'delivery obstacle|incorrect address)', re.I)

BUY_RE = re.compile(r'\b(rfq|inquir|enquir|quot|price|pricing|cost|budget|proposal|offer|'
                    r'interest|need|require|buy|purchase|order|spec|datasheet|catalog|'
                    r'catalogue|machine|reflow|wave solder|pick and place|smt|smd|tht|dip|'
                    r'insertion|conveyor|loader|unloader|stencil|feeder|nozzle|aoi|spi|'
                    r'solder paste|pcb assembly|production line|turnkey|spare part|'
                    r'capability|capacity|delivery|lead time|moq)\b', re.I)
PO_RE = re.compile(r'\b(purchase order|p\.?o\.?\s*#|po number|order confirm|proforma|'
                   r'pro forma|contract|invoice|payment|deposit|t/?t|l/?c|down ?payment|'
                   r'balance|shipment|shipping arrangement|new vendor)\b', re.I)
INQ_RE = re.compile(r'\b(rfq|inquir|enquir|quot|price|pricing|cost|datasheet|catalog|'
                    r'catalogue|spec|interest|need|require|requirement)\b', re.I)
CLEAN_RE = re.compile(r'^\s*((re|fwd|fw|答复|回复|转发|res|antw|rif|enc|tr|sv|vs|aw|自动回复|'
                      r'automatic reply|auto reply|read|le[ií]do|przeczytane|прочтено|已读)\s*[:：]\s*|\s*\[.{0,20}\]\s*)+', re.I)

CC = {'uk':'United Kingdom','br':'Brazil','mx':'Mexico','vn':'Vietnam','tr':'Turkey',
 'in':'India','de':'Germany','fr':'France','it':'Italy','es':'Spain','nl':'Netherlands',
 'be':'Belgium','pl':'Poland','ru':'Russia','ua':'Ukraine','cz':'Czech Republic',
 'se':'Sweden','no':'Norway','dk':'Denmark','fi':'Finland','ch':'Switzerland','at':'Austria',
 'pt':'Portugal','gr':'Greece','ie':'Ireland','au':'Australia','nz':'New Zealand',
 'ca':'Canada','jp':'Japan','kr':'South Korea','cn':'China','hk':'Hong Kong, China',
 'tw':'Taiwan, China','sg':'Singapore','my':'Malaysia','th':'Thailand','id':'Indonesia',
 'ph':'Philippines','pk':'Pakistan','bd':'Bangladesh','lk':'Sri Lanka','za':'South Africa',
 'eg':'Egypt','ng':'Nigeria','ke':'Kenya','ae':'UAE','sa':'Saudi Arabia','il':'Israel',
 'ir':'Iran','ro':'Romania','hu':'Hungary','sk':'Slovakia','si':'Slovenia','hr':'Croatia',
 'rs':'Serbia','bg':'Bulgaria','ee':'Estonia','lv':'Latvia','lt':'Lithuania','by':'Belarus',
 'kz':'Kazakhstan','ar':'Argentina','cl':'Chile','co':'Colombia','pe':'Peru','uy':'Uruguay',
 've':'Venezuela','ec':'Ecuador','cr':'Costa Rica','pa':'Panama','gt':'Guatemala',
 'do':'Dominican Republic','pr':'Puerto Rico','ma':'Morocco','tn':'Tunisia','dz':'Algeria',
 'eu':'European Union','us':'United States','ca.us':'United States'}


def dom(a):
    return a.rsplit('@', 1)[1].lower().strip('<> ') if '@' in a else ''


def key_of(addr):
    """公司聚合键：免费邮箱取完整地址，企业邮箱取归并后的域名"""
    d = norm_dom(dom(addr))
    return addr.lower() if d in FREE else (d or addr.lower())


def norm_dom(d):
    """归并采购平台域与邮件系统子域"""
    if not d:
        return ''
    p = d.split('.')
    if len(p) >= 3 and p[-2] in PORTAL and p[0] not in SUBDOM:
        return f'{p[-3]}.{p[-1]}'
    if len(p) >= 3 and p[0] in SUBDOM:
        return '.'.join(p[1:])
    return d


def clean_subject(s):
    prev = None
    while prev != s:
        prev = s
        s = CLEAN_RE.sub('', s).strip()
    return s.strip(' -–—:：')


def is_black(d):
    if not d:
        return True
    for b in BLACK:
        if b in d:
            return True
    return False


def country_of(d):
    parts = d.split('.')
    for n in (2, 1):
        if len(parts) >= n + 1:
            tld = '.'.join(parts[-n:]) if n == 2 else parts[-1]
            if tld in CC:
                return CC[tld]
    return ''


def cname_of(d):
    if not d or '.' not in d:
        return ''
    main = d.split('.')[0]
    main = re.sub(r'^(mail|email|info|service|sales|contact|www|na|cn|hk)\d*$', '', main)
    if not main:
        main = d.split('.')[0]
    main = main.replace('-', ' ').replace('_', ' ')
    return ' '.join(w.capitalize() if w.islower() else w for w in main.split())


def split_name(nm, addr):
    nm = re.sub(r'["\']', '', (nm or '')).strip()
    if nm.lower() == addr.lower() or '@' in nm:
        nm = ''
    if not nm:
        nm = addr.split('@')[0]
    nm = re.sub(r'[0-9_]+$', '', nm).strip()
    nm = re.sub(r'[._-]+', ' ', nm).strip()
    parts = [p for p in nm.split() if p]
    if not parts:
        return ('', '')
    if len(parts) == 1:
        return (parts[0][:1].upper() + parts[0][1:], '')
    return (parts[0][:1].upper() + parts[0][1:],
            ' '.join(parts[1:])[:1].upper() + ' '.join(parts[1:])[1:])


# ---------------- 主流程 ----------------
comp = collections.defaultdict(lambda: {
    'n_in': 0, 'n_out': 0, 'n_buy': 0, 'n_po': 0, 'n_inq': 0, 'n_bounce': 0,
    'first': '', 'last': '', 'subjects': collections.Counter(),
    'people': collections.Counter(), 'accounts': collections.Counter(),
    'ascii': collections.Counter(),
})
people = collections.defaultdict(lambda: {
    'n': 0, 'n_out': 0, 'n_buy': 0, 'n_po': 0, 'first': '', 'last': '',
    'subjects': collections.Counter(), 'name': '', 'ckey': ''})
noise = collections.Counter()
recs = kept = 0

with open(SRC) as f:
    for line in f:
        r = json.loads(line)
        recs += 1
        fm = r['from'].lower()
        tos = [t for t in r['to'].split(';') if t]
        fd = norm_dom(dom(fm))
        own_from = fd in OWN_DOM or dom(fm) in OWN_DOM or fm in OWN_ADDR
        own_to = [t for t in tos if dom(t) in OWN_DOM or t in OWN_ADDR]
        dt = r['date']
        sub = clean_subject(r['subject'])
        bounce = bool(BOUNCE_RE.search(r['subject']))
        if own_from:
            exts = [t for t in tos if dom(t) not in OWN_DOM and t not in OWN_ADDR]
            for t in exts:
                d = norm_dom(dom(t))
                if is_black(d):
                    noise[d] += 1
                    continue
                c = comp[key_of(t)]
                c['n_out'] += 1
                c['n_buy'] += 1 if BUY_RE.search(sub) else 0
                c['n_po'] += 1 if PO_RE.search(sub) else 0
                if dt:
                    c['last'] = max(c['last'], dt)
                    if not c['first'] or dt < c['first']:
                        c['first'] = dt
                if sub:
                    c['subjects'][sub[:120]] += 1
                    if sub.isascii():
                        c['ascii'][sub[:120]] += 1
                c['accounts'][r['account']] += 1
                pp = people[t.lower()]
                pp['n_out'] += 1
                pp['n'] += 1
                pp['ckey'] = key_of(t)
                if dt:
                    pp['last'] = max(pp['last'], dt)
                    if not pp['first'] or dt < pp['first']:
                        pp['first'] = dt
                if sub:
                    pp['subjects'][sub[:120]] += 1
                kept += 1
        elif own_to:
            if is_black(fd):
                noise[fd] += 1
                continue
            c = comp[key_of(fm)]
            c['n_in'] += 1
            c['n_bounce'] += 1 if bounce else 0
            c['n_buy'] += 1 if BUY_RE.search(sub) else 0
            c['n_po'] += 1 if PO_RE.search(sub) else 0
            c['n_inq'] += 1 if INQ_RE.search(sub) else 0
            if dt:
                c['last'] = max(c['last'], dt)
                if not c['first'] or dt < c['first']:
                    c['first'] = dt
            if sub:
                c['subjects'][sub[:120]] += 1
                if sub.isascii():
                    c['ascii'][sub[:120]] += 1
            c['accounts'][r['account']] += 1
            nm = r['sender_name']
            if nm and nm.lower() != fm and '@' not in nm:
                c['people'][f'{nm} <{fm}>'] += 1
            else:
                c['people'][fm] += 1
            pp = people[fm]
            pp['n'] += 1
            pp['ckey'] = key_of(fm)
            pp['n_buy'] += 1 if BUY_RE.search(sub) else 0
            pp['n_po'] += 1 if PO_RE.search(sub) else 0
            if nm and nm.lower() != fm and '@' not in nm and len(nm) > len(pp['name']):
                pp['name'] = nm
            if dt:
                pp['last'] = max(pp['last'], dt)
                if not pp['first'] or dt < pp['first']:
                    pp['first'] = dt
            if sub:
                pp['subjects'][sub[:120]] += 1
            kept += 1

print('records', recs, 'kept', kept, 'domains', len(comp), file=sys.stderr)

# ---------------- 计分与分级 ----------------
rows = []
for key, c in comp.items():
    n_total = c['n_in'] + c['n_out']
    if n_total < 1:
        continue
    # 冷推销过滤：我方从未回复过 + 命中推销关键词 + 往来很密（群发特征）
    if c['n_out'] == 0 and c['n_in'] >= 8 and any(k in key for k in COLD_SPAM):
        continue
    eff_in = c['n_in'] - c['n_bounce']
    last = c['last'] or c['first']
    try:
        days = (TODAY - datetime.date.fromisoformat(last)).days if last else 99999
    except Exception:
        days = 99999
    bonus = 30 if days <= 90 else (15 if days <= 365 else (5 if days <= 730 else 0))
    score = c['n_out'] * 5 + max(eff_in, 0) * 1 + c['n_buy'] * 8 + c['n_po'] * 20 + bonus
    buylike = c['n_buy'] >= 1 or c['n_po'] >= 1 or c['n_inq'] >= 3
    replied = c['n_out'] >= 1
    if (score >= 100 and c['n_in'] >= 10 and c['n_out'] >= 5 and days <= 365
            and (c['n_po'] >= 1 or c['n_buy'] >= 5)):
        g = 'A'
    elif (score >= 40 and replied and days <= 730 and (c['n_buy'] >= 1 or c['n_inq'] >= 5)):
        g = 'B'
    elif buylike and replied and days <= 730:
        g = 'C'
    elif buylike and replied and days > 730 and n_total >= 5:
        g = 'D'
    elif replied:
        g = 'E'
    else:
        g = 'F'   # 单向来信，我方从未回复
    src = c['ascii'] or c['subjects']
    top_sub = src.most_common(1)[0][0] if src else ''
    top_name = c['people'].most_common(1)[0][0] if c['people'] else ''
    addr = ''
    m = re.search(r'<([^>]+)>', top_name)
    if m:
        addr = m.group(1).lower()
    elif top_name and '@' in top_name:
        addr = top_name.lower()
    nm = re.sub(r'\s*<[^>]*>\s*', '', top_name).strip()
    fn, ln = split_name(nm, addr)
    rows.append({
        'key': key, 'addr': addr, 'grade': g, 'score': score,
        'n_in': c['n_in'], 'n_out': c['n_out'], 'n_total': n_total,
        'n_buy': c['n_buy'], 'n_po': c['n_po'], 'n_inq': c['n_inq'], 'n_bounce': c['n_bounce'],
        'first': c['first'], 'last': last, 'days': days,
        'company': cname_of(key), 'country': country_of(key), 'website': key,
        'firstname': fn, 'lastname': ln, 'subject': top_sub,
        'accounts': '; '.join(f'{k}({v})' for k, v in c['accounts'].most_common(3)),
        'people_n': len(c['people']),
        'top_people': '; '.join(f'{p}×{n}' for p, n in c['people'].most_common(5)),
    })

# F 级（我方从未回复）仅保留有采购/询盘/PO 信号的，其余视为营销噪声丢弃
before = len(rows)
rows = [r for r in rows
        if r['grade'] != 'F' or (r['n_inq'] >= 1 or r['n_buy'] >= 1 or r['n_po'] >= 1)]
print('F filtered', before, '->', len(rows), file=sys.stderr)

# 输出 people 明细
prows = []
for addr, p in people.items():
    if p['n'] < 2 and p['n_out'] < 1:
        continue
    src = p['subjects']
    prows.append({
        'email': addr, 'name': p['name'], 'ckey': p['ckey'],
        'n': p['n'], 'n_out': p['n_out'],
        'first': p['first'], 'last': p['last'],
        'subject': src.most_common(1)[0][0] if src else '',
    })
prows.sort(key=lambda r: (-r['n_out'], -r['n']))
with open('/tmp/people_rows.json', 'w') as fo:
    json.dump(prows, fo, ensure_ascii=False)
print('people rows', len(prows), file=sys.stderr)

order = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5}
rows.sort(key=lambda r: (order[r['grade']], -r['score']))
cnt = collections.Counter(r['grade'] for r in rows)
print('graded:', dict(sorted(cnt.items())), file=sys.stderr)
print('replied(有我方回复):', sum(1 for r in rows if r['n_out'] >= 1), file=sys.stderr)

with open('/tmp/contacts_rows.json', 'w') as fo:
    json.dump(rows, fo, ensure_ascii=False)
with open('/tmp/noise_domains.json', 'w') as fo:
    json.dump(noise.most_common(400), fo, ensure_ascii=False)
