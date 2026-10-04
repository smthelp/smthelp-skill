"""
Gmail Reader for Foreign Trade Email Sorter - Full Version with Gmail API Support
"""

import os
import base64
import re
from datetime import datetime

# 尝试导入Google API库
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# 权限范围
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 关键词
INQUIRY_KEYWORDS = ['interested in', 'quote', 'quotation', 'price', 'pricing', 'inquiry', 'enquiry', 'rfq', 'request for quote', 'order', 'purchase', 'buy', 'looking for', 'sample', 'catalog', 'catalogue', 'brochure', 'moq', 'lead time', 'delivery time', 'payment terms', 'can you provide', 'do you sell', 'do you have', 'how much', 'what is the price', 'send me', 'need', 'want to buy', 'would like to']
MARKETING_KEYWORDS = ['unsubscribe', 'promotion', 'discount', 'sale', 'offer', 'newsletter', 'subscribe', 'update', 'notification', 'alibaba', 'made-in-china', 'globalsources', 'tradekey', 'exhibition', 'trade show', 'fair', 'conference', 'webinar', 'free shipping', 'limited time', 'special offer']
SPAM_KEYWORDS = ['winner', 'congratulations', 'lottery', 'prize', 'urgent: verify', 'account suspended', 'click here', '100% free', 'act now', 'limited time', 'order now', 'make money', 'earn extra', 'work from home']


def get_gmail_service():
    """获取Gmail API服务"""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), '..', 'token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
    
    if not os.path.exists(credentials_path):
        print(f"Error: credentials.json not found at {credentials_path}")
        print("Please follow GMAIL_SETUP.md to configure Gmail API")
        return None
    
    # 加载已有token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # 如果没有有效token，进行授权
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            print("Opening browser for Gmail authorization...")
            creds = flow.run_local_server(port=0)
        
        # 保存token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("Authorization successful! Token saved.")
    
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
    return body


def classify_email(subject, body):
    """分类邮件"""
    text = f"{subject} {body}".lower()
    for keyword in SPAM_KEYWORDS:
        if keyword in text:
            return 'SPAM'
    inquiry_score = sum(1 for keyword in INQUIRY_KEYWORDS if keyword in text)
    if inquiry_score >= 2:
        return 'INQUIRY'
    for keyword in MARKETING_KEYWORDS:
        if keyword in text:
            return 'MARKETING'
    return 'OTHER'


def extract_inquiry_info(subject, body, sender):
    """提取询盘信息"""
    info = {'sender_name': '', 'email': '', 'company': '', 'product': '', 'quantity': '', 'target_price': '', 'lead_time': '', 'priority': 'LOW', 'summary': ''}
    
    # 提取邮箱
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
    if email_match:
        info['email'] = email_match.group(0)
    
    # 提取姓名
    name_match = re.search(r'^([^<]+)<', sender)
    if name_match:
        info['sender_name'] = name_match.group(1).strip()
    else:
        info['sender_name'] = sender.split('@')[0] if '@' in sender else sender
    
    # 提取公司
    for pattern in [r'from\s+([A-Z][A-Za-z0-9\s&]+(?:Ltd|Inc|Corp|GmbH|SARL|LLC))', r'company[:\s]+([A-Z][A-Za-z0-9\s&]+(?:Ltd|Inc|Corp|GmbH|SARL|LLC))']:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            info['company'] = match.group(1).strip()
            break
    
    # 提取产品
    for pattern in [r'interested in\s+(.{3,50}?)(?:\.|,|;|\?|$)', r'looking for\s+(.{3,50}?)(?:\.|,|;|\?|$)', r'quote for\s+(.{3,50}?)(?:\.|,|;|\?|$)']:
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