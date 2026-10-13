# SynapseSense Video Production Suite

> **Official Repository**: [https://github.com/Pranshmish/Synapsense-Video.git](https://github.com/Pranshmish/Synapsense-Video.git)  
> **Aesthetic Standard**: Tier-1 Silicon Valley Keynote Minimalist Crystal (Apple / Google / Linear)  
> **Brand Website**: [synapsense.site](https://synapsense.site)

---

## 1. Overview & Purpose
This repository houses the complete video production, animation, and technical interview demonstration assets for **SynapseSense** hardware and physical-AI systems. 

It is engineered to provide any incoming developer, video editor, or autonomous AI agent with **all skills, design rules, render scripts, and context** required to immediately generate and iterate on broadcast-grade product videos and technical interview kits with zero setup friction.

---

## 2. Repository Structure
```
Videos/
├── .agent/
│   ├── rules/
│   │   ├── synapsense-video-rules.md         # Visual, branding & audio rules
│   │   ├── video-editing.md                  # Video editing standards
│   │   ├── handwritten-notes.md              # Document digitization rules
│   │   └── youtube-playlist-to-notes.md      # Video-to-notes extraction rules
│   └── skills/
│       ├── synapsense-video-production/      # Master keynote video skill
│       ├── video-editing/                    # FFmpeg, Remotion, Fal.ai pipelines
│       ├── handwritten-notes-to-pdf/         # Handwritten scan extraction
│       ├── write-like-human/                 # Natural human copywriting
│       └── youtube-playlist-to-notes/        # Multimodal study notes generator
│
├── Robotic Arm/
│   ├── enhanced_photos/                      # Studio AI product photographs (clean reflections)
│   ├── enhanced_clips/                       # AI-enhanced functioning clips (silent, clean bg)
│   │   ├── robotic_arm_clip_01_pick_and_place.mp4
│   │   ├── robotic_arm_clip_02_macro_gripper_precision.mp4
│   │   ├── robotic_arm_clip_03_6axis_kinematic_articulation.mp4
│   │   └── robotic_arm_clip_04_real_testbench_prototype.mp4
│   ├── media/                                # Raw prototype footage & images
│   ├── Final/
│   │   ├── robotic_arm_physical_ai_showcase_1min.mp4
│   │   └── Project_Robotic_Arm_Technical_Interview_Dossier.md
│   └── render_robotic_arm_showcase.py        # Python/OpenCV/FFmpeg 60 FPS renderer
│
├── Sentinel/
│   ├── Final/
│   │   ├── synapsense_sentinel_crystal_1min.mp4        # SynapseSense client video
│   │   ├── project_sentinel_interview_showcase_1min.mp4 # Technical interview video
│   │   └── Project_Sentinel_Technical_Interview_Dossier.md
│   ├── images/                               # Brand logos & circuit board assets
│   ├── videos-sentinel/                      # Raw demonstration clips
│   └── render_sentinel_crystal.py            # Automated render script
│
├── CONTEXT.md                                # Context ingestion guide for new AI sessions
└── README.md                                 # This file
```

---

## 3. Active Projects

### A. 6-DOF Robotic Manipulator (Physical AI & Kinematics)
- **Domain**: Embedded Motion Control, Real-Time FreeRTOS, Analytical Inverse Kinematics (<15ms), 6-Axis Servo Coordination.
- **Enhanced Studio Assets**:
  - `robotic_arm_studio_1791920937900.jpg`: Neutral studio isolation on white reflective table.
  - `robotic_arm_action_1791920994544.jpg`: Reaching & precision grasping with cyan ambient lighting.
  - `robotic_arm_upright_1791920965692.jpg`: Vertical 6-axis kinematic alignment.
  - `robotic_arm_lab_1791921019325.jpg`: R&D engineering workstation with laptop telemetry.
  - `robotic_arm_pick_blue_cube.jpg`: Active payload hoist of solid blue block.
  - `robotic_arm_macro_red_cube.jpg`: Macro gear-meshing detail of dual-gear claw gripping red cube.
- **Enhanced Video Clips** (`Robotic Arm/enhanced_clips/`):
  - 100% silent (`-an`), all background chatter and room noise removed.
  - No synthetic servo sounds.
  - Smooth camera dollies and studio lighting transitions.

### B. Project Sentinel (Edge AI & IoT Embedded Telemetry)
- **Domain**: On-Device Vision, Low-Power Sensor Fusion, Cloud-Free Edge Inference.
- **Two Distinct Versions**:
  1. **SynapseSense Client Showcase**: Highlights `synapsense.site`, white logo integration, and commercial platform capabilities.
  2. **Technical Interview Showcase**: Anonymized objective engineering demonstration focusing on edge compute, latency, and state machines.

---

## 4. How to Generate New Videos (Workflow for New Sessions)
When creating or modifying videos in a new session:

1. **Read Context First**: Ingest `CONTEXT.md` and `.agent/rules/synapsense-video-rules.md`.
2. **Visual Standard**:
   - Background: Pure porcelain white (`#F8FAFC`).
   - Cards: Glassmorphism (`rgba(255, 255, 255, 0.88)` with `rgba(226, 232, 240, 0.95)` border).
   - Accents: Deep Cyan (`#0284C7`), Electric Cyan (`#00D4FF`), Emerald (`#10B981`).
   - Motion: All movements must use smooth S-curve easing ($S(t) = t^2(3 - 2t)$).
3. **Audio Standard**:
   - Strip phone microphone audio (`-an`).
   - Do NOT add synthetic servo noises or sound effects.
   - For presentation videos, use clean studio narration at ~1.05x speed and soft ambient background music at -24 dB.
4. **Execution**:
   - Write rendering logic in Python utilizing PIL (typography/cards), OpenCV (compositing/blending), and FFmpeg (`stdin` pipe to H.264 MP4).
