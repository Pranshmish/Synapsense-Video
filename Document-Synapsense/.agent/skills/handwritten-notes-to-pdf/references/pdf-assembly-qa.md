# Assembling the Final PDF + QA

## Structure

- **Title/header**: subject name, and date range or chapter/topic if the
  student gave one.
- **Table of contents** for anything longer than ~5 pages of source
  material, linking to each topic/page — useful for exam-day skimming.
- **Preserve the student's page-to-page structure** (don't merge two
  distinct source pages into one continuous flowing section if the
  student kept them as separate topics).
- **Diagrams**: embed the cropped, preprocessed source image inline at
  the point it appeared, rather than only describing it in text —
  descriptions are a fallback, not a replacement, when the diagram is
  substantive (graphs, circuits, mechanism drawings, geometry figures).
- **Formulas**: rendered from the LaTeX captured in transcription, not
  re-typed from scratch (avoids re-introducing errors at this stage).
- **Flag list**: a dedicated final section (or the very top) listing
  every `[unclear: ...]` item with a page/topic reference, so the
  student can fix all of them in one pass before exams instead of
  hunting through the document.

## Formatting for exam usability, not just readability

- Consistent heading levels so the student can jump around fast.
- Keep original numbering (Q1, Q2a, etc.) exactly as written — renumbering
  breaks cross-references to a textbook or problem set.
- Don't compress whitespace so much that formulas and diagrams feel
  cramped — these need visual room more than prose does.

## Final QA pass before delivering

Go through the assembled PDF once, side-by-side with the source images,
checking specifically for:

- [ ] Every source image is represented somewhere in the PDF (nothing
      dropped).
- [ ] Page/section order matches what the student specified.
- [ ] Every `[unclear: ...]` flag is still present and now collected in
      the flag list (none silently resolved during assembly).
- [ ] Numbers, signs, and units spot-checked once more against the
      images.
- [ ] Diagrams/tables render correctly (not garbled by the PDF
      generation step itself).
- [ ] Filename is clear and dated/topic-labeled, not "output.pdf".

## What to tell the student when you deliver it

- The flag list, up front, so they know exactly what to double-check.
- Which pages (if any) you couldn't fully read even after preprocessing,
  and what a better source photo would need (per
  `references/image-preprocessing.md`) if they want a fully clean
  re-pass.
