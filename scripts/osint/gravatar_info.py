#!/usr/bin/env python3
"""
gravatar_info.py - Check if an email has a Gravatar and show hash

Example:
  python3 scripts/osint/gravatar_info.py user@example.com
"""
from __future__ import annotations
import argparse
import hashlib
import sys
import urllib.request

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def main() -> int:
    p = argparse.ArgumentParser(description='Gravatar presence checker')
    p.add_argument('email')
    args = p.parse_args()

    em = args.email.strip().lower().encode('utf-8')
    h = hashlib.md5(em).hexdigest()
    url = f'https://www.gravatar.com/avatar/{h}?d=404'
    print(f"{YELLOW}Email:{NC} {args.email}", flush=True)
    print(f"  {GREEN}MD5:{NC} {h}", flush=True)
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=6) as r:
            code = r.getcode()
            print(f"  {GREEN}Gravatar exists (HTTP {code}){NC}", flush=True)
    except Exception as e:
        print(f"  {RED}No gravatar or error:{NC} {e}", flush=True)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
