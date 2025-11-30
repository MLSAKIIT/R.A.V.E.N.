#!/usr/bin/env python3
"""
http_title_scan.py - Fetch HTTP title tags from a list of hosts

Example:
  python3 scripts/enumeration/http_title_scan.py hosts.txt --threads 50
"""
from __future__ import annotations
import argparse
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import http.client
from urllib.parse import urlparse

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def fetch_title(host: str, timeout=5) -> tuple[str, str]:
    try:
        parsed = urlparse(host if host.startswith('http') else f'http://{host}')
        conn = http.client.HTTPConnection(parsed.netloc or parsed.path, timeout=timeout)
        conn.request('GET', parsed.path or '/')
        r = conn.getresponse()
        data = r.read(2048).decode(errors='replace')
        conn.close()
        start = data.find('<title>')
        end = data.find('</title>')
        if start != -1 and end != -1 and end > start:
            return host, data[start+7:end].strip()
        return host, ''
    except Exception as e:
        return host, ''


def main() -> int:
    p = argparse.ArgumentParser(description='Fetch HTML titles')
    p.add_argument('hosts_file')
    p.add_argument('--threads', type=int, default=30)
    args = p.parse_args()

    try:
        with open(args.hosts_file, 'r', encoding='utf-8') as fh:
            hosts = [l.strip() for l in fh if l.strip()]
    except Exception as e:
        print(f"{RED}[!] Could not read hosts: {e}{NC}", flush=True)
        return 2

    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(fetch_title, h): h for h in hosts}
        for fut in as_completed(futures):
            host, title = fut.result()
            if title:
                print(f"{GREEN}[{host}] {title}{NC}", flush=True)
            else:
                print(f"{YELLOW}[{host}] (no title){NC}", flush=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())
