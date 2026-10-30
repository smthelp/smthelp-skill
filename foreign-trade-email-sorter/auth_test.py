#!/usr/bin/env python3
"""Quick test for Gmail authorization"""
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(base_dir, 'credentials.json')
token_path = os.path.join(base_dir, 'token.json')

print("=== Gmail Auth Test ===")
print(f"credentials.json exists: {os.path.exists(credentials_path)}")
print(f"token.json exists: {os.path.exists(token_path)}")

if not os.path.exists(credentials_path):
    print("ERROR: credentials.json not found!")
    sys.exit(1)

# Check credentials file content
import json
with open(credentials_path, 'r') as f:
    creds = json.load(f)
print(f"Client ID: {creds.get('installed', {}).get('client_id', 'N/A')[:20]}...")
print(f"Project ID: {creds.get('installed', {}).get('project_id', 'N/A')}")

print("\nDependencies check:")
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    print("✓ google-auth-oauthlib: OK")
except ImportError as e:
    print(f"✗ google-auth-oauthlib: {e}")
    sys.exit(1)

try:
    from googleapiclient.discovery import build
    print("✓ google-api-python-client: OK")
except ImportError as e:
    print(f"✗ google-api-python-client: {e}")
    sys.exit(1)

print("\nReady to authorize!")
print("Run: python auth_flow.py")
