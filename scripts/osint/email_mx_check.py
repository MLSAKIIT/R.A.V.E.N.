#!/usr/bin/env python3
"""
email_mx_check.py - Check if domain has MX records

Example:
  python3 scripts/osint/email_mx_check.py example.com
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import socket

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def run_cmd(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=6)
        return out.decode(errors='replace')
    except Exception as e:
        return f"ERROR: {e}"


def check_mx_dnspython(domain: str) -> str:
    """Use dnspython library if available"""
    try:
        import dns.resolver
        mx_records = dns.resolver.resolve(domain, 'MX')
        result = f"{GREEN}MX Records for {domain}:{NC}\n"
        for mx in mx_records:
            result += f"  {mx.preference} {mx.exchange}\n"
        return result
    except ImportError:
        return None
    except Exception as e:
        return f"{RED}Error: {e}{NC}"


def check_mx_nslookup(domain: str) -> str:
    """Use nslookup command if available"""
    if shutil.which('nslookup'):
        return run_cmd(['nslookup', '-type=mx', domain])
    return None


def check_mx_socket(domain: str) -> str:
    """Fallback using socket (limited, just resolves IP)"""
    try:
        ip = socket.gethostbyname(domain)
        return f"{GREEN}Domain resolves to: {ip}{NC}\n(Note: MX records require DNS library. Install: pip install dnspython)"
    except Exception as e:
        return f"{RED}Error resolving domain: {e}{NC}"


def main() -> int:
    p = argparse.ArgumentParser(description='Check MX records for domain')
    p.add_argument('domain', help='Target domain')
    args = p.parse_args()

    # Try dnspython first (best)
    result = check_mx_dnspython(args.domain)
    if result:
        print(result, flush=True)
        return 0

    # Try nslookup (good on Unix/Windows with PATH)
    result = check_mx_nslookup(args.domain)
    if result:
        print(result[:2000], flush=True)
        return 0

    # Fallback to socket (basic)
    result = check_mx_socket(args.domain)
    print(result, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
