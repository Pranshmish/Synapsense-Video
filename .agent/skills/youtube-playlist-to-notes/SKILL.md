---
name: youtube-playlist-to-notes
description: >
  Convert a YouTube video or playlist (lectures, tutorials, crash courses)
  into structured study notes that preserve the actual diagrams, on-screen
  images, flowcharts, and formulas shown in the video — not just a text
  summary of the transcript. Use this skill whenever the user gives a
  YouTube link/playlist and asks for "notes", "convert this playlist to
  notes", "make a PDF/notes from this video", or reports that diagrams
  came out wrong in a previous attempt. Do NOT rely on transcript text
  alone — transcripts don't contain what's drawn on screen, so this skill
  requires frame capture. Always consult
  references/video-content-extraction.md before pulling content,
  references/diagram-formula-reconstruction.md before handling any visual
  (this is where the previous version fell short — read it fully, don't
  skim), and references/notes-assembly-qa.md before producing the final
  file.
---

# YouTube Playlist → Notes

## Why this skill exists

The transcript alone loses everything drawn, diagrammed, or written on a
whiteboard/slide — which is often the most important content in a
technical video. A notes pipeline that only reads the transcript produces
notes with the right words and missing/wrong diagrams. This skill treats
audio/transcript and on-screen visuals as two separate tracks that must
both be captured and then merged.

## Workflow (do not skip steps)

### 1. Inventory the playlist
- List every video in order, with title and duration.
- Ask the user if they want one notes document per video, or one merged
  document for the whole playlist — this changes the structure step, so
  settle it before doing extraction work.
- If the playlist is long, ask whether to do it in batches rather than
  silently truncating coverage.

### 2. Extract per video (two parallel tracks)
- **Track A — spoken/transcript content**: get the transcript with
  timestamps. See `references/video-content-extraction.md`.
- **Track B — visual content**: identify every timestamp where a new
  diagram, slide, code block, formula, or flowchart appears, and capture
  it properly. See `references/video-content-extraction.md` for timing,
  and `references/diagram-formula-reconstruction.md` for how to actually
  reproduce it well — this is the step that went wrong last time, so
  don't shortcut it.
- Do these per video, not pooled across the whole playlist, so nothing
  gets misattributed to the wrong lecture.

### 3. Merge tracks into draft notes
- Walk the transcript in order; at each point a visual appeared, insert
  the reconstructed diagram/formula/flowchart inline at that point, not
  bunched at the end of the section.
- Preserve the presenter's own structure (their section breaks, numbered
  steps, "first/second/third") rather than reorganizing into a different
  outline.

### 4. Visual quality pass
- Before finalizing, look at every diagram/flowchart/formula you're about
  to include and check it against the quality bar in
  `references/diagram-formula-reconstruction.md`. Anything below that bar
  gets redone (different timestamp, tighter crop, rebuilt as
  mermaid/LaTeX) — never shipped as-is because it's "close enough."

### 5. Assemble and QA
- Follow `references/notes-assembly-qa.md` for structure, per-video
  sectioning, and the final checklist before delivering.

### 6. Hand off
- Tell the user which timestamps had visuals you couldn't capture
  cleanly (fast cuts, low resolution source, presenter's hand blocking
  the board) so they know where to spot-check against the original video.

## Ground rules throughout
- Never summarize a diagram in prose as a substitute for reproducing it —
  a sentence describing a flowchart is not a flowchart.
- Never guess at a formula from context alone if it was also shown
  on-screen — read the actual on-screen version.
- If the same diagram is redrawn progressively (built up step by step),
  capture the final complete version, not an intermediate one — see the
  reconstruction guide for how to find it.
