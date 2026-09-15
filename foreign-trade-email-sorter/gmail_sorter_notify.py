#!/usr/bin/env python3
"""
外贸邮件分类器 - 带飞书通知
高优先级询盘自动推送到飞书
"""

import os
import sys
import requests
from datetime import datetime

# 导入主分类器
from gmail_sorter import get_gmail_service, classify_email, get_email_body, get_priority

def send_feishu_notification(inquiry):
    """发送飞书通知"""
    
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    if not webhook_url:
        print("[WARN] 未设置 FEISHU_WEBHOOK_URL，跳过通知")
        return False
    
    # 构建通知消息
    subject = inquiry.get('subject', '无主题')[:50]
    sender = inquiry.get('info', {}).get('sender_email', '未知')
    priority = inquiry.get('priority', 'MEDIUM')
    body_preview = inquiry.get('body', '')[:100]
    
    # 飞书消息格式
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"""🔥 新的高优先级询盘！

📧 发件人：{sender}
📝 主题：{subject}
⚡ 优先级：{priority}

💬 摘要：
{body_preview}...

---
请及时跟进回复！"""
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[OK] 通知已发送：{sender}")
            return True
        else:
            print(f"[ERROR] 通知失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] 通知异常：{e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("外贸邮件分类器 - 带飞书通知")
    print("=" * 60)
    print()
    
    # 获取 Gmail 服务
    service = get_gmail_service()
    profile = service.users().getProfile(userId='me').execute()
    print(f"已连接：{profile['emailAddress']}\n")
    
    # 获取最近邮件
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=50
    ).execute()
    
    messages = results.get('messages', [])
    print(f"找到 {len(messages)} 封未读邮件，开始处理...\n")
    
    # 处理邮件
    high_priority_count = 0
    
    for msg_meta in messages:
        msg = service.users().messages().get(
            userId='me',
            id=msg_meta['id'],
            format='full'
        ).execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '无主题')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '未知')
        body = get_email_body(msg['payload'])
        
        # 分类
        category = classify_email(subject, body, sender)
        
        if category == 'inquiry':
            priority = get_priority(subject, body)
            
            inquiry = {
                'subject': subject,
                'sender': sender,
                'body': body,
                'info': {'sender_email': sender},
                'priority': priority
            }
            
            print(f"[{priority}] {subject[:50]}...")
            
            # 高优先级发送通知
            if priority == 'HIGH':
                send_feishu_notification(inquiry)
                high_priority_count += 1
    
    print(f"\n处理完成！发现 {high_priority_count} 封高优先级询盘")
    
    if high_priority_count > 0:
        print(f"已发送 {high_priority_count} 条飞书通知")


if __name__ == '__main__':
    main()
