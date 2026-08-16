#!/usr/bin/env python3
"""
email_extractor.py - Extract email addresses from the HTML content of a website

Example:
  python3 scripts/osint/email_extractor.py --url "http://example.com"
"""
from __future__ import annotations
import argparse
import re
import sys
import urllib.request

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


def fetch(url: str, timeout: int = 8) -> tuple[int, str]:
    try:
        import requests
        with requests.get(url, timeout=timeout) as r:
            return r.status_code, r.text
    except ImportError:
        pass
    except Exception as e:
        return 0, str(e)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(errors='replace')
    except Exception as e:
        return 0, str(e)


def extract_emails(html: str) -> list[str]:
    seen: set[str] = set()
    for match in EMAIL_RE.findall(html):
        local, _, domain = match.partition('@')
        if local.startswith('.') or local.endswith('.') or domain.startswith('.') or '..' in local:
            continue
        seen.add(match.lower())
    return sorted(seen)


def main() -> int:
    p = argparse.ArgumentParser(description='Extract email addresses from a webpage')
    p.add_argument('--url', required=True, help='Target URL to scan for emails')
    p.add_argument('--timeout', type=int, default=8, help='Request timeout in seconds')
    args = p.parse_args()

    code, body = fetch(args.url, args.timeout)
    if code == 0:
        print(f"{RED}[!] Failed to fetch {args.url}: {body}{NC}", flush=True)
        return 1

    emails = extract_emails(body)
    if not emails:
        print(f"{YELLOW}No email addresses found on {args.url}.{NC}", flush=True)
        return 0

    print(f"{GREEN}Found {len(emails)} unique email address(es) on {args.url}:{NC}", flush=True)
    for email in emails:
        print(email, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())