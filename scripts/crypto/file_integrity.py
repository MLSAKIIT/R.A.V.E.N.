#!/usr/bin/env python3
"""
file_integrity.py - Compute and verify file hashes (MD5 / SHA1 / SHA256)

Example:
  python3 scripts/crypto/file_integrity.py /path/to/file --show-all
  python3 scripts/crypto/file_integrity.py file1 file2 --hash sha256

Features:
- Minimal dependencies (Python stdlib)
- Colorized output
- Graceful error handling
"""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"


def compute_hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except Exception as e:
        raise
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="File integrity / hash utility")
    p.add_argument("files", nargs="+", help="Files to hash")
    p.add_argument("--hash", choices=("md5", "sha1", "sha256"), default="sha256",
                   help="Hash algorithm (default: sha256)")
    p.add_argument("--show-all", action="store_true", help="Also print MD5/SHA1/SHA256 for each file")
    args = p.parse_args()

    ok = True
    for fp in args.files:
        path = Path(fp)
        if not path.exists():
            print(f"{RED}[!] File not found:{NC} {fp}")
            ok = False
            continue

        try:
            main_hash = compute_hash(path, args.hash)
        except Exception as e:
            print(f"{RED}[!] Failed to read file:{NC} {fp} -> {e}")
            ok = False
            continue

        print(f"{GREEN}File:{NC} {fp}")
        print(f"  {YELLOW}{args.hash.upper()}: {NC}{main_hash}")

        if args.show_all:
            try:
                md5 = compute_hash(path, "md5")
                sha1 = compute_hash(path, "sha1")
                sha256 = compute_hash(path, "sha256")
                print(f"  {YELLOW}MD5:    {NC}{md5}")
                print(f"  {YELLOW}SHA1:   {NC}{sha1}")
                print(f"  {YELLOW}SHA256: {NC}{sha256}")
            except Exception as e:
                print(f"{RED}[!] Error computing extra hashes:{NC} {e}")

        print("")

    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
