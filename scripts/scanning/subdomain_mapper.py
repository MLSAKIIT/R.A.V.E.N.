#!/usr/bin/env python3
"""
subdomain_mapper.py - Lightweight subdomain mapper using DNS resolution

Example:
  python3 scripts/scanning/subdomain_mapper.py example.com --wordlist common

Notes:
- Uses Python stdlib only
- Default built-in wordlist is small and fast; you can pass a file with --wordlist-file
"""
from __future__ import annotations
import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"

DEFAULT_WORDS = [
    'www', 'mail', 'dev', 'test', 'api', 'staging', 'smtp', 'vpn', 'admin', 'portal'
]


def resolve(name: str) -> tuple[str, bool]:
    try:
        ip = socket.gethostbyname(name)
        return ip, True
    except Exception:
        return '', False


def main() -> int:
    p = argparse.ArgumentParser(description='Quick subdomain mapper')
    p.add_argument('domain', help='Target domain')
    p.add_argument('--wordlist-file', help='Path to newline wordlist')
    p.add_argument('--threads', type=int, default=30, help='Worker threads')
    args = p.parse_args()

    words = DEFAULT_WORDS
    if args.wordlist_file:
        try:
            with open(args.wordlist_file, 'r', encoding='utf-8') as fh:
                words = [w.strip() for w in fh if w.strip()]
        except Exception as e:
            print(f"{RED}[!] Failed to read wordlist file:{NC} {e}")
            return 2

    targets = [f"{w}.{args.domain}" for w in words]
    found = []

    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(resolve, t): t for t in targets}
        for fut in as_completed(futures):
            t = futures[fut]
            ip, ok = fut.result()
            if ok:
                print(f"{GREEN}[+] {t} -> {ip}{NC}")
                found.append((t, ip))

    if not found:
        print(f"{YELLOW}No subdomains discovered from the provided list.{NC}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
