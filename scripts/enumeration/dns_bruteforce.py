#!/usr/bin/env python3
"""
dns_bruteforce.py - Bruteforce subdomains using a wordlist (fast, stdlib only)

Example:
  python3 scripts/enumeration/dns_bruteforce.py example.com --wordlist common.txt
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


def try_resolve(name: str) -> tuple[str, bool]:
    try:
        ip = socket.gethostbyname(name)
        return ip, True
    except Exception:
        return '', False


def main() -> int:
    p = argparse.ArgumentParser(description='DNS bruteforce subdomains')
    p.add_argument('domain')
    p.add_argument('--wordlist', required=True)
    p.add_argument('--threads', type=int, default=50)
    args = p.parse_args()

    try:
        with open(args.wordlist, 'r', encoding='utf-8') as fh:
            words = [l.strip() for l in fh if l.strip()]
    except Exception as e:
        print(f"{RED}[!] Could not read wordlist: {e}{NC}", flush=True)
        return 2

    targets = [f"{w}.{args.domain}" for w in words]
    found = []
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(try_resolve, t): t for t in targets}
        for fut in as_completed(futures):
            t = futures[fut]
            ip, ok = fut.result()
            if ok:
                print(f"{GREEN}[+] {t} -> {ip}{NC}", flush=True)
                found.append((t, ip))

    if not found:
        print(f"{YELLOW}No results.{NC}", flush=True)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
