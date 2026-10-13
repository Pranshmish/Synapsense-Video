# Assembling the Final Notes + QA

## Structure

- **Title/header**: playlist or video title, source link, and duration.
- **Per-video sectioning**: even in a merged playlist document, keep a
  clear heading per video (with a link/timestamp back to the source) so
  the student can locate the original if they need to rewatch something.
- **Table of contents** linking to each video/topic section — essential
  for a merged playlist doc of any real length.
- **Inline visuals**: diagrams/formulas/flowcharts appear at the point in
  the notes that matches where they appeared in the video (per SKILL.md
  step 3) — not collected in an appendix at the end, which breaks the
  connection between explanation and visual.
- **Timestamps on major visuals**: caption each diagram/formula with its
  source timestamp (e.g. "12:34") so the student can jump to that exact
  moment in the video if the reconstruction needs double-checking.

## Content fidelity rules

- Keep the presenter's own terminology and examples — don't substitute
  your own example if theirs illustrates the same point; consistency
  with the video matters for a student cross-referencing both.
- Preserve the presenter's sequence/numbering of steps exactly (Step 1,
  Step 2...) rather than renumbering into a different scheme.
- Don't merge two distinct diagrams/concepts from different timestamps
  into one combined visual, even if they're related — keep the mapping
  one-timestamp-to-one-visual so it stays traceable to the source.

## Final QA pass before delivering

- [ ] Every video in the playlist (or the agreed batch) has a section —
      nothing silently skipped.
- [ ] Every captured visual passed the quality bar in
      `references/diagram-formula-reconstruction.md` — re-check this
      explicitly, don't assume it was done during capture.
- [ ] Formulas render correctly (LaTeX compiles, no broken syntax).
- [ ] Mermaid diagrams render correctly and match source arrow
      directions/labels on a final side-by-side glance.
- [ ] No `[unclear: ...]` flags were silently dropped during assembly —
      they're collected in one place for the handoff.
- [ ] Section order matches video order (or the user's requested order).

## What to tell the student when you deliver it

- The consolidated list of `[unclear: ...]` flags with their source
  timestamps, so they can jump straight to that second of the video and
  confirm.
- Any timestamps where a visual couldn't be captured cleanly at all
  (fast cut, presenter blocking the view for the whole segment) so they
  know exactly what to check manually rather than assuming full
  coverage.
