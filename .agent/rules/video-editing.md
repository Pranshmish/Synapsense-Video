# Rule: Video Editing Workflow & Principles

When handling video editing, cutting, footage processing, vlog creation, or video augmentation:

1. **Activate the Skill**:
   - Always activate and adhere to the `video-editing` skill workflow.

2. **Core Principle: Compression & Augmentation Over Generation**:
   - Do not attempt to generate entire videos from text prompts.
   - Focus on compressing, structuring, cutting, and augmenting real footage.

3. **Follow the 6-Layer Pipeline**:
   - **Layer 1 (Capture)**: Verify source footage (raw camera recordings, screen captures, audio assets).
   - **Layer 2 (Organization & EDL)**: Transcribe, plan narrative structure, identify dead sections/pauses, and generate explicit Edit Decision Lists (EDL) with exact timestamps (`start`, `end`, `label`).
   - **Layer 3 (Deterministic Cuts via FFmpeg)**:
     - Use FFmpeg for splitting, trimming (`-c copy` when exact keyframe cut is acceptable, or re-encoding if frame-accurate cuts are required).
     - Extract clean audio for speech-to-text / transcription (`pcm_s16le`, 16kHz).
     - Standardize audio loudness using `loudnorm` (e.g. `loudnorm=I=-16:TP=-1.5:LRA=11`).
     - Create editing proxies (`scale=960:-2`, ultrafast, crf 28) for rapid iteration on heavy files.
   - **Layer 4 (Programmable Composition via Remotion)**:
     - Use Remotion for programmatic overlays, lower thirds, titles, animated charts, and reusable scenes.
   - **Layer 5 (Selective Asset Generation)**:
     - Only generate missing assets (voiceover via ElevenLabs, SFX/insert shots via fal.ai/VideoDB). Never replace real footage with AI video unless explicitly directed.
   - **Layer 6 (Human Polish & Taste)**:
     - Pacing adjustments, caption styling, color grade, and final mix.

4. **Safety & Checkpoints**:
   - Always save a versioned checkpoint before making structural cuts or live editor project changes.
   - Keep rendered outputs, editable source project files, and raw media strictly separated.

5. **Multi-Platform Reframing**:
   - Format for target platform: 16:9 (YouTube), 9:16 (Shorts/TikTok/Reels), 1:1 (Feed).
