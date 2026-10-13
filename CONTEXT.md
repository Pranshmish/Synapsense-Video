# Agent Context & Operating Manual: SynapseSense Video Production

> **Purpose**: This document provides incoming AI agents and developers with the complete technical, aesthetic, and architectural context needed to continue producing broadcast-grade showcase videos, physical AI clips, and technical interview packages.

---

## 1. System Identity & Mission
You are working on the **SynapseSense Video Production Suite**. Your goal is to produce world-class product demonstration videos, technical interview companion kits, and AI-enhanced footage of physical AI hardware prototypes.

### Core Quality Benchmarks:
1. **Apple / Google Keynote Minimalist Aesthetic**:
   - Clean, bright porcelain white backgrounds (`#F8FAFC`).
   - Frosted glassmorphism on UI cards and callouts (`rgba(255, 255, 255, 0.88)`).
   - High-contrast slate typography (`#0B0F19`, `#0F172A`).
   - Tech accents: Deep Cyan (`#0284C7`), Electric Cyan (`#00D4FF`), Emerald Status (`#10B981`).
   - Never use dark grid boxes, wireframes, or cluttered hobbyist aesthetics.
2. **Deterministic Motion Graphics**:
   - All animations, camera dollies, zooms, and dissolves MUST use S-curve easing:
     $$\text{Easing}(t) = t^2(3 - 2t) \quad \text{for } t \in [0, 1]$$
   - 30 or 60 FPS output at 1920x1080 (1080p Full HD) or 4K.
3. **Strict Audio Policies**:
   - Phone footage audio MUST ALWAYS be stripped (`-an` in FFmpeg) to remove room chatter, coughs, clicks, and background television noise.
   - **DO NOT synthesize or add artificial servo motor sounds or gear noises** unless explicitly instructed by the user.
   - For presentation videos: use studio TTS narration mixed at -1 dB with soft ambient bed at -24 dB.
4. **Branding Integrity**:
   - SynapseSense website: **`synapsense.site`** (NEVER `.in` or `.com`).
   - SynapseSense logo must blend cleanly with light/white backgrounds.
   - Interview videos: 100% objective, no client branding, presented as engineering work.

---

## 2. Directory Layout & Key Files
- `Sentinel/`:
  - `Final/synapsense_sentinel_crystal_1min.mp4`: Official SynapseSense promotional video.
  - `Final/project_sentinel_interview_showcase_1min.mp4`: Anonymized technical interview showcase.
  - `Final/Project_Sentinel_Technical_Interview_Dossier.md`: Elevator pitches, scripts, and edge AI architecture.
  - `render_sentinel_crystal.py`: Python rendering script.
- `Robotic Arm/`:
  - `enhanced_photos/`: AI studio photos of the 6-DOF robotic arm on white reflective tables.
  - `enhanced_clips/`: Isolated, AI-enhanced functioning video clips (silent, clean studio background, no human hands):
    - `robotic_arm_clip_01_pick_and_place.mp4`
    - `robotic_arm_clip_02_macro_gripper_precision.mp4`
    - `robotic_arm_clip_03_6axis_kinematic_articulation.mp4`
    - `robotic_arm_clip_04_real_testbench_prototype.mp4`
  - `Final/robotic_arm_physical_ai_showcase_1min.mp4`: 60-second physical AI demonstration video.
  - `Final/Project_Robotic_Arm_Technical_Interview_Dossier.md`: Interview presentation kit, kinematics equations, RTOS task specs.
  - `render_robotic_arm_showcase.py`: Render pipeline for the full 60s video.
- `.agent/skills/`:
  - `synapsense-video-production/`: Main video generation and Keynote graphics skill.
  - `video-editing/`: FFmpeg, Remotion, and cutting workflows.
  - `handwritten-notes-to-pdf/`: Note transcription.
  - `youtube-playlist-to-notes/`: Video extraction.
  - `write-like-human/`: Copywriting standards.
- `.agent/rules/`:
  - `synapsense-video-rules.md`: Production, audio, and visual constraints.

---

## 3. How to Execute Work in a New Conversation

### Task A: Generating New AI-Enhanced Studio Photos of Prototypes
1. Locate prototype images in `Robotic Arm/media/` or `Sentinel/images/`.
2. Call `generate_image` with prompt emphasizing:
   - High-end studio lighting, white reflective tabletop, subtle ambient cyan glow, no human hands, razor-sharp focus.
3. Save to `enhanced_photos/`.

### Task B: Creating AI-Enhanced Video Clips of Hardware Moving
1. Create smooth cinematic pan/zoom sequences using S-curve interpolation between functional poses.
2. If using real video footage:
   - Apply center crop to eliminate messy desks or hands.
   - Adjust contrast, brightness, and color saturation via FFmpeg filters.
   - **MUTE AUDIO COMPLETELY (`-an`)**.
3. Save to `enhanced_clips/` and inspect.

### Task C: Rendering a Complete Showcase Video
1. Define the narrative storyboard (5-6 slides: Hero Intro, Architecture, Telemetry, Action Manipulation, Lab Bench, Call to Action).
2. Generate clean TTS audio files with edge-tts or Python TTS.
3. Combine using Python + OpenCV + PIL, piping raw frames directly into FFmpeg H.264 at 30 FPS.
4. Export to `Final/` directory alongside a complete `Technical_Interview_Dossier.md`.

---

## 4. Git Push & Remote Synchronization
- Remote: `https://github.com/Pranshmish/Synapsense-Video.git`
- Branch: `main`
- Run `git status`, stage all scripts, skills, rules, docs, and final video assets, commit with descriptive message, and push.
