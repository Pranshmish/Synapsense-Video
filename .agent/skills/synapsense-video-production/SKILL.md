---
name: synapsense-video-production
description: Master skill for producing Apple/Google keynote-caliber showcase videos, physical AI & robotics demonstrations, and technical interview presentation kits.
---

# SynapseSense Video Production & Motion Graphics Skill

## 1. Core Philosophy & Aesthetic Principles
All videos produced under this pipeline follow a **Tier-1 Silicon Valley Keynote Aesthetic** (Apple, Google, Humane, Linear):
- **Lighting & Ambiance**: Clean porcelain white backdrop (`#F8FAFC` to `#F1F5F9`), studio high-key illumination, subtle ambient cyan/glow accents (`#00D4FF`, `#38BDF8`).
- **Surface Physics**: Ultra-clean reflective studio tables with soft contact ground shadows (Gaussian blur $\sigma=15$, opacity 18-25%).
- **Component Styling**: Glassmorphic frosted cards (`rgba(255, 255, 255, 0.85)` with `1px solid rgba(226, 232, 240, 0.9)` borders and subtle drop shadows).
- **Typography Hierarchy**: Segoe UI Bold / Apple SF Pro Display:
  - Hero Titles: 54pt bold slate-950 (`#0B0F19`)
  - Section Headers: 38pt bold slate-900 (`#0F172A`)
  - Subheaders / Accent: 24pt cyan deep (`#0284C7`)
  - Technical Metrics / Code: 18pt Segoe UI / Monospace slate-700
- **Motion Dynamics**: Zero linear robotic cuts. Every motion uses cubic Hermite / S-curve interpolation ($S(t) = t^2(3 - 2t)$) for smooth acceleration and deceleration.

---

## 2. Asset Preparation & AI Studio Enhancement
Raw smartphone footage from lab benches and prototype desks is usually messy, with poor lighting, cluttered wires, and unwanted background objects.

### Step 1: Studio Photo Generation
To obtain pristine product isolation matching official hardware marketing:
1. Use `generate_image` referencing the prototype photo.
2. Prompt formula:
   > *"Cinematic high-end studio product photograph of the identical [device description] with [exact components, brackets, wires]. Placed on a pristine white glossy reflective surface in a minimalist Apple-style tech commercial environment. Soft daylight studio lighting, clean reflections, zero clutter, no human hands, razor-sharp focus."*

### Step 2: High-Quality Background Removal (BiRefNet / u2net)
When isolating video frames:
- Use `rembg` with `birefnet-general-lite` for fine mechanical edges and wiring.
- If processing real-time video clips, run `u2net` at 640x360 or crop the region of interest first to prevent memory bottlenecks.
- Composite onto pure white studio background with synthetic soft contact shadow.

---

## 3. Video Rendering Engine Architecture
All high-fidelity motion graphics are built using an optimized Python pipeline:
- **Renderer**: `PIL (Pillow)` for antialiased typography and vector shape rendering.
- **Image Processing**: `OpenCV (cv2)` for color grading, alpha blending, and cross-dissolves.
- **Video Encoder**: `FFmpeg` piped via `stdin` in raw `bgr24` or `yuv420p` format.
- **Specifications**: 1920x1080 (Full HD) @ 30 FPS or 60 FPS, H.264 profile High, CRF 18 (visually lossless).

### Core Pipeline Script Template:
```python
import subprocess, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

FFMPEG = "path/to/ffmpeg.exe"
WIDTH, HEIGHT, FPS = 1920, 1080, 30

def s_curve(t):
    return t * t * (3.0 - 2.0 * t)

# Stream frames directly to ffmpeg pipe without intermediate disk writes
cmd = [
    FFMPEG, "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "bgr24", "-r", str(FPS),
    "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-pix_fmt", "yuv420p", "-an", "output.mp4"
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
# Write frames in cv2 BGR format
# proc.stdin.write(frame_bgr.tobytes())
```

---

## 4. Audio Production Guidelines
Audio must be clean, deterministic, and distraction-free:
1. **Raw Video Audio**: ALWAYS strip raw microphone audio containing human voices, room chatter, background noise, or clicks (`-an` in FFmpeg).
2. **Servo Sounds**: DO NOT synthesize or inject artificial servo whine or gear buzz unless the client explicitly requests it.
3. **Narration**: Use studio-quality text-to-speech with natural cadence (~1.05x rate), clean low-cut filter at 80 Hz, and peak limiting at -1.0 dB.
4. **Ambient Music**: Soft, uplifting minimalist tech corporate soundtrack mixed at -22 dB to -26 dB under spoken narration.

---

## 5. Technical Interview & Portfolio Companion Kits
Every completed project video MUST be accompanied by a comprehensive technical interview dossier (`Project_*_Technical_Interview_Dossier.md`) covering:
- **30-Second Elevator Pitch**: High-impact summary of architecture, speed, and real-world results.
- **60-Second Deep-Dive Pitch**: Kinematic equations, firmware tasks, hardware power rails, and edge latency.
- **Screen-Share Video Script**: Exact timestamp-synchronized visual cues and spoken talking points.
- **System Architecture Diagrams**: Flowcharts, state machines, and hardware wiring schematics in Mermaid format.
- **Anticipated Interview Q&A**: Deep technical questions on inverse kinematics singularities, RTOS task priorities, ADC filtering, and failure recovery.
