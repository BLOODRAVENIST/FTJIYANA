<div align="center">

# 🔴 FTJIYANA

### External Web Pentesting Framework

**Bug Bounty Recon & Enumeration Tool**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Kali](https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kali-linux&logoColor=white)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-darkred?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)]()
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/bloodravenist)

**Made by [BLOODRAVENIST](https://github.com/BLOODRAVENIST)**

> ⚠️ **For Authorized Penetration Testing Only.**

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Phases](#-phases)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output](#-output)
- [Tool Coverage](#-tool-coverage)
- [Legal](#%EF%B8%8F-legal)
- [Support](#-support)

---

## ✨ Features

| Feature | Description |
|---|---|
| **40+ Web Tools** | Curated bug bounty tools, sequential execution |
| **19 Phases** | Subdomain → Probe → Tech → URLs → Crawl → Content → Params → Vuln → XSS → SQLi → CMDi → CORS → CRLF → Redirect → Takeover → Exposure → Misconfig → CVEs → GF |
| **URL/Endpoint Discovery** | gau, waybackurls, katana, gospider |
| **Parameter Fuzzing** | arjun, paramspider |
| **SQLi/XSS/SSRF/Redirect** | sqlmap, dalfox, gf patterns |
| **Takeover Detection** | subjack, nuclei takeovers |
| **Markdown Report** | Auto-generated per target |
| **Fast Mode** | Skip slow tools for quick recon |
| **Phase Filter** | Run only specific phase |

---

## 🎯 Phases

| Phase | Tools | What It Finds |
|---|---|---|
| **subdomain** | subfinder, assetfinder, amass, findomain, crt.sh | All subdomains |
| **probe** | httpx, httprobe | Live hosts |
| **tech** | whatweb, wafw00f | Tech stack, WAF |
| **urls** | gau, waybackurls, uro, anew | Historical URLs |
| **crawl** | katana, gospider | Current endpoints |
| **content** | gobuster, ffuf, feroxbuster, dirsearch | Hidden directories |
| **params** | arjun, paramspider | Hidden parameters |
| **vuln** | nuclei, nikto | Known vulns |
| **xss** | dalfox, xsstrike | XSS vulns |
| **sqli** | sqlmap | SQL injection |
| **cmdi** | commix | Command injection |
| **cors** | corsy | CORS misconfig |
| **crlf** | crlfuzz | CRLF injection |
| **redirect** | openredirex | Open redirects |
| **takeover** | subjack, nuclei | Subdomain takeover |
| **exposure** | nuclei | Exposed files |
| **misconfig** | nuclei | Misconfigurations |
| **cves** | nuclei | Critical CVEs |
| **gf** | gf patterns | Filter URLs for SSRF/XSS/SQLi/redirect |

---

## 🚀 Installation

### Prerequisites

    sudo apt update
    sudo apt install -y seclists nmap nikto gobuster ffuf feroxbuster dnsrecon

### Go Tools Install

    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    go install github.com/projectdiscovery/katana/cmd/katana@latest
    go install github.com/tomnomnom/assetfinder@latest
    go install github.com/tomnomnom/waybackurls@latest
    go install github.com/tomnomnom/anew@latest
    go install github.com/lc/gau/v2/cmd/gau@latest

### Setup

    git clone https://github.com/BLOODRAVENIST/FTJIYANA.git
    cd FTJIYANA
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

---

## 💻 Usage

### Full Scan

    python ftjiyana.py -u example.com --i-have-permission

### Fast Mode (Skip Slow Tools)

    python ftjiyana.py -u example.com --i-have-permission --fast

### Specific Phase

    python ftjiyana.py -u example.com --i-have-permission --phase subdomain

### Phase List

    python ftjiyana.py -u example.com --i-have-permission --phase xss
    python ftjiyana.py -u example.com --i-have-permission --phase sqli
    python ftjiyana.py -u example.com --i-have-permission --phase gf

### Command-Line Options

| Flag | Description | Default |
|---|---|---|
| `-u, --url` | Target URL or domain | **required** |
| `--i-have-permission` | Confirm written authorization | **required** |
| `--phase` | Run only specific phase | `all` |
| `--fast` | Skip slow tools (sqlmap, commix, nikto, etc.) | `false` |

---

## 📁 Output

    results/<domain>_<timestamp>/
    ├── FTJIYANA_REPORT.md      # Markdown report
    ├── subdomains.txt          # All discovered subdomains
    ├── urls.txt                # All discovered URLs
    └── raw/
        ├── subfinder.txt
        ├── httpx_probe.txt
        ├── nuclei_safe.txt
        └── ... (40+ tool outputs)

---

## 🛠 Tool Coverage

<details>
<summary><b>Click to expand full tool list</b></summary>

### Subdomain Enumeration
`subfinder` `assetfinder` `amass` `findomain` `crt.sh`

### Probing
`httpx` `httprobe`

### Technology Detection
`whatweb` `wafw00f`

### URL Discovery
`gau` `waybackurls` `uro` `anew`

### Crawling
`katana` `gospider`

### Content Discovery
`gobuster` `ffuf` `feroxbuster` `dirsearch`

### Parameter Discovery
`arjun` `paramspider`

### Vulnerability Scanning
`nuclei` `nikto`

### XSS
`dalfox` `xsstrike`

### SQL Injection
`sqlmap`

### Command Injection
`commix`

### CORS
`corsy`

### CRLF
`crlfuzz`

### Open Redirect
`openredirex`

### Subdomain Takeover
`subjack` `nuclei-takeovers`

### Nuclei Templates
`exposures` `misconfigurations` `cves`

### GF Patterns
`ssrf` `xss` `sqli` `redirect` `lfi` `rce` `idor`

</details>

---

## ⚖️ Legal

**FTJIYANA is for authorized penetration testing only.**

- ✅ Only use on systems you have **written permission** to test
- ✅ Use for bug bounty programs with valid scope
- ❌ Do NOT use on systems you don't own or have permission for

The author is not responsible for misuse. Unauthorized access is illegal under CFAA (US), Computer Misuse Act (UK), IT Act (India), and similar laws worldwide.

---

## ☕ Support

If FTJIYANA helped you in your bug bounty journey, consider buying me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20FTJIYANA-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/bloodravenist)

---

<div align="center">

**⭐ If FTJIYANA helped you, give it a star! ⭐**

Made with 🔴 by [BLOODRAVENIST](https://github.com/BLOODRAVENIST)

</div>
