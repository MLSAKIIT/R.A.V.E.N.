#!/usr/bin/env python3
"""
dirbuster_lite.py - Lightweight directory brute-forcer (std-words or file)

Example:
  python3 scripts/scanning/dirbuster_lite.py http://example.com/ --wordlist words.txt
"""
from __future__ import annotations
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import http.client
from urllib.parse import urlparse, urljoin

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"

DEFAULT_WORDS = ['admin','login','uploads','images','backup','test','dev','wp-admin']


def probe(base: str, path: str, timeout=6) -> tuple[str, int]:
    try:
        parsed = urlparse(base)
        host = parsed.netloc
        conn = http.client.HTTPConnection(host, timeout=timeout)
        conn.request('GET', urljoin(parsed.path or '/', path))
        r = conn.getresponse()
        status = r.status
        conn.close()
        return path, status
    except Exception:
        return path, 0


def main() -> int:
    p = argparse.ArgumentParser(description='Dirbuster-lite')
    p.add_argument('base')
    p.add_argument('--wordlist')
    p.add_argument('--threads', type=int, default=20)
    args = p.parse_args()

    words = DEFAULT_WORDS
    if args.wordlist:
        try:
            with open(args.wordlist, 'r', encoding='utf-8') as fh:
                words = [l.strip() for l in fh if l.strip()]
        except Exception as e:
            print(f"{RED}[!] Could not read wordlist: {e}{NC}", flush=True)
            return 2

    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(probe, args.base, w): w for w in words}
        for fut in as_completed(futures):
            path, status = fut.result()
            if status and status < 400:
                print(f"{GREEN}[{status}] {path}{NC}", flush=True)
            else:
                print(f"{YELLOW}[{status}] {path}{NC}", flush=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())
