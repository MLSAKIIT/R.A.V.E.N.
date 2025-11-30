#!/usr/bin/env python3
"""
tech_fingerprint.py - Simple tech stack fingerprint using headers and basic probes

Example:
  python3 scripts/scanning/tech_fingerprint.py http://example.com
"""
from __future__ import annotations
import argparse
import sys
import http.client
from urllib.parse import urlparse

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"

SIGS = {
    'X-Powered-By': ['PHP', 'ASP.NET'],
    'Server': ['nginx', 'Apache', 'IIS'],
    'X-Generator': ['WordPress']
}


def main() -> int:
    p = argparse.ArgumentParser(description='Basic tech fingerprint')
    p.add_argument('url')
    args = p.parse_args()

    parsed = urlparse(args.url if args.url.startswith('http') else f'http://{args.url}')
    host = parsed.netloc or parsed.path
    path = parsed.path or '/'
    try:
        conn = http.client.HTTPConnection(host, timeout=6)
        conn.request('HEAD', path)
        r = conn.getresponse()
        headers = {k: v for k, v in r.getheaders()}
        print(f"{YELLOW}Status:{NC} {r.status}", flush=True)
        for h, v in headers.items():
            print(f"  {GREEN}{h}:{NC} {v}", flush=True)
        found = []
        hv = ' '.join([f'{k}:{v}' for k, v in headers.items()])
        for sig, markers in SIGS.items():
            for m in markers:
                if m.lower() in hv.lower():
                    found.append(m)
        if found:
            print(f"{GREEN}Likely technologies:{NC} {', '.join(sorted(set(found)))}", flush=True)
    except Exception as e:
        print(f"{RED}[!] Error: {e}{NC}", flush=True)
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
