#!/usr/bin/env python3
"""
检查所有邮件（包括已读）
"""
import os
import base64
import re
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
    print("=" * 80)
    print("检查最近3天的所有邮件")
    print("=" * 80)
    
    service = get_service()
    
    # 查询最近3天
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y/%m/%d')
    query = f'after:{three_days_ago}'
    
    print(f"查询条件: {query}")
    print()
    
    results = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = results.get('messages', [])
    
    print(f"找到 {len(messages)} 封邮件")
    print("=" * 80)
    
    for i, msg_meta in enumerate(messages, 1):
        msg = service.users().messages().get(userId='me', id=msg_meta['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # 检查是否已读
        label_ids = msg.get('labelIds', [])
        is_unread = 'UNREAD' in label_ids
        
        body = get_body(msg['payload'])
        
        print(f"\n【邮件 #{i}】 {'[未读]' if is_unread else '[已读]'}")
        print("-" * 80)
        print(f"发件人: {sender}")
        print(f"主题: {subject}")
        print(f"日期: {date}")
        print(f"内容预览: {body[:300]}...")
        print("-" * 80)
    
    print(f"\n总计: {len(messages)} 封邮件")

if __name__ == '__main__':
    main()
