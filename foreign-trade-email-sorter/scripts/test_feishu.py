#!/usr/bin/env python3
"""
飞书通知测试脚本
测试 Webhook 是否正常工作
"""

import os
import requests
from datetime import datetime

def test_feishu_notification():
    """发送测试消息到飞书"""
    
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ 错误：未设置 FEISHU_WEBHOOK_URL 环境变量")
        print("\n请设置环境变量：")
        print("  Windows: $env:FEISHU_WEBHOOK_URL='https://...'")
        print("  Linux/Mac: export FEISHU_WEBHOOK_URL='https://...'")
        return False
    
    # 测试消息内容
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"🔔 询盘通知测试\n\n这是一条测试消息，确认飞书集成正常工作。\n\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('StatusCode') == 0 or result.get('code') == 0:
                print("✅ 飞书通知测试成功！")
                print("消息已发送到飞书群")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
            print(f"响应内容：{response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误：{e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("飞书通知测试")
    print("=" * 50)
    print()
    test_feishu_notification()
