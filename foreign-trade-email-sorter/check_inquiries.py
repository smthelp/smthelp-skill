#!/usr/bin/env python3
"""
检查询盘邮件 - 简化版
"""
import os
import base64
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
INQUIRY_KEYWORDS = ['interested in', 'quote', 'quotation', 'price', 'pricing', 
                    'inquiry', 'enquiry', 'rfq', 'request for quote', 
                    'order', 'purchase', 'buy', 'looking for', 'sample', 
                    'catalog', 'catalogue', 'brochure', 'moq', 
                    'lead time', 'delivery time', 'payment terms']

def get_service():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_dir, 'token.json')
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    return build('gmail', 'v1', credentials=creds)

def get_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                break
            elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                body = re.sub('<[^<]+?>', ' ', html)
                break
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    return body

def main():
    print("=" * 60)
    print("Checking for Inquiry Emails")
    print("=" * 60)
    
    service = get_service()
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=50).execute()
    messages = results.get('messages', [])
    
    print(f"Total unread: {len(messages)}")
    print()
    
    inquiry_count = 0
    
    for msg_meta in messages:
        msg = service.users().messages().get(userId='me', id=msg_meta['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        
        body = get_body(msg['payload'])
        text = (subject + " " + body).lower()
        
        # Check for inquiry keywords
        found_keywords = [k for k in INQUIRY_KEYWORDS if k in text]
        
        if found_keywords:
            inquiry_count += 1
            print("-" * 60)
            print(f"INQUIRY #{inquiry_count}")
            print(f"From: {sender.encode('ascii', 'ignore').decode('ascii')}")
            print(f"Subject: {subject.encode('ascii', 'ignore').decode('ascii')}")
            print(f"Keywords found: {found_keywords}")
            print()
            print("Content preview (first 500 chars):")
            print(body[:500].encode('ascii', 'ignore').decode('ascii'))
            print("-" * 60)
            print()
    
    print(f"Total inquiries found: {inquiry_count}")

if __name__ == '__main__':
    main()
