#!/usr/bin/env python3
"""
entropy_check.py - Scan files or directories for high-entropy files

Example:
  python3 scripts/crypto/entropy_check.py /path/to/dir --threshold 7.5
"""
from __future__ import annotations
import argparse
import math
import sys
from pathlib import Path

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0]*256
    for b in data:
        freq[b] += 1
    ent = 0.0
    ln = len(data)
    for f in freq:
        if f:
            p = f/ln
            ent -= p * math.log2(p)
    return ent


def check_file(pth: Path, threshold: float) -> None:
    try:
        data = pth.read_bytes()
    except Exception as e:
        print(f"{RED}[!] Read failed:{NC} {pth} -> {e}", flush=True)
        return
    ent = entropy(data[:65536])
    if ent >= threshold:
        print(f"{GREEN}[HIGH]{NC} {pth} entropy={ent:.2f}", flush=True)
    else:
        print(f"{YELLOW}[OK]   {NC} {pth} entropy={ent:.2f}", flush=True)


def main() -> int:
    p = argparse.ArgumentParser(description='Entropy scanner')
    p.add_argument('path', help='File or directory to scan')
    p.add_argument('--threshold', type=float, default=7.5)
    args = p.parse_args()

    pth = Path(args.path)
    if pth.is_dir():
        for child in pth.rglob('*'):
            if child.is_file():
                check_file(child, args.threshold)
    elif pth.is_file():
        check_file(pth, args.threshold)
    else:
        print(f"{RED}[!] Not found:{NC} {pth}", flush=True)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
