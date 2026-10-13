# Extracting Content From Video

Two separate extraction jobs. Don't let one stand in for the other.

## Track A: Transcript

1. Pull the transcript with timestamps, not just plain text — you need
   timestamps to align Track B (visuals) to the right point later.
2. If auto-generated captions are the only source, treat technical terms,
   names, and formula-spoken-aloud ("f of x equals...") as
   lower-confidence — cross-check these against on-screen text in Track B
   whenever the same content is also shown visually, since captions
   frequently mis-transcribe jargon.
3. Keep the transcript segmented by natural section breaks (the
   presenter's own "next, let's look at...", chapter markers if the video
   has them) rather than as one unbroken block — this segmentation is
   what you'll hang Track B content on in the merge step.

## Track B: Visual moments

### Finding the right timestamps
1. Scan through the video (or its frame timeline) looking for each point
   where the visible content *changes*: a new slide, a new whiteboard
   diagram, a code editor appearing, a graph being drawn, a formula being
   written.
2. For anything drawn progressively (built up stroke by stroke or step by
   step, e.g. a flowchart added to one box at a time) — do **not** grab
   the first frame you see it in. Find the timestamp just before the
   presenter moves on, where the diagram is at its most complete state.
   Grabbing an early, half-drawn frame is one of the main causes of
   incomplete diagrams.
3. For fast-cut content (slides that appear for only 1-2 seconds), sample
   more densely in that window rather than taking one frame and hoping
   it's not mid-transition (motion blur, half-faded slide).
4. Note the exact timestamp for each capture — you'll need it both for
   Track A alignment and for telling the user where to spot-check.

### Capture quality (read before grabbing frames)
- Grab the highest resolution the source offers. A frame downsampled to
  fit a chat preview is not good enough to embed in final notes — always
  work from the highest-res version available and only downsize (if
  needed at all) at the very final export step.
- If the presenter's hand, cursor, or webcam overlay is covering part of
  the diagram at your chosen timestamp, check a few frames earlier/later
  for a clean unobstructed view of the same complete diagram before
  settling on one.
- If on-screen text is small (dense slide, small whiteboard handwriting),
  crop tightly to that region rather than embedding the whole wide shot —
  see `references/diagram-formula-reconstruction.md` for what to do with
  the crop next.

## What counts as a "visual moment" worth capturing
Capture it if it's any of: a diagram, flowchart, architecture sketch,
graph/plot, table, code block, formula/equation, or a slide with
structured content (bullet hierarchy, comparison table). Don't capture
frames that are just the presenter talking with no informational content
on screen — those add noise without adding notes value.
