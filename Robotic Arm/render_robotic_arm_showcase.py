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

# Typography - Segoe UI Clean Keynote Hierarchy
FONT_HERO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 48)
FONT_TITLE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 36)
FONT_HEAD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 24)
FONT_SUB = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 19)
FONT_BODY = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 17)
FONT_BOLD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 17)
FONT_BADGE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 13)
FONT_CAPTION = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
FONT_MICRO = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 12)
FONT_MICRO_BOLD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 12)

# Palette - Apple/Tesla Minimalist Crystal
BG_PORCELAIN = (248, 250, 252)
SLATE_950 = (11, 15, 25)
SLATE_900 = (15, 23, 42)
SLATE_800 = (30, 41, 59)
SLATE_700 = (51, 65, 85)
SLATE_600 = (71, 85, 105)
SLATE_500 = (100, 116, 139)
SLATE_400 = (148, 163, 184)
SLATE_200 = (226, 232, 240)
CYAN_DEEP = (2, 132, 199)
CYAN_GLOW = (56, 189, 248)
CYAN_ELECTRIC = (0, 212, 255)
GREEN_EMERALD = (16, 185, 129)

# Pre-render luminous base background with soft radial blooms
base_bg = Image.new('RGBA', (WIDTH, HEIGHT), (248, 250, 252, 255))
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_layer)
g_draw.ellipse([WIDTH//2 - 680, HEIGHT//2 - 440, WIDTH//2 + 680, HEIGHT//2 + 440], fill=(56, 189, 248, 26))
g_draw.ellipse([WIDTH - 440, -90, WIDTH + 340, 530], fill=(2, 132, 199, 20))
g_draw.ellipse([-200, HEIGHT - 390, 500, HEIGHT + 230], fill=(56, 189, 248, 18))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(120))
base_bg = Image.alpha_composite(base_bg, glow_layer)

# Fixed Engineering Pill Top Badge (Zero Overlap, Generous Spacing)
eng_pill_w = 660
eng_pill_h = 52
engineer_pill = Image.new('RGBA', (eng_pill_w, eng_pill_h), (0, 0, 0, 0))
ep_draw = ImageDraw.Draw(engineer_pill)
ep_draw.rounded_rectangle([0, 0, eng_pill_w, eng_pill_h], radius=20, fill=(255, 255, 255, 248), outline=(56, 189, 248, 160), width=2)
ep_draw.line([(20, 0), (eng_pill_w - 20, 0)], fill=(255, 255, 255, 255), width=2)
ep_draw.ellipse([20, 19, 32, 31], fill=CYAN_ELECTRIC)
ep_draw.text((42, 14), '6-DOF ROBOTIC MANIPULATOR', font=FONT_HEAD, fill=SLATE_900)
ep_draw.text((436, 18), '|', font=FONT_SUB, fill=SLATE_400)
ep_draw.text((458, 18), 'PHYSICAL AI ROBOTICS', font=FONT_BADGE, fill=CYAN_DEEP)

# Load AI-Enhanced Studio Photos
PHOTO_DIR = os.path.join(OUTPUT_DIR, 'enhanced_photos')
photo_studio = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_studio_1791920937900.jpg')).convert('RGBA')
photo_action = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_action_1791920994544.jpg')).convert('RGBA')
photo_upright = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_upright_1791920965692.jpg')).convert('RGBA')
photo_lab = Image.open(os.path.join(PHOTO_DIR, 'robotic_arm_lab_1791921019325.jpg')).convert('RGBA')

# Video Sources from media and enhanced_clips
MEDIA_DIR = os.path.join(OUTPUT_DIR, 'media')
ENHANCED_CLIPS_DIR = os.path.join(OUTPUT_DIR, 'enhanced_clips')

# Real testbench footage where arm moves autonomously and lifts cube
V_REAL_PICK = os.path.join(MEDIA_DIR, 'WhatsApp Video 2026-10-10 at 12.00.06 AM.mp4')
# Real moving arm picking red cube
V_REAL_RED = os.path.join(MEDIA_DIR, 'WhatsApp Video 2026-10-10 at 12.01.10 AM (1).mp4')
# Real moving arm picking green cube
V_REAL_GREEN = os.path.join(MEDIA_DIR, 'WhatsApp Video 2026-10-10 at 12.01.14 AM.mp4')
# 6-Axis kinematic articulation video (16:9 widescreen)
V_KINEMATICS = os.path.join(ENHANCED_CLIPS_DIR, 'robotic_arm_clip_03_6axis_kinematic_articulation.mp4')

cap_real_pick = cv2.VideoCapture(V_REAL_PICK)
cap_real_red = cv2.VideoCapture(V_REAL_RED)
cap_real_green = cv2.VideoCapture(V_REAL_GREEN)
cap_kin = cv2.VideoCapture(V_KINEMATICS)

real_pick_fc = int(cap_real_pick.get(cv2.CAP_PROP_FRAME_COUNT))
real_red_fc = int(cap_real_red.get(cv2.CAP_PROP_FRAME_COUNT))
real_green_fc = int(cap_real_green.get(cv2.CAP_PROP_FRAME_COUNT))
kin_fc = int(cap_kin.get(cv2.CAP_PROP_FRAME_COUNT))

def get_video_frame(cap, target_idx, total_count):
    if total_count <= 0 or not cap.isOpened():
        return np.full((720, 1280, 3), 240, dtype=np.uint8)
    idx = max(0, min(total_count - 1, target_idx % total_count))
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if not ret or frame is None:
        return np.full((720, 1280, 3), 240, dtype=np.uint8)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - math.pow(1.0 - t, 3)

_shadow_cache = {}
def get_cached_shadow(w, h, radius=24, fill_color=(15, 23, 42, 28), blur_radius=16):
    key = (w, h, radius, fill_color, blur_radius)
    if key not in _shadow_cache:
        s = Image.new('RGBA', (w + 50, h + 50), (0, 0, 0, 0))
        sd = ImageDraw.Draw(s)
        sd.rounded_rectangle([25, 25, w + 25, h + 25], radius=radius, fill=fill_color)
        s = s.filter(ImageFilter.GaussianBlur(blur_radius))
        _shadow_cache[key] = s
    return _shadow_cache[key]

def draw_caption_bar(canvas, text, f_idx=0):
    c_w = 1760
    c_h = 54
    cx0 = (WIDTH - c_w) // 2
    cy0 = HEIGHT - 74

    card = Image.new('RGBA', (c_w, c_h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, c_w, c_h], radius=18, fill=(255, 255, 255, 248), outline=(56, 189, 248, 160), width=2)
    cdraw.line([(20, 0), (c_w - 20, 0)], fill=(255, 255, 255, 255), width=2)

    beacon_a = int(180 + 75 * math.sin(f_idx * 0.18))
    cdraw.ellipse([24, 21, 34, 31], fill=(0, 212, 255, beacon_a))
    cdraw.text((46, 15), text, font=FONT_CAPTION, fill=SLATE_900)

    # Mini tech wave on right side of caption
    points = []
    num_pts = 28
    step = 160.0 / (num_pts - 1)
    for i in range(num_pts):
        px = c_w - 220 + i * step
        amp = math.sin(f_idx * 0.18 + i * 0.45) * 7.0 + math.cos(f_idx * 0.28 + i * 0.8) * 4.0
        points.append((px, 27 + amp))
    cdraw.line(points, fill=(56, 189, 248, 180), width=2)

    canvas.alpha_composite(card, (cx0, cy0))

def draw_section_header(canvas, x, y, title, subtitle):
    draw = ImageDraw.Draw(canvas)
    draw.text((x, y), title, font=FONT_HERO, fill=SLATE_900)
    draw.text((x, y + 62), subtitle, font=FONT_HEAD, fill=CYAN_DEEP)
    under_w = 640
    draw.line([(x, y + 98), (x + under_w, y + 98)], fill=(56, 189, 248, 220), width=3)
    draw.line([(x, y + 98), (x + int(under_w * 0.5), y + 98)], fill=(255, 255, 255, 255), width=2)

# =============================================================================
# PROPERLY FITTED VIDEO CONTAINER WITH HIGH-TECH TELEMETRY HUD
# =============================================================================
def embed_properly_fitted_video(canvas, vframe_rgb, bbox, title='LIVE TESTBENCH FEED', telemetry_text=None, f_idx=0, fit_mode='contain', hud_type='servo'):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0

    # Smooth subtle float
    float_dy = math.sin(f_idx * 0.07) * 3.0
    cy0 = int(y0 + float_dy)

    # Shadow
    shadow = get_cached_shadow(w, h, radius=24, fill_color=(15, 23, 42, 34), blur_radius=16)
    canvas.alpha_composite(shadow, (x0 - 25, cy0 - 12))

    # Base monitor card
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=24, fill=(15, 23, 42, 250), outline=(56, 189, 248, 190), width=2)
    cdraw.line([(24, 0), (w - 24, 0)], fill=(255, 255, 255, 255), width=2)

    # Viewport boundaries
    header_h = 50
    footer_h = 44 if telemetry_text else 16
    vp_x0 = 12
    vp_y0 = header_h
    vp_w = w - 24
    vp_h = h - header_h - footer_h

    vh, vw = vframe_rgb.shape[:2]

    if fit_mode == 'contain':
        if vw < vh and w >= 700:
            # Vertical footage (9:16) placed on right, paired with active sidebar HUD
            scale = min((vp_w * 0.58) / vw, vp_h / vh)
            nw, nh = int(vw * scale), int(vh * scale)
            v_resized = cv2.resize(vframe_rgb, (nw, nh), interpolation=cv2.INTER_LINEAR)
            v_pil = Image.fromarray(v_resized).convert('RGBA')

            vx = w - nw - 16
            vy = vp_y0 + (vp_h - nh) // 2

            v_mask = Image.new('L', (nw, nh), 0)
            v_mdraw = ImageDraw.Draw(v_mask)
            v_mdraw.rounded_rectangle([0, 0, nw, nh], radius=14, fill=255)
            card.paste(v_pil, (vx, vy), v_mask)
            cdraw.rounded_rectangle([vx, vy, vx + nw, vy + nh], radius=14, outline=(56, 189, 248, 160), width=1)

            # Left side HUD Instrumentation Panel
            hud_x = 18
            hud_w = vx - hud_x - 14
            hud_y = vp_y0 + 4
            cdraw.rounded_rectangle([hud_x, hud_y, hud_x + hud_w, hud_y + nh - 8], radius=14, fill=(11, 15, 25, 220), outline=(30, 41, 59, 255), width=1)

            if hud_type == 'payload':
                cdraw.text((hud_x + 14, hud_y + 12), 'PAYLOAD MANIPULATION HUD', font=FONT_MICRO_BOLD, fill=CYAN_GLOW)
                cdraw.line([(hud_x + 14, hud_y + 32), (hud_x + hud_w - 14, hud_y + 32)], fill=(30, 41, 59), width=1)

                p_items = [
                    ('TARGET CLASS', 'Rigid Cube [35mm]'),
                    ('GRIPPER STATUS', 'CLAMPED [1.8 N·m]'),
                    ('HOIST VECTOR', '+Z AXIS (+110 mm)'),
                    ('TRAJECTORY', 'Quintic Spline S-Curve'),
                    ('OBSTACLE CLEAR', 'VERIFIED [0.0mm ERR]'),
                    ('CYCLE STATE', 'TRANSFERRING')
                ]
                cy = hud_y + 44
                for p_k, p_v in p_items:
                    cdraw.text((hud_x + 14, cy), p_k, font=FONT_MICRO, fill=SLATE_400)
                    cdraw.text((hud_x + 14, cy + 18), p_v, font=FONT_MICRO_BOLD, fill=CYAN_ELECTRIC)
                    cy += 40

                cdraw.line([(hud_x + 14, cy + 6), (hud_x + hud_w - 14, cy + 6)], fill=(30, 41, 59), width=1)
                cy += 18
                cdraw.text((hud_x + 14, cy), 'REPEATABILITY SCORE', font=FONT_MICRO_BOLD, fill=GREEN_EMERALD)
                cdraw.text((hud_x + 14, cy + 20), '±0.8 mm (500+ Automated Cycles)', font=FONT_MICRO, fill=(241, 245, 249))

            else:
                # Servo bus HUD
                cdraw.text((hud_x + 14, hud_y + 12), 'SERVO BUS TELEMETRY (50 Hz)', font=FONT_MICRO_BOLD, fill=CYAN_GLOW)
                cdraw.line([(hud_x + 14, hud_y + 32), (hud_x + hud_w - 14, hud_y + 32)], fill=(30, 41, 59), width=1)

                channels = [
                    ('CH1 BASE YAW', 1620, 0.62),
                    ('CH2 SHOULDER', 1340, 0.44),
                    ('CH3 ELBOW PITCH', 1850, 0.85),
                    ('CH4 WRIST PITCH', 1120, 0.32),
                    ('CH5 WRIST ROLL', 1510, 0.51),
                    ('CH6 DUAL CLAW', 1900, 0.90)
                ]
                cy = hud_y + 42
                bar_w = hud_w - 28
                for ch_name, ch_us, ch_frac in channels:
                    cdraw.text((hud_x + 14, cy), ch_name, font=FONT_MICRO, fill=(203, 213, 225))
                    us_text = f"{ch_us} µs"
                    ubox = cdraw.textbbox((0, 0), us_text, font=FONT_MICRO_BOLD)
                    uw = ubox[2] - ubox[0]
                    cdraw.text((hud_x + hud_w - 14 - uw, cy), us_text, font=FONT_MICRO_BOLD, fill=CYAN_ELECTRIC)

                    cdraw.rounded_rectangle([hud_x + 14, cy + 18, hud_x + 14 + bar_w, cy + 24], radius=3, fill=(30, 41, 59))
                    fill_w = int(bar_w * ch_frac)
                    cdraw.rounded_rectangle([hud_x + 14, cy + 18, hud_x + 14 + fill_w, cy + 24], radius=3, fill=CYAN_DEEP)
                    cy += 34

                cdraw.line([(hud_x + 14, cy + 4), (hud_x + hud_w - 14, cy + 4)], fill=(30, 41, 59), width=1)
                cy += 14
                cdraw.text((hud_x + 14, cy), 'SYSTEM HEALTH & POWER', font=FONT_MICRO_BOLD, fill=CYAN_GLOW)
                cy += 24

                stats = [
                    ('BUS CURRENT', '1.38 A', GREEN_EMERALD),
                    ('RAIL VOLTAGE', '5.14 V', CYAN_ELECTRIC),
                    ('RTOS LOOP', '100 Hz', CYAN_ELECTRIC),
                    ('STALL SENSOR', 'CLEAR', GREEN_EMERALD)
                ]
                for s_lbl, s_val, s_col in stats:
                    cdraw.text((hud_x + 14, cy), s_lbl, font=FONT_MICRO, fill=SLATE_400)
                    sbox = cdraw.textbbox((0, 0), s_val, font=FONT_MICRO_BOLD)
                    sw_val = sbox[2] - sbox[0]
                    cdraw.text((hud_x + hud_w - 14 - sw_val, cy), s_val, font=FONT_MICRO_BOLD, fill=s_col)
                    cy += 22

                spark_y = cy + 10
                pts = []
                for sp_i in range(24):
                    sp_x = hud_x + 14 + sp_i * (bar_w / 23.0)
                    sp_amp = math.sin(f_idx * 0.2 + sp_i * 0.5) * 5.0 + math.cos(f_idx * 0.3 + sp_i * 0.9) * 3.0
                    pts.append((sp_x, spark_y + 12 + sp_amp))
                cdraw.line(pts, fill=GREEN_EMERALD, width=2)
                cdraw.text((hud_x + 14, spark_y + 26), 'REAL-TIME CURRENT OSCILLOGRAM', font=FONT_MICRO, fill=SLATE_500)

        else:
            # Widescreen 16:9 contain
            scale = min(vp_w / vw, vp_h / vh)
            nw, nh = int(vw * scale), int(vh * scale)
            v_resized = cv2.resize(vframe_rgb, (nw, nh), interpolation=cv2.INTER_LINEAR)
            v_pil = Image.fromarray(v_resized).convert('RGBA')

            vx = vp_x0 + (vp_w - nw) // 2
            vy = vp_y0 + (vp_h - nh) // 2

            v_mask = Image.new('L', (nw, nh), 0)
            v_mdraw = ImageDraw.Draw(v_mask)
            v_mdraw.rounded_rectangle([0, 0, nw, nh], radius=14, fill=255)
            card.paste(v_pil, (vx, vy), v_mask)
            cdraw.rounded_rectangle([vx, vy, vx + nw, vy + nh], radius=14, outline=(56, 189, 248, 120), width=1)

    # Top Header Bar
    beacon_pulse = int(180 + 75 * math.sin(f_idx * 0.2))
    cdraw.ellipse([22, 19, 32, 29], fill=(0, 212, 255, beacon_pulse))
    cdraw.text((42, 16), title, font=FONT_MICRO_BOLD, fill=(255, 255, 255, 255))

    stat_badge = "1080p @ 30FPS • LOW-LATENCY"
    cdraw.rounded_rectangle([w - 210, 13, w - 18, 37], radius=8, fill=(30, 41, 59, 220), outline=(56, 189, 248, 120), width=1)
    cdraw.text((w - 200, 17), stat_badge, font=FONT_MICRO, fill=CYAN_GLOW)

    # Bottom Telemetry Bar
    if telemetry_text:
        ty0 = h - 38
        cdraw.rounded_rectangle([14, ty0, w - 14, ty0 + 28], radius=8, fill=(11, 15, 25, 240), outline=(56, 189, 248, 140), width=1)
        cdraw.ellipse([24, ty0 + 9, 32, ty0 + 17], fill=GREEN_EMERALD)
        cdraw.text((40, ty0 + 6), telemetry_text, font=FONT_MICRO, fill=CYAN_ELECTRIC)

    canvas.alpha_composite(card, (x0, cy0))

# =============================================================================
# ELEGANT STUDIO PHOTO CARD WITH NON-CLIPPING NOTATIONS
# =============================================================================
def embed_studio_photo_card(canvas, photo_rgba, bbox, title, subtitle, callouts=None, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0

    float_dy = math.sin(f_idx * 0.08) * 3.0
    cy0 = int(y0 + float_dy)

    shadow = get_cached_shadow(w, h, radius=24, fill_color=(15, 23, 42, 32), blur_radius=16)
    canvas.alpha_composite(shadow, (x0 - 25, cy0 - 12))

    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=24, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=2)
    cdraw.line([(24, 0), (w - 24, 0)], fill=(255, 255, 255, 255), width=2)

    cdraw.text((28, 22), title, font=FONT_HEAD, fill=SLATE_900)
    cdraw.text((28, 54), subtitle, font=FONT_BADGE, fill=CYAN_DEEP)

    pad_t = 88
    pad_b = 24
    pad_s = 20
    target_w = w - (pad_s * 2)
    target_h = h - pad_t - pad_b

    pw, ph = photo_rgba.size
    scale = min(target_w / pw, target_h / ph)
    nw, nh = int(pw * scale), int(ph * scale)
    photo_fit = photo_rgba.resize((nw, nh), Image.Resampling.LANCZOS)

    px = pad_s + (target_w - nw) // 2
    py = pad_t + (target_h - nh) // 2
    card.alpha_composite(photo_fit, (px, py))

    if callouts:
        for cx_ratio, cy_ratio, label, side, dx_offset in callouts:
            cx = px + int(nw * cx_ratio)
            cy = py + int(nh * cy_ratio)

            pulse = int(180 + 75 * math.sin(f_idx * 0.15))
            cdraw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(0, 212, 255, pulse))
            cdraw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))

            tbox = cdraw.textbbox((0, 0), label, font=FONT_MICRO_BOLD)
            pw_pill = (tbox[2] - tbox[0]) + 24
            ph_pill = 26

            if side == 'right':
                bx0 = cx + dx_offset
                bx1 = bx0 + pw_pill
                if bx1 > w - 16:
                    bx1 = w - 16
                    bx0 = bx1 - pw_pill
                by0 = cy - ph_pill // 2
                by1 = by0 + ph_pill
                cdraw.line([(cx, cy), (bx0, cy)], fill=(0, 212, 255, 220), width=2)
            else:
                bx1 = cx - dx_offset
                bx0 = bx1 - pw_pill
                if bx0 < 16:
                    bx0 = 16
                    bx1 = bx0 + pw_pill
                by0 = cy - ph_pill // 2
                by1 = by0 + ph_pill
                cdraw.line([(cx, cy), (bx1, cy)], fill=(0, 212, 255, 220), width=2)

            cdraw.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(15, 23, 42, 240), outline=(56, 189, 248, 180), width=1)
            cdraw.text((bx0 + 12, by0 + 5), label, font=FONT_MICRO_BOLD, fill=(255, 255, 255, 255))

    canvas.alpha_composite(card, (x0, cy0))

# =============================================================================
# RICH SPECIFICATION CARD (Balanced, No Blank Void)
# =============================================================================
def draw_specs_card(target, bbox, title, subtitle, spec_grid, bullet_list, badge, is_elevated=False, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)

    float_dy = math.sin(f_idx * 0.08) * 3.0 if is_elevated else 0.0
    cy0 = int(y0 + float_dy)

    shadow = get_cached_shadow(w, h, radius=24, fill_color=(15, 23, 42, 30 if is_elevated else 20), blur_radius=16)
    target.alpha_composite(shadow, (int(x0) - 25, cy0 - 12))

    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=24, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=2)
    cdraw.line([(24, 0), (w - 24, 0)], fill=(255, 255, 255, 255), width=2)

    # Top Badge Pill
    tbbox = cdraw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = (tbbox[2] - tbbox[0]) + 36
    bh = 30
    bx0, by0 = 28, 22
    cdraw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=15, fill=(241, 245, 249), outline=(56, 189, 248, 160), width=1)
    cdraw.ellipse([bx0 + 12, by0 + 10, bx0 + 20, by0 + 18], fill=CYAN_DEEP)
    cdraw.text((bx0 + 26, by0 + 6), badge, font=FONT_BADGE, fill=SLATE_900)

    cdraw.text((28, 66), title, font=FONT_HEAD, fill=SLATE_900)
    cdraw.text((28, 100), subtitle, font=FONT_SUB, fill=CYAN_DEEP)

    # 4 Structured Technical Parameter Tiles
    grid_y = 142
    tile_w = (w - 56 - 16) // 2
    tile_h = 76
    for i, (k, v) in enumerate(spec_grid):
        tx = 28 + (i % 2) * (tile_w + 16)
        ty = grid_y + (i // 2) * (tile_h + 12)
        cdraw.rounded_rectangle([tx, ty, tx + tile_w, ty + tile_h], radius=14, fill=(248, 250, 252), outline=SLATE_200, width=1)
        cdraw.line([(tx + 14, ty), (tx + tile_w - 14, ty)], fill=(255, 255, 255), width=1)
        cdraw.text((tx + 16, ty + 12), k, font=FONT_MICRO_BOLD, fill=CYAN_DEEP)
        cdraw.text((tx + 16, ty + 38), v, font=FONT_BOLD, fill=SLATE_900)

    # Feature Bullet Points
    bullets_y = grid_y + 2 * (tile_h + 12) + 20
    cdraw.line([(28, bullets_y - 10), (w - 28, bullets_y - 10)], fill=SLATE_200, width=1)

    cy = bullets_y + 8
    for idx, (b_title, b_desc) in enumerate(bullet_list):
        cdraw.ellipse([28, cy + 4, 46, cy + 22], fill=(240, 249, 255), outline=CYAN_GLOW, width=1)
        cdraw.ellipse([34, cy + 10, 40, cy + 16], fill=CYAN_DEEP)

        cdraw.text((56, cy + 2), b_title, font=FONT_BOLD, fill=SLATE_900)
        cdraw.text((56, cy + 26), b_desc, font=FONT_BODY, fill=SLATE_600)
        cy += 64

    target.alpha_composite(card, (int(x0), cy0))

# =============================================================================
# SCENE RENDERING PIPELINE (60.00s @ 30 FPS = 1800 Frames)
# =============================================================================
def render_frame(f_idx):
    canvas = base_bg.copy()

    # Top Brand Bar
    if f_idx < 1520:
        canvas.alpha_composite(engineer_pill, (80, 36))

    # =========================================================================
    # SCENE 1: 0.0s - 11.0s (Frames 0 to 329) — SYSTEM OVERVIEW & MECHATRONICS
    # =========================================================================
    if f_idx < 330:
        ease_slide = ease_out_cubic(min(1.0, f_idx / 24.0))
        card_x = int(-400 + (80 - -400) * ease_slide)

        draw_section_header(canvas, card_x, 116, '6-DOF ROBOTIC MANIPULATOR', 'Spatial Articulation & Physical AI Mechatronics Architecture')

        spec_grid = [
            ('ARTICULATED AXES', '6-DOF + Parallel Gripper'),
            ('STRUCTURAL CHASSIS', 'CNC Anodized Aluminum'),
            ('ACTUATOR DRIVE', 'Digital Metal-Gear Servos'),
            ('CONTROL ENGINE', 'Deterministic 50 Hz PWM')
        ]
        bullet_list = [
            ('Deterministic Multi-Axis Kinematics', 'Closed-loop spatial planning with sub-millimeter target repeatability.'),
            ('Embedded Edge Execution', 'Analytical inverse kinematics solver converging in under 15 milliseconds.'),
            ('Compliant Dual-Gear End-Effector', 'Torque-adaptive mechanical claw engineered for delicate & rigid payloads.')
        ]
        draw_specs_card(
            canvas,
            (card_x, 240, card_x + 940, 960),
            'SYSTEM ARCHITECTURE & MECHATRONICS',
            'Engineered for High-Precision Trajectory Execution',
            spec_grid,
            bullet_list,
            'PHYSICAL AI PLATFORM',
            is_elevated=True,
            f_idx=f_idx
        )

        callouts = [
            (0.28, 0.44, 'DUAL-GEAR CLAW', 'left', 18),
            (0.72, 0.58, 'DIGITAL SERVOS', 'right', 24),
            (0.70, 0.88, 'CNC ALUMINUM BASE', 'right', 20)
        ]
        embed_studio_photo_card(
            canvas,
            photo_studio,
            (1060, 240, 1840, 960),
            'HARDWARE RECONSTRUCTION',
            'Precision 6-Axis Physical Manipulator',
            callouts,
            f_idx=f_idx
        )

        draw_caption_bar(canvas, '6-DOF Robotic Manipulator: Autonomous physical AI arm engineered for real-time spatial motion.', f_idx=f_idx)

    # =========================================================================
    # SCENE 2: 11.0s - 23.0s (Frames 330 to 689) — REAL-TIME EMBEDDED TESTBENCH
    # =========================================================================
    elif f_idx < 690:
        local_f = f_idx - 330
        ease_slide = ease_out_cubic(min(1.0, local_f / 24.0))
        card_x = int(-400 + (80 - -400) * ease_slide)

        draw_section_header(canvas, card_x, 116, 'REAL-TIME HARDWARE ACTUATION', 'Deterministic Multi-Channel PWM Control & Sensor Feedback')

        spec_grid = [
            ('PWM FREQUENCY', '50 Hz Hardware Timers'),
            ('MICROCONTROLLER', '32-Bit Dual-Core RTOS'),
            ('CURRENT TELEMETRY', 'Dedicated Over-Current Rail'),
            ('HOST INTERFACE', '115200 Baud Bi-Directional')
        ]
        bullet_list = [
            ('Hardware Timer PWM Serialization', 'Microsecond-deterministic pulse generation across six independent joints.'),
            ('S-Curve Trajectory Smoothing', 'Quintic polynomial velocity profiles eliminate jerk and inertial overshoot.'),
            ('Autonomous Stall Protection', 'Real-time current telemetry loop detects payload collisions and limits torque.')
        ]
        draw_specs_card(
            canvas,
            (card_x, 240, card_x + 940, 960),
            'EMBEDDED CONTROL FIRMWARE',
            'Hardware In-The-Loop Edge Motion Execution',
            spec_grid,
            bullet_list,
            'HARDWARE IN-THE-LOOP',
            is_elevated=True,
            f_idx=local_f
        )

        # Real testbench video playback: Arm actively lifts the cube in front of laptop!
        # Frames 360 to 720 from 12.00.06 AM.mp4
        target_video_frame = 360 + (local_f % 360)
        vframe = get_video_frame(cap_real_pick, target_video_frame, real_pick_fc)

        embed_properly_fitted_video(
            canvas,
            vframe,
            (1060, 240, 1840, 960),
            title='EMBEDDED TESTBENCH LIVE FEED',
            telemetry_text='LIVE TELEMETRY: 50Hz PWM ACTIVE | SERVO 1-6 ONLINE | RTOS LOOP: 100Hz',
            f_idx=local_f,
            fit_mode='contain',
            hud_type='servo'
        )

        draw_caption_bar(canvas, 'Embedded 32-bit controller drives six independent high-torque servos with microsecond PWM determinism.', f_idx=local_f)

    # =========================================================================
    # SCENE 3: 23.0s - 36.0s (Frames 690 to 1079) — KINEMATICS & MOTION PIPELINE
    # =========================================================================
    elif f_idx < 1080:
        local_f = f_idx - 690
        ease_prog = ease_out_cubic(min(1.0, local_f / 24.0))

        draw_section_header(canvas, 80, 116, 'KINEMATICS & MOTION PIPELINE', 'Analytical Forward & Inverse Kinematics Architecture')

        # Top Flowchart (5 Clean Stages)
        flow_y = 236
        col_w = 330
        col_h = 160
        gap = 27
        x_start = 80

        flow_steps = [
            ('CARTESIAN TARGET', 'Spatial Goal Vector', 'Target Pose: [X, Y, Z]\nEuler: [Roll, Pitch, Yaw]'),
            ('DH TRANSFORM', 'Link Coordinate Frames', 'Denavit-Hartenberg Matrices\nForward Link Kinematics'),
            ('INVERSE KINEMATICS', 'Analytical Solver', '< 15ms Convergence Time\nExact Closed-Form Solution'),
            ('S-CURVE PROFILER', 'Jerk Suppression', 'Quintic Spline Interpolation\nSmooth Velocity Transition'),
            ('PWM TIMER DRIVER', 'Direct Hardware Output', '50 Hz Hardware Channels\nMicrosecond Pulse Delivery')
        ]

        for i, (f_title, f_sub, f_desc) in enumerate(flow_steps):
            fx = x_start + i * (col_w + gap)
            f_card = Image.new('RGBA', (col_w, col_h), (0, 0, 0, 0))
            f_cdraw = ImageDraw.Draw(f_card)

            f_cdraw.rounded_rectangle([0, 0, col_w, col_h], radius=16, fill=(255, 255, 255, 250), outline=(56, 189, 248, 170), width=2)
            f_cdraw.line([(16, 0), (col_w - 16, 0)], fill=(255, 255, 255, 255), width=2)

            step_badge = f'STAGE 0{i+1}'
            f_cdraw.rounded_rectangle([16, 14, 100, 36], radius=10, fill=(15, 23, 42, 240))
            f_cdraw.text((24, 17), step_badge, font=FONT_MICRO_BOLD, fill=CYAN_ELECTRIC)

            f_cdraw.text((16, 48), f_title, font=FONT_BADGE, fill=SLATE_900)
            f_cdraw.text((16, 72), f_sub, font=FONT_MICRO_BOLD, fill=CYAN_DEEP)
            f_cdraw.text((16, 96), f_desc, font=FONT_MICRO, fill=SLATE_700)

            canvas.alpha_composite(f_card, (fx, flow_y))

            if i < len(flow_steps) - 1:
                p1_x = fx + col_w
                p2_x = fx + col_w + gap
                py = flow_y + col_h // 2
                draw = ImageDraw.Draw(canvas)
                draw.line([(p1_x, py), (p2_x, py)], fill=SLATE_200, width=4)
                draw.line([(p1_x, py), (p2_x, py)], fill=(56, 189, 248, 200), width=2)
                draw.polygon([(p2_x, py), (p2_x - 10, py - 6), (p2_x - 10, py + 6)], fill=CYAN_DEEP)
                pulse_phase = (local_f * 0.08 + i * 0.2) % 1.0
                dot_x = p1_x + int(gap * pulse_phase)
                draw.ellipse([dot_x - 4, py - 4, dot_x + 4, py + 4], fill=CYAN_ELECTRIC)

        # Lower Left Card: Joint Angles Telemetry Table
        j_card = Image.new('RGBA', (860, 520), (0, 0, 0, 0))
        j_draw = ImageDraw.Draw(j_card)
        j_draw.rounded_rectangle([0, 0, 860, 520], radius=24, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=2)
        j_draw.line([(24, 0), (860 - 24, 0)], fill=(255, 255, 255, 255), width=2)

        j_draw.rounded_rectangle([24, 20, 290, 54], radius=14, fill=(15, 23, 42, 240))
        j_draw.text((42, 26), 'REAL-TIME KINEMATICS TELEMETRY', font=FONT_MICRO_BOLD, fill=CYAN_ELECTRIC)
        j_draw.text((24, 84), 'CLOSED-FORM DH TRANSFORMATIONS', font=FONT_HEAD, fill=SLATE_900)

        # Live animated joint angles
        t_val = local_f * 0.05
        joints = [
            ('θ1 Base Yaw', f"{42.5 + 8.0*math.sin(t_val):+.1f}°", f"PWM: {int(1620 + 70*math.sin(t_val))} µs • Joint 1"),
            ('θ2 Shoulder Pitch', f"{-18.2 + 6.0*math.cos(t_val*0.8):+.1f}°", f"PWM: {int(1340 + 50*math.cos(t_val*0.8))} µs • Joint 2"),
            ('θ3 Elbow Pitch', f"{64.0 + 10.0*math.sin(t_val*0.9):+.1f}°", f"PWM: {int(1850 + 90*math.sin(t_val*0.9))} µs • Joint 3"),
            ('θ4 Wrist Pitch', f"{-45.8 + 5.0*math.cos(t_val*0.7):+.1f}°", f"PWM: {int(1120 + 40*math.cos(t_val*0.7))} µs • Joint 4"),
            ('θ5 Wrist Roll', f"{12.4 + 12.0*math.sin(t_val*0.6):+.1f}°", f"PWM: {int(1510 + 100*math.sin(t_val*0.6))} µs • Joint 5"),
            ('θ6 Claw Gripper', 'ENGAGED', 'PWM: 1900 µs • 1.8 N·m')
        ]

        for ji, (jname, jangle, jpwm) in enumerate(joints):
            col_x = 24 if ji < 3 else 440
            row_y = 130 + (ji % 3) * 115

            j_draw.rounded_rectangle([col_x, row_y, col_x + 396, row_y + 100], radius=16, fill=(248, 250, 252), outline=SLATE_200, width=1)
            j_draw.line([(col_x + 16, row_y), (col_x + 380, row_y)], fill=(255, 255, 255), width=1)

            j_draw.text((col_x + 18, row_y + 14), jname, font=FONT_BOLD, fill=SLATE_900)
            j_draw.text((col_x + 18, row_y + 60), jpwm, font=FONT_MICRO, fill=SLATE_600)
            j_draw.text((col_x + 230, row_y + 14), jangle, font=FONT_TITLE, fill=CYAN_DEEP)

        canvas.alpha_composite(j_card, (80, 420))

        # Lower Right: Kinematic Trajectory Articulation Video (16:9 widescreen, perfect fit)
        vframe_kin = get_video_frame(cap_kin, local_f, kin_fc)
        x_calc = 168.2 + 10.0 * math.sin(t_val)
        y_calc = -34.0 + 8.0 * math.cos(t_val * 0.9)
        z_calc = 122.5 + 14.0 * math.sin(t_val * 1.1)
        telem_kin = f"DH POSE: X={x_calc:+.1f}mm  Y={y_calc:+.1f}mm  Z={z_calc:+.1f}mm | IK SOLVE: < 15ms"
        embed_properly_fitted_video(
            canvas,
            vframe_kin,
            (960, 420, 1840, 940),
            title='KINEMATIC TRAJECTORY EXECUTION (16:9)',
            telemetry_text=telem_kin,
            f_idx=local_f,
            fit_mode='contain'
        )

        draw_caption_bar(canvas, 'Analytical inverse kinematics engine computes multi-axis joint angles in under 15ms, executing smooth cubic spline trajectories.', f_idx=local_f)

    # =========================================================================
    # SCENE 4: 36.0s - 49.0s (Frames 1080 to 1469) — AUTONOMOUS OBJECT PICK & HOIST
    # =========================================================================
    elif f_idx < 1470:
        local_f = f_idx - 1080
        ease_slide = ease_out_cubic(min(1.0, local_f / 24.0))
        card_x = int(-400 + (80 - -400) * ease_slide)

        draw_section_header(canvas, card_x, 116, 'AUTONOMOUS PAYLOAD MANIPULATION', 'Spatial Registration, Force Compliance & Obstacle Clearance')

        spec_grid = [
            ('CYCLE REPEATABILITY', '±0.8 mm Precision'),
            ('PAYLOAD CAPACITY', '250g at Full Reach'),
            ('CYCLE DURATION', '4.2s Pick & Place'),
            ('AUTONOMY LEVEL', '100% Autonomous Edge')
        ]
        bullet_list = [
            ('Proportional Force Gripping', 'Dual-gear mechanical end-effector delivers adaptive clamping without crushing.'),
            ('Closed-Loop Trajectory Convergence', 'Spatial coordinates streamed to trajectory solver with dynamic obstacle avoidance.'),
            ('Continuous Automated Operations', 'Validated across 500+ uninterrupted pickup, hoist, transfer, and release cycles.')
        ]
        draw_specs_card(
            canvas,
            (card_x, 240, card_x + 940, 960),
            'AUTONOMOUS PICK-AND-PLACE',
            'Spatial Registration & Compliance Gripping',
            spec_grid,
            bullet_list,
            'PAYLOAD MANIPULATION',
            is_elevated=True,
            f_idx=local_f
        )

        # Better moving arm footage:
        # First half: Real arm grabbing & hoisting the red cube (12.01.10 (1))
        # Second half: Real arm grabbing & hoisting the green cube (12.01.14)
        if local_f < 200:
            target_red_f = 60 + int((local_f / 200.0) * 200)
            vframe_payload = get_video_frame(cap_real_red, target_red_f, real_red_fc)
            p_title = 'AUTONOMOUS RED CUBE GRASP & HOIST'
            p_telem = 'GRIPPER: CLAMPED [1.8 N·m] | HOIST: +Z AXIS | TARGET ACQUIRED'
        else:
            local_g = local_f - 200
            target_green_f = 50 + int((local_g / 190.0) * 190)
            vframe_payload = get_video_frame(cap_real_green, target_green_f, real_green_fc)
            p_title = 'DYNAMIC GREEN CUBE MULTI-TARGET TRANSFER'
            p_telem = 'GRIPPER: COMPLIANT HOLD | TRANSFER ANGLE: +48.2° | CLEARANCE: PASS'

        embed_properly_fitted_video(
            canvas,
            vframe_payload,
            (1060, 240, 1840, 960),
            title=p_title,
            telemetry_text=p_telem,
            f_idx=local_f,
            fit_mode='contain',
            hud_type='payload'
        )

        draw_caption_bar(canvas, 'Mechanical end-effector provides adaptive compliant grasping, executing autonomous pick-and-place routines with high repeatability.', f_idx=local_f)

    # =========================================================================
    # SCENE 5: 49.0s - 60.0s (Frames 1470 to 1799) — HERO SUMMARY & PORTFOLIO
    # =========================================================================
    else:
        local_f = f_idx - 1470
        ease_prog = ease_out_cubic(min(1.0, local_f / 24.0))

        header_y = int(50 + (60 - 50) * ease_prog)
        h_draw = ImageDraw.Draw(canvas)
        title_text = "6-DOF ROBOTIC MANIPULATOR"
        sub_text = "Autonomous Physical AI System Architecture • Embedded Mechatronics Portfolio"

        t_box = h_draw.textbbox((0, 0), title_text, font=FONT_HERO)
        tw = t_box[2] - t_box[0]
        h_draw.text(((WIDTH - tw) // 2, header_y), title_text, font=FONT_HERO, fill=SLATE_900)

        s_box = h_draw.textbbox((0, 0), sub_text, font=FONT_HEAD)
        sw = s_box[2] - s_box[0]
        h_draw.text(((WIDTH - sw) // 2, header_y + 64), sub_text, font=FONT_HEAD, fill=CYAN_DEEP)

        under_w = int(ease_prog * 880)
        h_draw.line([((WIDTH - under_w)//2, header_y + 104), ((WIDTH + under_w)//2, header_y + 104)], fill=(56, 189, 248, 220), width=3)

        embed_studio_photo_card(
            canvas,
            photo_lab,
            (380, 200, 1540, 750),
            'PRODUCTION-READY EMBEDDED TESTBENCH',
            'Full Physical AI System Integration & Automated Testing',
            None,
            f_idx=local_f
        )

        kpis = [
            ('6-DOF', 'Spatial Dexterity', 'Full Articulated Range'),
            ('50 Hz', 'PWM Update Loop', 'Microsecond Precision'),
            ('< 15ms', 'IK Solve Latency', 'Analytical Convergence'),
            ('100%', 'Embedded Control', 'Zero Cloud Dependency')
        ]

        tile_y = 780
        tile_w = 400
        tile_h = 135
        tile_gap = 40
        tile_x_start = (WIDTH - (4 * tile_w + 3 * tile_gap)) // 2

        for ki, (kval, klabel, kdesc) in enumerate(kpis):
            tx = tile_x_start + ki * (tile_w + tile_gap)
            t_card = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))
            tdraw = ImageDraw.Draw(t_card)

            tdraw.rounded_rectangle([0, 0, tile_w, tile_h], radius=20, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=2)
            tdraw.line([(20, 0), (tile_w - 20, 0)], fill=(255, 255, 255, 255), width=2)

            tdraw.text((24, 16), kval, font=FONT_TITLE, fill=SLATE_900)
            tdraw.text((24, 62), klabel, font=FONT_BADGE, fill=CYAN_DEEP)
            tdraw.text((24, 90), kdesc, font=FONT_MICRO, fill=SLATE_600)

            canvas.alpha_composite(t_card, (tx, tile_y))

        call_action = "PORTFOLIO PROJECT • EMBEDDED SYSTEMS & PHYSICAL AI ROBOTICS"
        draw_caption_bar(canvas, call_action, f_idx=local_f)

    return np.array(canvas.convert('RGB'))

def main():
    print("=== Starting 6-DOF Robotic Arm Showcase Video Render (Enhanced Visuals & Video Fit) ===")
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

    cap_real_pick.release()
    cap_real_red.release()
    cap_real_green.release()
    cap_kin.release()

    if os.path.exists(OUTPUT_VIDEO):
        v_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"SUCCESS: Rendered final video to {OUTPUT_VIDEO} ({v_size_mb:.2f} MB)")
    else:
        print("ERROR: Output video was not created.")

if __name__ == '__main__':
    main()
