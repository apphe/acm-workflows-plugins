#!/usr/bin/env python3
"""
Simple Google Docs Downloader
Just download docs in different formats - that's it!
"""

import argparse
import json
import re
import sys
from pathlib import Path

def find_tokens():
    """Find tokens in common locations."""
    locations = [
        Path.home() / '.config' / 'google-tokens.json',
        Path.home() / '.google' / 'google-tokens.json'
    ]

    for path in locations:
        if path.exists():
            return path
    return None

def setup_auth():
    """Simple OAuth setup."""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("❌ Install: pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)

    # Find credentials
    creds_file = None
    for path in [Path.home() / '.config' / 'google-credentials.json',
                 Path.home() / '.google' / 'google-credentials.json']:
        if path.exists():
            creds_file = path
            break

    if not creds_file:
        print("❌ No google-credentials.json found in ~/.config/ or ~/.google/")
        sys.exit(1)

    # OAuth flow
    scopes = ['https://www.googleapis.com/auth/documents.readonly',
              'https://www.googleapis.com/auth/spreadsheets.readonly',
              'https://www.googleapis.com/auth/drive.readonly']

    flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), scopes)
    creds = flow.run_local_server(port=8080)

    # Save tokens
    token_file = Path.home() / '.config' / 'google-tokens.json'
    token_file.parent.mkdir(exist_ok=True)

    with open(token_file, 'w') as f:
        f.write(creds.to_json())

    print(f"✅ Setup complete! Tokens saved to {token_file}")

def download(url, format_type='markdown'):
    """Download document."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from google_auth_httplib2 import AuthorizedHttp
        import markdownify
        import httplib2
        import os
    except ImportError:
        print("❌ Install: pip install google-auth google-auth-oauthlib google-api-python-client markdownify")
        sys.exit(1)

    # Get document ID
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        print("❌ Invalid Google Docs/Sheets URL")
        sys.exit(1)

    doc_id = match.group(1)

    # Determine type
    is_sheet = 'spreadsheet' in url or 'sheets.google' in url

    # Load tokens
    token_file = find_tokens()
    if not token_file:
        print("❌ Run: python3 download.py --setup")
        sys.exit(1)

    # Load and refresh credentials
    scopes = ['https://www.googleapis.com/auth/documents.readonly',
              'https://www.googleapis.com/auth/spreadsheets.readonly',
              'https://www.googleapis.com/auth/drive.readonly']
    creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, 'w') as f:
                f.write(creds.to_json())
        else:
            print("❌ Run: python3 download.py --setup")
            sys.exit(1)

    # Format mappings
    formats = {
        'docs': {
            'markdown': 'text/html',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'txt': 'text/plain'
        },
        'sheets': {
            'csv': 'text/csv',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'pdf': 'application/pdf'
        }
    }

    doc_type = 'sheets' if is_sheet else 'docs'

    if format_type not in formats[doc_type]:
        print(f"❌ Format '{format_type}' not supported for {doc_type}")
        print(f"Available: {', '.join(formats[doc_type].keys())}")
        sys.exit(1)

    mime_type = formats[doc_type][format_type]

    # Configure HTTP client with proxy and timeout
    proxy_info = None
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    if https_proxy:
        # Parse proxy URL (e.g., "http://proxy.example.com:3128/")
        proxy_url = https_proxy.replace('http://', '').replace('https://', '').rstrip('/')
        if ':' in proxy_url:
            proxy_host, proxy_port = proxy_url.split(':', 1)
            proxy_port = int(proxy_port)
        else:
            proxy_host = proxy_url
            proxy_port = 3128

        try:
            import socks
            proxy_info = httplib2.ProxyInfo(
                proxy_type=socks.PROXY_TYPE_HTTP,
                proxy_host=proxy_host,
                proxy_port=proxy_port
            )
        except ImportError:
            print("⚠️  Warning: PySocks not installed, proxy may not work", file=sys.stderr)

    http = httplib2.Http(proxy_info=proxy_info, timeout=30)

    # Authorize the HTTP client with credentials
    authorized_http = AuthorizedHttp(creds, http=http)

    # Download
    try:
        if is_sheet:
            service = build('sheets', 'v4', http=authorized_http, cache_discovery=False)
            request = service.spreadsheets().export(spreadsheetId=doc_id, mimeType=mime_type)
        else:
            service = build('drive', 'v3', http=authorized_http, cache_discovery=False)
            request = service.files().export(fileId=doc_id, mimeType=mime_type)

        print(f"📥 Downloading document...", file=sys.stderr)
        content = request.execute(num_retries=3)

        # Convert to markdown if needed
        if format_type == 'markdown' and not is_sheet:
            content = markdownify.markdownify(content.decode('utf-8')).encode('utf-8')

        # Output to stdout for piping
        if isinstance(content, bytes):
            content_str = content.decode('utf-8')
        else:
            content_str = content

        # Print to stdout (for script capture)
        print(content_str)

        # Also save to file for reference
        ext = '.md' if format_type == 'markdown' else f'.{format_type}'
        filename = f"document_{doc_id}{ext}"

        if format_type in ['pdf', 'docx', 'xlsx']:
            with open(filename, 'wb') as f:
                f.write(content if isinstance(content, bytes) else content.encode('utf-8'))
        else:
            with open(filename, 'w') as f:
                f.write(content_str)

        print(f"✅ Downloaded: {filename}", file=sys.stderr)

    except Exception as e:
        print(f"❌ Download failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Simple Google Docs downloader")
    parser.add_argument('--setup', action='store_true', help='Setup authentication')
    parser.add_argument('url', nargs='?', help='Google Docs/Sheets URL')
    parser.add_argument('--format', default='markdown',
                       help='Format: markdown, docx, pdf, txt (docs) or csv, xlsx, pdf (sheets)')

    args = parser.parse_args()

    if args.setup:
        setup_auth()
    elif args.url:
        download(args.url, args.format)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()