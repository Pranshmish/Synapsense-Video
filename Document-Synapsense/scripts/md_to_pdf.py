#!/usr/bin/env python3
"""
SynapseSense Markdown to PDF Compiler
Converts GFM Markdown with KaTeX math, tables, callouts, and code highlighting into styled vector PDFs.
"""

import os
import sys
import re
import tempfile
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_TO_PDF_SCRIPT = os.path.join(SCRIPT_DIR, "html_to_pdf.py")

HTML_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <!-- KaTeX for math rendering -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '$', right: '$', display: false}},
      {{left: '\\\\(', right: '\\\\)', display: false}},
      {{left: '\\\\[', right: '\\\\]', display: true}}
    ]}});"></script>

  <style>
    @page {{
      size: A4 portrait;
      margin: 18mm 20mm 20mm 20mm;
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8.5pt;
        color: #94A3B8;
      }}
    }}
    
    * {{
      box-sizing: border-box;
    }}

    body {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
      font-size: 10pt;
      line-height: 1.55;
      color: #0F172A;
      background: #FFFFFF;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    h1, h2, h3, h4 {{
      color: #0B0F19;
      font-weight: 700;
      line-height: 1.25;
      margin-top: 1.4em;
      margin-bottom: 0.5em;
      break-after: avoid;
      page-break-after: avoid;
    }}

    h1 {{
      font-size: 22pt;
      border-bottom: 2px solid #0284C7;
      padding-bottom: 6px;
      margin-top: 0;
    }}

    h2 {{
      font-size: 14pt;
      color: #0F172A;
      border-bottom: 1px solid #E2E8F0;
      padding-bottom: 4px;
    }}

    h3 {{
      font-size: 11.5pt;
      color: #1E293B;
    }}

    p {{
      margin: 0.6em 0;
      color: #334155;
    }}

    blockquote {{
      margin: 1em 0;
      padding: 10px 16px;
      background: #F8FAFC;
      border-left: 4px solid #0284C7;
      color: #1E293B;
      font-style: normal;
      border-radius: 0 6px 6px 0;
      break-inside: avoid;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.2em 0;
      font-size: 9pt;
      break-inside: avoid;
      page-break-inside: avoid;
    }}

    th, td {{
      padding: 8px 12px;
      text-align: left;
      border-bottom: 1px solid #E2E8F0;
    }}

    th {{
      background: #F1F5F9;
      color: #0F172A;
      font-weight: 600;
      border-top: 1px solid #CBD5E1;
      border-bottom: 2px solid #94A3B8;
    }}

    tr:nth-child(even) td {{
      background: #F8FAFC;
    }}

    code {{
      font-family: 'Consolas', 'JetBrains Mono', monospace;
      font-size: 8.8pt;
      background: #F1F5F9;
      color: #0F172A;
      padding: 2px 5px;
      border-radius: 4px;
      border: 1px solid #E2E8F0;
    }}

    pre {{
      background: #0F172A;
      color: #F8FAFC;
      padding: 12px 16px;
      border-radius: 6px;
      overflow-x: auto;
      font-size: 8.5pt;
      line-height: 1.45;
      break-inside: avoid;
      page-break-inside: avoid;
      margin: 1em 0;
    }}

    pre code {{
      background: transparent;
      color: inherit;
      border: none;
      padding: 0;
    }}

    hr {{
      border: none;
      height: 1px;
      background: #E2E8F0;
      margin: 1.5em 0;
    }}

    ul, ol {{
      margin: 0.6em 0;
      padding-left: 24px;
      color: #334155;
    }}

    li {{
      margin: 0.3em 0;
    }}

    .badge {{
      display: inline-block;
      padding: 2px 8px;
      font-size: 8pt;
      font-weight: 600;
      border-radius: 12px;
      background: #E0F2FE;
      color: #0284C7;
      margin-right: 6px;
    }}
  </style>
</head>
<body>
  {body}
</body>
</html>
"""

def simple_markdown_to_html(md_text):
    """Simple parser for standard markdown features (headers, tables, lists, code, blockquotes)."""
    lines = md_text.splitlines()
    html_lines = []
    in_code = False
    in_table = False
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Code fences
        if stripped.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                html_lines.append(f'<pre><code class="{lang}">')
                in_code = True
            continue

        if in_code:
            # Escape HTML
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_lines.append(escaped)
            continue

        # Tables
        if "|" in line and (line.startswith("|") or stripped.startswith("|")):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", p) for p in parts if p):
                continue  # Divider line
            
            if not in_table:
                html_lines.append("<table><thead><tr>")
                for p in parts:
                    html_lines.append(f"<th>{p}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
            else:
                html_lines.append("<tr>")
                for p in parts:
                    html_lines.append(f"<td>{p}</td>")
                html_lines.append("</tr>")
            continue
        elif in_table:
            html_lines.append("</tbody></table>")
            in_table = False

        # Blank lines
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Headers
        if stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4>{stripped[5:]}</h4>")
        elif stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{stripped[2:]}</li>")
        elif stripped.startswith("---"):
            html_lines.append("<hr>")
        else:
            # Inline formatting
            p_line = stripped
            p_line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p_line)
            p_line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", p_line)
            p_line = re.sub(r"`(.+?)`", r"<code>\1</code>", p_line)
            html_lines.append(f"<p>{p_line}</p>")

    if in_code:
        html_lines.append("</code></pre>")
    if in_table:
        html_lines.append("</tbody></table>")
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)

def compile_md_to_pdf(input_md, output_pdf):
    with open(input_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    title = os.path.splitext(os.path.basename(input_md))[0].replace("_", " ").title()
    body_html = simple_markdown_to_html(md_text)
    full_html = HTML_SHELL.format(title=title, body=body_html)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(full_html)
        tmp_html = tmp.name

    try:
        cmd = [sys.executable, HTML_TO_PDF_SCRIPT, tmp_html, output_pdf]
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    compile_md_to_pdf(sys.argv[1], sys.argv[2])
