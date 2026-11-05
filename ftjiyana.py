#!/usr/bin/env python3
"""
FTJIYANA v1.0.0 — External Web Pentesting Framework
Bug Bounty Recon & Enumeration Tool
by BLOODRAVENIST · For Authorized Testing Only
"""
import os, sys, json, time, subprocess, argparse, re, signal
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import pyfiglet

VERSION = "1.0.0"
BASE = Path(__file__).parent
CFG = BASE / "config"
OUT = BASE / "results"
ERR = BASE / "errors"

console = Console()

def banner():
    console.print(f"[bold red]{pyfiglet.figlet_format('FTJIYANA', font='ansi_shadow')}[/bold red]")
    console.print(Panel.fit(
        "[bold red]EXTERNAL WEB PENTESTING FRAMEWORK[/bold red]\n"
        "[dim red]Bug Bounty Recon & Enumeration[/dim red]\n"
        "[dim red]by BLOODRAVENIST · For Authorized Testing Only[/dim red]\n"
        f"[dim red]v{VERSION}[/dim red]",
        border_style="red", box=box.DOUBLE))

def normalize_url(input_str):
    """Accepts domain or URL, returns (url, domain)."""
    if not input_str.startswith(("http://", "https://")):
        url = f"https://{input_str}"
    else:
        url = input_str
    parsed = urlparse(url)
    domain = parsed.netloc
    return url, domain

def run_cmd(cmd, timeout=300, input_file=None):
    """Run shell command with timeout, return (success, stdout, stderr)."""
    full = f"timeout {timeout}s bash -c {json.dumps(cmd)} </dev/null 2>&1"
    try:
        r = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=timeout+15)
        return r.returncode == 0, r.stdout or "", r.stderr or ""
    except subprocess.TimeoutExpired:
        return False, "", f"Timeout {timeout}s"
    except Exception as e:
        return False, "", str(e)

def save_output(outdir, name, content):
    """Save raw output to file."""
    f = outdir / "raw" / f"{name}.txt"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "w") as fh:
        fh.write(content)
    return f

def extract_urls_from_output(text):
    """Extract URLs from tool output."""
    urls = re.findall(r'https?://[^\s<>"\']+', text)
    return list(set(urls))

def run_phase(outdir, tools, url, domain, phase_filter=None):
    """Run tools for a phase."""
    subdomains_file = outdir / "subdomains.txt"
    urls_file = outdir / "urls.txt"

    # Create placeholder files
    if not subdomains_file.exists():
        subdomains_file.write_text(f"{domain}\n")
    if not urls_file.exists():
        urls_file.write_text(f"{url}\n")

    results = []
    for tool in tools:
        if phase_filter and tool.get("phase") not in phase_filter:
            continue

        cmd = tool["command"]
        cmd = cmd.replace("<url>", url)
        cmd = cmd.replace("<domain>", domain)
        cmd = cmd.replace("<subdomains_file>", str(subdomains_file))
        cmd = cmd.replace("<urls_file>", str(urls_file))

        console.print(f"[cyan]  → {tool['name']}[/cyan]", end=" ")
        start = time.time()
        ok, stdout, stderr = run_cmd(cmd, tool.get("timeout", 300))
        elapsed = time.time() - start

        # Save output
        output = stdout + ("\n# STDERR:\n" + stderr if stderr else "")
        save_output(outdir, tool["name"], output)

        # Extract URLs and append to urls file
        new_urls = extract_urls_from_output(stdout)
        if new_urls:
            with open(urls_file, "a") as f:
                for u in new_urls:
                    f.write(u + "\n")

        if ok:
            console.print(f"[green]✓ {elapsed:.1f}s[/green]")
        else:
            console.print(f"[red]✗ {elapsed:.1f}s[/red]")

        results.append({"tool": tool["name"], "ok": ok, "elapsed": elapsed})
        time.sleep(2)  # small gap between tools

    return results

def generate_report(outdir, url, domain, results, elapsed):
    """Generate markdown report."""
    rep = outdir / "FTJIYANA_REPORT.md"
    with open(rep, "w") as f:
        f.write(f"# FTJIYANA Recon Report\n\n")
        f.write(f"**Target:** `{url}`  \n")
        f.write(f"**Domain:** `{domain}`  \n")
        f.write(f"**Time:** {datetime.now().isoformat()}  \n")
        f.write(f"**Elapsed:** {elapsed:.1f}s  \n\n")

        f.write("## Tool Results\n\n| # | Tool | Status | Time |\n|---|---|---|---|\n")
        for i, r in enumerate(results, 1):
            f.write(f"| {i} | {r['tool']} | {'✓' if r['ok'] else '✗'} | {r['elapsed']:.1f}s |\n")

        f.write("\n## Raw Outputs\n\nSee `raw/` directory for detailed tool outputs.\n")

        # Check for interesting findings
        f.write("\n## Quick Summary\n\n")
        subdomains_file = outdir / "subdomains.txt"
        urls_file = outdir / "urls.txt"
        if subdomains_file.exists():
            subs = subdomains_file.read_text().strip().split("\n")
            f.write(f"- Subdomains found: {len([s for s in subs if s])}\n")
        if urls_file.exists():
            urls = urls_file.read_text().strip().split("\n")
            f.write(f"- URLs collected: {len([u for u in urls if u])}\n")

    return rep

def main():
    parser = argparse.ArgumentParser(description="FTJIYANA — Web Bug Bounty Recon")
    parser.add_argument("-u", "--url", required=True, help="Target URL or domain")
    parser.add_argument("--i-have-permission", action="store_true", required=True)
    parser.add_argument("--phase", choices=["subdomain", "probe", "tech", "vuln", "content", "urls", "crawl", "params", "xss", "sqli", "cmdi", "cors", "crlf", "redirect", "takeover", "exposure", "misconfig", "cves", "gf", "all"], default="all")
    parser.add_argument("--fast", action="store_true", help="Fast mode (skip slow tools)")
    args = parser.parse_args()

    banner()

    if not args.i_have_permission:
        console.print("[red]✗ --i-have-permission required[/red]")
        sys.exit(1)

    url, domain = normalize_url(args.url)
    console.print(f"\n[bold red]Target:[/bold red] {url}")
    console.print(f"[bold red]Domain:[/bold red] {domain}\n")

    # Load tools
    tools = json.load(open(CFG / "tools.json"))

    # Fast mode: skip slow tools
    if args.fast:
        skip = ["sqlmap", "commix", "nikto", "nuclei_cves", "nuclei_misconfig"]
        tools = [t for t in tools if t["name"] not in skip]

    # Filter by phase
    if args.phase != "all":
        tools = [t for t in tools if t.get("phase") == args.phase]

    # Output dir
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_domain = domain.replace(".", "_").replace(":", "_")
    outdir = OUT / f"{safe_domain}_{ts}"
    outdir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold red]Running {len(tools)} tools...[/bold red]\n")

    start = time.time()
    results = []

    # Run tools by phase order
    phase_order = ["subdomain", "probe", "tech", "urls", "crawl", "content", "params", "vuln", "xss", "sqli", "cmdi", "cors", "crlf", "redirect", "takeover", "exposure", "misconfig", "cves", "gf"]
    for phase in phase_order:
        phase_tools = [t for t in tools if t.get("phase") == phase]
        if not phase_tools:
            continue
        console.print(f"\n[bold red]═══ {phase.upper()} ═══[/bold red]")
        phase_results = run_phase(outdir, phase_tools, url, domain)
        results.extend(phase_results)

    elapsed = time.time() - start
    report = generate_report(outdir, url, domain, results, elapsed)

    console.print("\n" + "="*60)
    ok_count = sum(1 for r in results if r["ok"])
    console.print(Panel.fit(
        f"[bold green]Complete[/bold green]\n"
        f"Tools: {ok_count}/{len(results)}  ·  Time: {elapsed:.1f}s\n"
        f"Report: [red]{report}[/red]\nOutput: {outdir}",
        border_style="red"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(130)
