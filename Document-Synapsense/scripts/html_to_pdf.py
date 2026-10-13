#!/usr/bin/env python3
"""
SynapseSense HTML to PDF Converter
Uses native Edge / Chromium Headless to render pixel-perfect vector PDFs with zero external dependencies.
"""

import os
import sys
import subprocess
import shutil

def find_browser():
    """Find Microsoft Edge or Google Chrome binary on Windows/Linux/Mac."""
    # Windows standard paths
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    
    # Check PATH
    for b in ["msedge", "edge", "google-chrome", "chrome", "chromium"]:
        found = shutil.which(b)
        if found:
            return found
            
    return None

def convert_html_to_pdf(input_html, output_pdf, landscape=False):
    browser = find_browser()
    if not browser:
        print("Error: Could not locate Microsoft Edge or Google Chrome executable.", file=sys.stderr)
        sys.exit(1)

    abs_html = os.path.abspath(input_html)
    abs_pdf = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(abs_pdf), exist_ok=True)

    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-local-file-accesses",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={abs_pdf}",
        f"file:///{abs_html.replace(os.sep, '/')}"
    ]

    print(f"Compiling PDF using {os.path.basename(browser)}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"Success! Generated: {abs_pdf} ({round(os.path.getsize(abs_pdf) / 1024, 1)} KB)")
        return abs_pdf
    else:
        print(f"Error compiling PDF: {res.stderr}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python html_to_pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    convert_html_to_pdf(sys.argv[1], sys.argv[2])
