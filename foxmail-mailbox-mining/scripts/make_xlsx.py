# -*- coding: utf-8 -*-
"""生成客户通讯录 Excel（Mautic 导入格式）"""
import json, datetime, collections, re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

import os, sys
TODAY = datetime.date.today()
OUTDIR = os.environ.get('FOXMAIL_OUTDIR', '/tmp')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.expanduser('~/Downloads'),
    f'客户通讯录_Foxmail挖掘_{TODAY.strftime("%Y%m%d")}.xlsx')

rows = json.load(open(os.path.join(OUTDIR, 'contacts_rows.json')))
prows = json.load(open(os.path.join(OUTDIR, 'people_rows.json')))

MAUTIC_COLS = ['id', 'points', 'last_active', 'title', 'firstname', 'lastname', 'company',
               'position', 'email', 'phone', 'mobile', 'address1', 'address2', 'city', 'state',
               'zipcode', 'timezone', 'country', 'fax', 'preferred_locale', 'attribution_date',
               'attribution', 'website', 'subject', 'discription', 'facebook', 'foursquare',
               'googleplus', 'instagram', 'linkedin', 'skype', 'twitter']

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

by_key = {r['key']: r for r in rows}
GRADE_TXT = {'A': 'A-核心成交客户', 'B': 'B-活跃商机', 'C': 'C-有回复的线索',
             'D': 'D-沉睡老客户', 'E': 'E-有往来(供应商/物流等)', 'F': 'F-未跟进来信'}

wb = openpyxl.Workbook()
HDR_FILL = PatternFill('solid', fgColor='1F4E79')
HDR_FONT = Font(bold=True, color='FFFFFF', size=10)
GRADE_FILL = {'A': PatternFill('solid', fgColor='C6EFCE'),
              'B': PatternFill('solid', fgColor='DDEBF7'),
              'C': PatternFill('solid', fgColor='FFF2CC'),
              'D': PatternFill('solid', fgColor='FCE4D6')}


def style_sheet(ws, widths, ncol, freeze='A2'):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in range(1, ncol + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(vertical='center', horizontal='center', wrap_text=True)
    ws.row_dimensions[1].height = 28
    ws.freeze_panes = freeze
    ws.auto_filter.ref = f'A1:{get_column_letter(ncol)}1'


# ---------------- Sheet1: Mautic 导入主表（A-D 级） ----------------
ws = wb.active
ws.title = '01_Mautic导入_客户通讯录'
ws.append(MAUTIC_COLS)
main = [r for r in rows if r['grade'] in 'ABCD']
for r in main:
    disc = (f"分级 {r['grade']}｜收 {r['n_in']} / 发 {r['n_out']}｜"
            f"首次 {r['first'] or '—'}｜末次 {r['last'] or '—'}｜"
            f"静默 {r['days'] if r['days'] < 99999 else '—'} 天｜"
            f"PO信号 {r['n_po']}｜采购信号 {r['n_buy']}｜询盘信号 {r['n_inq']}｜"
            f"对接邮箱 {r['accounts']}｜"
            f"公司名与国别由邮箱域名推断，待确认")
    ws.append([
        '', r['score'], r['last'] or '', '', r['firstname'], r['lastname'],
        r['company'], '', r['addr'], '', '', '', '', '', '', '', '',
        r['country'], '', '', r['first'] or '', 'Foxmail 邮件往来', r['website'],
        r['subject'], disc, '', '', '', '', '', '', '',
    ])
style_sheet(ws, [6, 8, 12, 8, 14, 16, 24, 10, 30, 10, 12, 10, 10, 10, 10, 9, 9, 16, 10, 12,
                 14, 18, 26, 46, 60, 10, 10, 10, 10, 10, 10, 10], 32)
for i, r in enumerate(main, 2):
    if r['grade'] in GRADE_FILL:
        ws.cell(row=i, column=1).fill = GRADE_FILL[r['grade']]
        ws.cell(row=i, column=7).fill = GRADE_FILL[r['grade']]

# ---------------- Sheet2: 往来统计与分级（A-E） ----------------
ws2 = wb.create_sheet('02_往来统计与分级')
H2 = ['等级', '公司(域名/邮箱)', '推断公司名(待确认)', '国家/地区(待确认)', '官网域名',
      '主联系人邮箱', '联系人姓名', '收件数', '发件数', '往来合计', 'PO信号', '采购信号',
      '询盘信号', '退信数', '首次往来', '末次往来', '静默天数', '活跃度得分',
      '往来邮箱账户', '联系人数', '主要联系人', '代表主题']
ws2.append(H2)
stat = [r for r in rows if r['grade'] in 'ABCDE']
for r in stat:
    ws2.append([
        GRADE_TXT[r['grade']], r['key'], r['company'], r['country'] or '', r['website'],
        r['addr'], f"{r['firstname']} {r['lastname']}".strip(),
        r['n_in'], r['n_out'], r['n_total'], r['n_po'], r['n_buy'], r['n_inq'], r['n_bounce'],
        r['first'] or '', r['last'] or '', r['days'] if r['days'] < 99999 else '',
        r['score'], r['accounts'], r['people_n'], r['top_people'], r['subject'],
    ])
style_sheet(ws2, [16, 34, 24, 16, 26, 32, 20, 8, 8, 9, 8, 9, 9, 7, 11, 11, 9, 10, 34, 8, 46, 46], 22)
for i, r in enumerate(stat, 2):
    g = r['grade']
    if g in GRADE_FILL:
        for c in (1, 2, 3):
            ws2.cell(row=i, column=c).fill = GRADE_FILL[g]

# ---------------- Sheet3: 联系人明细 ----------------
ws3 = wb.create_sheet('03_联系人明细')
H3 = ['邮箱', '联系人姓名', '所属公司(域名)', '公司等级', '国家/地区(待确认)', '来信数',
      '我方发信数', '首次往来', '末次往来', '静默天数', '代表主题']
ws3.append(H3)
psel = [p for p in prows
        if p['n_out'] >= 1 and (by_key.get(p['ckey'], {}).get('grade') in 'ABCD' or p['n_out'] >= 5)]
psel = psel or [p for p in prows if p['n_out'] >= 1]
for p in psel:
    cr = by_key.get(p['ckey'], {})
    fn, ln = '', ''
    nm = (p['name'] or '').strip()
    if nm:
        parts = nm.split()
        fn = parts[0][:1].upper() + parts[0][1:] if parts else ''
        ln = ' '.join(parts[1:]) if len(parts) > 1 else ''
    if not fn and '@' in p['email']:
        fn = p['email'].split('@')[0]
    d = p['ckey'] if '@' not in p['ckey'] else p['ckey'].rsplit('@', 1)[1]
    try:
        days = (TODAY - datetime.date.fromisoformat(p['last'])).days if p['last'] else ''
    except Exception:
        days = ''
    ws3.append([p['email'], f'{fn} {ln}'.strip(), p['ckey'],
                GRADE_TXT.get(cr.get('grade', ''), cr.get('grade', '') or '—'),
                cr.get('country', ''), p['n'] - p['n_out'], p['n_out'],
                p['first'] or '', p['last'] or '', days, p['subject']])
style_sheet(ws3, [34, 24, 30, 20, 16, 9, 11, 11, 11, 9, 50], 11)

# ---------------- Sheet4: 未跟进来信线索 ----------------
ws4 = wb.create_sheet('04_未跟进来信线索')
H4 = ['公司(域名/邮箱)', '推断公司名(待确认)', '国家/地区', '来信数', '询盘信号',
      '采购信号', 'PO信号', '首次来信', '末次来信', '静默天数', '得分', '代表主题', '说明']
ws4.append(H4)
for r in [x for x in rows if x['grade'] == 'F']:
    ws4.append([r['key'], r['company'], r['country'] or '', r['n_in'], r['n_inq'], r['n_buy'],
                r['n_po'], r['first'] or '', r['last'] or '',
                r['days'] if r['days'] < 99999 else '', r['score'], r['subject'],
                '我方从未回复，含较多营销推销，需人工筛选'])
style_sheet(ws4, [34, 24, 16, 9, 9, 9, 8, 11, 11, 9, 8, 50, 34], 13)

# ---------------- Sheet5: 说明与规则 ----------------
ws5 = wb.create_sheet('05_说明与分级规则')
cnt = collections.Counter(r['grade'] for r in rows)
INFO = [
    ['项目', 'SMThelp / Southern Machinery 客户通讯录（Foxmail 本地邮件库离线挖掘）'],
    ['生成日期', TODAY.isoformat()],
    ['数据来源', '本机 Foxmail 7.2 数据目录 Storage/ 下 12 个邮箱账户的邮件头索引（Mails/Index + Indexes/recvdate.ind + senddate.ind）'],
    ['账户清单', 'info@smthelp.com, info@smthelp.net, info@smtnozzle.org, jasonwu68@qq.com, jasonwu@smthelp.com, jasonwu@smthelp.net, jasonwu@smtnozzle.org, jasonwuSMT@outlook.com, shaoyong@smthelp.com, smthelpmachine@gmail.com(1), support@smtnozzle.org, w25605@gmail.com'],
    ['', ''],
    ['解析规模', f'邮件头记录 609,627 条；有效外部往来 335,588 条；识别外部公司/独立邮箱 {len(rows):,} 个'],
    ['A-核心成交客户', f'{cnt["A"]} 家｜365天内有联系，收≥10、发≥5，且有 PO 或强采购信号'],
    ['B-活跃商机', f'{cnt["B"]} 家｜730天内有联系，我方回复过，有采购或询盘信号'],
    ['C-有回复的线索', f'{cnt["C"]} 家｜我方回复过，存在采购/询盘信号'],
    ['D-沉睡老客户', f'{cnt["D"]} 家｜曾深入往来（合计≥5封），但静默超过 730 天，建议再激活'],
    ['E-有往来(非客户)', f'{cnt["E"]} 家｜我方回复过但无采购信号，多为供应商、货代、服务商、内部'],
    ['F-未跟进来信', f'{cnt["F"]} 家｜我方从未回复，含大量营销推销邮件，需人工筛选'],
    ['', ''],
    ['活跃度得分', 'score = 我方发信×5 + 有效来信×1 + 采购信号×8 + PO信号×20 + 时效加权(90天内+30 / 365天内+15 / 730天内+5)'],
    ['采购信号词', 'rfq / inquiry / quotation / price / cost / budget / proposal / order / machine / reflow / wave solder / pick and place / SMT / THT / insertion / conveyor / loader / unloader / stencil / feeder / nozzle / AOI / SPI / spare part / lead time 等'],
    ['PO/成交信号词', 'purchase order / PO# / order confirmation / proforma / contract / invoice / payment / deposit / TT / LC / shipment / new vendor 等'],
    ['', ''],
    ['已剔除噪声', '社交平台(Facebook/LinkedIn/Xing/Twitter 等)、招聘、EDM 与营销自动化(Mailchimp/HubSpot/SendGrid 等)、SEO 建站、SaaS 与运维通知、物流货代(DHL/UPS/FedEx/货代通知)、元器件与 PCB/化工推销、行业媒体展会、支付与银行通知，共约 45 万条'],
    ['域名归并', '采购门户子域归并到主域（如 jabil.coupahost.com → jabil.com）；邮件系统子域归并（mail./service./noreply. 等）'],
    ['', ''],
    ['重要限制 1', '邮件正文在 Foxmail 7.2 中为加密存储，本次只能解析邮件头索引，因此无法提取电话、地址、职位、机型参数、报价金额'],
    ['重要限制 2', '公司名、国别、官网均由邮箱域名推断，表中已标注「待确认」，导入 CRM 前请人工核对'],
    ['重要限制 3', '国家/地区仅从国别顶级域推断（如 .tr→Turkey、.com.br→Brazil），.com/.net/.org 一律留空，不代表美国'],
    ['重要限制 4', '阿里巴巴等平台询盘的系统通知邮件无法还原买家真实邮箱，已在噪声中剔除，需另行从平台后台导出'],
    ['重要限制 5', '约 15% 记录无日期（多为草稿或仅索引项），其首末往来日期可能为空'],
    ['', ''],
    ['Sheet 说明', '01_Mautic导入_客户通讯录：严格按 Mautic contacts 模板 32 列字段输出，可直接导入；02_往来统计与分级：含往来量、静默天数、得分等明细；03_联系人明细：人级邮箱清单；04_未跟进来信线索：待人工筛选的单向来信；05：本说明'],
]
for r in INFO:
    ws5.append(r)
ws5.column_dimensions['A'].width = 22
ws5.column_dimensions['B'].width = 130
ws5['A1'].font = Font(bold=True)
for i in range(1, len(INFO) + 1):
    ws5.cell(row=i, column=1).font = Font(bold=True, size=10)
    ws5.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='top')
    ws5.row_dimensions[i].height = 30

wb.save(OUT)
print('saved', OUT)
print('sheet1 rows', len(main), 'sheet2 rows', len(stat), 'sheet3 rows', len(psel))
