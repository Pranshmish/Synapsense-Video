# Reconstructing Diagrams, Flowcharts, and Formulas Well

This is the step that produced weak results before. The fix is: stop
treating every visual the same way, and hold every visual to an explicit
quality bar before it goes in the final notes.

## Decide: recreate vs. embed screenshot

For each captured visual, pick one deliberately — don't defer to whichever
is easiest:

- **Recreate as clean vector (preferred when possible)**: flowcharts,
  simple architecture diagrams, decision trees, sequence diagrams, and
  most graphs with clean structure should be rebuilt as Mermaid diagrams
  (flowchart/sequence/graph syntax) or clean SVG, not left as a photo of
  a whiteboard. A recreated flowchart is crisp at any zoom, matches the
  notes' visual style, and is far more legible than a whiteboard photo.
  - Read every label, arrow direction, and box shape from the captured
    frame carefully before recreating — the recreation must match the
    original exactly, not just "a flowchart with similar boxes." If a
    label is unreadable at full resolution, mark it `[unclear: label]`
    in the recreation rather than inventing plausible text.
- **Embed the actual frame (when recreation would lose information)**:
  complex hand-drawn diagrams with idiosyncratic annotations, real
  photos/screenshots the presenter is showing (a physical device, a UI
  screenshot, a research paper figure), or anything where exact visual
  fidelity matters more than cleanliness. Crop it tightly first (see
  below) — never embed the full wide camera shot with a diagram as a
  small part of it.

## Formulas

- Always transcribe formulas as LaTeX (`$...$` / `$$...$$`), reading them
  directly from the on-screen version — don't derive them from the
  presenter's spoken description, which is often less precise (a
  presenter says "x squared over two" for several different things
  depending on context; the board doesn't lie).
- Preserve exact notation: subscripts, vectors/bold, summation/integral
  bounds, and any custom notation the presenter defines earlier in the
  video (check for a "let X denote..." moment and stay consistent with
  it throughout).
- If a formula is built up across multiple steps (derivation), capture
  the final form as the primary formula and optionally the key
  intermediate steps as a short numbered derivation underneath — don't
  only keep the first or the last line if the middle steps are the point
  of the lesson.

## Flowcharts and diagrams specifically

- Read arrow direction carefully — this is the single most common
  reconstruction error. A→B is not the same note as B→A.
  Verify every arrow in the frame before finalizing the Mermaid/SVG
  version.
- Preserve branch conditions on decision diamonds exactly as labeled
  ("yes/no", "success/fail", specific thresholds) — don't generalize
  them to "condition met/not met."
- Keep the same box shapes where they're semantically meaningful (diamond
  = decision, rectangle = process, etc.) if the presenter used that
  convention — don't flatten everything to plain boxes.

## Quality bar before shipping any visual

Before including a reconstructed or embedded visual in the final notes,
confirm all of these:

- [ ] Every label/word in it is legible at 100% zoom in the final output
      (not just "readable if you squint").
- [ ] Arrow directions and connections match the source exactly.
- [ ] No cropped-off edges — the full diagram is present, not cut off at
      a frame boundary.
- [ ] If recreated: side-by-side comparison with the source frame
      confirms structural match (same number of nodes/branches, same
      relationships).
- [ ] If embedded as an image: resolution is sharp, not blurry/pixelated
      when viewed at the size it'll appear in the notes.
- [ ] Nothing was silently invented to fill an unreadable part — unclear
      elements are flagged, not guessed.

If a visual fails any of these, go back to
`references/video-content-extraction.md` and re-capture at a better
timestamp/crop rather than shipping a weak version to hit a deadline.
