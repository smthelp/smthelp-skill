#!/usr/bin/env python3
"""
Test Gmail Connection for Foreign Trade Email Sorter
"""

import os

print("=" * 60)
print("Foreign Trade Email Sorter - Gmail Connection Test")
print("=" * 60)
print()

# 检查 credentials.json
base_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(base_dir, 'credentials.json')
token_path = os.path.join(base_dir, 'token.json')

print("Step 1: Checking configuration files...")
print(f"  Base directory: {base_dir}")
print(f"  credentials.json: {'EXISTS' if os.path.exists(credentials_path) else 'NOT FOUND'}")
print(f"  token.json: {'EXISTS' if os.path.exists(token_path) else 'NOT FOUND'}")
print()

if not os.path.exists(credentials_path):
    print("ERROR: credentials.json not found!")
    print()
    print("Please follow these steps:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable Gmail API")
    print("4. Create OAuth 2.0 credentials (Desktop app)")
    print("5. Download credentials.json")
    print(f"6. Place it in: {base_dir}")
    print()
    print("For detailed instructions, see GMAIL_SETUP.md")
    exit(1)

# 检查依赖
print("Step 2: Checking Python dependencies...")
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    print("  Google API libraries: OK")
except ImportError as e:
    print(f"  ERROR: {e}")
    print()
    print("Please install dependencies:")
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

print()
print("Step 3: Connecting to Gmail...")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

try:
    creds = None
    
    # 加载已有token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        print("  Loading saved token...")
    
    # 授权流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("  Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("  Starting authorization flow...")
            print("  A browser window will open. Please login to your Gmail and grant permission.")
            print()
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 保存token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("  Token saved for future use.")
    
    # 连接Gmail
    print("  Building Gmail service...")
    service = build('gmail', 'v1', credentials=creds)
    
    # 测试获取用户信息
    print("  Testing connection...")
    profile = service.users().getProfile(userId='me').execute()
    email = profile.get('emailAddress', 'Unknown')
    
    print()
    print("=" * 60)
    print("SUCCESS! Connected to Gmail.")
    print(f"Email: {email}")
    print("=" * 60)
    print()
    
    # 获取未读邮件数量
    print("Step 4: Checking unread emails...")
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=1).execute()
    messages = results.get('messages', [])
    
    if messages:
        print(f"  Found unread emails. Ready to process!")
    else:
        print("  No unread emails found.")
    
    print()
    print("You can now run: python gmail_sorter.py")
    print()
    
except Exception as e:
    print(f"  ERROR: {e}")
    print()
    print("Troubleshooting:")
    print("1. Make sure credentials.json is valid")
    print("2. Check your internet connection")
    print("3. Ensure Gmail API is enabled in Google Cloud Console")
    exit(1)
