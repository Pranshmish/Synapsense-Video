---
name: handwritten-notes-to-pdf
description: >
  Convert photographed handwritten assignments, notes, or exam prep sheets
  into an accurate, clean, well-structured PDF. Use this skill whenever the
  user uploads photos of handwriting, mentions "handwritten notes", "my
  assignment photos", "scan my notes", "convert my notes to PDF", or asks
  for help with an agent misreading their handwriting. This skill exists
  specifically because raw OCR on handwriting is unreliable — do NOT
  transcribe handwriting in a single pass without following this workflow.
  Always consult references/image-preprocessing.md before reading images,
  references/ocr-transcription-guide.md before transcribing, and
  references/pdf-assembly-qa.md before producing the final file.
---

# Handwritten Notes → PDF

## Why this skill exists

Single-pass OCR/VLM reading of handwriting fails silently: it produces
plausible-looking wrong text instead of erroring out. For exam prep, a
wrong formula or a silently dropped negative sign is worse than no notes
at all. This skill forces a slower, checkable pipeline instead of "read
image → dump text → make PDF."

## Workflow (do not skip steps)

### 1. Inventory
- List every image the user provided, in the order they should appear
  (ask the user for the order if it's not obvious — don't guess page order).
- Note subject/topic per image if the user gives it (helps step 3 a lot).
- Flag any image that's blurry, dark, cropped, or rotated *before* doing
  any transcription — see `references/image-preprocessing.md`.

### 2. Preprocess
- Follow `references/image-preprocessing.md` for every image: crop, deskew,
  contrast, split multi-page shots. Don't skip this to save time — bad
  source images are the #1 cause of misread handwriting, not weak OCR.

### 3. Transcribe (the hard part)
- Follow `references/ocr-transcription-guide.md`. Key rule: never silently
  guess an unclear word — mark it `[unclear: best-guess]` and let the user
  confirm rather than presenting a guess as fact.
- Handle math, diagrams, and tables separately from prose text (see the
  guide) — they need different treatment than sentences.
- Do this per-image, not as one giant blob across all images — it's much
  easier to catch errors when each transcription maps cleanly back to one
  source photo.

### 4. Self-check pass
- Before assembling anything, re-open each source image next to your
  transcription and re-read it once more, specifically hunting for:
  numbers, signs (+/−), units, subscripts, and any word you weren't
  fully sure about the first time.
- This second pass catches most remaining errors and is cheap compared to
  redoing a wrong transcription later.

### 5. Assemble the PDF
- Follow `references/pdf-assembly-qa.md` for layout, structure, and the
  final QA checklist before you hand the file to the user.

### 6. Hand off
- Tell the user, in one place, every `[unclear: ...]` flag left in the
  document, so they can fix those from memory in seconds rather than you
  guessing wrong under exam pressure.
- Don't bury this list inside the PDF only — surface it in your reply too.

## Ground rules throughout
- Never invent content to fill a gap (a missing word, a cut-off formula).
  Mark it and move on.
- Preserve the student's own structure (headings, numbering, margin notes)
  rather than "cleaning it up" into a different structure — exam notes are
  often organized the way the student thinks, which matters for recall.
- If a page mixes subjects or is out of order, ask rather than assume.
