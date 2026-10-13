---
name: synapsense-document-pdf-engine
description: Production-grade system for compiling Markdown, HTML, technical specifications, and handwritten notes into broadcast-quality vector PDFs (whitepapers, dossiers, resumes, reports).
---

# SynapseSense Document & PDF Engine Skill

## 1. Overview & Architecture
The SynapseSense Document & PDF Engine renders **pixel-perfect, high-DPI vector PDFs** directly from HTML/CSS and Markdown. It uses Windows native Headless Chromium / Microsoft Edge with hardware acceleration disabled, ensuring 100% deterministic, zero-dependency PDF rendering across any machine.

### Key Capabilities:
- **Print Layout Engine**: Full CSS Paged Media (`@page { size: A4; margin: 20mm; }`) with automatic page counters, running headers, and footers.
- **Typography & Math**: Native KaTeX / MathJax LaTeX rendering, Inter / Segoe UI / Computer Modern typography.
- **Orphan & Break Control**: Strict prevention of split tables, dangling headers, or awkward page cuts using `break-inside: avoid` and `page-break-inside: avoid`.
- **Vector Graphics & Diagrams**: Direct SVG and Mermaid diagram embedding without pixelation.

---

## 2. Page Setup & CSS Standards

Every document template MUST include the following core CSS print rules:

```css
@page {
  size: A4 portrait; /* or letter */
  margin: 18mm 20mm 20mm 20mm;
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-size: 9pt;
    color: #64748B;
  }
}

body {
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #0F172A; /* Slate 900 */
  background: #FFFFFF;
  margin: 0;
  padding: 0;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* Prevent unwanted page cuts */
h1, h2, h3, h4 {
  break-after: avoid;
  page-break-after: avoid;
  color: #0B0F19;
}

table, figure, pre, .card, .diagram-box, .callout {
  break-inside: avoid;
  page-break-inside: avoid;
}
```

---

## 3. Supported Document Types & Presets

1. **Executive Dossier / Technical Summary (2-3 Pages)**:
   - High-impact layout for engineering interviews and client reviews.
   - Includes: 30s Elevator Pitch, 60s Deep Dive, System Architecture Block Diagram, Hardware Pinout / Power Specs, Performance Benchmarks.
2. **Technical Whitepaper / Research Specification (4-12 Pages)**:
   - IEEE / Silicon Valley two-column or clean single-column format.
   - Abstract, System Architecture, Mathematical Modeling (KaTeX formulas), Experimental Validation, Failure Recovery, References.
3. **ATS-Optimized Engineering Resume (1 Page)**:
   - Single-column high-density layout. Strict font sizing (10pt body, 14pt section heads).
   - Zero multi-column table hacks that confuse ATS parsers.
4. **Digitized Study Notes & Lecture Guides**:
   - Cornell-style margin notes, formula highlight boxes, step-by-step worked examples.

---

## 4. PDF Generation CLI Commands

### Python Command (Recommended):
```bash
python scripts/html_to_pdf.py input.html output.pdf
# Or from Markdown:
python scripts/md_to_pdf.py input.md output.pdf
```

### Direct Edge Headless Command:
```bash
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" \
  --headless \
  --disable-gpu \
  --run-all-compositor-stages-before-draw \
  --print-to-pdf="output.pdf" \
  "input.html"
```
