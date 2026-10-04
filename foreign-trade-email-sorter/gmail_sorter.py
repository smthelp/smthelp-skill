#!/usr/bin/env python3
"""
Foreign Trade Email Sorter - Gmail Reader
读取Gmail邮件并分类，生成询盘报告
"""

import os
import sys
import base64
import re
import argparse
from datetime import datetime

# 尝试导入Google API
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("Warning: Google API libraries not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# 权限范围
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 分类关键词
INQUIRY_KEYWORDS = ['interested in', 'quote', 'quotation', 'price', 'pricing', 'inquiry', 'enquiry', 'rfq', 'request for quote', 'order', 'purchase', 'buy', 'looking for', 'sample', 'catalog', 'catalogue', 'brochure', 'moq', 'lead time', 'delivery time', 'payment terms', 'can you provide', 'do you sell', 'do you have', 'how much', 'what is the price', 'send me', 'need', 'want to buy', 'would like to']
MARKETING_KEYWORDS = ['unsubscribe', 'promotion', 'discount', 'sale', 'offer', 'newsletter', 'subscribe', 'update', 'notification', 'alibaba', 'made-in-china', 'globalsources', 'tradekey', 'exhibition', 'trade show', 'fair', 'conference', 'webinar', 'free shipping', 'limited time', 'special offer']
SPAM_KEYWORDS = ['winner', 'congratulations', 'lottery', 'prize', 'urgent: verify', 'account suspended', 'click here', '100% free', 'act now', 'limited time', 'order now', 'make money', 'earn extra', 'work from home']


def get_gmail_service():
    """获取Gmail API服务"""
    if not GOOGLE_API_AVAILABLE:
        return None
    
    creds = None
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_dir, 'token.json')
    credentials_path = os.path.join(base_dir, 'credentials.json')
    
    if not os.path.exists(credentials_path):
        print(f"Error: credentials.json not found")
        print(f"Please place credentials.json in: {base_dir}")
        return None
    
    # 加载token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # 授权流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            print("Opening browser for Gmail authorization...")
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("Authorization successful!")
    
    return build('gmail', 'v1', credentials=creds)


def get_email_body(payload):
    """提取邮件正文"""
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                break
            elif part['mimeType'] == 'text/html' and 'data' in part['body'] and not body:
                html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                body = re.sub('<[^<]+?>', ' ', html)
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    return body[:2000]  # 限制长度


# 自动排除的邮箱域名（系统通知、新闻订阅等）
AUTO_SKIP_DOMAINS = [
    'no-reply@', 'noreply@', 'notification@', 'notifications@',
    'system-mail@', 'status@', 'marketing@',
    'newsletter@', 'updates@', 'news@'
]

# 自动排除的发件人（完整邮箱或名称）
AUTO_SKIP_SENDERS = [
    'substack', 'medium', 'twitter', 'facebook', 'linkedin',
    'github', 'dribbble', 'artlist', 'discogs', 'about.me',
    'elementor', 'instagram', 'indie hackers', 'elephant journal',
    'openai', 'sensible medicine', 'michael easter', 'ivan hug',
    'chris ryan'
]

# 自动排除的主题关键词
AUTO_SKIP_SUBJECTS = [
    'security alert', '2-step verification', 'welcome to',
    'confirm your email', 'verify your', 'subscription confirmed',
    'unsubscribe', 'newsletter', 'weekly digest', 'monthly',
    'what\'s new', 'incident updated', 'elevated errors'
]

# 强询盘关键词（必须包含这些才算询盘）
STRONG_INQUIRY_KEYWORDS = [
    'quote', 'quotation', 'inquiry', 'enquiry', 'rfq', 
    'request for quote', 'interested in your product',
    'interested in your company', 'price list', 'catalogue',
    'can you quote', 'please quote', 'send me quote',
    'inquire about', 'learn more about your', 'your products',
    # 中文询盘关键词
    '询价', '报价', '咨询', '询盘', '价格', '产品',
    '有兴趣', '采购', '订购', '请问', '了解一下'
]

def should_skip_email(sender, subject):
    """检查是否应该跳过此邮件"""
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    # 检查域名
    for domain in AUTO_SKIP_DOMAINS:
        if domain in sender_lower:
            return True
    
    # 检查发件人名称
    for skip in AUTO_SKIP_SENDERS:
        if skip in sender_lower:
            return True
    
    # 检查主题关键词
    for skip_subj in AUTO_SKIP_SUBJECTS:
        if skip_subj in subject_lower:
            return True
    
    return False

def classify_email(subject, body, sender):
    """分类邮件"""
    text = (subject + " " + body).lower()
    
    # 首先检查是否自动跳过（系统通知、新闻订阅等）
    if should_skip_email(sender, subject):
        return 'other'
    
    # 检查垃圾邮件
    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            return 'spam'
    
    # 检查询盘 - 使用强关键词，避免误判
    strong_matches = 0
    for keyword in STRONG_INQUIRY_KEYWORDS:
        if keyword in text:
            strong_matches += 1
    
    # 需要至少1个强关键词才算询盘
    if strong_matches >= 1:
        return 'inquiry'
    
    # 检查营销邮件
    for keyword in MARKETING_KEYWORDS:
        if keyword in text:
            return 'marketing'
    
    return 'other'


def extract_inquiry_info(subject, body, sender):
    """提取询盘信息"""
    info = {
        'sender_name': '',
        'sender_email': '',
        'company': '',
        'product': '',
        'quantity': '',
        'target_price': '',
        'lead_time': '',
        'country': ''
    }
    
    # 提取邮箱
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
    if email_match:
        info['sender_email'] = email_match.group(0)
    
    # 提取姓名
    name_match = re.match(r'^([^<]+)', sender)
    if name_match:
        info['sender_name'] = name_match.group(1).strip()
    
    # 提取公司（从签名中）
    company_patterns = [
        r'(?:company|co\.?|ltd|inc|corp)[:\s]*([^\n]+)',
        r'\n([^\n]+(?:ltd|limited|co\.?|inc|corp)[^\n]*)'
    ]
    for pattern in company_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['company'] = match.group(1).strip()[:50]
            break
    
    # 提取数量
    qty_patterns = [
        r'(\d+[\d,]*)\s*(pcs|pieces|units|sets|cartons|containers?)',
        r'(?:quantity|qty|moq)[:\s]*(\d+[\d,]*)',
        r'(\d{3,})\s*(pcs|units)?'
    ]
    for pattern in qty_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['quantity'] = match.group(0)[:30]
            break
    
    # 提取目标价
    price_patterns = [
        r'(?:target price|price|budget)[:\s]*[$€£]?(\d+[\d,]*\.?\d*)',
        r'[$€£](\d+[\d,]*\.?\d*)\s*/?\s*(pc|piece|unit)',
        r'(\d+[\d,]*\.?\d*)\s*usd'
    ]
    for pattern in price_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['target_price'] = match.group(0)[:30]
            break
    
    # 提取交期
    lead_patterns = [
        r'(?:lead time|delivery|shipping time)[:\s]*(\d+)\s*(days?|weeks?)',
        r'(\d+)\s*(days?|weeks?)\s*(?:delivery|lead time)'
    ]
    for pattern in lead_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['lead_time'] = match.group(0)[:30]
            break
    
    return info


def get_priority(subject, body, info):
    """判断优先级 - 优化版"""
    text = (subject + " " + body).lower()
    
    # 高优先级：有具体数量和价格，或明确的紧急意向
    if info['quantity'] and info['target_price']:
        return 'HIGH'
    if info['quantity'] and ('order' in text or 'purchase' in text):
        return 'HIGH'
    if 'urgent' in text or 'asap' in text or 'immediately' in text:
        return 'HIGH'
    
    # 中优先级：有数量、目标价、交期要求，或明确的产品意向
    if info['quantity'] or info['target_price'] or info['lead_time']:
        return 'MEDIUM'
    if any(kw in text for kw in ['quote', 'quotation', 'rfq', 'price list']):
        return 'MEDIUM'
    
    # 低优先级：仅询问信息或初步了解
    return 'LOW'


def process_emails(service, max_results=50):
    """处理邮件"""
    print(f"Fetching up to {max_results} unread emails...")
    
    # 读取最近3天的邮件（包括已读和未读）
    from datetime import datetime, timedelta
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y/%m/%d')
    query = f'after:{three_days_ago}'
    
    results = service.users().messages().list(
        userId='me', 
        q=query, 
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        print("No unread emails found.")
        return []
    
    print(f"Found {len(messages)} unread emails. Processing...")
    
    inquiries = []
    marketing = []
    spam = []
    other = []
    
    for msg_meta in messages:
        msg = service.users().messages().get(userId='me', id=msg_meta['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        body = get_email_body(msg['payload'])
        category = classify_email(subject, body, sender)
        
        if category == 'inquiry':
            info = extract_inquiry_info(subject, body, sender)
            priority = get_priority(subject, body, info)
            inquiries.append({
                'id': msg_meta['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body[:500],
                'info': info,
                'priority': priority
            })
        elif category == 'marketing':
            marketing.append({'subject': subject, 'sender': sender})
        elif category == 'spam':
            spam.append({'subject': subject, 'sender': sender})
        else:
            other.append({'subject': subject, 'sender': sender})
    
    return {
        'inquiries': inquiries,
        'marketing': marketing,
        'spam': spam,
        'other': other
    }


def generate_report(results, email_address):
    """生成报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = os.path.join(os.path.dirname(__file__), 'reports', f'inquiry-report-{today}.txt')
    
    inquiries = results['inquiries']
    marketing = results['marketing']
    spam = results['spam']
    other = results['other']
    
    high = [i for i in inquiries if i['priority'] == 'HIGH']
    medium = [i for i in inquiries if i['priority'] == 'MEDIUM']
    low = [i for i in inquiries if i['priority'] == 'LOW']
    
    report_lines = [
        f"外贸询盘日报 - {today}",
        "=" * 60,
        "",
        "今日统计",
        f"  总邮件数: {len(inquiries) + len(marketing) + len(spam) + len(other)}",
        f"  询盘邮件: {len(inquiries)}",
        f"    - 高优先级: {len(high)}",
        f"    - 中优先级: {len(medium)}",
        f"    - 低优先级: {len(low)}",
        f"  营销邮件: {len(marketing)}",
        f"  垃圾邮件: {len(spam)}",
        f"  其他: {len(other)}",
        "",
        "=" * 60,
    ]
    
    if high:
        report_lines.extend(["", f"高优先级询盘 ({len(high)})", "=" * 60])
        for i, inquiry in enumerate(high, 1):
            info = inquiry['info']
            report_lines.extend([
                "",
                f"[INQUIRY #{i}]",
                "-" * 40,
                f"客户: {info['sender_name'] or 'N/A'} ({info['company'] or 'N/A'})",
                f"邮箱: {info['sender_email'] or 'N/A'}",
                f"主题: {inquiry['subject']}",
                f"产品: {info['product'] or 'N/A'}",
                f"数量: {info['quantity'] or 'N/A'}",
                f"目标价: {info['target_price'] or 'N/A'}",
                f"交期: {info['lead_time'] or 'N/A'}",
                f"优先级: {inquiry['priority']}",
                "",
                f"内容摘要: {inquiry['body'][:200]}..."
            ])
    
    if medium:
        report_lines.extend(["", f"中优先级询盘 ({len(medium)})", "=" * 60])
        for i, inquiry in enumerate(medium, 1):
            info = inquiry['info']
            report_lines.extend([
                "",
                f"[INQUIRY #{i}]",
                "-" * 40,
                f"邮箱: {info['sender_email'] or inquiry['sender']}",
                f"主题: {inquiry['subject']}",
                f"优先级: {inquiry['priority']}"
            ])
    
    if low:
        report_lines.extend(["", f"低优先级询盘 ({len(low)})", "=" * 60])
        for i, inquiry in enumerate(low, 1):
            info = inquiry['info']
            report_lines.extend([
                "",
                f"[INQUIRY #{i}]",
                "-" * 40,
                f"邮箱: {info['sender_email'] or inquiry['sender']}",
                f"主题: {inquiry['subject'] or '(No Subject)'}",
                f"优先级: {inquiry['priority']}"
            ])
    
    if 询盘邮件:
        report_lines.extend([
            "",
            "=" * 60,
            "待回复清单",
            "=" * 60,
            ""
        ])
        for i, inquiry in enumerate(inquiries, 1):
            info = inquiry['info']
            report_lines.append(f"{i}. {info['sender_email'] or inquiry['sender']} - {inquiry['subject'][:40] or 'No Subject'} ({inquiry['priority']})")
        
        # 添加回复建议
        report_lines.extend([
            "",
            "=" * 60,
            "REPLY TEMPLATES",
            "=" * 60,
            "",
            "【快速回复模板】",
            "",
            "For 高优先级:",
            "---",
            "Hi [Name],",
            "",
            "Thank you for your inquiry. We can definitely help with [product].",
            "Could you please provide more details about:",
            "- Specific requirements",
            "- Target quantity",
            "- Delivery timeline",
            "",
            "Best regards,",
            "[Your name]",
            "",
            "For MEDIUM/低优先级:",
            "---",
            "Hi [Name],",
            "",
            "Thanks for reaching out! I've attached our product catalog.",
            "Please let me know which products interest you.",
            "",
            "Best regards,",
            "[Your name]"
        ])
    
    report_lines.extend([
        "",
        "=" * 60,
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"来源邮箱: {email_address}",
        "=" * 60
    ])
    
    report_text = "\n".join(report_lines)
    
    # 保存报告
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_text, report_path


def main():
    parser = argparse.ArgumentParser(description='Foreign Trade Email Sorter')
    parser.add_argument('--max', type=int, default=50, help='Maximum emails to process')
    parser.add_argument('--no-report', action='store_true', help='Do not save report to file')
    args = parser.parse_args()
    
    print("=" * 60)
    print("Foreign Trade Email Sorter")
    print("=" * 60)
    print()
    
    # 获取服务
    service = get_gmail_service()
    if not service:
        print("Failed to connect to Gmail.")
        return 1
    
    # 获取邮箱地址
    profile = service.users().getProfile(userId='me').execute()
    email_address = profile.get('emailAddress', 'Unknown')
    print(f"Connected to: {email_address}")
    print()
    
    # 处理邮件
    results = process_emails(service, max_results=args.max)
    
    # 生成报告
    if not args.no_report:
        report_text, report_path = generate_report(results, email_address)
        print(f"\nReport saved to: {report_path}")
        print("\n" + "=" * 60)
        print("REPORT PREVIEW")
        print("=" * 60)
        print(report_text[:2000])
        if len(report_text) > 2000:
            print("\n... (truncated)")
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())