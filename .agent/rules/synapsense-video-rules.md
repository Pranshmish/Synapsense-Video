# SynapseSense Video Production Rules & Guidelines

These rules apply to all video creation, editing, asset generation, and presentation kits created within this workspace.

## 1. Visual Aesthetics & Design System
- **No Cluttered Dark Grids**: Never use pitch-black backgrounds covered in wireframe grids. Use clean, bright, high-key porcelain white (`#F8FAFC`) or subtle titanium grey gradients.
- **Glassmorphism**: Component cards must have clean frosted white fills (`rgba(255, 255, 255, 0.88)`), light subtle borders (`rgba(226, 232, 240, 0.95)`), and soft blurred shadows.
- **Color Palette**:
  - Background: `#F8FAFC` (Porcelain Slate)
  - Dark Headings: `#0F172A` (Slate 900)
  - Body Text: `#334155` (Slate 700)
  - Primary Brand Accent: `#0284C7` (Cyan 600)
  - Secondary Electric Accent: `#00D4FF` (Electric Cyan)
  - Status / Success: `#10B981` (Emerald 500)
- **Typography**: Always use crisp, modern sans-serif fonts (`Segoe UI Bold`, `SF Pro Display`, `Inter`). Ensure strict visual hierarchy between titles, subtitles, and telemetry chips.

## 2. Branding Guidelines
- **SynapseSense Showcase**:
  - Website is strictly `synapsense.site` (NEVER `.in` or `.com`).
  - SynapseSense logo must blend cleanly with the light/white background without dark box artifacts.
  - Do NOT display third-party vendor names (such as RS Components or generic board clones) unless explicitly part of the client spec.
- **Interview & Personal Portfolio Videos**:
  - Do NOT mention SynapseSense or client names when creating personal portfolio / interview demonstration videos.
  - Present the project objectively as an autonomous embedded systems / physical AI / robotics engineering showcase.

## 3. Video Footage & Animation Standards
- **Motion Smoothing**: Never use abrupt cuts or linear easing. All transitions, zoom movements, and telemetry bar graphs must follow S-curve easing ($S(t) = t^2(3 - 2t)$).
- **Resolution & Frame Rate**: Always render at 1920x1080 (1080p Full HD) or 3840x2160 (4K) at 30 FPS or 60 FPS using H.264 High Profile (`crf 18`).
- **Aspect Ratio**: Default to 16:9 for presentations and web showcases, unless mobile 9:16 is specifically requested.

## 4. Audio Processing Constraints
- **Human Voice Removal**: All raw video clips captured on phone microphones must have human chatter, background voices, and ambient room noise 100% stripped (`-an` in FFmpeg).
- **Synthetic Sound Effects**: Do NOT add synthetic servo motor whine or gear sounds unless the user explicitly asks for them.
- **Clean Voiceover**: When adding professional narration, use crystal-clear studio TTS at standard speaking tempo (~1.05x), with low-end rumble rolled off at 80 Hz.
