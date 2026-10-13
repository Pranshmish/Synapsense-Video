import os
import sys
import math
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FFMPEG = r'D:\Espressif\tools\python_env\idf5.3_py3.13_env\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
MASTER_AUDIO = os.path.join(OUTPUT_DIR, 'master_crystal_audio_60s.wav')
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, 'synapsense_sentinel_crystal_1min.mp4')

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 1800  # Exactly 60.00 seconds

# Typography - Keynote Clean Bold Hierarchy
FONT_HERO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 62)
FONT_TITLE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 40)
FONT_HEAD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 27)
FONT_SUB = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
FONT_BODY = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 19)
FONT_BADGE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 14)
FONT_CAPTION = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
FONT_MICRO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 12)

# Luminous Crystal Palette (Strictly White, Slate/Black, and Electric Cyan)
BG_PORCELAIN = (248, 250, 252)
SLATE_950 = (11, 15, 25)
SLATE_900 = (15, 23, 42)
SLATE_800 = (30, 41, 59)
SLATE_600 = (71, 85, 105)
SLATE_400 = (148, 163, 184)
CYAN_DEEP = (2, 132, 199)
CYAN_GLOW = (56, 189, 248)
CYAN_ELECTRIC = (0, 212, 255)
CYAN_LIGHT = (224, 242, 254)

# Load Shield & Recolored Text for White/Crystal Theme
shield_img = Image.open(os.path.join(OUTPUT_DIR, 'synapsense_shield_tight.png')).convert('RGBA')
text_img = Image.open(os.path.join(OUTPUT_DIR, 'synapsense_text_for_white_bg.png')).convert('RGBA')

# 1. Top Brand Pill (Clean frosted crystal pill - standalone, no side tags)
sh_h = 44
sh_w = int(shield_img.width * (sh_h / shield_img.height))
sh_resized = shield_img.resize((sh_w, sh_h), Image.Resampling.LANCZOS)

tx_h = 36
tx_w = int(text_img.width * (tx_h / text_img.height))
tx_resized = text_img.resize((tx_w, tx_h), Image.Resampling.LANCZOS)

lockup_w = sh_w + 14 + tx_w
pill_w = lockup_w + 44
pill_h = 64

logo_pill_white = Image.new('RGBA', (pill_w, pill_h), (0, 0, 0, 0))
lp_draw = ImageDraw.Draw(logo_pill_white)
lp_draw.rounded_rectangle([0, 0, pill_w, pill_h], radius=24, fill=(255, 255, 255, 245), outline=(56, 189, 248, 160), width=2)
lp_draw.line([(24, 0), (pill_w - 24, 0)], fill=(255, 255, 255, 255), width=2)
logo_pill_white.paste(sh_resized, (20, (pill_h - sh_h)//2), sh_resized)
logo_pill_white.paste(tx_resized, (20 + sh_w + 14, (pill_h - tx_h)//2), tx_resized)

# 2. Hero Outro Plaque Logo Lockup (Clean hero badge)
h_sh_h = 108
h_sh_w = int(shield_img.width * (h_sh_h / shield_img.height))
h_sh_resized = shield_img.resize((h_sh_w, h_sh_h), Image.Resampling.LANCZOS)

h_tx_h = 86
h_tx_w = int(text_img.width * (h_tx_h / text_img.height))
h_tx_resized = text_img.resize((h_tx_w, h_tx_h), Image.Resampling.LANCZOS)

h_lock_w = h_sh_w + 24 + h_tx_w
h_pill_w = h_lock_w + 72
h_pill_h = 138

hero_logo_badge_white = Image.new('RGBA', (h_pill_w, h_pill_h), (0, 0, 0, 0))
hl_draw = ImageDraw.Draw(hero_logo_badge_white)
hl_draw.rounded_rectangle([0, 0, h_pill_w, h_pill_h], radius=32, fill=(255, 255, 255, 248), outline=(56, 189, 248, 180), width=2)
hl_draw.line([(32, 0), (h_pill_w - 32, 0)], fill=(255, 255, 255, 255), width=2)
hero_logo_badge_white.paste(h_sh_resized, (36, (h_pill_h - h_sh_h)//2), h_sh_resized)
hero_logo_badge_white.paste(h_tx_resized, (36 + h_sh_w + 24, (h_pill_h - h_tx_h)//2), h_tx_resized)

# Load Isolated Sentinel Hardware Photos
PHOTO_DIR = os.path.join(OUTPUT_DIR, 'Photos')
photo_product = Image.open(os.path.join(PHOTO_DIR, 'sentinel_product_perfect.png')).convert('RGBA')

# Pre-render base porcelain crystal background (NO GRID LINES)
base_bg = Image.new('RGBA', (WIDTH, HEIGHT), (248, 250, 252, 255))

# Luminous radial cyan ambient lights (Apple studio lighting)
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_layer)
g_draw.ellipse([WIDTH//2 - 650, HEIGHT//2 - 420, WIDTH//2 + 650, HEIGHT//2 + 420], fill=(56, 189, 248, 32))
g_draw.ellipse([WIDTH - 420, -80, WIDTH + 320, 520], fill=(2, 132, 199, 25))
g_draw.ellipse([-180, HEIGHT - 380, 480, HEIGHT + 220], fill=(56, 189, 248, 22))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(130))
base_bg = Image.alpha_composite(base_bg, glow_layer)

# Video Sources (Strictly Booth and Live Demo, Robot completely excluded)
V_BOOTH = os.path.join(OUTPUT_DIR, 'videos-sentinel', 'WhatsApp Video 2026-09-28 at 9.25.12 PM.mp4')
V_DEMO = os.path.join(OUTPUT_DIR, 'videos-sentinel', 'WhatsApp Video 2026-10-02 at 6.24.06 PM.mp4')

cap_booth = cv2.VideoCapture(V_BOOTH)
cap_demo = cv2.VideoCapture(V_DEMO)

booth_fc = int(cap_booth.get(cv2.CAP_PROP_FRAME_COUNT))
demo_fc = int(cap_demo.get(cv2.CAP_PROP_FRAME_COUNT))

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

def ease_in_out_sine(t):
    t = max(0.0, min(1.0, t))
    return -(math.cos(math.pi * t) - 1.0) / 2.0

# -------------------------------------------------------------
# MOTION GRAPHIC ASSETS & GENERATORS
# -------------------------------------------------------------

def draw_motion_particles(canvas, f_idx):
    """
    Renders 16 floating luminous cyan bokeh particles moving gracefully across the canvas.
    """
    p_draw = ImageDraw.Draw(canvas)
    for i in range(16):
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
    """
    Renders tech corner brackets around an area.
    """
    x0, y0 = cx - w//2, cy - h//2
    x1, y1 = cx + w//2, cy + h//2
    # Top-Left
    draw.line([(x0, y0), (x0 + line_len, y0)], fill=col, width=width)
    draw.line([(x0, y0), (x0, y0 + line_len)], fill=col, width=width)
    # Top-Right
    draw.line([(x1, y0), (x1 - line_len, y0)], fill=col, width=width)
    draw.line([(x1, y0), (x1, y0 + line_len)], fill=col, width=width)
    # Bottom-Left
    draw.line([(x0, y1), (x0 + line_len, y1)], fill=col, width=width)
    draw.line([(x0, y1), (x0, y1 - line_len)], fill=col, width=width)
    # Bottom-Right
    draw.line([(x1, y1), (x1 - line_len, y1)], fill=col, width=width)
    draw.line([(x1, y1), (x1, y1 - line_len)], fill=col, width=width)

def draw_animated_waveform(draw, x0, y, w, f_idx, col=(56, 189, 248, 170)):
    """
    Renders an oscilloscope audio/telemetry waveform bar.
    """
    points = []
    num_pts = 32
    step = w / (num_pts - 1)
    for i in range(num_pts):
        px = x0 + i * step
        amp = math.sin(f_idx * 0.18 + i * 0.45) * 8.0 + math.cos(f_idx * 0.28 + i * 0.8) * 5.0
        points.append((px, y + amp))
    draw.line(points, fill=col, width=2)

def draw_kinetic_header(canvas, x, y, title, subtitle, local_frame, anim_delay=0):
    """
    Renders key headers with kinetic slide-up entrance and cyan glow highlight underbar below the subtitle.
    """
    h_draw = ImageDraw.Draw(canvas)
    f_rel = max(0, local_frame - anim_delay)
    prog = ease_out_cubic(min(1.0, f_rel / 22.0))
    
    dy = int(24 * (1.0 - prog))
    alpha_mul = prog
    
    h_draw.text((x, y + dy), title, font=FONT_HERO, fill=SLATE_900)
    h_draw.text((x, y + 80 + dy), subtitle, font=FONT_HEAD, fill=CYAN_DEEP)
    
    # Animated Underline bar expanding from left cleanly below the subtitle
    under_w = int(prog * 580)
    h_draw.line([(x, y + 124 + dy), (x + under_w, y + 124 + dy)], fill=(56, 189, 248, int(220 * alpha_mul)), width=3)
    h_draw.line([(x, y + 124 + dy), (x + int(under_w * 0.6), y + 124 + dy)], fill=(255, 255, 255, int(255 * alpha_mul)), width=2)

def draw_crystal_card(target, bbox, title, subtitle, bullets, badge, is_elevated=False, f_idx=0):
    """
    Frosted glass card with LINE-BY-LINE progressive text reveal and floating animation.
    """
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    if w <= 10 or h <= 10:
        return

    # Weightless floating motion
    float_dy = math.sin(f_idx * 0.08) * 4.0 if is_elevated else 0.0
    cy0 = int(y0 + float_dy)

    # Multi-tier Apple-style soft drop shadow
    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=26, fill=(15, 23, 42, 36 if is_elevated else 20))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18 if is_elevated else 12))
    target.alpha_composite(shadow, (int(x0) - 30, cy0 - 15))

    # Frosted glassmorphic card surface
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    card_fill = (255, 255, 255, 248) if is_elevated else (255, 255, 255, 240)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=card_fill)
    
    # Specular rim and border with cyan illumination
    border_col = (56, 189, 248, 210) if is_elevated else (203, 213, 225, 140)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, outline=border_col, width=2)
    cdraw.line([(26, 0), (w - 26, 0)], fill=(255, 255, 255, 255), width=2)

    # Dynamic Badge Pill
    tbbox = cdraw.textbbox((0, 0), badge, font=FONT_BADGE)
    bw = (tbbox[2] - tbbox[0]) + 44
    bh = 32
    bx0, by0 = 26, 24
    cdraw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=16, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=1)
    cdraw.line([(bx0 + 12, by0), (bx0 + bw - 12, by0)], fill=(255, 255, 255, 255), width=1)
    beacon_alpha = int(180 + 75 * math.sin(f_idx * 0.15))
    cdraw.ellipse([bx0 + 14, by0 + 11, bx0 + 22, by0 + 19], fill=(56, 189, 248, beacon_alpha))
    cdraw.text((bx0 + 28, by0 + 7), badge, font=FONT_BADGE, fill=SLATE_900)

    # Title & Subtitle
    cdraw.text((26, 72), title, font=FONT_HEAD, fill=SLATE_900)
    cdraw.text((26, 110), subtitle, font=FONT_SUB, fill=CYAN_DEEP)

    # LINE-BY-LINE progressive appearance (staggered animation)
    cy = 158
    for idx, bullet in enumerate(bullets):
        line_start_f = 6 + idx * 10
        if f_idx >= line_start_f:
            line_prog = ease_out_cubic(min(1.0, (f_idx - line_start_f) / 16.0))
            slide_dx = int(22 * (1.0 - line_prog))
            
            # Subtle expanding line tracer behind newly arrived bullet
            if line_prog < 0.95:
                tracer_w = int(line_prog * 400)
                cdraw.line([(26, cy + 18), (26 + tracer_w, cy + 18)], fill=(56, 189, 248, int(150 * (1.0 - line_prog))), width=1)

            # Bullet dot
            cdraw.ellipse([26 + slide_dx, cy + 6, 36 + slide_dx, cy + 16], fill=CYAN_DEEP)
            cdraw.ellipse([29 + slide_dx, cy + 9, 33 + slide_dx, cy + 13], fill=(255, 255, 255))
            cdraw.text((48 + slide_dx, cy), bullet, font=FONT_BODY, fill=SLATE_800)
        cy += 36

    target.alpha_composite(card, (int(x0), cy0))

def draw_animated_arrow(draw, p1, p2, phase):
    x1, y1 = p1
    x2, y2 = p2
    # Base arrow track
    draw.line([(x1, y1), (x2, y2)], fill=(226, 232, 240, 255), width=6)
    draw.line([(x1, y1), (x2, y2)], fill=(56, 189, 248, 180), width=2)

    # Arrow head
    if abs(x2 - x1) >= abs(y2 - y1):
        draw.polygon([(x2, y2), (x2 - 16, y2 - 9), (x2 - 16, y2 + 9)], fill=CYAN_DEEP)
    else:
        draw.polygon([(x2, y2), (x2 - 9, y2 - 16), (x2 + 9, y2 - 16)], fill=CYAN_DEEP)

    # Moving glowing energy particles with motion blur trails
    for i in range(4):
        pulse_pos = (phase + i / 4.0) % 1.0
        px = x1 + (x2 - x1) * pulse_pos
        py = y1 + (y2 - y1) * pulse_pos
        trail_pos = (pulse_pos - 0.04) % 1.0
        tx = x1 + (x2 - x1) * trail_pos
        ty = y1 + (y2 - y1) * trail_pos
        draw.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=(56, 189, 248, 120))
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(56, 189, 248, 190))
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255, 255))

def draw_caption_bar(canvas, text, f_idx=0):
    """
    Clean, frosted footer caption bar with proper spacing above screen bottom.
    """
    if not text:
        return
    cw, ch = 1520, 56
    cx = (WIDTH - cw) // 2
    cy = 988  # Clean comfortable spacing from bottom border

    # Frosted pill
    pill = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle([0, 0, cw, ch], radius=28, fill=(255, 255, 255, 246), outline=(56, 189, 248, 170), width=2)
    pdraw.line([(28, 0), (cw - 28, 0)], fill=(255, 255, 255, 255), width=2)

    # Shimmer glint across caption
    s_x = int(-100 + (cw + 200) * ((f_idx % 90) / 90.0))
    pdraw.line([(s_x, 0), (s_x + 60, ch)], fill=(255, 255, 255, 120), width=3)

    bbox = pdraw.textbbox((0, 0), text, font=FONT_CAPTION)
    tw = bbox[2] - bbox[0]
    pdraw.text(((cw - tw)//2, (ch - 30)//2), text, font=FONT_CAPTION, fill=SLATE_900)

    canvas.alpha_composite(pill, (cx, cy))

def embed_crystal_video_frame(canvas, rgb_frame, bbox, hud_text=None, f_idx=0):
    """
    Clean video frame without distracting reticle targets or dark grids.
    """
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)

    float_dy = math.sin(f_idx * 0.07) * 3.0
    cy0 = int(y0 + float_dy)

    vid_pil = Image.fromarray(rgb_frame).resize((w, h), Image.Resampling.LANCZOS)

    mask = Image.new('L', (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=255)

    shadow = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([20, 20, w + 20, h + 20], radius=26, fill=(15, 23, 42, 40))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (x0 - 20, cy0 - 10))

    canvas.paste(vid_pil, (x0, cy0), mask)

    border = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border)
    bdraw.rounded_rectangle([0, 0, w, h], radius=26, outline=(255, 255, 255, 220), width=3)
    bdraw.rounded_rectangle([2, 2, w - 2, h - 2], radius=24, outline=(56, 189, 248, 150), width=2)

    if hud_text:
        bdraw.rounded_rectangle([18, 18, 235, 52], radius=15, fill=(255, 255, 255, 242), outline=(56, 189, 248, 180), width=1)
        bdraw.ellipse([28, 28, 36, 36], fill=(56, 189, 248, 255))
        bdraw.text((44, 26), hud_text, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(border, (x0, cy0))

def embed_glassmorph_photo_card(canvas, photo_img, bbox, badge_text, sub_title, callouts, f_idx=0):
    """
    Renders Sentinel product photo card cleanly with callouts and sonar ripples from lens, NO grey laser scanner line.
    """
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)

    # Harmonic weightless floating motion
    float_dy = math.sin(f_idx * 0.08) * 4.0
    cy0 = int(y0 + float_dy)

    # Ambient drop shadow behind card
    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=28, fill=(15, 23, 42, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

    # White glass card
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=28, fill=(255, 255, 255, 246), outline=(56, 189, 248, 190), width=2)
    cdraw.line([(28, 0), (w - 28, 0)], fill=(255, 255, 255, 255), width=2)

    # Top Frosted White Glass Badge
    tbb = cdraw.textbbox((0, 0), badge_text, font=FONT_BADGE)
    bw = tbb[2] - tbb[0] + 44
    cdraw.rounded_rectangle([24, 20, 24 + bw, 50], radius=15, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=1)
    cdraw.ellipse([34, 31, 42, 39], fill=(56, 189, 248, 255))
    cdraw.text((48, 27), badge_text, font=FONT_BADGE, fill=SLATE_900)
    cdraw.text((24, 62), sub_title, font=FONT_HEAD, fill=CYAN_DEEP)

    # Scale photo with side clearance for clean callout lines
    avail_w = w - 240
    avail_h = h - 210
    scale = min(avail_w / photo_img.width, avail_h / photo_img.height)
    tw = int(photo_img.width * scale)
    th = int(photo_img.height * scale)
    p_scaled = photo_img.resize((tw, th), Image.Resampling.LANCZOS)

    ix = (w - tw) // 2
    iy = 105 + (avail_h - th) // 2

    # Luminous cyan floor glow under hardware
    fglow = Image.new('RGBA', (tw + 40, 60), (0, 0, 0, 0))
    fgd = ImageDraw.Draw(fglow)
    fgd.ellipse([10, 10, tw + 30, 50], fill=(56, 189, 248, 45))
    fglow = fglow.filter(ImageFilter.GaussianBlur(12))
    card.alpha_composite(fglow, (ix - 20, iy + th - 30))

    # Soft contact shadow
    pshad = Image.new('RGBA', (tw + 40, 50), (0, 0, 0, 0))
    psd = ImageDraw.Draw(pshad)
    psd.ellipse([20, 10, tw + 20, 40], fill=(15, 23, 42, 40))
    pshad = pshad.filter(ImageFilter.GaussianBlur(10))
    card.alpha_composite(pshad, (ix - 20, iy + th - 25))

    card.paste(p_scaled, (ix, iy), p_scaled)

    # Motion Graphic: Expanding Sonar Rings radiating from camera lens
    cam_center_x = ix + int(tw * 0.50)
    cam_center_y = iy + int(th * 0.11)
    for r_idx in range(3):
        sonar_radius = int(14 + ((f_idx * 2.8 + r_idx * 28) % 75))
        sonar_alpha = int(max(0, 190 * (1.0 - sonar_radius / 75.0)))
        cdraw.ellipse(
            [cam_center_x - sonar_radius, cam_center_y - sonar_radius, cam_center_x + sonar_radius, cam_center_y + sonar_radius],
            outline=(56, 189, 248, sonar_alpha), width=2
        )

    # Technical HUD Callouts with flowing energy tracer pulses along connecting lines (LINE-BY-LINE appearance)
    for c_idx, (rel_x, rel_y, label, side) in enumerate(callouts):
        c_delay = 10 + c_idx * 14
        if f_idx >= c_delay:
            c_prog = ease_out_cubic(min(1.0, (f_idx - c_delay) / 18.0))
            
            pt_x = ix + int(tw * rel_x)
            pt_y = iy + int(th * rel_y)

            # Anchor point
            cdraw.ellipse([pt_x - 6, pt_y - 6, pt_x + 6, pt_y + 6], fill=(56, 189, 248, 140))
            cdraw.ellipse([pt_x - 3, pt_y - 3, pt_x + 3, pt_y + 3], fill=(255, 255, 255, 255))

            tbb = cdraw.textbbox((0, 0), label, font=FONT_BADGE)
            lb_w = tbb[2] - tbb[0] + 32
            lb_h = 28
            by0 = pt_y - 14

            if side == 'right':
                bx0 = w - lb_w - 20
                elbow_x = min(bx0 - 15, pt_x + 35)
                cdraw.line([(pt_x, pt_y), (elbow_x, pt_y - 4), (bx0, pt_y - 4)], fill=(56, 189, 248, 220), width=2)
                tracer_pos = (f_idx * 0.08) % 1.0
                tx = pt_x + (bx0 - pt_x) * tracer_pos
                ty = pt_y + ((pt_y - 4) - pt_y) * tracer_pos
                cdraw.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=(255, 255, 255, 255))
            else:
                bx0 = 20
                elbow_x = max(bx0 + lb_w + 15, pt_x - 35)
                cdraw.line([(pt_x, pt_y), (elbow_x, pt_y - 4), (bx0 + lb_w, pt_y - 4)], fill=(56, 189, 248, 220), width=2)
                tracer_pos = (f_idx * 0.08) % 1.0
                tx = pt_x + ((bx0 + lb_w) - pt_x) * tracer_pos
                ty = pt_y + ((pt_y - 4) - pt_y) * tracer_pos
                cdraw.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=(255, 255, 255, 255))

            # Callout Badge
            cdraw.rounded_rectangle([bx0, by0, bx0 + lb_w, by0 + lb_h], radius=10, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=1)
            cdraw.text((bx0 + 16, by0 + 6), label, font=FONT_BADGE, fill=SLATE_900)

    # Bottom technical status footer
    cdraw.rounded_rectangle([24, h - 55, w - 24, h - 18], radius=12, fill=(241, 245, 249, 240), outline=(203, 213, 225, 140), width=1)
    spec_txt = 'REAL-TIME HARDWARE STACK • 100% OFFLINE AUTONOMY'
    cdraw.ellipse([36, h - 39, 44, h - 31], fill=(56, 189, 248, 255))
    cdraw.text((52, h - 47), spec_txt, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(card, (x0, cy0))

def draw_animated_neural_web_card(canvas, bbox, f_idx=0):
    """
    Apple / Google style animated Neural Architecture Web Component Card with LINE-BY-LINE appearance.
    """
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)

    float_dy = math.sin(f_idx * 0.08) * 4.0
    cy0 = int(y0 + float_dy)

    # Drop shadow
    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=28, fill=(15, 23, 42, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

    # White crystal card body
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=28, fill=(255, 255, 255, 248), outline=(56, 189, 248, 190), width=2)
    cdraw.line([(28, 0), (w - 28, 0)], fill=(255, 255, 255, 255), width=2)

    # Card Header
    badge_txt = 'DUAL-CORE ARCHITECTURE'
    tbb = cdraw.textbbox((0, 0), badge_txt, font=FONT_BADGE)
    bw = tbb[2] - tbb[0] + 44
    cdraw.rounded_rectangle([24, 20, 24 + bw, 50], radius=15, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=1)
    cdraw.ellipse([34, 31, 42, 39], fill=(56, 189, 248, 255))
    cdraw.text((48, 27), badge_txt, font=FONT_BADGE, fill=SLATE_900)
    cdraw.text((24, 62), 'ARDUINO UNO Q EDGE SOC TOPOLOGY', font=FONT_HEAD, fill=CYAN_DEEP)

    # Component Box 1: Qualcomm QRB2210 Neural Engine
    if f_idx >= 5:
        cdraw.rounded_rectangle([24, 110, w - 24, 250], radius=18, fill=(248, 250, 252, 240), outline=(56, 189, 248, 160), width=2)
        cdraw.ellipse([42, 126, 52, 136], fill=(56, 189, 248, 255))
        cdraw.text((60, 122), 'QUALCOMM QRB2210 ARM64 ENGINE', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 160), '• Quad-Core 64-bit ARM Cortex-A53 @ 2.0 GHz', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 190), '• Hexagon DSP Vector Extensions • Hardware INT8 Acceleration', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 220), '• Dedicated YOLOv8 + ArcFace Neural Pipeline Worker', font=FONT_BODY, fill=CYAN_DEEP)

    # Bus Interconnect with Animated Energy Pulses
    if f_idx >= 15:
        bus_y1, bus_y2 = 250, 310
        cdraw.line([(w // 2, bus_y1), (w // 2, bus_y2)], fill=(226, 232, 240, 255), width=8)
        cdraw.line([(w // 2, bus_y1), (w // 2, bus_y2)], fill=(56, 189, 248, 200), width=3)
        p_pos = (f_idx * 0.1) % 1.0
        py = bus_y1 + (bus_y2 - bus_y1) * p_pos
        cdraw.ellipse([w // 2 - 6, py - 6, w // 2 + 6, py + 6], fill=(255, 255, 255, 255))
        cdraw.text((w // 2 + 20, 272), 'HIGH-SPEED DMA & MEMORY BUS', font=FONT_BADGE, fill=SLATE_600)

    # Component Box 2: STM32U585 Real-Time Coprocessor
    if f_idx >= 25:
        cdraw.rounded_rectangle([24, 310, w - 24, 450], radius=18, fill=(248, 250, 252, 240), outline=(56, 189, 248, 160), width=2)
        cdraw.ellipse([42, 326, 52, 336], fill=(56, 189, 248, 255))
        cdraw.text((60, 322), 'STM32U585 ULTRA-LOW-POWER MCU', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 360), '• Deterministic Hardware Interrupt Handling & GPIO Control', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 390), '• Zero-Lag 30 FPS HUD Frame Buffer Serialization', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 420), '• Instant Acoustic Strobe & Deterrence Triggering', font=FONT_BODY, fill=CYAN_DEEP)

    # Live Animated Telemetry Section: 80% Compute Gating Efficiency Meter
    if f_idx >= 35:
        cdraw.rounded_rectangle([24, 475, w - 24, 620], radius=18, fill=(241, 245, 249, 240), outline=(203, 213, 225, 160), width=1)
        cdraw.text((42, 492), 'DYNAMIC GATED INFERENCE EFFICIENCY', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 526), 'SCRFD-500M Human Presence Gating Threshold', font=FONT_BODY, fill=SLATE_600)

        # Meter Bar Background
        bar_x0, bar_y0, bar_x1, bar_y1 = 42, 560, w - 42, 592
        cdraw.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=12, fill=(226, 232, 240, 255))
        # Meter Fill
        meter_val = 0.80 + 0.02 * math.sin(f_idx * 0.12)
        fill_x1 = bar_x0 + int((bar_x1 - bar_x0) * meter_val)
        cdraw.rounded_rectangle([bar_x0, bar_y0, fill_x1, bar_y1], radius=12, fill=CYAN_DEEP)
        cdraw.rounded_rectangle([bar_x0 + 2, bar_y0 + 2, fill_x1 - 2, bar_y1 - 2], radius=10, fill=CYAN_GLOW)
        cdraw.text((fill_x1 - 240, bar_y0 + 6), '80% COMPUTE SLASHED', font=FONT_BADGE, fill=(255, 255, 255))

    # Live Real-Time Telemetry Tickers
    if f_idx >= 45:
        t_y = 645
        t_tags = [
            ('INFERENCE LATENCY', 'OPTIMIZED'),
            ('THERMAL STATE', 'COOL / NOMINAL'),
            ('UI FRAME JITTER', '0.00% ZERO LAG')
        ]
        box_w = (w - 48 - (len(t_tags) - 1) * 14) // len(t_tags)
        for idx, (label, val) in enumerate(t_tags):
            tx0 = 24 + idx * (box_w + 14)
            cdraw.rounded_rectangle([tx0, t_y, tx0 + box_w, t_y + 115], radius=14, fill=(248, 250, 252, 250), outline=(56, 189, 248, 140), width=1)
            cdraw.text((tx0 + 14, t_y + 14), label, font=FONT_MICRO, fill=SLATE_600)
            cdraw.text((tx0 + 14, t_y + 40), val, font=FONT_BODY, fill=CYAN_DEEP)
            cdraw.ellipse([tx0 + 14, t_y + 85, tx0 + 22, t_y + 93], fill=CYAN_GLOW)
            cdraw.text((tx0 + 28, t_y + 80), 'ACTIVE', font=FONT_MICRO, fill=SLATE_800)

    # Footer status
    cdraw.rounded_rectangle([24, h - 55, w - 24, h - 18], radius=12, fill=(241, 245, 249, 240), outline=(203, 213, 225, 140), width=1)
    status_txt = 'QUALCOMM HEXAGON DSP + STM32U585 • ARDUINO UNO Q ARCHITECTURE'
    cdraw.ellipse([36, h - 39, 44, h - 31], fill=(56, 189, 248, 255))
    cdraw.text((52, h - 47), status_txt, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(card, (x0, cy0))

def render_frame(f_idx):
    sec = f_idx / FPS
    canvas = base_bg.copy()
    draw = ImageDraw.Draw(canvas)

    # 1. Background Motion Graphics: Floating luminous bokeh particles
    draw_motion_particles(canvas, f_idx)

    # Top Brand Bar: STANDALONE SynapSense Logo Pill (NO side tags at right)
    if f_idx < 1515:
        nav_dy = int(math.sin(f_idx * 0.05) * 2.0)
        canvas.alpha_composite(logo_pill_white, (80, 42 + nav_dy))

    # =========================================================================
    # SCENE 1: 0.0s - 9.5s (Frames 0 to 284) — PARTNERSHIP & MISSION
    # =========================================================================
    if f_idx < 285:
        ease_slide = ease_out_cubic(min(1.0, f_idx / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        vframe = get_video_frame(cap_booth, f_idx, booth_fc)
        embed_crystal_video_frame(canvas, vframe, (1260, 110, 1780, 950), hud_text='LIVE RS × ARDUINO BOOTH', f_idx=f_idx)

        # Kinetic animated headers with underline pulse
        draw_kinetic_header(canvas, card_x, 142, 'SENTINEL', 'Autonomous Perimeter Defense Architecture', f_idx)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 1040, 930),
            'ENTERPRISE PERIMETER INTELLIGENCE',
            'Engineered for RS Components & Arduino Ecosystem',
            [
                'Official Industry Collaboration with Arduino India & RS Components',
                'Edge Qualcomm QRB2210 SoC Architecture with STM32U585 MCU',
                'Zero Cloud Dependency • Autonomous Edge Defense Execution',
                'High-Fidelity Optical Ingestion & Real-Time Dual AI Threat Analysis',
                'Live Validated at National Engineering & Industry Expo'
            ],
            'OFFICIAL PARTNERSHIP',
            is_elevated=True,
            f_idx=f_idx
        )

        draw_caption_bar(canvas, 'In official partnership with RS Components and Arduino India, SynapSense introduces SENTINEL.', f_idx=f_idx)

    # =========================================================================
    # SCENE 2: 9.5s - 19.0s (Frames 285 to 569) — REAL SENTINEL HARDWARE PHOTO (UNCUT CAMERA)
    # =========================================================================
    elif f_idx < 570:
        local_f = f_idx - 285
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        product_callouts = [
            (0.50, 0.11, 'KREO OWL 1080P SENSOR', 'right'),
            (0.50, 0.46, 'CIRCULAR RETICLE HUD DISPLAY', 'left'),
            (0.50, 0.78, 'UNO Q EDGE SOC', 'right')
        ]
        embed_glassmorph_photo_card(
            canvas,
            photo_product,
            (1180, 110, 1820, 950),
            'SENTINEL HARDWARE UNIT',
            'Physical Edge Deployment',
            product_callouts,
            f_idx=local_f
        )

        # Kinetic animated headers
        draw_kinetic_header(canvas, card_x, 142, 'EDGE HARDWARE STACK', 'Arduino UNO Q Edge Compute Architecture', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 980, 930),
            'QUALCOMM QRB2210 & STM32U585 MCU',
            'Dedicated Compute Workload Isolation',
            [
                'Quad-Core 64-bit ARM Cortex-A53 Compute Engine (Qualcomm QRB2210)',
                'STM32U585 Ultra-Low-Power Real-Time Microcontroller Core',
                'Waveshare 1.28-inch Round Circular HUD Display (30 FPS Stream)',
                'Kreo Owl 1080p Optical Telemetry & Wide Dynamic Range Sensor',
                'Zero Cloud Latency • Complete Offline Security Autonomy'
            ],
            'EDGE HARDWARE ARCHITECTURE',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Engineered on the Arduino UNO Q Edge SoC, Sentinel brings surveillance to the hardware frontier.', f_idx=local_f)

    # =========================================================================
    # SCENE 3: 19.0s - 30.5s (Frames 570 to 914) — ZERO-FREEZE SLIDESHOW + MOVING ARROWS
    # =========================================================================
    elif f_idx < 915:
        local_f = f_idx - 570
        arrow_phase = (local_f % 30) / 30.0

        # Kinetic Header
        draw_kinetic_header(canvas, 100, 136, 'ZERO-FREEZE DECOUPLED PIPELINE', 'Asynchronous Multithreaded Processing • Zero Display Lag • Instant Triggering', local_f)

        # Card 1 (Slides from left)
        c1_ease = ease_out_cubic(min(1.0, local_f / 25.0))
        c1_x0 = int(-400 + (80 - -400) * c1_ease)
        draw_crystal_card(
            canvas,
            (c1_x0, 275, c1_x0 + 480, 860),
            '01. CAMERA & HUD',
            'Continuous 30 FPS Stream',
            [
                'Kreo Owl 1080p Optical Sensor',
                'Waveshare Round Circular HUD',
                'Dedicated Display Rendering Core',
                'Zero Frame Dropping UI Loop',
                'Continuous Visual Telemetry'
            ],
            'STAGE 01 • INGESTION',
            is_elevated=(local_f < 110),
            f_idx=local_f
        )

        # Animated Moving Arrow 1
        if local_f > 15:
            draw_animated_arrow(draw, (c1_x0 + 480, 560), (c1_x0 + 590, 560), arrow_phase)

        # Card 2 (Slides up from bottom)
        c2_ease = ease_out_cubic(min(1.0, max(0.0, (local_f - 25) / 25.0)))
        c2_y0 = int(1200 + (275 - 1200) * c2_ease)
        draw_crystal_card(
            canvas,
            (680, c2_y0, 1170, c2_y0 + 585),
            '02. DECOUPLED QUEUE',
            'Asynchronous Neural Worker',
            [
                'Non-Blocking Memory Ring Buffer',
                '2-4 FPS AI Inference Worker',
                'Decoupled from Display Loop',
                'Zero Memory Allocation Jitter',
                'Hardware Thermal Optimization'
            ],
            'STAGE 02 • NEURAL QUEUE',
            is_elevated=(110 <= local_f < 220),
            f_idx=local_f
        )

        # Animated Moving Arrow 2
        if local_f > 40:
            draw_animated_arrow(draw, (1170, 560), (1270, 560), arrow_phase)

        # Card 3 (Slides in from right)
        c3_ease = ease_out_cubic(min(1.0, max(0.0, (local_f - 50) / 25.0)))
        c3_x0 = int(2000 + (1270 - 2000) * c3_ease)
        draw_crystal_card(
            canvas,
            (c3_x0, 275, c3_x0 + 480, 860),
            '03. INSTANT RESPONSE',
            'Deterministic Edge Response',
            [
                'Preloaded Flash Waveforms in RAM',
                'DMA Direct Memory Access Bus',
                'Hardware Strobe & Deterrence',
                'Instant Acoustic Deterrence',
                'Telemetry Synced to Dashboard'
            ],
            'STAGE 03 • DETERRENCE',
            is_elevated=(local_f >= 220),
            f_idx=local_f
        )

        # Bottom Architecture Metric Banner with animated live waveform
        draw.rounded_rectangle([180, 890, 1740, 952], radius=18, fill=(255, 255, 255, 245), outline=(56, 189, 248, 160), width=2)
        draw.text((220, 908), 'ARCHITECTURAL GUARANTEE: UI NEVER FREEZES WHILE HEAVY AI RUNS • 100% DETERMINISTIC EXECUTION', font=FONT_HEAD, fill=SLATE_900)
        draw_animated_waveform(draw, 1540, 921, 160, local_f)

        draw_caption_bar(canvas, 'Powered by a zero-freeze pipeline, feeds render at 30 FPS, decoupled from neural inference.', f_idx=local_f)

    # =========================================================================
    # SCENE 4: 30.5s - 41.5s (Frames 915 to 1244) — DUAL-ENGINE AI & NEURAL WEB CARD (NO INNER PCB PHOTO)
    # =========================================================================
    elif f_idx < 1245:
        local_f = f_idx - 915
        arrow_phase = (local_f % 30) / 30.0

        # Right Side: Interactive Animated Neural Web Component Card (Replaces raw PCB photo)
        draw_animated_neural_web_card(
            canvas,
            (1140, 110, 1840, 950),
            f_idx=local_f
        )

        # Kinetic Header
        draw_kinetic_header(canvas, 100, 136, 'DUAL-ENGINE EDGE AI', 'YOLOv8 Threat Detection & Gated ArcFace Biometrics', local_f)

        draw_crystal_card(
            canvas,
            (100, 275, 1070, 565),
            'MODEL 01: YOLOv8 THREAT CLASSIFIER',
            'INT8 Quantized Real-Time Perimeter Surveillance',
            [
                'Real-Time Detection of Weapons, Unlawful Entry, & Intrusion Zones',
                'Custom INT8 Quantization optimized for Qualcomm Hexagon DSP & ARM64',
                'Continuous 360-degree Boundary Vector Ingestion'
            ],
            'REAL-TIME THREAT AI',
            is_elevated=True,
            f_idx=local_f
        )

        # Animated Moving Arrow Connecting Model 1 to Model 2
        draw_animated_arrow(draw, (585, 565), (585, 635), arrow_phase)

        draw_crystal_card(
            canvas,
            (100, 635, 1070, 925),
            'MODEL 02: GATED ARCFACE BIOMETRICS',
            'MobileFaceNet 512-D Neural Feature Embeddings',
            [
                'Gated SCRFD-500M scheduling triggers biometrics ONLY on verified human presence',
                '80% Compute Reduction slashes battery draw and processor thermal overhead',
                'Instant Authorized vs Unauthorized Identification with zero cloud round-trip'
            ],
            '80% COMPUTE SLASHED',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Dual neural models orchestrate threat detection and biometrics. Gated inference slashes compute by 80%.', f_idx=local_f)

    # =========================================================================
    # SCENE 5: 41.5s - 50.5s (Frames 1245 to 1514) — RS COMPONENTS EXPO LIVE DEMO
    # =========================================================================
    elif f_idx < 1515:
        local_f = f_idx - 1245
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        vframe = get_video_frame(cap_demo, local_f, demo_fc)
        embed_crystal_video_frame(canvas, vframe, (1260, 110, 1780, 950), hud_text='LIVE AT INDUSTRY EXPO', f_idx=local_f)

        # Kinetic Header
        draw_kinetic_header(canvas, card_x, 142, 'INDUSTRY VALIDATION', 'Live Showcase at RS Components & Arduino India Booth', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 1040, 930),
            'LIVE INDUSTRIAL BENCHMARK',
            'Proven in Front of Enterprise Leaders & System Integrators',
            [
                'Demonstrated Live to Hundreds of Industry Leaders & Embedded Engineers',
                'Validated Stability over Continuous Multi-Hour Autonomous Exhibition',
                'Zero-Freeze Architecture Praised for Responsiveness and Robustness',
                'Official Endorsement within the Arduino Uno Q Partner Showcase',
                'Ready for Commercial Deployment Across High-Security Infrastructure'
            ],
            'PROVEN AT EXPO',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Showcased live at the RS Components booth, Sentinel proved its mettle to industry leaders.', f_idx=local_f)

    # =========================================================================
    # SCENE 6: 50.5s - 60.0s (Frames 1515 to 1800) — GRAND FINALE (PURE SYNAPSENSE FOCUS)
    # =========================================================================
    else:
        local_f = f_idx - 1515

        cw, ch = 1380, 720
        cx = (WIDTH - cw) // 2
        cy = (HEIGHT - ch) // 2 + 10

        hero_card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        hdraw = ImageDraw.Draw(hero_card)
        hdraw.rounded_rectangle([0, 0, cw, ch], radius=32, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=3)
        hdraw.line([(32, 0), (cw - 32, 0)], fill=(255, 255, 255, 255), width=3)

        # Corner tech brackets for hero plaque
        draw_hud_tech_bracket(hdraw, cw // 2, ch // 2, cw - 40, ch - 40, col=(56, 189, 248, 140), line_len=36, width=2)

        # Specular light shimmer across hero plaque
        shimmer_x = int(-200 + (cw + 400) * ((local_f % 90) / 90.0))
        hdraw.line([(shimmer_x, 0), (shimmer_x + 110, ch)], fill=(255, 255, 255, 150), width=6)

        # Central Hero SynapSense Logo Badge
        hero_card.paste(hero_logo_badge_white, ((cw - h_pill_w)//2, 50), hero_logo_badge_white)

        # Title: SYNAPSENSE SENTINEL
        bbox = hdraw.textbbox((0, 0), 'SYNAPSENSE SENTINEL', font=FONT_HERO)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, 225), 'SYNAPSENSE SENTINEL', font=FONT_HERO, fill=SLATE_900)

        # Tagline: NEXT-GENERATION AUTONOMOUS PERIMETER DEFENSE
        sub_text = 'Next-Generation Autonomous Perimeter Defense & Edge Intelligence'
        bbox = hdraw.textbbox((0, 0), sub_text, font=FONT_HEAD)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, 305), sub_text, font=FONT_HEAD, fill=CYAN_DEEP)

        # Underline kinetic pulse bar cleanly placed below the tagline
        p_len = int(460 + 60 * math.sin(local_f * 0.1))
        hdraw.line([((cw - p_len)//2, 360), ((cw + p_len)//2, 360)], fill=(56, 189, 248, 220), width=3)
        hdraw.line([((cw - int(p_len*0.6))//2, 360), ((cw + int(p_len*0.6))//2, 360)], fill=(255, 255, 255, 255), width=2)

        # Value Proposition Badges (SynapSense Core Strengths ONLY)
        synap_features = ['100% OFFLINE AUTONOMY', 'ZERO-FREEZE PIPELINE', 'DUAL-ENGINE NEURAL AI']
        total_p_w = 0
        p_widths = []
        for p_label in synap_features:
            p_bb = hdraw.textbbox((0, 0), p_label, font=FONT_SUB)
            pw = p_bb[2] - p_bb[0] + 52
            p_widths.append(pw)
            total_p_w += pw
        total_p_w += (len(synap_features) - 1) * 20

        px = (cw - total_p_w) // 2
        py = 398
        for idx, p_label in enumerate(synap_features):
            pw = p_widths[idx]
            hdraw.rounded_rectangle([px, py, px + pw, py + 46], radius=23, fill=(255, 255, 255, 245), outline=(56, 189, 248, 180), width=2)
            hdraw.line([(px + 18, py), (px + pw - 18, py)], fill=(255, 255, 255, 255), width=1)
            # Pulsing beacon
            beacon_alpha = int(180 + 75 * math.sin((local_f + idx * 15) * 0.15))
            hdraw.ellipse([px + 16, py + 19, px + 24, py + 27], fill=(56, 189, 248, beacon_alpha))
            hdraw.text((px + 32, py + 11), p_label, font=FONT_SUB, fill=SLATE_900)
            px += pw + 20

        # Official Website Button (Strictly synapsense.site)
        btn_w = 560
        btn_x0 = (cw - btn_w) // 2
        btn_y0 = 485
        hdraw.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + 80], radius=24, fill=(255, 255, 255, 255), outline=(56, 189, 248, 220), width=2)
        hdraw.line([btn_x0 + 20, btn_y0, btn_x0 + btn_w - 20, btn_y0], fill=(255, 255, 255, 255), width=2)
        
        url_text = 'www.synapsense.site'
        bbox = hdraw.textbbox((0, 0), url_text, font=FONT_TITLE)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, btn_y0 + 18), url_text, font=FONT_TITLE, fill=CYAN_DEEP)

        call_action = 'Deploy Enterprise Edge Intelligence Today'
        bbox = hdraw.textbbox((0, 0), call_action, font=FONT_SUB)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, 600), call_action, font=FONT_SUB, fill=SLATE_600)

        # Shadow
        h_shadow = Image.new('RGBA', (cw + 60, ch + 60), (0, 0, 0, 0))
        hs_draw = ImageDraw.Draw(h_shadow)
        hs_draw.rounded_rectangle([30, 30, cw + 30, ch + 30], radius=32, fill=(15, 23, 42, 35))
        h_shadow = h_shadow.filter(ImageFilter.GaussianBlur(24))
        canvas.alpha_composite(h_shadow, (cx - 30, cy - 20))
        canvas.alpha_composite(hero_card, (cx, cy))

        draw_caption_bar(canvas, 'SynapSense Sentinel. Empowering autonomous perimeter defense. Welcome to the future.', f_idx=local_f)

        # Subtle white crystal fadeout in final 20 frames
        if local_f > 265:
            fade_prog = (local_f - 265) / 20.0
            fade_layer = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, int(255 * fade_prog)))
            canvas.alpha_composite(fade_layer)

    return np.array(canvas.convert('RGB'))

def main():
    print(f'Starting Sentinel White & Crystal Master 60s Render (SynapSense Site & Line-by-Line Edition)...')
    print(f'Output: {OUTPUT_VIDEO}')
    print(f'Total frames: {TOTAL_FRAMES} @ {FPS} FPS (60.00 seconds)')

    cmd = [
        FFMPEG, '-y',
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
        '-b:a', '256k',
        '-shortest',
        OUTPUT_VIDEO
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    for f in range(TOTAL_FRAMES):
        frame_rgb = render_frame(f)
        proc.stdin.write(frame_rgb.tobytes())
        if f % 150 == 0 or f == TOTAL_FRAMES - 1:
            print(f'Rendered frame {f}/{TOTAL_FRAMES} ({f/TOTAL_FRAMES*100:.1f}%) - {f/FPS:.1f}s')

    proc.stdin.close()
    stderr = proc.stderr.read().decode('utf-8', errors='ignore')
    proc.wait()

    cap_booth.release()
    cap_demo.release()

    if proc.returncode == 0:
        print('RENDER COMPLETE! Output written to:', OUTPUT_VIDEO)
        size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f'File Size: {size_mb:.2f} MB')
    else:
        print('RENDER FAILED!')
        print(stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
