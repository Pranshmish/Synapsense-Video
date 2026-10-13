# Agent Context: SynapseSense Document & PDF Making System

> **Mission**: This operational manual equips any incoming AI agent or engineer in a new conversation with the complete instructions, design constraints, and script references to generate broadcast-grade vector PDFs (executive dossiers, whitepapers, resumes, study notes) with 100% determinism.

---

## 1. Core Engine Architecture
PDF generation in `Document-Synapsense` does NOT rely on heavy Node packages or broken LaTeX compilers. It uses **Native Microsoft Edge / Chromium Headless** with hardware acceleration disabled and print compositor active:

```bash
# General CLI Command:
python scripts/html_to_pdf.py <input.html> <output.pdf>
python scripts/md_to_pdf.py <input.md> <output.pdf>
```

### Why this is unbeatable:
- **Zero Configuration**: Edge is pre-installed natively on Windows (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`).
- **Full Modern Web Standards**: Flexbox, CSS Grid, `@page` margin boxes, KaTeX math formulas, web fonts (`Inter`, `Segoe UI`, `Roboto`), and SVG graphics.
- **Fast Execution**: Average compilation takes 1.5 to 3 seconds for 200+ DPI vector outputs.

---

## 2. Visual Rules & Typography
- **Primary Body Font**: `Segoe UI`, `Inter`, or `Roboto` (clean sans-serif).
- **Academic / IEEE Research**: `Computer Modern` or `Times New Roman`.
- **Palette**:
  - Headings: Deep Slate (`#0B0F19`, `#0F172A`)
  - Body: Slate 700 (`#334155`)
  - Primary Brand Accent: Deep Cyan (`#0284C7`)
  - Status / Success: Emerald (`#10B981`)
  - Card Fills: `#F8FAFC`, Borders: `#E2E8F0`
- **Page Break Budget**:
  - Resumes: Strictly 1 page.
  - Executive Summaries: Strictly 2 pages.
  - Always enforce: `break-inside: avoid; page-break-inside: avoid;` on cards, tables, callouts, and formulas.

---

## 3. How to Execute Common User Tasks

### Task 1: Generate an Executive Technical Dossier from Markdown
1. Write the technical specifications into a markdown file (`specs.md`) using standard GFM headers, tables, and blockquotes.
2. Run:
   ```bash
   python scripts/md_to_pdf.py specs.md output_dossier.pdf
   ```
3. Verify file size and page layout.

### Task 2: Build a Custom Designed PDF using HTML/CSS Templates
1. Start from one of the battle-tested templates in `templates/`:
   - `executive_dossier_template.html`: For hardware / robotics project summaries.
   - `modern_tech_resume.html`: For single-page ATS-optimized engineering resumes.
   - `cornell_study_notes.html`: For digitized lecture notes, formula sheets, and study guides.
2. Populate the content.
3. Run:
   ```bash
   python scripts/html_to_pdf.py input.html output.pdf
   ```

### Task 3: Transcribe Handwritten Notes to PDF
1. Refer to `.agent/skills/handwritten-notes-to-pdf/SKILL.md`.
2. Inspect the uploaded handwritten image, transcribe text and math into LaTeX/KaTeX, structure into Cornell or textbook format using `templates/cornell_study_notes.html`, and compile to PDF.
