#!/usr/bin/env python3
"""
调试版邮件分类器 - 显示详细内容
"""
import os
import sys
import base64
import re
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 询盘关键词
INQUIRY_KEYWORDS = ['interested in', 'quote', 'quotation', 'price', 'pricing', 
                    'inquiry', 'enquiry', 'rfq', 'request for quote', 
                    'order', 'purchase', 'buy', 'looking for', 'sample', 
                    'catalog', 'catalogue', 'brochure', 'moq', 
                    'lead time', 'delivery time', 'payment terms']

# 过滤列表
SKIP_DOMAINS = ['no-reply@google.com', 'noreply@google.com', 'notification@google.com']
SKIP_SENDERS = ['substack', 'medium', 'github', 'dribbble', 'artlist', 'discogs']

def get_gmail_service():
    """获取Gmail服务"""
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
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
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
    return body[:3000]

def should_skip(sender, subject):
    """检查是否应该跳过"""
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    for domain in SKIP_DOMAINS:
        if domain in sender_lower:
            return True
    
    for skip in SKIP_SENDERS:
        if skip in sender_lower:
            return True
    
    return False

def classify_with_details(subject, body, sender):
    """分类并返回详细信息"""
    text = (subject + " " + body).lower()
    
    # 检查是否跳过
    if should_skip(sender, subject):
        return 'skipped', []
    
    # 查找匹配的关键词
    matched_keywords = []
    for keyword in INQUIRY_KEYWORDS:
        if keyword in text:
            matched_keywords.append(keyword)
    
    if matched_keywords:
        return 'inquiry', matched_keywords
    
    return 'other', []

def main():
    print("=" * 80)
    print("邮件分类调试器 - 显示所有邮件详情")
    print("=" * 80)
    print()
    
    service = get_gmail_service()
    profile = service.users().getProfile(userId='me').execute()
    print(f"邮箱: {profile.get('emailAddress')}")
    print()
    
    # 获取未读邮件
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=50).execute()
    messages = results.get('messages', [])
    
    print(f"找到 {len(messages)} 封未读邮件")
    print("=" * 80)
    
    inquiry_count = 0
    
    for i, msg_meta in enumerate(messages, 1):
        msg = service.users().messages().get(userId='me', id=msg_meta['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        
        body = get_email_body(msg['payload'])
        category, keywords = classify_with_details(subject, body, sender)
        
        print(f"\n【邮件 #{i}】")
        print("-" * 80)
        print(f"发件人: {sender}")
        print(f"主题: {subject}")
        print(f"分类: {category.upper()}")
        
        if category == 'inquiry':
            inquiry_count += 1
            print(f"[OK] 匹配关键词: {', '.join(keywords)}")
            print(f"\n内容预览:")
            print(body[:800])
        elif category == 'skipped':
            print(f"[SKIP] 已过滤（系统通知/新闻订阅）")
        else:
            # 显示内容前200字符帮助调试
            print(f"内容片段: {body[:200]}...")
        
        print("-" * 80)
    
    print(f"\n{'=' * 80}")
    print(f"总结: 找到 {inquiry_count} 封询盘邮件")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()
