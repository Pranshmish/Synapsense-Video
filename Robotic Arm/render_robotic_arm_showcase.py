import os
import sys
import math
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG = r'D:\Espressif\tools\python_env\idf5.3_py3.13_env\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
MASTER_AUDIO = os.path.join(OUTPUT_DIR, 'master_robotic_arm_audio_60s.wav')
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, 'Final', 'robotic_arm_physical_ai_showcase_1min.mp4')

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 1800  # Exactly 60.00 seconds

# Typography - Keynote Clean Bold Hierarchy
FONT_HERO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 54)
FONT_TITLE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 38)
FONT_HEAD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 25)
FONT_SUB = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
FONT_BODY = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 18)
FONT_BADGE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 14)
FONT_CAPTION = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 21)
FONT_MICRO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 12)

# Palette - Apple/Google Keynote Minimalist Crystal
BG_PORCELAIN = (248, 250, 252)
SLATE_950 = (11, 15, 25)
SLATE_900 = (15, 23, 42)
SLATE_800 = (30, 41, 59)
SLATE_600 = (71, 85, 105)
SLATE_400 = (148, 163, 184)
CYAN_DEEP = (2, 132, 199)
CYAN_GLOW = (56, 189, 248)
CYAN_ELECTRIC = (0, 212, 255)

# Engineering Pill Top Badge Lockup
eng_pill_w = 540
eng_pill_h = 56
engineer_pill = Image.new('RGBA', (eng_pill_w, eng_pill_h), (0, 0, 0, 0))
ep_draw = ImageDraw.Draw(engineer_pill)
ep_draw.rounded_rectangle([0, 0, eng_pill_w, eng_pill_h], radius=22, fill=(255, 255, 255, 248), outline=(56, 189, 248, 180), width=2)
ep_draw.line([(22, 0), (eng_pill_w - 22, 0)], fill=(255, 255, 255, 255), width=2)
ep_draw.ellipse([20, 20, 32, 32], fill=(0, 212, 255, 255))
ep_draw.text((42, 14), '6-DOF ROBOTIC MANIPULATOR', font=FONT_HEAD, fill=SLATE_900)
ep_draw.text((410, 18), '• PHYSICAL AI', font=FONT_BADGE, fill=CYAN_DEEP)

# Load AI-Enhanced Studio Photos
PHOTO_DIR = os.path.join(OUTPUT_DIR, 'enhanced_photos')
photo_studio = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_studio_1791920937900.jpg')).convert('RGBA')
photo_action = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_action_1791920994544.jpg')).convert('RGBA')
photo_upright = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_upright_1791920965692.jpg')).convert('RGBA')
photo_lab = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_lab_1791921019325.jpg')).convert('RGBA')

# Pre-render luminous base background with soft radial blooms
base_bg = Image.new('RGBA', (WIDTH, HEIGHT), (248, 250, 252, 255))
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_layer)
g_draw.ellipse([WIDTH//2 - 680, HEIGHT//2 - 440, WIDTH//2 + 680, HEIGHT//2 + 440], fill=(56, 189, 248, 30))
g_draw.ellipse([WIDTH - 440, -90, WIDTH + 340, 530], fill=(2, 132, 199, 24))
g_draw.ellipse([-200, HEIGHT - 390, 500, HEIGHT + 230], fill=(56, 189, 248, 20))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(130))
base_bg = Image.alpha_composite(base_bg, glow_layer)

# Video Sources from media/
ENHANCED_CLIPS_DIR = os.path.join(OUTPUT_DIR, 'enhanced_clips')
V_PICK_PLACE = os.path.join(ENHANCED_CLIPS_DIR, 'robotic_arm_clip_01_pick_and_place.mp4')
V_MACRO = os.path.join(ENHANCED_CLIPS_DIR, 'robotic_arm_clip_02_macro_gripper_precision.mp4')
V_KINEMATICS = os.path.join(ENHANCED_CLIPS_DIR, 'robotic_arm_clip_03_6axis_kinematic_articulation.mp4')
V_REAL_TESTBENCH = os.path.join(ENHANCED_CLIPS_DIR, 'robotic_arm_clip_04_real_testbench_prototype.mp4')

cap_real = cv2.VideoCapture(V_REAL_TESTBENCH)
cap_kin = cv2.VideoCapture(V_KINEMATICS)
cap_pick = cv2.VideoCapture(V_PICK_PLACE)
cap_macro = cv2.VideoCapture(V_MACRO)

real_fc = int(cap_real.get(cv2.CAP_PROP_FRAME_COUNT))
kin_fc = int(cap_kin.get(cv2.CAP_PROP_FRAME_COUNT))
pick_fc = int(cap_pick.get(cv2.CAP_PROP_FRAME_COUNT))
macro_fc = int(cap_macro.get(cv2.CAP_PROP_FRAME_COUNT))

def get_video_frame(cap, frame_idx, total_count):
    if total_count <= 0:
        return np.full((1024, 576, 3), 240, dtype=np.uint8)
    target = frame_idx % total_count
    cap.set(cv2.CAP_PROP_POS_FRAMES, target)
    ret, frame = cap.read()
    if not ret or frame is None:
        return np.full((1024, 576, 3), 240, dtype=np.uint8)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - math.pow(1.0 - t, 3)

def draw_motion_particles(canvas, f_idx):
    p_draw = ImageDraw.Draw(canvas)
    for i in range(18):
        speed_x = 0.4 + (i % 5) * 0.25
        speed_y = 0.3 + (i % 4) * 0.2
        base_x = (i * 123 + 70) % WIDTH
        base_y = (i * 211 + 45) % HEIGHT
        px = int((base_x + f_idx * speed_x) % (WIDTH + 60) - 30)
        py = int((base_y - f_idx * speed_y) % (HEIGHT + 60) - 30)
        radius = 2 + (i % 3)
        pulse = 0.5 + 0.5 * math.sin(f_idx * 0.08 + i)
        alpha = int(40 + 70 * pulse)
        p_draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=(56, 189, 248, alpha))

def draw_hud_tech_bracket(draw, cx, cy, w, h, col=(56, 189, 248, 180), line_len=20, width=2):
    x0, y0 = cx - w//2, cy - h//2
    x1, y1 = cx + w//2, cy + h//2
    draw.line([(x0, y0), (x0 + line_len, y0)], fill=col, width=width)
    draw.line([(x0, y0), (x0, y0 + line_len)], fill=col, width=width)
    draw.line([(x1, y0), (x1 - line_len, y0)], fill=col, width=width)
    draw.line([(x1, y0), (x1, y0 + line_len)], fill=col, width=width)
    draw.line([(x0, y1), (x0 + line_len, y1)], fill=col, width=width)
    draw.line([(x0, y1), (x0, y1 - line_len)], fill=col, width=width)
    draw.line([(x1, y1), (x1 - line_len, y1)], fill=col, width=width)
    draw.line([(x1, y1), (x1, y1 - line_len)], fill=col, width=width)

def draw_animated_waveform(draw, x0, y, w, f_idx, col=(56, 189, 248, 170)):
    points = []
    num_pts = 32
    step = w / (num_pts - 1)
    for i in range(num_pts):
        px = x0 + i * step
        amp = math.sin(f_idx * 0.18 + i * 0.45) * 8.0 + math.cos(f_idx * 0.28 + i * 0.8) * 5.0
        points.append((px, y + amp))
    draw.line(points, fill=col, width=2)

def draw_kinetic_header(canvas, x, y, title, subtitle, local_frame, anim_delay=0):
    h_draw = ImageDraw.Draw(canvas)
    f_rel = max(0, local_frame - anim_delay)
    prog = ease_out_cubic(min(1.0, f_rel / 22.0))
    dy = int(24 * (1.0 - prog))
    alpha_mul = prog
    
    h_draw.text((x, y + dy), title, font=FONT_HERO, fill=SLATE_900)
    h_draw.text((x, y + 74 + dy), subtitle, font=FONT_HEAD, fill=CYAN_DEEP)
    
    under_w = int(prog * 620)
    h_draw.line([(x, y + 114 + dy), (x + under_w, y + 114 + dy)], fill=(56, 189, 248, int(220 * alpha_mul)), width=3)
    h_draw.line([(x, y + 114 + dy), (x + int(under_w * 0.6), y + 114 + dy)], fill=(255, 255, 255, int(255 * alpha_mul)), width=2)

def draw_crystal_card(target, bbox, title, subtitle, bullets, badge, is_elevated=False, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    if w <= 10 or h <= 10:
        return

_shadow_cache = {}

def get_cached_shadow(w, h, radius=26, fill_color=(15, 23, 42, 34), blur_radius=16):
    key = (w, h, radius, fill_color, blur_radius)
    if key not in _shadow_cache:
        s = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
        sd = ImageDraw.Draw(s)
        sd.rounded_rectangle([30, 30, w + 30, h + 30], radius=radius, fill=fill_color)
        s = s.filter(ImageFilter.GaussianBlur(blur_radius))
        _shadow_cache[key] = s
    return _shadow_cache[key]

def draw_crystal_card(target, bbox, title, subtitle, bullets, badge, is_elevated=False, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    if w <= 10 or h <= 10:
        return

    float_dy = math.sin(f_idx * 0.08) * 4.0 if is_elevated else 0.0
    cy0 = int(y0 + float_dy)

    s_fill = (15, 23, 42, 36 if is_elevated else 20)
    s_blur = 18 if is_elevated else 12
    shadow = get_cached_shadow(w, h, 26, s_fill, s_blur)
    target.alpha_composite(shadow, (int(x0) - 30, cy0 - 15))

    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    card_fill = (255, 255, 255, 248) if is_elevated else (255, 255, 255, 240)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=card_fill)
    
    border_col = (56, 189, 248, 210) if is_elevated else (203, 213, 225, 140)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, outline=border_col, width=2)
    cdraw.line([(26, 0), (w - 26, 0)], fill=(255, 255, 255, 255), width=2)

    # Top Badge Pill
    tbbox = cdraw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = (tbbox[2] - tbbox[0]) + 44
    bh = 32
    bx0, by0 = 26, 24
    cdraw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=16, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=1)
    cdraw.line([(bx0 + 12, by0), (bx0 + bw - 12, by0)], fill=(255, 255, 255, 255), width=1)
    beacon_alpha = int(180 + 75 * math.sin(f_idx * 0.15))
    cdraw.ellipse([bx0 + 14, by0 + 11, bx0 + 22, by0 + 19], fill=(56, 189, 248, beacon_alpha))
    cdraw.text((bx0 + 28, by0 + 7), badge, font=FONT_BADGE, fill=SLATE_900)

    cdraw.text((26, 72), title, font=FONT_HEAD, fill=SLATE_900)
    cdraw.text((26, 108), subtitle, font=FONT_SUB, fill=CYAN_DEEP)

    cy = 154
    for idx, bullet in enumerate(bullets):
        line_start_f = 6 + idx * 10
        if f_idx >= line_start_f:
            line_prog = ease_out_cubic(min(1.0, (f_idx - line_start_f) / 16.0))
            slide_dx = int(22 * (1.0 - line_prog))
            cdraw.ellipse([26 + slide_dx, cy + 6, 36 + slide_dx, cy + 16], fill=CYAN_DEEP)
            cdraw.ellipse([29 + slide_dx, cy + 9, 33 + slide_dx, cy + 13], fill=(255, 255, 255))
            cdraw.text((48 + slide_dx, cy), bullet, font=FONT_BODY, fill=SLATE_800)
        cy += 35

    target.alpha_composite(card, (int(x0), cy0))

def draw_animated_arrow(draw, p1, p2, phase):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([(x1, y1), (x2, y2)], fill=(226, 232, 240, 255), width=6)
    draw.line([(x1, y1), (x2, y2)], fill=(56, 189, 248, 180), width=2)
    if abs(x2 - x1) >= abs(y2 - y1):
        draw.polygon([(x2, y2), (x2 - 16, y2 - 9), (x2 - 16, y2 + 9)], fill=CYAN_DEEP)
    else:
        draw.polygon([(x2, y2), (x2 - 9, y2 - 16), (x2 + 9, y2 - 16)], fill=CYAN_DEEP)

    # Moving pulse dot
    dot_t = (phase % 1.0)
    dx = x1 + (x2 - x1) * dot_t
    dy = y1 + (y2 - y1) * dot_t
    draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(0, 212, 255, 255))

def embed_crystal_video_frame(canvas, vframe_rgb, bbox, hud_text='LIVE FEED', f_idx=0):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0

    # Smooth subtle float
    float_dy = math.sin(f_idx * 0.07) * 3.0
    cy0 = int(y0 + float_dy)
    cy1 = int(y1 + float_dy)

    # Shadow (Cached)
    shadow = get_cached_shadow(w, h, radius=24, fill_color=(15, 23, 42, 38), blur_radius=16)
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

    # Resize video frame to fit container
    vh, vw = vframe_rgb.shape[:2]
    scale = max(w / vw, h / vh)
    nw, nh = int(vw * scale), int(vh * scale)
    v_resized = cv2.resize(vframe_rgb, (nw, nh))
    
    # Crop to exact container size
    cx = (nw - w) // 2
    cy = (nh - h) // 2
    v_cropped = v_resized[cy:cy+h, cx:cx+w]

    v_pil = Image.fromarray(v_cropped).convert('RGBA')

    # Create rounded corner mask
    mask = Image.new('L', (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, w, h], radius=24, fill=255)

    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    card.paste(v_pil, (0, 0), mask)
    cdraw = ImageDraw.Draw(card)

    # Clean glassmorphic overlay border
    cdraw.rounded_rectangle([0, 0, w, h], radius=24, outline=(56, 189, 248, 220), width=3)
    cdraw.line([(24, 0), (w - 24, 0)], fill=(255, 255, 255, 255), width=2)

    # Top HUD Banner
    cdraw.rounded_rectangle([20, 20, 280, 58], radius=16, fill=(15, 23, 42, 210), outline=(56, 189, 248, 180), width=1)
    beacon_pulse = int(180 + 75 * math.sin(f_idx * 0.2))
    cdraw.ellipse([34, 34, 44, 44], fill=(0, 212, 255, beacon_pulse))
    cdraw.text((54, 28), hud_text, font=FONT_BADGE, fill=(255, 255, 255, 255))

    # Bottom Live Telemetry Coordinates
    cdraw.rounded_rectangle([20, h - 68, w - 20, h - 20], radius=16, fill=(15, 23, 42, 220), outline=(56, 189, 248, 160), width=1)
    
    # Animated telemetry string
    t_val = f_idx * 0.05
    x_pos = 180.0 + 15.0 * math.sin(t_val)
    y_pos = -35.0 + 12.0 * math.cos(t_val * 0.8)
    z_pos = 110.0 + 20.0 * math.sin(t_val * 1.2)
    telem_str = f"CLOSED-LOOP POSITION: X={x_pos:+.1f}mm  Y={y_pos:+.1f}mm  Z={z_pos:+.1f}mm"
    cdraw.text((36, h - 56), telem_str, font=FONT_BADGE, fill=(0, 212, 255))
    
    # Tech corner brackets
    draw_hud_tech_bracket(cdraw, w // 2, h // 2, w - 80, h - 80, col=(0, 212, 255, 140))

    canvas.alpha_composite(card, (x0, cy0))

_photo_fit_cache = {}

def embed_glassmorph_photo_card(canvas, photo_rgba, bbox, title, subtitle, callouts=None, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0

    float_dy = math.sin(f_idx * 0.08) * 4.0
    cy0 = int(y0 + float_dy)

    # Shadow (Cached)
    shadow = get_cached_shadow(w, h, radius=26, fill_color=(15, 23, 42, 34), blur_radius=18)
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

    # Base card
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=(255, 255, 255, 248))
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, outline=(56, 189, 248, 200), width=2)
    cdraw.line([(26, 0), (w - 26, 0)], fill=(255, 255, 255, 255), width=2)

    # Header
    cdraw.text((28, 24), title, font=FONT_HEAD, fill=SLATE_900)
    cdraw.text((28, 58), subtitle, font=FONT_BADGE, fill=CYAN_DEEP)

    # Photo content area
    pad_t = 94
    pad_b = 24
    pad_s = 20
    target_w = w - (pad_s * 2)
    target_h = h - pad_t - pad_b

    cache_key = (id(photo_rgba), target_w, target_h)
    if cache_key not in _photo_fit_cache:
        pw, ph = photo_rgba.size
        scale = min(target_w / pw, target_h / ph)
        nw, nh = int(pw * scale), int(ph * scale)
        _photo_fit_cache[cache_key] = (photo_rgba.resize((nw, nh), Image.Resampling.LANCZOS), nw, nh)

    photo_fit, nw, nh = _photo_fit_cache[cache_key]

    px = pad_s + (target_w - nw) // 2
    py = pad_t + (target_h - nh) // 2
    card.alpha_composite(photo_fit, (px, py))

    # Optional Callout pins
    if callouts:
        for cx_ratio, cy_ratio, label, side in callouts:
            cx = px + int(nw * cx_ratio)
            cy = py + int(nh * cy_ratio)
            
            pulse = int(180 + 75 * math.sin(f_idx * 0.15))
            cdraw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(0, 212, 255, pulse))
            cdraw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
            
            pbox = cdraw.textbbox((0, 0), label, font=FONT_MICRO)
            pw_pill = (pbox[2] - pbox[0]) + 20
            ph_pill = 24
            
            if side == 'right':
                bx0 = cx + 24
                bx1 = bx0 + pw_pill
                by0 = cy - ph_pill // 2
                by1 = by0 + ph_pill
                cdraw.line([(cx, cy), (bx0, cy)], fill=(0, 212, 255, 200), width=2)
            else:
                bx1 = cx - 24
                bx0 = bx1 - pw_pill
                by0 = cy - ph_pill // 2
                by1 = by0 + ph_pill
                cdraw.line([(cx, cy), (bx1, cy)], fill=(0, 212, 255, 200), width=2)
                
            cdraw.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(15, 23, 42, 230), outline=(56, 189, 248, 180), width=1)
            cdraw.text((bx0 + 10, by0 + 4), label, font=FONT_MICRO, fill=(255, 255, 255, 255))

    canvas.alpha_composite(card, (x0, cy0))

def draw_caption_bar(canvas, text, f_idx=0):
    c_w = 1760
    c_h = 56
    cx0 = (WIDTH - c_w) // 2
    cy0 = HEIGHT - 76

    card = Image.new('RGBA', (c_w, c_h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, c_w, c_h], radius=20, fill=(255, 255, 255, 248), outline=(56, 189, 248, 170), width=2)
    cdraw.line([(20, 0), (c_w - 20, 0)], fill=(255, 255, 255, 255), width=2)

    beacon_a = int(180 + 75 * math.sin(f_idx * 0.18))
    cdraw.ellipse([24, 22, 34, 32], fill=(0, 212, 255, beacon_a))
    cdraw.text((46, 16), text, font=FONT_CAPTION, fill=SLATE_900)

    # Mini tech wave on right side of caption
    draw_animated_waveform(cdraw, c_w - 240, 28, 180, f_idx, col=(56, 189, 248, 180))

    canvas.alpha_composite(card, (cx0, cy0))

# =============================================================================
# SCENE RENDERING PIPELINE (60.00s @ 30 FPS = 1800 Frames)
# =============================================================================
def render_frame(f_idx):
    canvas = base_bg.copy()
    draw = ImageDraw.Draw(canvas)

    # Background Motion Particles
    draw_motion_particles(canvas, f_idx)

    # Top Brand Bar: 6-DOF Robotic Manipulator Engineering Pill
    if f_idx < 1520:
        nav_dy = int(math.sin(f_idx * 0.05) * 2.0)
        canvas.alpha_composite(engineer_pill, (80, 40 + nav_dy))

    # =========================================================================
    # SCENE 1: 0.0s - 11.0s (Frames 0 to 329) — SYSTEM OVERVIEW & MECHATRONICS
    # =========================================================================
    if f_idx < 330:
        ease_slide = ease_out_cubic(min(1.0, f_idx / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        # Right photo card
        callouts = [
            (0.38, 0.58, 'DUAL-GEAR MECHANICAL CLAW', 'left'),
            (0.72, 0.62, 'HIGH-TORQUE DIGITAL SERVOS', 'right'),
            (0.68, 0.88, 'REINFORCED CNC ALUMINUM BASE', 'right')
        ]
        embed_glassmorph_photo_card(
            canvas,
            photo_studio,
            (1140, 110, 1820, 950),
            '6-DOF HARDWARE MANIPULATOR',
            'Full Physical AI Spatial System',
            callouts,
            f_idx=f_idx
        )

        draw_kinetic_header(canvas, card_x, 140, '6-DOF ROBOTIC MANIPULATOR', 'Autonomous Physical AI & Spatial Motion Architecture', f_idx)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 980, 930),
            '6-AXIS ARTICULATED MANIPULATION',
            'Engineered for High-Precision Trajectory Execution',
            [
                '6-DOF Articulated Spatial Arm with Multi-Link Aluminum Alloy Chassis',
                'High-Torque Metal Gear Digital Servos with Dedicated Current Rail',
                'Deterministic Real-Time Microcontroller Loop Running FreeRTOS',
                'Closed-Loop Spatial Kinematics with Sub-millimeter Target Precision',
                'Dual-Gear Mechanical Gripper End-Effector for Adaptive Payloads'
            ],
            'SYSTEM ARCHITECTURE',
            is_elevated=True,
            f_idx=f_idx
        )

        draw_caption_bar(canvas, '6-DOF Robotic Manipulator: Autonomous physical AI arm engineered for real-time spatial motion.', f_idx=f_idx)

    # =========================================================================
    # SCENE 2: 11.0s - 23.0s (Frames 330 to 689) — EMBEDDED REAL-TIME ACTUATION (REAL FOOTAGE)
    # =========================================================================
    elif f_idx < 690:
        local_f = f_idx - 330
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        # Embedded Video: Real prototype testbench (silent, 16:9 centered crop)
        vframe = get_video_frame(cap_real, local_f, real_fc)
        embed_crystal_video_frame(
            canvas,
            vframe,
            (1120, 110, 1820, 950),
            hud_text='EMBEDDED TESTBENCH LIVE FEED',
            f_idx=local_f
        )

        draw_kinetic_header(canvas, card_x, 140, 'REAL-TIME HARDWARE ACTUATION', 'Embedded Control Firmware & Multi-Channel PWM Generation', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 960, 930),
            'DETERMINISTIC JOINT CONTROL',
            '50 Hz Hardware PWM Driver with S-Curve Smoothing',
            [
                '32-Bit Microcontroller Managing FreeRTOS High-Frequency Tasks',
                'Hardware Timer PWM Serialization Across 6 Independent Channels',
                'Dynamic Trajectory S-Curve Smoothing to Eliminate Inertial Oscillation',
                'Dedicated Power Distribution with Over-Current & Stall Detection',
                'Bi-Directional Telemetry Dashboard for Real-Time Pose Monitoring'
            ],
            'EMBEDDED FIRMWARE',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Embedded 32-bit controller drives six independent high-torque servos with microsecond PWM determinism.', f_idx=local_f)

    # =========================================================================
    # SCENE 3: 23.0s - 36.0s (Frames 690 to 1079) — KINEMATICS & MOTION FLOWCHART
    # =========================================================================
    elif f_idx < 1080:
        local_f = f_idx - 690
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))

        draw_kinetic_header(canvas, 100, 136, 'KINEMATICS & MOTION PIPELINE', 'Analytical Forward & Inverse Kinematics Architecture', local_f)

        # Interactive Kinematics Flowchart (5 Columns)
        flow_y = 280
        col_w = 320
        col_h = 190
        gap = 36
        x_start = 100

        flow_steps = [
            ('CARTESIAN TARGET', 'Spatial Pose Input', 'X, Y, Z, Roll, Pitch, Yaw\nTarget Goal Vector'),
            ('DH TRANSFORM', 'Forward Kinematics', 'Denavit-Hartenberg Matrices\nLink Frame Rotations'),
            ('INVERSE KINEMATICS', 'Analytical Solver', '< 15ms Analytical Convergence\nMulti-Joint Coordinate Map'),
            ('S-CURVE INTERPOLATOR', 'Trajectory Smoothing', 'Cubic Spline Velocity Profiling\nInertia Jerk Suppression'),
            ('PWM TIMER DRIVER', 'Hardware Output', '50 Hz Hardware Timers\nDirect Servo Angle Actuation')
        ]

        for i, (f_title, f_sub, f_desc) in enumerate(flow_steps):
            fx = x_start + i * (col_w + gap)
            f_card = Image.new('RGBA', (col_w, col_h), (0, 0, 0, 0))
            f_cdraw = ImageDraw.Draw(f_card)
            
            f_cdraw.rounded_rectangle([0, 0, col_w, col_h], radius=20, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=2)
            f_cdraw.line([(20, 0), (col_w - 20, 0)], fill=(255, 255, 255, 255), width=2)
            
            # Step pill
            step_badge = f'STAGE 0{i+1}'
            f_cdraw.rounded_rectangle([18, 16, 110, 42], radius=12, fill=(15, 23, 42, 230))
            f_cdraw.text((28, 20), step_badge, font=FONT_MICRO, fill=(0, 212, 255))
            
            f_cdraw.text((18, 54), f_title, font=FONT_BADGE, fill=SLATE_900)
            f_cdraw.text((18, 80), f_sub, font=FONT_MICRO, fill=CYAN_DEEP)
            f_cdraw.text((18, 108), f_desc, font=FONT_MICRO, fill=SLATE_800)
            
            canvas.alpha_composite(f_card, (fx, flow_y))

            # Flow arrow to next stage
            if i < len(flow_steps) - 1:
                p1 = (fx + col_w, flow_y + col_h // 2)
                p2 = (fx + col_w + gap, flow_y + col_h // 2)
                draw_animated_arrow(draw, p1, p2, phase=local_f * 0.08 + i * 0.2)

        # Lower Split: Left side live joint telemetry card, Right side real dynamic articulation video
        # Lower Left Card: Joint Angles Telemetry
        j_card = Image.new('RGBA', (820, 420), (0, 0, 0, 0))
        j_draw = ImageDraw.Draw(j_card)
        j_draw.rounded_rectangle([0, 0, 820, 420], radius=24, fill=(255, 255, 255, 248), outline=(56, 189, 248, 190), width=2)
        j_draw.line([(24, 0), (820 - 24, 0)], fill=(255, 255, 255, 255), width=2)
        
        j_draw.rounded_rectangle([24, 20, 280, 56], radius=16, fill=(15, 23, 42, 220))
        j_draw.text((44, 28), 'REAL-TIME KINEMATIC SOLVER', font=FONT_BADGE, fill=(0, 212, 255))
        j_draw.text((24, 86), 'ANALYTICAL JOINT TRANSFORMATIONS', font=FONT_HEAD, fill=SLATE_900)
        
        # 6 Joint Readouts
        joints = [
            ('θ1 Base Yaw', f"{42.5 + 10.0*math.sin(local_f*0.06):+.1f}°", 'PWM: 1620 µs'),
            ('θ2 Shoulder Pitch', f"{-18.2 + 8.0*math.cos(local_f*0.05):+.1f}°", 'PWM: 1340 µs'),
            ('θ3 Elbow Pitch', f"{64.0 + 12.0*math.sin(local_f*0.07):+.1f}°", 'PWM: 1850 µs'),
            ('θ4 Wrist Pitch', f"{-45.8 + 6.0*math.cos(local_f*0.06):+.1f}°", 'PWM: 1120 µs'),
            ('θ5 Wrist Roll', f"{12.4 + 15.0*math.sin(local_f*0.04):+.1f}°", 'PWM: 1510 µs'),
            ('θ6 Claw Gripper', 'ENGAGED [1.8 N·m]', 'PWM: 1900 µs')
        ]
        
        for ji, (jname, jangle, jpwm) in enumerate(joints):
            row_y = 136 + ji * 44
            col_x1 = 28
            col_x2 = 420
            target_x = col_x1 if ji < 3 else col_x2
            target_y = 136 + (ji % 3) * 85
            
            j_draw.rounded_rectangle([target_x, target_y, target_x + 370, target_y + 70], radius=14, fill=(248, 250, 252, 240), outline=(226, 232, 240, 255), width=1)
            j_draw.text((target_x + 16, target_y + 12), jname, font=FONT_BODY, fill=SLATE_900)
            j_draw.text((target_x + 16, target_y + 40), jpwm, font=FONT_MICRO, fill=SLATE_600)
            j_draw.text((target_x + 220, target_y + 18), jangle, font=FONT_HEAD, fill=CYAN_DEEP)

        canvas.alpha_composite(j_card, (100, 510))

        # Lower Right: AI-Enhanced Kinematic Articulation Video
        vframe_dyn = get_video_frame(cap_kin, local_f, kin_fc)
        embed_crystal_video_frame(
            canvas,
            vframe_dyn,
            (960, 510, 1820, 930),
            hud_text='KINEMATIC MOTION EXECUTION',
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Analytical inverse kinematics engine computes multi-axis joint angles in under 15ms, executing smooth cubic spline trajectories.', f_idx=local_f)

    # =========================================================================
    # SCENE 4: 36.0s - 49.0s (Frames 1080 to 1469) — ADAPTIVE MANIPULATION & BLOCKS
    # =========================================================================
    elif f_idx < 1470:
        local_f = f_idx - 1080
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        # Right video card: AI-Enhanced Studio Pick & Place and Macro Grasp
        if local_f < 200:
            vframe_blocks = get_video_frame(cap_pick, local_f, pick_fc)
        else:
            vframe_blocks = get_video_frame(cap_macro, local_f - 200, macro_fc)
        embed_crystal_video_frame(
            canvas,
            vframe_blocks,
            (1120, 110, 1820, 950),
            hud_text='AUTONOMOUS PICK & PLACE',
            f_idx=local_f
        )

        draw_kinetic_header(canvas, card_x, 140, 'ADAPTIVE OBJECT MANIPULATION', 'Autonomous Pick-and-Place & Computer Vision Integration', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 960, 930),
            'AUTONOMOUS PICK-AND-PLACE',
            'Spatial Registration & Compliance Gripping',
            [
                'Dual-Gear Mechanical Gripper Delivering Proportional Clamping Force',
                'Spatial Coordinates Streamed via Low-Latency Serial / Optical Link',
                'Closed-Loop Trajectory Convergence with Dynamic Target Re-planning',
                'Sub-Millimeter Repeatability Across 500+ Continuous Automated Cycles',
                'Zero Human Intervention • 100% Autonomous Edge Motion Execution'
            ],
            'PAYLOAD MANIPULATION',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Mechanical end-effector provides adaptive compliant grasping, executing autonomous pick-and-place routines with high repeatability.', f_idx=local_f)

    # =========================================================================
    # SCENE 5: 49.0s - 60.0s (Frames 1470 to 1799) — HERO SUMMARY & PORTFOLIO METRICS
    # =========================================================================
    else:
        local_f = f_idx - 1470
        ease_prog = ease_out_cubic(min(1.0, local_f / 24.0))

        # Centered Kinetic Header
        header_y = int(60 + (80 - 60) * ease_prog)
        h_draw = ImageDraw.Draw(canvas)
        title_text = "6-DOF ROBOTIC MANIPULATOR"
        sub_text = "Autonomous Physical AI System Architecture • Embedded Mechatronics Portfolio"

        t_box = h_draw.textbbox((0, 0), title_text, font=FONT_HERO)
        tw = t_box[2] - t_box[0]
        h_draw.text(((WIDTH - tw) // 2, header_y), title_text, font=FONT_HERO, fill=SLATE_900)

        s_box = h_draw.textbbox((0, 0), sub_text, font=FONT_HEAD)
        sw = s_box[2] - s_box[0]
        h_draw.text(((WIDTH - sw) // 2, header_y + 70), sub_text, font=FONT_HEAD, fill=CYAN_DEEP)

        under_w = int(ease_prog * 860)
        h_draw.line([((WIDTH - under_w)//2, header_y + 112), ((WIDTH + under_w)//2, header_y + 112)], fill=(56, 189, 248, 220), width=3)

        # Center Hero Card with Modern R&D Testbench Render
        embed_glassmorph_photo_card(
            canvas,
            photo_lab,
            (460, 230, 1460, 750),
            'PRODUCTION-READY TESTBENCH',
            'Full Physical AI System Integration',
            None,
            f_idx=local_f
        )

        # 4 High-Tech KPI Metric Tiles
        kpis = [
            ('6-DOF', 'Spatial Dexterity', 'Full Articulated Range'),
            ('50 Hz', 'PWM Update Loop', 'Microsecond Precision'),
            ('< 15ms', 'IK Solve Latency', 'Analytical Convergence'),
            ('100%', 'Embedded Control', 'Zero Cloud Dependency')
        ]

        tile_y = 780
        tile_w = 380
        tile_h = 135
        tile_gap = 40
        tile_x_start = (WIDTH - (4 * tile_w + 3 * tile_gap)) // 2

        for ki, (kval, klabel, kdesc) in enumerate(kpis):
            tx = tile_x_start + ki * (tile_w + tile_gap)
            t_card = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))
            tdraw = ImageDraw.Draw(t_card)
            
            tdraw.rounded_rectangle([0, 0, tile_w, tile_h], radius=20, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=2)
            tdraw.line([(20, 0), (tile_w - 20, 0)], fill=(255, 255, 255, 255), width=2)
            
            tdraw.text((22, 14), kval, font=FONT_TITLE, fill=SLATE_900)
            tdraw.text((22, 60), klabel, font=FONT_BADGE, fill=CYAN_DEEP)
            tdraw.text((22, 88), kdesc, font=FONT_MICRO, fill=SLATE_600)
            
            canvas.alpha_composite(t_card, (tx, tile_y))

        # Bottom Call to Action
        call_action = "PORTFOLIO PROJECT • EMBEDDED SYSTEMS & PHYSICAL AI ROBOTICS"
        draw_caption_bar(canvas, call_action, f_idx=local_f)

    # Convert PIL RGBA to RGB numpy array for FFmpeg
    return np.array(canvas.convert('RGB'))

def main():
    print(f"=== Starting 6-DOF Robotic Arm Showcase Video Render ===")
    print(f"Resolution: {WIDTH}x{HEIGHT} @ {FPS} FPS | Duration: 60.00s ({TOTAL_FRAMES} frames)")
    print(f"Master Audio: {MASTER_AUDIO}")
    print(f"Output Video: {OUTPUT_VIDEO}")

    cmd = [
        FFMPEG,
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{WIDTH}x{HEIGHT}',
        '-pix_fmt', 'rgb24',
        '-r', str(FPS),
        '-i', '-',
        '-i', MASTER_AUDIO,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        OUTPUT_VIDEO
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    try:
        for f in range(TOTAL_FRAMES):
            frame_rgb = render_frame(f)
            proc.stdin.write(frame_rgb.tobytes())
            if f % 150 == 0 or f == TOTAL_FRAMES - 1:
                print(f"Rendered frame {f}/{TOTAL_FRAMES} ({(f/TOTAL_FRAMES*100):.1f}%)")
    except Exception as e:
        print(f"Error during render: {e}")
        proc.kill()
        sys.exit(1)
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.wait()

    cap_real.release()
    cap_kin.release()
    cap_pick.release()
    cap_macro.release()

    if os.path.exists(OUTPUT_VIDEO):
        v_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"SUCCESS: Rendered final video to {OUTPUT_VIDEO} ({v_size_mb:.2f} MB)")
    else:
        print("ERROR: Output video was not created.")

if __name__ == '__main__':
    main()
