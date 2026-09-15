"""
Gmail Reader for Foreign Trade Email Sorter
读取Gmail邮件并分类为：Inquiry / Marketing / Spam
"""

import os
import base64
import re
from datetime import datetime

# 询盘关键词
INQUIRY_KEYWORDS = [
    'interested in', 'quote', 'quotation', 'price', 'pricing',
    'inquiry', 'enquiry', 'rfq', 'request for quote',
    'order', 'purchase', 'buy', 'looking for',
    'sample', 'catalog', 'catalogue', 'brochure',
    'moq', 'lead time', 'delivery time', 'payment terms',
    'can you provide', 'do you sell', 'do you have',
    'how much', 'what is the price', 'send me',
    'need', 'want to buy', 'would like to'
]

# 营销邮件关键词
MARKETING_KEYWORDS = [
    'unsubscribe', 'promotion', 'discount', 'sale', 'offer',
    'newsletter', 'subscribe', 'update', 'notification',
    'alibaba', 'made-in-china', 'globalsources', 'tradekey',
    'exhibition', 'trade show', 'fair', 'conference',
    'webinar', 'free shipping', 'limited time', 'special offer'
]

# 垃圾邮件关键词
SPAM_KEYWORDS = [
    'winner', 'congratulations', 'lottery', 'prize',
    'urgent: verify', 'account suspended', 'click here',
    '100% free', 'act now', 'limited time', 'order now',
    'make money', 'earn extra', 'work from home'
]


def classify_email(subject, body):
    """分类邮件"""
    text = f"{subject} {body}".lower()
    
    # 检查垃圾邮件
    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            return 'SPAM'
    
    # 检查询盘
    inquiry_score = sum(1 for keyword in INQUIRY_KEYWORDS if keyword in text)
    if inquiry_score >= 2:
        return 'INQUIRY'
    
    # 检查营销邮件
    for keyword in MARKETING_KEYWORDS:
        if keyword in text:
            return 'MARKETING'
    
    # 默认分类
    return 'OTHER'


def extract_inquiry_info(subject, body, sender):
    """提取询盘信息"""
    info = {
        'sender_name': '',
        'email': '',
        'company': '',
        'product': '',
        'quantity': '',
        'target_price': '',
        'lead_time': '',
        'priority': 'LOW',
        'summary': ''
    }
    
    # 提取邮箱
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
    if email_match:
        info['email'] = email_match.group(0)
    
    # 提取发件人姓名
    name_match = re.search(r'^([^<]+)<', sender)
    if name_match:
        info['sender_name'] = name_match.group(1).strip()
    else:
        info['sender_name'] = sender.split('@')[0]
    
    # 提取公司名
    company_patterns = [
        r'from\s+([A-Z][A-Za-z0-9\s&]+(?:Ltd|Inc|Corp|GmbH|SARL|LLC|BV|AB|AS|Pte))',
        r'company[:\s]+([A-Z][A-Za-z0-9\s&]+(?:Ltd|Inc|Corp|GmbH|SARL|LLC))',
    ]
    for pattern in company_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['company'] = match.group(1).strip()
            break
    
    # 提取产品
    product_patterns = [
        r'interested in\s+(.{3,50}?)(?:\.|,|;|\?|$)',
        r'looking for\s+(.{3,50}?)(?:\.|,|;|\?|$)',
        r'quote for\s+(.{3,50}?)(?:\.|,|;|\?|$)',
    ]
    for pattern in product_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['product'] = match.group(1).strip()
            break
    
    if not info['product']:
        info['product'] = subject[:50]
    
    # 提取数量
    qty_match = re.search(r'(\d+,?\d*)\s*(pcs|pieces|units|sets|cartons|boxes)', body, re.IGNORECASE)
    if qty_match:
        info['quantity'] = f"{qty_match.group(1)} {qty_match.group(2)}"
    
    # 提取目标价
    price_match = re.search(r'(?:price|budget).*?\$?\s*(\d+\.?\d*)', body, re.IGNORECASE)
    if price_match:
        info['target_price'] = f"${price_match.group(1)}"
    
    # 提取交期
    lead_match = re.search(r'(\d+)\s*days|lead time', body, re.IGNORECASE)
    if lead_match:
        info['lead_time'] = f"{lead_match.group(1)} days"
    
    # 生成摘要
    sentences = [s.strip() for s in re.split(r'[.!?]', body) if len(s.strip()) > 20]
    if sentences:
        summary = '. '.join(sentences[:2])
        info['summary'] = summary[:150] + '...' if len(summary) > 150 else summary
    
    # 判断优先级
    score = 0
    if info['quantity']: score += 3
    if info['target_price']: score += 3
    if info['lead_time']: score += 2
    if re.search(r'order|purchase|buy', body, re.IGNORECASE): score += 2
    if info['company']: score += 1
    
    if score >= 6:
        info['priority'] = 'HIGH'
    elif score >= 3:
        info['priority'] = 'MEDIUM'
    else:
        info['priority'] = 'LOW'
    
    return info


def generate_report(inquiries, marketing_count, spam_count, total_count):
    """生成报告"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_time = datetime.now().strftime('%H:%M')
    
    # 按优先级分组
    high = [i for i in inquiries if i['priority'] == 'HIGH']
    medium = [i for i in inquiries if i['priority'] == 'MEDIUM']
    low = [i for i in inquiries if i['priority'] == 'LOW']
    
    lines = []
    lines.append(f"Foreign Trade Inquiry Report - {report_date}")
    lines.append("=" * 50)
    lines.append("")
    lines.append("DAILY STATISTICS")
    lines.append(f"- Total Emails: {total_count}")
    lines.append(f"- Inquiries: {len(inquiries)}")
    lines.append(f"- Marketing: {marketing_count}")
    lines.append(f"- Spam/Junk: {spam_count}")
    lines.append("")
    lines.append("=" * 50)
    
    # 高优先级
    if high:
        lines.append("")
        lines.append(f"HIGH PRIORITY INQUIRIES ({len(high)})")
        lines.append("=" * 50)
        lines.append("")
        
        for i, inq in enumerate(high, 1):
            lines.append(f"[INQUIRY #{i}]")
            lines.append("-" * 40)
            lines.append(f"Customer: {inq['sender_name']} ({inq['company']})")
            lines.append(f"Email: {inq['email']}")
            lines.append(f"Product: {inq['product']}")
            lines.append(f"Quantity: {inq['quantity']}")
            lines.append(f"Target Price: {inq['target_price']}")
            lines.append(f"Lead Time: {inq['lead_time']}")
            lines.append(f"Priority: HIGH")
            lines.append(f"Summary: {inq['summary']}")
            lines.append("")
    
    # 中优先级
    if medium:
        lines.append("")
        lines.append(f"MEDIUM PRIORITY INQUIRIES ({len(medium)})")
        lines.append("=" * 50)
        lines.append("")
        
        for i, inq in enumerate(medium, 1):
            lines.append(f"[INQUIRY #{i}]")
            lines.append(f"Customer: {inq['sender_name']}")
            lines.append(f"Email: {inq['email']}")
            lines.append(f"Product: {inq['product']}")
            lines.append(f"Priority: MEDIUM")
            lines.append(f"Summary: {inq['summary'][:100]}...")
            lines.append("")
    
    # 低优先级
    if low:
        lines.append("")
        lines.append(f"LOW PRIORITY INQUIRIES ({len(low)})")
        lines.append("=" * 50)
        lines.append("")
        
        for i, inq in enumerate(low, 1):
            lines.append(f"[INQUIRY #{i}] {inq['email']} - {inq['product']} (LOW)")
    
    # 待回复清单
    lines.append("")
    lines.append("=" * 50)
    lines.append("REPLY CHECKLIST")
    lines.append("=" * 50)
    
    for i, inq in enumerate(inquiries, 1):
        lines.append(f"{i}. {inq['email']} - {inq['product']} ({inq['priority']})")
    
    lines.append("")
    lines.append("=" * 50)
    lines.append(f"Generated: {report_date} {report_time}")
    lines.append("Source: Gmail")
    
    return "\n".join(lines)


def test_with_sample_data():
    """使用示例数据测试"""
    print("=" * 50)
    print("Foreign Trade Email Sorter - Test Mode")
    print("=" * 50)
    print()
    
    # 示例邮件数据
    test_emails = [
        {
            'subject': 'Quote for LED Strip Lights - 5000 pcs',
            'body': 'Hello, I am interested in your LED Strip Lights - 5050 SMD. We need 5000 pcs with target price .50/pc. Lead time 30 days. Please send quotation. From ABC Trading Ltd.',
            'sender': 'john@abctrading.com'
        },
        {
            'subject': 'Bluetooth Speakers Inquiry',
            'body': 'Hi, looking for Bluetooth Speakers. Need 1000 units. What is your MOQ and price? We are Euro Import SARL from Spain.',
            'sender': 'maria@euroimport.es'
        },
        {
            'subject': 'Newsletter: Spring Sale 2026',
            'body': 'Unsubscribe | Spring Sale up to 50% off! Limited time offer.',
            'sender': 'marketing@somevendor.com'
        },
        {
            'subject': 'Congratulations! You won!',
            'body': 'Congratulations! You are a winner! Click here to claim your prize!',
            'sender': 'spam@lottery.com'
        }
    ]
    
    inquiries = []
    marketing_count = 0
    spam_count = 0
    
    for email in test_emails:
        category = classify_email(email['subject'], email['body'])
        print(f"Email: {email['subject'][:40]}... -> {category}")
        
        if category == 'INQUIRY':
            info = extract_inquiry_info(email['subject'], email['body'], email['sender'])
            inquiries.append(info)
        elif category == 'MARKETING':
            marketing_count += 1
        elif category == 'SPAM':
            spam_count += 1
    
    # 生成报告
    print("\nGenerating report...")
    report = generate_report(inquiries, marketing_count, spam_count, len(test_emails))
    
    # 保存报告
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, f"inquiry-report-{datetime.now().strftime('%Y-%m-%d')}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[OK] Report saved: {report_file}")
    print("\n" + "=" * 50)
    print("REPORT CONTENT:")
    print("=" * 50)
    print(report)


if __name__ == '__main__':
    test_with_sample_data()
