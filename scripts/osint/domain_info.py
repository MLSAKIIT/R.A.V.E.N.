#!/usr/bin/env python3
"""
domain_info.py - Query basic domain info (A, MX via nslookup and optional whois)

Example:
  python3 scripts/osint/domain_info.py example.com

Notes:
- Uses system 'nslookup' and 'whois' when available. Falls back to socket for A record.
"""
from __future__ import annotations
import argparse
import shutil
import socket
import subprocess
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def run_cmd(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=8)
        return out.decode(errors='replace')
    except Exception as e:
        return f"ERROR: {e}"


def main() -> int:
    p = argparse.ArgumentParser(description='Quick domain information gatherer')
    p.add_argument('domain', help='Target domain')
    args = p.parse_args()

    domain = args.domain
    print(f"{YELLOW}Domain:{NC} {domain}")

    # A record via socket
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {GREEN}A:{NC} {ip}")
    except Exception as e:
        print(f"  {RED}A lookup failed:{NC} {e}")

    # nslookup for MX
    if shutil.which('nslookup'):
        out = run_cmd(['nslookup', '-type=mx', domain])
        print(f"  {YELLOW}MX records (nslookup):{NC}\n{out.strip()}")
    else:
        print(f"  {RED}nslookup not available on system{NC}")

    # whois if available
    if shutil.which('whois'):
        out = run_cmd(['whois', domain])
        # print only first 2000 chars for brevity
        print(f"  {YELLOW}whois (truncated):{NC}\n{out[:2000].strip()}")
    else:
        print(f"  {RED}whois not installed; skipping{NC}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
