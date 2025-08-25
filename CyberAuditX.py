#!/usr/bin/env python3

import os
import platform
import subprocess
import json
import argparse
import re
from datetime import datetime

report = {}

def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True)
    except Exception as e:
        return f"Error: {e}"

def check_os():
    report['os_info'] = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'architecture': platform.machine()
    }

def check_ports():
    cmd = "netstat -tuln" if platform.system() != "Windows" else "netstat -ano"
    report['open_ports'] = run_command(cmd)

def check_sensitive_files():
    keywords = ['password', 'secret', 'key', 'token']
    found = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if any(k in file.lower() for k in keywords):
                path = os.path.join(root, file)
                found.append(path)
    report['sensitive_files'] = found

def check_world_writable():
    if platform.system() == "Windows":
        report['world_writable'] = "Not supported on Windows"
        return
    cmd = "find / -type f -perm -o+w 2>/dev/null"
    result = run_command(cmd)
    report['world_writable'] = result.splitlines()

def check_users_groups():
    if platform.system() == "Windows":
        report['users'] = run_command("net user").splitlines()
        report['groups'] = "Use PowerShell for detailed group info"
    else:
        try:
            with open("/etc/passwd") as f:
                users = [line.split(":")[0] for line in f]
            with open("/etc/group") as f:
                groups = [line.split(":")[0] for line in f]
            report['users'] = users
            report['groups'] = groups
        except Exception as e:
            report['users'] = f"Error: {e}"
            report['groups'] = f"Error: {e}"

def check_firewall():
    cmds = {
        "Linux": ["ufw status", "iptables -L"],
        "Windows": ["netsh advfirewall show allprofiles"]
    }
    for cmd in cmds.get(platform.system(), []):
        result = run_command(cmd)
        if "Error" not in result and result.strip():
            report['firewall'] = result
            return
    report['firewall'] = "Firewall status unavailable"

def check_env_vars():
    sensitive = {}
    for k, v in os.environ.items():
        if re.search(r'(pass|key|token|secret)', k, re.IGNORECASE):
            sensitive[k] = v
    report['env_secrets'] = sensitive

def deep_scan():
    tools = {
        'nmap': 'nmap -sV localhost',
        'chkrootkit': 'chkrootkit',
        'lynis': 'lynis audit system',
        'clamav': 'clamscan -r /'
    }
    deep_results = {}
    for tool, cmd in tools.items():
        if run_command(f"which {tool}").strip():
            deep_results[tool] = run_command(cmd)
        else:
            deep_results[tool] = f"{tool} not installed"
    report['deep_scan'] = deep_results

def save_report():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"cyberaudit_report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[✔] Report saved as {filename}")

def parse_args():
    parser = argparse.ArgumentParser(description="CyberAuditX - System Security Audit Tool")
    parser.add_argument('--quick', action='store_true', help='Run basic audit')
    parser.add_argument('--deep', action='store_true', help='Run deep scan with external tools')
    parser.add_argument('--json', action='store_true', help='Save output to JSON file')
    parser.add_argument('--verbose', action='store_true', help='Print detailed output')
    parser.add_argument('--sensitive', action='store_true', help='Scan for sensitive files and env vars')
    parser.add_argument('--firewall', action='store_true', help='Check firewall status')
    parser.add_argument('--writable', action='store_true', help='Scan for world-writable files')
    parser.add_argument('--all', action='store_true', help='Run full audit')
    return parser.parse_args()

def main():
    args = parse_args()
    print("🔍 Running CyberAuditX...")

    if args.quick or args.all:
        check_os()
        check_ports()
        check_users_groups()

    if args.sensitive or args.all:
        check_sensitive_files()
        check_env_vars()

    if args.writable or args.all:
        check_world_writable()

    if args.firewall or args.all:
        check_firewall()

    if args.deep or args.all:
        deep_scan()

    if args.json or args.all:
        save_report()

    if args.verbose:
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
