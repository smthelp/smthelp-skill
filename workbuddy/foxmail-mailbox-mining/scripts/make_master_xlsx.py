# -*- coding: utf-8 -*-
"""生成 SMThelp Master 客户库 Excel（面向外贸营销再激活，非 CRM 导入格式）"""
import json, datetime, collections, re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

TODAY = datetime.date.today()
OUT = f'/tmp/SMThelp_Master客户库_邮件挖掘_{TODAY:%Y%m%d}.xlsx'

rows = json.load(open('/tmp/contacts_rows.json'))
prows = json.load(open('/tmp/people_rows.json'))

SKIP = {'na', 'eu', 'us', 'uk', 'cn', 'hk', 'tw', 'jp', 'kr', 'in', 'br', 'apac', 'emea',
        'amer', 'americas', 'asia', 'europe', 'global', 'intl', 'international', 'mail',
        'email', 'info', 'service', 'sales', 'contact', 'www', 'web', 'green', 'community',
        'my', 'the', 'go', 'online', 'shop', 'store', 'corp', 'inc', 'ltd', 'group', 'team',
        'admin', 'office', 'support', 'help', 'news', 'newsroom', 'press', 'careers'}


def cname_of(d):
    if not d or '.' not in d:
        return ''
    for seg in d.split('.'):
        s = re.sub(r'\d+$', '', seg)
        if len(s) >= 3 and s.lower() not in SKIP:
            return s.replace('-', ' ').replace('_', ' ').title()
    seg = d.split('.')[0]
    return seg.replace('-', ' ').title()


for r in rows:
    r['company'] = cname_of(r['key'])
    r['inq_yn'] = '是' if (r['n_inq'] >= 1 or r['n_buy'] >= 1 or r['n_po'] >= 1) else '否'
    r['days_s'] = r['days'] if r['days'] < 99999 else ''

by_key = {r['key']: r for r in rows}
GRADE_TXT = {'A': 'A-核心成交客户', 'B': 'B-活跃商机', 'C': 'C-有回复的线索',
             'D': 'D-沉睡老客户', 'E': 'E-供应商与服务商', 'F': 'F-未跟进来信'}
GRADE_DESC = {
    'A': '365天内有联系，收≥10、发≥5，且有 PO 或强采购信号',
    'B': '730天内有联系，我方回复过，有采购或询盘信号',
    'C': '我方回复过，存在采购/询盘信号',
    'D': '曾深入往来（合计≥5封），但静默超过 730 天，建议再激活',
    'E': '我方回复过但无采购信号，多为供应商、货代、服务商、内部往来',
    'F': '我方从未回复，含较多营销推销，需人工筛选',
}

wb = openpyxl.Workbook()
HDR_FILL = PatternFill('solid', fgColor='1F4E79')
HDR_FONT = Font(bold=True, color='FFFFFF', size=10)
GRADE_FILL = {'A': PatternFill('solid', fgColor='C6EFCE'),
              'B': PatternFill('solid', fgColor='DDEBF7'),
              'C': PatternFill('solid', fgColor='FFF2CC'),
              'D': PatternFill('solid', fgColor='FCE4D6'),
              'E': PatternFill('solid', fgColor='EDEDED'),
              'F': PatternFill('solid', fgColor='F2F2F2')}


def style_sheet(ws, widths, ncol, freeze='A2'):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in range(1, ncol + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(vertical='center', horizontal='center', wrap_text=True)
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = freeze
    ws.auto_filter.ref = f'A1:{get_column_letter(ncol)}1'


# ---------------- Sheet1: Master 客户库（A-D 级，真正谈过话的） ----------------
ws = wb.active
ws.title = '01_Master客户库'
H1 = ['等级', '公司名(待确认)', '国家/地区(待确认)', '官网域名', '主联系人邮箱', '主联系人',
      '是否询盘', '收件数', '发件数', '往来合计', 'PO信号', '采购信号', '询盘信号',
      '首次接触', '最后接触', '静默天数', '活跃度得分', '联系人数', '代表主题', '对接我方邮箱']
ws.append(H1)
main = [r for r in rows if r['grade'] in 'ABCD']
for r in main:
    ws.append([
        GRADE_TXT[r['grade']], r['company'], r['country'] or '', r['website'], r['addr'],
        f"{r['firstname']} {r['lastname']}".strip(), r['inq_yn'],
        r['n_in'], r['n_out'], r['n_total'], r['n_po'], r['n_buy'], r['n_inq'],
        r['first'] or '', r['last'] or '', r['days_s'], r['score'], r['people_n'],
        r['subject'], r['accounts'],
    ])
style_sheet(ws, [16, 24, 16, 26, 32, 20, 8, 8, 8, 9, 8, 9, 9, 11, 11, 9, 10, 8, 46, 34], 20)
for i, r in enumerate(main, 2):
    if r['grade'] in GRADE_FILL:
        for c in (1, 2, 3):
            ws.cell(row=i, column=c).fill = GRADE_FILL[r['grade']]

# ---------------- Sheet2: 供应商与服务商（E 级） ----------------
ws2 = wb.create_sheet('02_供应商与服务商')
H2 = ['等级', '公司名(待确认)', '国家/地区(待确认)', '官网域名', '主联系人邮箱', '主联系人',
      '收件数', '发件数', '往来合计', '首次接触', '最后接触', '静默天数', '代表主题']
ws2.append(H2)
sel2 = [r for r in rows if r['grade'] == 'E']
for r in sel2:
    ws2.append([GRADE_TXT[r['grade']], r['company'], r['country'] or '', r['website'],
                r['addr'], f"{r['firstname']} {r['lastname']}".strip(),
                r['n_in'], r['n_out'], r['n_total'], r['first'] or '', r['last'] or '',
                r['days_s'], r['subject']])
style_sheet(ws2, [16, 24, 16, 26, 32, 20, 8, 8, 9, 11, 11, 9, 50], 13)

# ---------------- Sheet3: 未跟进来信线索（F 级） ----------------
ws3 = wb.create_sheet('03_未跟进来信线索')
H3 = ['公司名(待确认)', '国家/地区(待确认)', '官网域名', '主联系人邮箱', '来信数', '询盘信号',
      '采购信号', 'PO信号', '首次来信', '末次来信', '静默天数', '得分', '代表主题', '说明']
ws3.append(H3)
sel3 = [r for r in rows if r['grade'] == 'F']
for r in sel3:
    ws3.append([r['company'], r['country'] or '', r['website'], r['addr'], r['n_in'],
                r['n_inq'], r['n_buy'], r['n_po'], r['first'] or '', r['last'] or '',
                r['days_s'], r['score'], r['subject'], '我方从未回复，含营销推销，需人工筛选'])
style_sheet(ws3, [24, 16, 26, 32, 8, 9, 9, 8, 11, 11, 9, 8, 50, 34], 14)

# ---------------- Sheet4: 联系人明细 ----------------
ws4 = wb.create_sheet('04_联系人明细')
H4 = ['邮箱', '联系人姓名', '所属公司(域名/邮箱)', '公司等级', '国家/地区(待确认)', '来信数',
      '我方发信数', '首次往来', '末次往来', '静默天数', '代表主题']
ws4.append(H4)
psel = [p for p in prows
        if p['n_out'] >= 1 and (by_key.get(p['ckey'], {}).get('grade') in 'ABCD' or p['n_out'] >= 5)]
for p in psel:
    cr = by_key.get(p['ckey'], {})
    nm = (p['name'] or '').strip()
    fn = ln = ''
    if nm:
        parts = nm.split()
        fn = parts[0][:1].upper() + parts[0][1:] if parts else ''
        ln = ' '.join(parts[1:]) if len(parts) > 1 else ''
    if not fn and '@' in p['email']:
        fn = p['email'].split('@')[0]
    try:
        days = (TODAY - datetime.date.fromisoformat(p['last'])).days if p['last'] else ''
    except Exception:
        days = ''
    ws4.append([p['email'], f'{fn} {ln}'.strip(), p['ckey'],
                GRADE_TXT.get(cr.get('grade', ''), cr.get('grade', '') or '—'),
                cr.get('country', ''), p['n'] - p['n_out'], p['n_out'],
                p['first'] or '', p['last'] or '', days, p['subject']])
style_sheet(ws4, [34, 24, 30, 20, 16, 9, 11, 11, 11, 9, 50], 11)

# ---------------- Sheet5: 国别分布 ----------------
ws5 = wb.create_sheet('05_国别分布')
H5 = ['国家/地区', '公司数', '占比', '往来邮件封数', '户均往来封数', 'A级', 'B级', 'C级', 'D级']
ws5.append(H5)
cust = [r for r in rows if r['grade'] in 'ABCD']
cc = collections.Counter(r['country'] for r in cust if r['country'])
cv = collections.Counter()
cg = collections.defaultdict(collections.Counter)
for r in cust:
    if r['country']:
        cv[r['country']] += r['n_total']
        cg[r['country']][r['grade']] += 1
tot_c = sum(cc.values())
for k, v in sorted(cc.items(), key=lambda x: -cv[x[0]]):
    g = cg[k]
    ws5.append([k, v, f'{v / tot_c:.1%}' if tot_c else '', cv[k],
                round(cv[k] / v, 1) if v else 0, g['A'], g['B'], g['C'], g['D']])
n_blank = sum(1 for r in cust if not r['country'])
v_blank = sum(r['n_total'] for r in cust if not r['country'])
ws5.append(['(无法推断：.com/.net/.org 等)', n_blank,
            f'{n_blank / len(cust):.1%}' if cust else '', v_blank,
            round(v_blank / n_blank, 1) if n_blank else 0, '', '', '', ''])
style_sheet(ws5, [26, 10, 9, 14, 14, 8, 8, 8, 8], 9)

# ---------------- Sheet6: 说明与分级规则 ----------------
ws6 = wb.create_sheet('06_说明与分级规则')
cnt = collections.Counter(r['grade'] for r in rows)
replied = sum(1 for r in rows if r['n_out'] >= 1)
INFO = [
    ['项目', 'SMThelp / Southern Machinery Master 客户库（Foxmail 本地邮件库离线挖掘）'],
    ['生成日期', TODAY.isoformat()],
    ['数据源', '本机 Foxmail 7.2 数据目录 Storage/ 下 12 个邮箱账户的邮件头索引（Mails/Index + Indexes/recvdate.ind + senddate.ind）'],
    ['账户清单', 'info@smthelp.com, info@smthelp.net, info@smtnozzle.org, jasonwu68@qq.com, jasonwu@smthelp.com, jasonwu@smthelp.net, jasonwu@smtnozzle.org, jasonwuSMT@outlook.com, shaoyong@smthelp.com, smthelpmachine@gmail.com(1), support@smtnozzle.org, w25605@gmail.com'],
    ['', ''],
    ['解析规模', f'邮件头记录 {sum(1 for _ in open("/tmp/headers.jsonl")):,} 条；识别外部公司/独立邮箱 {len(rows):,} 个'],
    ['其中我方回复过', f'{replied:,} 个（这是「真正谈过话」的口径，比任何买来的名单都可靠）'],
    ['', ''],
    ['A-核心成交客户', f'{cnt["A"]} 家｜{GRADE_DESC["A"]}'],
    ['B-活跃商机', f'{cnt["B"]} 家｜{GRADE_DESC["B"]}'],
    ['C-有回复的线索', f'{cnt["C"]} 家｜{GRADE_DESC["C"]}'],
    ['D-沉睡老客户', f'{cnt["D"]} 家｜{GRADE_DESC["D"]}'],
    ['E-供应商与服务商', f'{cnt["E"]} 家｜{GRADE_DESC["E"]}'],
    ['F-未跟进来信', f'{cnt["F"]} 家｜{GRADE_DESC["F"]}'],
    ['', ''],
    ['活跃度得分', 'score = 我方发信×5 + 有效来信×1 + 采购信号×8 + PO信号×20 + 时效加权（90天内+30 / 365天内+15 / 730天内+5）'],
    ['「是否询盘」判定', '命中以下任一即标「是」：询盘信号≥1 或 采购信号≥1 或 PO信号≥1'],
    ['采购信号词', 'rfq / inquiry / quotation / price / cost / budget / proposal / order / machine / reflow / wave solder / pick and place / SMT / THT / insertion / conveyor / loader / unloader / stencil / feeder / nozzle / AOI / SPI / spare part / lead time 等'],
    ['PO/成交信号词', 'purchase order / PO# / order confirmation / proforma / contract / invoice / payment / deposit / TT / LC / shipment / new vendor 等'],
    ['', ''],
    ['已剔除噪声', '社交平台、招聘、EDM 与营销自动化、SEO 建站、SaaS 与运维通知、物流货代（DHL/UPS/FedEx 等）、元器件与 PCB/化工推销、行业媒体展会、支付与银行通知'],
    ['域名归并', '采购门户子域归并到主域（如 jabil.coupahost.com → jabil.com）；邮件系统子域归并（mail./service./noreply. 等）；免费邮箱按完整地址聚合，避免把 gmail.com 聚为一家'],
    ['', ''],
    ['重要限制 1', '邮件正文在 Foxmail 7.2 中为加密存储，本次只能解析邮件头索引，因此无法提取电话、地址、职位、机型参数、报价金额'],
    ['重要限制 2', '公司名、国别、官网均由邮箱域名推断，表中已标注「待确认」，正式使用前请人工核对'],
    ['重要限制 3', '国家/地区仅从国别顶级域推断（如 .tr→Turkey、.com.br→Brazil），.com/.net/.org 一律留空，不代表美国'],
    ['重要限制 4', '阿里巴巴等平台询盘的系统通知邮件无法还原买家真实邮箱，已在噪声中剔除，需另行从平台后台导出'],
    ['重要限制 5', '约 15% 记录无日期（多为草稿或仅索引项），其首末往来日期可能为空'],
    ['重要限制 6', 'E 级为供应商与服务商，非客户，单独成表以免污染客户库'],
    ['', ''],
    ['Sheet 说明', '01_Master客户库：A-D 级，我方真正回复过的客户，主表；02_供应商与服务商：E 级；03_未跟进来信线索：F 级，待人工筛选；04_联系人明细：人级邮箱清单；05_国别分布：按国家统计公司数与往来量；06：本说明'],
    ['建议用法', 'A 级做重点维护；B 级 30 天内主动触达；D 级（静默>730天）是最值得做再激活的一批——他们曾经买过或深入谈过；C 级按国别批量做 EDM 冷启动测试'],
]
for r in INFO:
    ws6.append(r)
ws6.column_dimensions['A'].width = 24
ws6.column_dimensions['B'].width = 132
for i in range(1, len(INFO) + 1):
    ws6.cell(row=i, column=1).font = Font(bold=True, size=10)
    ws6.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='top')
    ws6.row_dimensions[i].height = 30

wb.save(OUT)
print('saved', OUT)
print('01_Master客户库', len(main), '｜02_E级', len(sel2), '｜03_F级', len(sel3),
      '｜04_联系人', len(psel), '｜05_国别', len(cc) + 1)
