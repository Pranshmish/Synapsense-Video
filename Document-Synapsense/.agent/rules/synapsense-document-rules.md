# SynapseSense Document & PDF Making Rules

These rules govern the creation, styling, and compilation of all PDF documents, whitepapers, dossiers, and resumes in the SynapseSense ecosystem.

## 1. Visual Hierarchy & Typography
- **Primary Body Font**: Use `Segoe UI`, `Inter`, or `Roboto` for tech specs and dossiers; use `Times New Roman` or `Computer Modern` for academic research papers.
- **Font Sizes**:
  - Document Title: 24pt - 28pt Bold (`#0B0F19`)
  - Section Headings (H1): 16pt - 18pt Bold (`#0F172A`)
  - Subheadings (H2): 12pt - 14pt Semi-Bold (`#1E293B`)
  - Body Text: 9.5pt - 10.5pt Regular (`#334155`)
  - Captions, Footnotes, Metadata: 8pt - 9pt (`#64748B`)
- **Line Height**: Maintain `1.45` to `1.55` line height for readability without wasting vertical page space.

## 2. Page Budgeting & Break Control
- **Strict Target Page Counts**:
  - Resumes: Strictly 1 page (unless senior 10+ years experience, then strictly 2 pages). Never leave 3 lines spilling onto a blank second page.
  - Executive Dossiers: Strictly 2 pages or strictly 3 pages.
- **Page Break Rules**:
  - Always enforce `break-inside: avoid;` on tables, cards, callout boxes, and code blocks.
  - Never allow a heading to sit as the last line on a page (`break-after: avoid;`).
  - Maintain consistent 18mm - 20mm margins on all 4 sides.

## 3. Brand & Professional Identity
- **Website Reference**: Always refer to the official company domain as **`synapsense.site`** (NEVER `.in` or `.com`).
- **Logo Integration**: Logos must be cleanly rendered SVGs or transparent high-DPI PNGs blending smoothly with the document header.
- **Color Palette**:
  - Primary Accent: `#0284C7` (Cyan 600)
  - Secondary Glow: `#00D4FF` (Electric Cyan)
  - Dark Headings: `#0F172A` (Slate 900)
  - Card Backgrounds: `#F8FAFC` (Slate 50)
  - Border Lines: `#E2E8F0` (Slate 200)

## 4. Mathematical & Code Precision
- **KaTeX Equations**: Use display math `$$ ... $$` for standalone equations, centered with equation numbers on the right. Inline math `$ ... $` must use non-breaking spaces before units (e.g., `$50\text{ Hz}$`, `$15\text{ ms}$`).
- **Code Listings**: Use monospace font (`Consolas`, `JetBrains Mono`, `Fira Code`) at 8.5pt with light grey background (`#F1F5F9`), subtle 1px border, and syntax highlighting.
