# 🔐 CyberAuditX

CyberAuditX is a cross-platform Python tool for auditing system security hygiene. It checks for open ports, sensitive files, misconfigured permissions, exposed secrets, and integrates with popular security tools for deep scans.

---

## ✨ Features

- OS & system info
- Open ports scan
- Sensitive file discovery
- World-writable file detection
- User/group audit
- Firewall status
- Environment variable scan
- Deep scan via `nmap`, `chkrootkit`, `lynis`, `clamav`
- JSON report output

---

## ⚙️ Requirements

- Python 3.6+
- Optional tools for deep scans:
  - `nmap`
  - `chkrootkit`
  - `lynis`
  - `clamav`

---

## 🚀 Usage
# pip install -r requirements.txt

Run the script using Python 3:

```bash
python3 CyberAuditX.py [OPTIONS]
```

### 🔧 Options

| Option         | Description                                                  |
|----------------|--------------------------------------------------------------|
| `--quick`      | Run basic audit (OS info, ports, users/groups)               |
| `--deep`       | Perform deep scan using external tools                       |
| `--sensitive`  | Scan for sensitive files and environment variables           |
| `--writable`   | Detect world-writable files                                  |
| `--firewall`   | Check firewall status                                        |
| `--json`       | Save output to a timestamped JSON file                       |
| `--verbose`    | Print detailed output to console                             |
| `--all`        | Run full audit (includes all checks and saves report)        |

### 📌 Examples

- **Quick audit**:
  ```bash
  python3 CyberAuditX.py --quick
  ```

- **Full audit with report**:
  ```bash
  sudo python3 CyberAuditX.py --all --json
  ```

- **Sensitive data scan only**:
  ```bash
  python3 CyberAuditX.py --sensitive --verbose
  ```

---

## 📋 Output

- Results are stored in a structured JSON-style report.
- If `--json` is used, a file named like `cyberaudit_report_YYYY-MM-DD_HH-MM-SS.json` is created.
- Verbose mode prints the full report to the console.

---

## 🔍 What It Checks

### Basic Audit
- OS and architecture info
- Open ports (`netstat`)
- Users and groups (`/etc/passwd`, `/etc/group` or `net user`)

### Sensitive Data
- Files with names containing `password`, `secret`, `key`, `token`
- Environment variables with sensitive keywords

### Permissions
- World-writable files (Linux only)

### Firewall
- Status via `ufw`, `iptables`, or `netsh advfirewall`

### Deep Scan
- Uses external tools (if installed) to scan for malware, rootkits, and vulnerabilities

---

## 🧠 Tips

- Run regularly to monitor changes in system security.
- Use `--json` to archive reports and compare over time.
- Combine with cron jobs or scheduled tasks for automation.

---

## ⚠️ Notes

- Some features require root/admin privileges.
- Deep scan tools must be installed separately.
- Windows support is partial (some features like world-writable scan are not available).

---

## 📄 License

MIT

Made by Gabriel Pokiano 
```

