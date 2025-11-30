#!/usr/bin/env python3
"""
email_mx_check.py - Check if domain has MX records (via nslookup or socket fallback)

Example:
  python3 scripts/osint/email_mx_check.py example.com
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys

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


def main() -> int:
    p = argparse.ArgumentParser(description='Check MX records for domain')
    p.add_argument('domain')
    args = p.parse_args()

    if shutil.which('nslookup'):
        out = run_cmd(['nslookup', '-type=mx', args.domain])
        print(out[:2000], flush=True)
        return 0
    else:
        print(f"{YELLOW}nslookup not available; please install or run on Unix-like system{NC}", flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
