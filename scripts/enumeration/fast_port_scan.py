#!/usr/bin/env python3
"""
fast_port_scan.py - Simple, fast TCP connect port scanner

Example:
  python3 scripts/enumeration/fast_port_scan.py 10.0.0.1 --start 1 --end 1024 --threads 200

Notes:
- Uses only Python stdlib
- Color output and graceful errors
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


def scan_port(host: str, port: int, timeout: float = 0.5) -> tuple[int, bool]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return port, True
    except Exception:
        return port, False


def main() -> int:
    p = argparse.ArgumentParser(description="Fast TCP connect port scanner")
    p.add_argument("host", help="Target hostname or IP")
    p.add_argument("--start", type=int, default=1, help="Start port (default:1)")
    p.add_argument("--end", type=int, default=1024, help="End port (default:1024)")
    p.add_argument("--threads", type=int, default=100, help="Worker threads (default:100)")
    p.add_argument("--timeout", type=float, default=0.5, help="Connect timeout seconds")
    args = p.parse_args()

    try:
        socket.gethostbyname(args.host)
    except Exception as e:
        print(f"{RED}[!] Could not resolve host:{NC} {args.host} -> {e}")
        return 2

    ports = range(args.start, args.end + 1)
    open_ports = []

    print(f"{YELLOW}Scanning {args.host} ports {args.start}-{args.end} with {args.threads} threads...{NC}")
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = {ex.submit(scan_port, args.host, p, args.timeout): p for p in ports}
        for fut in as_completed(futures):
            port, ok = fut.result()
            if ok:
                print(f"{GREEN}[+] {port}/tcp open{NC}")
                open_ports.append(port)

    if not open_ports:
        print(f"{RED}No open ports found in range.{NC}")
        return 1
    print("")
    print(f"{YELLOW}Open ports:{NC} {', '.join(map(str, sorted(open_ports)))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
