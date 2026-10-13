import os
import sys
import math
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

FFMPEG = r"D:\Espressif\tools\python_env\idf5.3_py3.13_env\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
BASE_DIR = r"c:\Users\ASUS\Desktop\Document\Videos\Robotic Arm"
PHOTOS_DIR = os.path.join(BASE_DIR, "enhanced_photos")
CLIPS_DIR = os.path.join(BASE_DIR, "enhanced_clips")
OUT_DIR = os.path.join(BASE_DIR, "Final")
os.makedirs(OUT_DIR, exist_ok=True)

OUT_VIDEO = os.path.join(OUT_DIR, "robotic_arm_ai_functioning_film.mp4")

WIDTH = 1920
HEIGHT = 1080
FPS = 30

def s_curve(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def fit_full_screen(pil_img, target_w=WIDTH, target_h=HEIGHT):
    """Scale and crop to fill full 16:9 1920x1080 frame cleanly."""
    w, h = pil_img.size
    scale = max(target_w / w, target_h / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = pil_img.resize((nw, nh), Image.Resampling.LANCZOS)
    
    # Center crop to target_w, target_h
    cx = (nw - target_w) // 2
    cy = (nh - target_h) // 2
    cropped = resized.crop((cx, cy, cx + target_w, cy + target_h))
    return cropped

def generate_cinematic_motion(pil_img, num_frames, zoom_start=1.0, zoom_end=1.12, pan_start=(0, 0), pan_end=(0, 0), fade_in=0, fade_out=0):
    """Generate high-end cinematic dolly, slow tracking, and subtle vignette."""
    full_img = fit_full_screen(pil_img)
    w, h = full_img.size
    frames = []

    for i in range(num_frames):
        t = s_curve(i / float(num_frames - 1))
        zoom = zoom_start + (zoom_end - zoom_start) * t
        dx = pan_start[0] + (pan_end[0] - pan_start[0]) * t
        dy = pan_start[1] + (pan_end[1] - pan_start[1]) * t

        crop_w = int(w / zoom)
        crop_h = int(h / zoom)
        cx = int(w / 2 + dx * w)
        cy = int(h / 2 + dy * h)

        x1 = max(0, min(w - crop_w, cx - crop_w // 2))
        y1 = max(0, min(h - crop_h, cy - crop_h // 2))
        x2 = x1 + crop_w
        y2 = y1 + crop_h

        cropped = full_img.crop((x1, y1, x2, y2))
        frame = cropped.resize((w, h), Image.Resampling.BILINEAR)

        np_frame = np.array(frame)

        # Handle fade in / out
        alpha = 1.0
        if fade_in > 0 and i < fade_in:
            alpha = s_curve(i / float(fade_in))
        elif fade_out > 0 and i >= (num_frames - fade_out):
            alpha = s_curve((num_frames - 1 - i) / float(fade_out))

        if alpha < 1.0:
            # Fade to/from clean white studio
            white = np.full_like(np_frame, 255)
            np_frame = cv2.addWeighted(np_frame, alpha, white, 1.0 - alpha, 0)

        frames.append(np_frame)
    return frames

def build_ai_functioning_film():
    print("=== Compiling Cinematic AI Video of Robotic Arm Functioning ===")
    
    # Load all studio photos
    img_studio = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_studio_1791920937900.jpg"))
    img_upright = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_upright_1791920965692.jpg"))
    img_action = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_action_1791920994544.jpg"))
    img_pick = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_pick_blue_cube.jpg"))
    img_macro = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_macro_red_cube.jpg"))
    img_lab = Image.open(os.path.join(PHOTOS_DIR, "robotic_arm_lab_1791921019325.jpg"))
    
    all_film_frames = []

    # Sequence 1: Awakening & Home Stance (0s - 5s = 150 frames)
    # Slow dolly push-in on clean reflective white table
    print("Generating Scene 1: Awakening Stance...")
    s1 = generate_cinematic_motion(img_studio, 150, zoom_start=1.0, zoom_end=1.10, pan_start=(0, 0.02), pan_end=(0.02, -0.01), fade_in=25)
    
    # Sequence 2: Vertical Kinematic Calibration (5s - 10s = 150 frames)
    # Slow vertical pan showing full 6-DOF link extension
    print("Generating Scene 2: 6-Axis Extension...")
    s2 = generate_cinematic_motion(img_upright, 150, zoom_start=1.02, zoom_end=1.14, pan_start=(0, 0.06), pan_end=(0, -0.06))

    # Sequence 3: Reaching Down for Payload (10s - 15s = 150 frames)
    # Dynamic diagonal tracking into the workspace
    print("Generating Scene 3: Trajectory Reach...")
    s3 = generate_cinematic_motion(img_action, 150, zoom_start=1.0, zoom_end=1.12, pan_start=(-0.02, 0), pan_end=(0.04, -0.02))

    # Sequence 4: Autonomous Block Hoist (15s - 20s = 150 frames)
    # Gripper holding blue block, lifting upward in equilibrium
    print("Generating Scene 4: Autonomous Pick & Hoist...")
    s4 = generate_cinematic_motion(img_pick, 150, zoom_start=1.0, zoom_end=1.10, pan_start=(0.03, 0), pan_end=(-0.02, -0.01))

    # Sequence 5: Macro Dual-Gear Claw Actuation (20s - 25s = 150 frames)
    # Extreme close-up on interlocking gears and compliance grip on red cube
    print("Generating Scene 5: Macro Gripper Action...")
    s5 = generate_cinematic_motion(img_macro, 150, zoom_start=1.0, zoom_end=1.15, pan_start=(-0.03, 0), pan_end=(0.03, -0.02))

    # Sequence 6: Modern R&D Testbench Workstation (25s - 30s = 150 frames)
    # Wide cinematic reveal of the full automated workstation with telemetry
    print("Generating Scene 6: Lab Workstation Reveal...")
    s6 = generate_cinematic_motion(img_lab, 150, zoom_start=1.05, zoom_end=1.0, pan_start=(0.02, 0), pan_end=(-0.02, 0), fade_out=30)

    # Cross-dissolve transitions between sequences (20 frames each)
    trans_len = 20
    scenes = [s1, s2, s3, s4, s5, s6]

    for idx, sc in enumerate(scenes):
        if idx == 0:
            all_film_frames.extend(sc[:-trans_len])
        else:
            prev_sc = scenes[idx - 1]
            for i in range(trans_len):
                t = s_curve(i / float(trans_len - 1))
                blend = cv2.addWeighted(prev_sc[-trans_len + i], 1.0 - t, sc[i], t, 0)
                all_film_frames.append(blend)
            if idx < len(scenes) - 1:
                all_film_frames.extend(sc[trans_len:-trans_len])
            else:
                all_film_frames.extend(sc[trans_len:])

    total_frames = len(all_film_frames)
    dur_sec = total_frames / float(FPS)
    print(f"Total film frames: {total_frames} (~{dur_sec:.1f} seconds)")

    # Write out using FFmpeg pipe - Completely Silent (-an), 1080p 60/30fps H.264
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-an",  # Pure video, NO voices, NO synthetic servo whine
        OUT_VIDEO
    ]

    print(f"Encoding to {OUT_VIDEO}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for frame in all_film_frames:
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        proc.stdin.write(bgr.tobytes())
    proc.stdin.close()
    proc.wait()

    if os.path.exists(OUT_VIDEO):
        sz = round(os.path.getsize(OUT_VIDEO) / (1024 * 1024), 2)
        print(f"SUCCESS: AI Video Generated at: {OUT_VIDEO} ({sz} MB, {dur_sec:.1f}s)")
    else:
        print("ERROR: Film was not created.")

if __name__ == "__main__":
    build_ai_functioning_film()
