#!/usr/bin/env python3
import os, sys, base64, re
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
INQUIRY_KEYWORDS = ['interested in', 'quote', 'quotation', 'price', 'inquiry', 'order', 'purchase', 'buy', 'sample', 'catalog', 'moq', 'lead time']
MARKETING_KEYWORDS = ['unsubscribe', 'promotion', 'discount', 'newsletter', 'alibaba', 'special offer']
SPAM_KEYWORDS = ['winner', 'congratulations', 'lottery', 'verify your', 'make money']
SKIP_DOMAINS = ['no-reply@', 'noreply@', 'notification@']

def get_gmail_service():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_dir, 'token.json')
    credentials_path = os.path.join(base_dir, 'credentials.json')
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            print("正在授权...")
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w', encoding='utf-8') as f:
                f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_email_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                break
    return body[:2000]

def classify_email(subject, body, sender):
    text = (subject + " " + body).lower()
    for d in SKIP_DOMAINS:
        if d in sender.lower(): return 'other'
    for kw in SPAM_KEYWORDS:
        if kw in text: return 'spam'
    for kw in INQUIRY_KEYWORDS:
        if kw in text: return 'inquiry'
    for kw in MARKETING_KEYWORDS:
        if kw in text: return 'marketing'
    return 'other'

def get_priority(subject, body):
    text = (subject + " " + body).lower()
    if 'quote' in text or 'price' in text or 'order' in text: return 'HIGH'
    if 'catalog' in text or 'sample' in text: return 'MEDIUM'
    return 'LOW'

def generate_report(results, email_address):
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = os.path.join(os.path.dirname(__file__), 'reports', f'询盘报告-{today}.txt')
    inquiries = results['inquiries']
    high = [i for i in inquiries if i['priority'] == 'HIGH']
    medium = [i for i in inquiries if i['priority'] == 'MEDIUM']
    low = [i for i in inquiries if i['priority'] == 'LOW']
    lines = [
        f"📊 外贸询盘日报 - {today}", "=" * 60, "",
        "📈 今日统计",
        f"  总邮件：{len(inquiries) + len(results['marketing']) + len(results['spam']) + len(results['other'])} 封",
        f"  ✉️ 询盘：{len(inquiries)} 封 ⭐",
        f"    - 🔴 高：{len(high)}", f"    - 🟡 中：{len(medium)}", f"    - 🟢 低：{len(low)}",
        f"  📢 营销：{len(results['marketing'])}", f"  🗑️ 垃圾：{len(results['spam'])}",
        "", "=" * 60
    ]
    if high:
        lines.extend(["", "🔴 高优先级询盘", "=" * 60])
        for i, inq in enumerate(high, 1):
            lines.extend(["", f"【询盘 #{i}】", f"邮箱：{inq['info'].get('sender_email', 'N/A')}", f"主题：{inq['subject'] or '(无)'}", f"优先级：🔴 HIGH"])
    if medium:
        lines.extend(["", "🟡 中优先级询盘", "=" * 60])
        for i, inq in enumerate(medium, 1):
            lines.extend(["", f"【询盘 #{i}】", f"邮箱：{inq['info'].get('sender_email', 'N/A')}", f"主题：{inq['subject'] or '(无)'}"])
    lines.extend(["", "=" * 60, f"生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}", f"邮箱：{email_address}", "=" * 60])
    report_text = "\n".join(lines)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    return report_text, report_path

def main():
    print("=" * 60)
    print("外贸邮件分类器 - 中文版")
    print("=" * 60)
    service = get_gmail_service()
    profile = service.users().getProfile(userId='me').execute()
    print(f"已连接：{profile['emailAddress']}\n")
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y/%m/%d')
    results = service.users().messages().list(userId='me', q=f'after:{three_days_ago}', maxResults=50).execute()
    messages = results.get('messages', [])
    print(f"处理 {len(messages)} 封邮件...\n")
    inquiries, marketing, spam, other = [], [], [], []
    for msg_meta in messages:
        msg = service.users().messages().get(userId='me', id=msg_meta['id'], format='full').execute()
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '无主题')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '未知')
        body = get_email_body(msg['payload'])
        cat = classify_email(subject, body, sender)
        if cat == 'inquiry':
            inquiries.append({'subject': subject, 'sender': sender, 'body': body, 'info': {'sender_email': sender}, 'priority': get_priority(subject, body)})
        elif cat == 'marketing': marketing.append(1)
        elif cat == 'spam': spam.append(1)
        else: other.append(1)
    report, path = generate_report({'inquiries': inquiries, 'marketing': marketing, 'spam': spam, 'other': other}, profile['emailAddress'])
    print(f"报告已保存：{path}\n")
    print(report)
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
