# Rule: YouTube Playlist to Notes Conversion

When converting a YouTube video or playlist to comprehensive study notes and PDFs:
1. Always activate and strictly follow the `youtube-playlist-to-notes` skill workflow.
2. Treat audio/transcript (Track A) and on-screen visuals (Track B) as two separate parallel tracks per video.
3. Apply the visual reconstruction protocol (diagram-formula-reconstruction.md):
   - Recreate flowcharts, block diagrams, circuit schematics, and state graphs as crisp, clean vector graphics (Mermaid/SVG).
   - Embed tightly-cropped high-resolution frames only when exact visual fidelity/uniqueness matters.
   - Strictly verify arrow directions and node labels against the source video.
4. Pass the mandatory Visual Quality Checklist before finalizing:
   - Legible at 100% zoom.
   - All arrows and connections structurally verified.
   - No clipped edges or obscured regions.
   - No silently-invented labels (use [unclear: ...] if ambiguous).
5. Frame capture root cause fix (video-content-extraction.md):
   - Never capture mid-draw or progressive sketch steps.
   - Capture at the timestamp just before moving to the next topic where the diagram is complete.
   - Ensure presenter's hand, body, or cursor is not obstructing any part of the diagram.
6. Design & Branding Rules:
   - NO background watermark.
   - Include running footer: Made by Pranshul Mishra : "Thank me later" with dynamic page numbers.
   - Save output notes and PDFs in `Pranshul/Control/C-notes` using references in `Pranshul/Control/C-ref`.
