# Image Preprocessing for Handwriting OCR

Most "the AI can't read my handwriting" complaints are actually image
quality problems, not recognition problems. Fix the image first.

## Checklist per image

1. **Orientation** — rotate to upright before doing anything else. A
   sideways or upside-down page tanks recognition even if the model
   "understands" rotation conceptually.
2. **Crop tightly** to the page edges. Remove desk, fingers, other pages
   in frame, phone edges. Extra background gives the model irrelevant
   pixels to get distracted by.
3. **One page per image.** If a photo captures two pages of a notebook
   at once, split it into two images before transcribing — trying to
   read both in one pass increases cross-page word-mixing errors.
4. **Lighting**
   - Flag/fix: shadows across the page (a hand or phone blocking light),
     glare/glossy hotspots on the paper, or a photo taken in dim light.
   - If contrast between ink and paper is low, increase contrast —
     but don't over-sharpen to the point pencil strokes fragment into
     dots.
5. **Resolution** — the text should be legible to *you* at 100% zoom.
   If you have to squint or guess at a human level, the model will do
   worse than you, not better. Ask the user for a re-photo of any page
   that fails this test rather than pushing a bad image through.
6. **Ink type matters**
   - Pencil: often low-contrast — boost contrast/exposure specifically
     for these pages.
   - Blue/light-colored pen: sometimes under-detected — a mild
     grayscale + contrast pass helps.
   - Highlighter or colored annotations over text: note that these may
     need to be read as a separate "annotation" layer, not merged into
     the base sentence.
7. **Multi-column or margin notes** — don't flatten these into the main
   text stream. Note their position (e.g., "margin note next to
   paragraph 2") so the transcription guide's structure step can keep
   them distinguishable.

## When to ask the user for a re-shot instead of proceeding

Ask for a better photo rather than transcribing a bad one when:
- More than ~20% of a page is unreadable even after contrast fixes.
- The page is a formula-heavy or diagram-heavy page and any part of the
  diagram/formula is cut off or blurred — these can't be reconstructed
  from context the way prose sometimes can.
- Glare fully whites out a region of text.

It's faster for the student to reshoot one page than for you to guess
wrong on something they'll study from.
