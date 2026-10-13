# SynapseSense Document & PDF Suite

> **Part of**: [https://github.com/Pranshmish/Synapsense-Video.git](https://github.com/Pranshmish/Synapsense-Video.git)  
> **Official Domain**: [synapsense.site](https://synapsense.site)  
> **Output Quality**: High-DPI Vector PDFs (Print-Ready, ATS-Optimized, KaTeX Math)

---

## 1. Overview
`Document-Synapsense` is an enterprise-grade document creation and PDF publishing engine designed for engineering teams, technical interview candidates, and researchers.

It allows you to turn raw Markdown files, HTML templates, handwritten notes, and technical dossiers into publication-quality vector PDFs in seconds using native Windows Edge/Chromium Headless with zero fragile dependencies.

---

## 2. Directory Structure
```
Document-Synapsense/
├── .agent/
│   ├── rules/
│   │   ├── synapsense-document-rules.md   # Design, typography & margin rules
│   │   ├── handwritten-notes.md            # Handwritten note transcription standards
│   │   └── resume-cv-rules.md              # ATS formatting & action-verb rules
│   └── skills/
│       ├── synapsense-document-pdf-engine/ # Master PDF compilation skill
│       ├── handwritten-notes-to-pdf/       # Handwriting OCR & transcription pipeline
│       ├── youtube-playlist-to-notes/      # Video tutorial to notes generator
│       └── write-like-human/               # Human-sounding technical copywriting
│
├── scripts/
│   ├── html_to_pdf.py                     # Native Edge headless HTML->PDF printer
│   └── md_to_pdf.py                       # Markdown + KaTeX + tables to styled PDF
│
├── templates/
│   ├── executive_dossier_template.html    # 2-page hardware & AI project dossier
│   ├── modern_tech_resume.html            # 1-page ATS engineering resume
│   └── cornell_study_notes.html           # Structured study notes with formula callouts
│
├── samples/
│   ├── sample_robotic_arm_dossier.pdf     # Pre-compiled sample executive dossier
│   └── Project_Robotic_Arm_Interview_Dossier.pdf # Compiled markdown dossier PDF
│
├── CONTEXT.md                             # AI operating manual for new chat sessions
└── README.md                              # This documentation
```

---

## 3. Quick Start CLI

### Convert Any Markdown Document to PDF:
```bash
python scripts/md_to_pdf.py my_project.md my_project.pdf
```

### Convert Any HTML File to PDF:
```bash
python scripts/html_to_pdf.py templates/executive_dossier_template.html my_dossier.pdf
```

### Custom Page Layouts:
All templates use standard CSS `@page` styling:
```css
@page {
  size: A4 portrait;
  margin: 18mm 20mm 20mm 20mm;
}
```
Tables, diagrams, and callout boxes automatically enforce `break-inside: avoid;` to prevent awkward splits across pages.
