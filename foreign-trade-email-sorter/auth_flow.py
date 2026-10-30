#!/usr/bin/env python3
"""Gmail Authorization Flow"""
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
base_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(base_dir, 'credentials.json')
token_path = os.path.join(base_dir, 'token.json')

print("=== Gmail Authorization ===")
print("This will open a browser for you to authorize Gmail access.")
print()

creds = None

# Load existing token
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    print("Loading existing token...")

# If no valid token, start auth flow
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        print("Refreshing expired token...")
        creds.refresh(Request())
    else:
        print("Starting authorization flow...")
        print("A browser window will open. Please:")
        print("1. Login to your Gmail account")
        print("2. Click 'Allow' to grant permission")
        print()
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save token
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    print("Token saved!")

# Test connection
print("\nTesting Gmail connection...")
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
email = profile.get('emailAddress', 'Unknown')

print(f"\nSUCCESS! Connected to: {email}")
print(f"Total messages: {profile.get('messagesTotal', 'Unknown')}")
print(f"Threads: {profile.get('threadsTotal', 'Unknown')}")

# Check unread
results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
messages = results.get('messages', [])
print(f"Unread emails: {len(messages)}")

print("\nAuthorization complete!")
print("You can now run: python gmail_sorter.py")
