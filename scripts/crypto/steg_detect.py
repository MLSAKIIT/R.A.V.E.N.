#!/usr/bin/env python3
"""
steg_detect.py - Simple check for common steg markers in files (basic heuristic)

Example:
  python3 scripts/crypto/steg_detect.py suspect.jpg

Notes:
- Scans for common steg tool headers and high-entropy appended data
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import math

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


def main() -> int:
    p = argparse.ArgumentParser(description='Simple steg heuristic detector')
    p.add_argument('files', nargs='+', help='Files to inspect')
    args = p.parse_args()

    for fn in args.files:
        pth = Path(fn)
        if not pth.exists():
            print(f"{RED}[!] Missing:{NC} {fn}", flush=True)
            continue
        try:
            data = pth.read_bytes()
        except Exception as e:
            print(f"{RED}[!] Read error:{NC} {fn} -> {e}", flush=True)
            continue

        ent = entropy(data[-4096:]) if len(data) > 1024 else entropy(data)
        print(f"{YELLOW}{fn}:{NC} entropy={ent:.2f}", flush=True)

        markers = []
        if b"steg" in data.lower() or b"steganography" in data.lower():
            markers.append('steg-marker')
        if b"upx" in data[:512].lower():
            markers.append('packed-exec')

        if markers:
            print(f"  {GREEN}Markers:{NC} {', '.join(markers)}", flush=True)
        if ent > 7.5:
            print(f"  {GREEN}[!] High entropy detected - possible embedded data{NC}", flush=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())
