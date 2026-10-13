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
MASTER_AUDIO = os.path.join(OUTPUT_DIR, 'interview_audio_60s.wav')
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, 'Final', 'project_sentinel_interview_showcase_1min.mp4')

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_FRAMES = 1800  # Exactly 60.00 seconds

# Typography - Keynote Clean Bold Hierarchy
FONT_HERO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 58)
FONT_TITLE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 38)
FONT_HEAD = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 26)
FONT_SUB = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 21)
FONT_BODY = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 19)
FONT_BADGE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 14)
FONT_CAPTION = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
FONT_MICRO = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 12)

# Palette
BG_PORCELAIN = (248, 250, 252)
SLATE_950 = (11, 15, 25)
SLATE_900 = (15, 23, 42)
SLATE_800 = (30, 41, 59)
SLATE_600 = (71, 85, 105)
SLATE_400 = (148, 163, 184)
CYAN_DEEP = (2, 132, 199)
CYAN_GLOW = (56, 189, 248)
CYAN_ELECTRIC = (0, 212, 255)

# Sentinel Top Engineer Pill Lockup
eng_pill_w = 480
eng_pill_h = 58
engineer_pill = Image.new('RGBA', (eng_pill_w, eng_pill_h), (0, 0, 0, 0))
ep_draw = ImageDraw.Draw(engineer_pill)
ep_draw.rounded_rectangle([0, 0, eng_pill_w, eng_pill_h], radius=22, fill=(255, 255, 255, 246), outline=(56, 189, 248, 170), width=2)
ep_draw.line([(22, 0), (eng_pill_w - 22, 0)], fill=(255, 255, 255, 255), width=2)
ep_draw.ellipse([20, 21, 32, 33], fill=(0, 212, 255, 255))
ep_draw.text((42, 15), 'PROJECT SENTINEL', font=FONT_HEAD, fill=SLATE_900)
ep_draw.text((310, 18), '• EDGE AI SYSTEM', font=FONT_BADGE, fill=CYAN_DEEP)

# Load Hardware Photos
PHOTO_DIR = os.path.join(OUTPUT_DIR, 'Photos')
photo_product = Image.open(os.path.join(PHOTO_DIR, 'sentinel_product_perfect.png')).convert('RGBA')

# Base background
base_bg = Image.new('RGBA', (WIDTH, HEIGHT), (248, 250, 252, 255))
glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow_layer)
g_draw.ellipse([WIDTH//2 - 650, HEIGHT//2 - 420, WIDTH//2 + 650, HEIGHT//2 + 420], fill=(56, 189, 248, 32))
g_draw.ellipse([WIDTH - 420, -80, WIDTH + 320, 520], fill=(2, 132, 199, 25))
g_draw.ellipse([-180, HEIGHT - 380, 480, HEIGHT + 220], fill=(56, 189, 248, 22))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(130))
base_bg = Image.alpha_composite(base_bg, glow_layer)

# Video Sources
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

def draw_motion_particles(canvas, f_idx):
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
    h_draw.text((x, y + 76 + dy), subtitle, font=FONT_HEAD, fill=CYAN_DEEP)
    
    under_w = int(prog * 580)
    h_draw.line([(x, y + 118 + dy), (x + under_w, y + 118 + dy)], fill=(56, 189, 248, int(220 * alpha_mul)), width=3)
    h_draw.line([(x, y + 118 + dy), (x + int(under_w * 0.6), y + 118 + dy)], fill=(255, 255, 255, int(255 * alpha_mul)), width=2)

def draw_crystal_card(target, bbox, title, subtitle, bullets, badge, is_elevated=False, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    if w <= 10 or h <= 10:
        return

    float_dy = math.sin(f_idx * 0.08) * 4.0 if is_elevated else 0.0
    cy0 = int(y0 + float_dy)

    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=26, fill=(15, 23, 42, 36 if is_elevated else 20))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18 if is_elevated else 12))
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
    cdraw.text((26, 110), subtitle, font=FONT_SUB, fill=CYAN_DEEP)

    cy = 158
    for idx, bullet in enumerate(bullets):
        line_start_f = 6 + idx * 10
        if f_idx >= line_start_f:
            line_prog = ease_out_cubic(min(1.0, (f_idx - line_start_f) / 16.0))
            slide_dx = int(22 * (1.0 - line_prog))
            cdraw.ellipse([26 + slide_dx, cy + 6, 36 + slide_dx, cy + 16], fill=CYAN_DEEP)
            cdraw.ellipse([29 + slide_dx, cy + 9, 33 + slide_dx, cy + 13], fill=(255, 255, 255))
            cdraw.text((48 + slide_dx, cy), bullet, font=FONT_BODY, fill=SLATE_800)
        cy += 36

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

    for i in range(4):
        pulse_pos = (phase + i / 4.0) % 1.0
        px = x1 + (x2 - x1) * pulse_pos
        py = y1 + (y2 - y1) * pulse_pos
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(56, 189, 248, 190))
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255, 255))

def draw_caption_bar(canvas, text, f_idx=0):
    if not text:
        return
    cw, ch = 1520, 56
    cx = (WIDTH - cw) // 2
    cy = 988

    pill = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle([0, 0, cw, ch], radius=28, fill=(255, 255, 255, 246), outline=(56, 189, 248, 170), width=2)
    pdraw.line([(28, 0), (cw - 28, 0)], fill=(255, 255, 255, 255), width=2)

    bbox = pdraw.textbbox((0, 0), text, font=FONT_CAPTION)
    tw = bbox[2] - bbox[0]
    pdraw.text(((cw - tw)//2, (ch - 30)//2), text, font=FONT_CAPTION, fill=SLATE_900)
    canvas.alpha_composite(pill, (cx, cy))

def embed_crystal_video_frame(canvas, rgb_frame, bbox, hud_text=None, f_idx=0):
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
        bdraw.rounded_rectangle([18, 18, 260, 52], radius=15, fill=(255, 255, 255, 242), outline=(56, 189, 248, 180), width=1)
        bdraw.ellipse([28, 28, 36, 36], fill=(56, 189, 248, 255))
        bdraw.text((44, 26), hud_text, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(border, (x0, cy0))

def embed_glassmorph_photo_card(canvas, photo_img, bbox, badge_text, sub_title, callouts, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    float_dy = math.sin(f_idx * 0.08) * 4.0
    cy0 = int(y0 + float_dy)

    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=28, fill=(15, 23, 42, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card)
    cdraw.rounded_rectangle([0, 0, w, h], radius=28, fill=(255, 255, 255, 246), outline=(56, 189, 248, 190), width=2)
    cdraw.line([(28, 0), (w - 28, 0)], fill=(255, 255, 255, 255), width=2)

    # Badge
    tbb = cdraw.textbbox((0, 0), badge_text, font=FONT_BADGE)
    bw = tbb[2] - tbb[0] + 44
    cdraw.rounded_rectangle([24, 20, 24 + bw, 50], radius=15, fill=(255, 255, 255, 250), outline=(56, 189, 248, 180), width=1)
    cdraw.ellipse([34, 31, 42, 39], fill=(56, 189, 248, 255))
    cdraw.text((48, 27), badge_text, font=FONT_BADGE, fill=SLATE_900)
    cdraw.text((24, 62), sub_title, font=FONT_HEAD, fill=CYAN_DEEP)

    avail_w = w - 240
    avail_h = h - 210
    scale = min(avail_w / photo_img.width, avail_h / photo_img.height)
    tw = int(photo_img.width * scale)
    th = int(photo_img.height * scale)
    p_scaled = photo_img.resize((tw, th), Image.Resampling.LANCZOS)
    ix = (w - tw) // 2
    iy = 105 + (avail_h - th) // 2

    # Luminous cyan floor glow
    fglow = Image.new('RGBA', (tw + 40, 60), (0, 0, 0, 0))
    fgd = ImageDraw.Draw(fglow)
    fgd.ellipse([10, 10, tw + 30, 50], fill=(56, 189, 248, 45))
    fglow = fglow.filter(ImageFilter.GaussianBlur(12))
    card.alpha_composite(fglow, (ix - 20, iy + th - 30))

    card.paste(p_scaled, (ix, iy), p_scaled)

    # Expanding Sonar Rings radiating from camera lens
    cam_center_x = ix + int(tw * 0.50)
    cam_center_y = iy + int(th * 0.11)
    for r_idx in range(3):
        sonar_radius = int(14 + ((f_idx * 2.8 + r_idx * 28) % 75))
        sonar_alpha = int(max(0, 190 * (1.0 - sonar_radius / 75.0)))
        cdraw.ellipse(
            [cam_center_x - sonar_radius, cam_center_y - sonar_radius, cam_center_x + sonar_radius, cam_center_y + sonar_radius],
            outline=(56, 189, 248, sonar_alpha), width=2
        )

    # Technical Callouts (LINE-BY-LINE)
    for c_idx, (rel_x, rel_y, label, side) in enumerate(callouts):
        c_delay = 10 + c_idx * 14
        if f_idx >= c_delay:
            pt_x = ix + int(tw * rel_x)
            pt_y = iy + int(th * rel_y)
            cdraw.ellipse([pt_x - 5, pt_y - 5, pt_x + 5, pt_y + 5], fill=(56, 189, 248, 160))
            cdraw.ellipse([pt_x - 2, pt_y - 2, pt_x + 2, pt_y + 2], fill=(255, 255, 255, 255))

            tbb = cdraw.textbbox((0, 0), label, font=FONT_BADGE)
            lb_w = tbb[2] - tbb[0] + 32
            lb_h = 28
            by0 = pt_y - 14

            if side == 'right':
                bx0 = w - lb_w - 20
                elbow_x = min(bx0 - 15, pt_x + 35)
                cdraw.line([(pt_x, pt_y), (elbow_x, pt_y - 4), (bx0, pt_y - 4)], fill=(56, 189, 248, 220), width=2)
            else:
                bx0 = 20
                elbow_x = max(bx0 + lb_w + 15, pt_x - 35)
                cdraw.line([(pt_x, pt_y), (elbow_x, pt_y - 4), (bx0 + lb_w, pt_y - 4)], fill=(56, 189, 248, 220), width=2)

            cdraw.rounded_rectangle([bx0, by0, bx0 + lb_w, by0 + lb_h], radius=10, fill=(255, 255, 255, 250), outline=(56, 189, 248, 190), width=1)
            cdraw.text((bx0 + 16, by0 + 6), label, font=FONT_BADGE, fill=SLATE_900)

    cdraw.rounded_rectangle([24, h - 55, w - 24, h - 18], radius=12, fill=(241, 245, 249, 240), outline=(203, 213, 225, 140), width=1)
    spec_txt = 'REAL-TIME HARDWARE STACK • 100% OFFLINE AUTONOMY'
    cdraw.ellipse([36, h - 39, 44, h - 31], fill=(56, 189, 248, 255))
    cdraw.text((52, h - 47), spec_txt, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(card, (x0, cy0))

def draw_animated_neural_web_card(canvas, bbox, f_idx=0):
    x0, y0, x1, y1 = bbox
    w = int(x1 - x0)
    h = int(y1 - y0)
    float_dy = math.sin(f_idx * 0.08) * 4.0
    cy0 = int(y0 + float_dy)

    shadow = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([30, 30, w + 30, h + 30], radius=28, fill=(15, 23, 42, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    canvas.alpha_composite(shadow, (x0 - 30, cy0 - 15))

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
    cdraw.text((24, 62), 'COMPUTE TOPOLOGY & BUS ARBITRATION', font=FONT_HEAD, fill=CYAN_DEEP)

    # Box 1
    if f_idx >= 5:
        cdraw.rounded_rectangle([24, 110, w - 24, 250], radius=18, fill=(248, 250, 252, 240), outline=(56, 189, 248, 160), width=2)
        cdraw.ellipse([42, 126, 52, 136], fill=(56, 189, 248, 255))
        cdraw.text((60, 122), 'ARM64 NEURAL INFERENCE ENGINE', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 160), '• Quad-Core 64-bit ARM Cortex-A53 Compute Cluster', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 190), '• DSP Vector Acceleration • INT8 Quantized Tensor Pipeline', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 220), '• Asynchronous Thread Pool for YOLOv8 & ArcFace Workers', font=FONT_BODY, fill=CYAN_DEEP)

    # Bus
    if f_idx >= 15:
        bus_y1, bus_y2 = 250, 310
        cdraw.line([(w // 2, bus_y1), (w // 2, bus_y2)], fill=(226, 232, 240, 255), width=8)
        cdraw.line([(w // 2, bus_y1), (w // 2, bus_y2)], fill=(56, 189, 248, 200), width=3)
        p_pos = (f_idx * 0.1) % 1.0
        py = bus_y1 + (bus_y2 - bus_y1) * p_pos
        cdraw.ellipse([w // 2 - 6, py - 6, w // 2 + 6, py + 6], fill=(255, 255, 255, 255))
        cdraw.text((w // 2 + 20, 272), 'HIGH-SPEED DMA & MEMORY BUS', font=FONT_BADGE, fill=SLATE_600)

    # Box 2
    if f_idx >= 25:
        cdraw.rounded_rectangle([24, 310, w - 24, 450], radius=18, fill=(248, 250, 252, 240), outline=(56, 189, 248, 160), width=2)
        cdraw.ellipse([42, 326, 52, 336], fill=(56, 189, 248, 255))
        cdraw.text((60, 322), 'ULTRA-LOW-POWER REAL-TIME MCU', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 360), '• Deterministic Hardware Interrupt Handling & Actuation', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 390), '• Zero-Lag 30 FPS Frame Buffer Serialization', font=FONT_BODY, fill=SLATE_800)
        cdraw.text((42, 420), '• Sub-millisecond Hardware Acoustic Strobe Triggering', font=FONT_BODY, fill=CYAN_DEEP)

    # Efficiency Meter
    if f_idx >= 35:
        cdraw.rounded_rectangle([24, 475, w - 24, 620], radius=18, fill=(241, 245, 249, 240), outline=(203, 213, 225, 160), width=1)
        cdraw.text((42, 492), 'DYNAMIC GATED INFERENCE EFFICIENCY', font=FONT_HEAD, fill=SLATE_900)
        cdraw.text((42, 526), 'SCRFD-500M Human Presence Gating Threshold', font=FONT_BODY, fill=SLATE_600)

        bar_x0, bar_y0, bar_x1, bar_y1 = 42, 560, w - 42, 592
        cdraw.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=12, fill=(226, 232, 240, 255))
        meter_val = 0.80 + 0.02 * math.sin(f_idx * 0.12)
        fill_x1 = bar_x0 + int((bar_x1 - bar_x0) * meter_val)
        cdraw.rounded_rectangle([bar_x0, bar_y0, fill_x1, bar_y1], radius=12, fill=CYAN_DEEP)
        cdraw.rounded_rectangle([bar_x0 + 2, bar_y0 + 2, fill_x1 - 2, bar_y1 - 2], radius=10, fill=CYAN_GLOW)
        cdraw.text((fill_x1 - 240, bar_y0 + 6), '80% COMPUTE SLASHED', font=FONT_BADGE, fill=(255, 255, 255))

    # Live Tickers
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

    cdraw.rounded_rectangle([24, h - 55, w - 24, h - 18], radius=12, fill=(241, 245, 249, 240), outline=(203, 213, 225, 140), width=1)
    status_txt = 'EMBEDDED EDGE TOPOLOGY • ZERO CLOUD DEPENDENCY'
    cdraw.ellipse([36, h - 39, 44, h - 31], fill=(56, 189, 248, 255))
    cdraw.text((52, h - 47), status_txt, font=FONT_BADGE, fill=SLATE_900)

    canvas.alpha_composite(card, (x0, cy0))

def render_frame(f_idx):
    sec = f_idx / FPS
    canvas = base_bg.copy()
    draw = ImageDraw.Draw(canvas)

    # Background Motion Graphics: Floating luminous bokeh particles
    draw_motion_particles(canvas, f_idx)

    # Top Brand Bar: Clean Project Sentinel Engineering Pill
    if f_idx < 1515:
        nav_dy = int(math.sin(f_idx * 0.05) * 2.0)
        canvas.alpha_composite(engineer_pill, (80, 42 + nav_dy))

    # =========================================================================
    # SCENE 1: 0.0s - 9.5s (Frames 0 to 284) — PROBLEM & EMBEDDED EDGE MISSION
    # =========================================================================
    if f_idx < 285:
        ease_slide = ease_out_cubic(min(1.0, f_idx / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        vframe = get_video_frame(cap_booth, f_idx, booth_fc)
        embed_crystal_video_frame(canvas, vframe, (1260, 110, 1780, 950), hud_text='EDGE DEPLOYMENT TEST', f_idx=f_idx)

        draw_kinetic_header(canvas, card_x, 142, 'PROJECT SENTINEL', 'Autonomous Edge Security & Physical AI Architecture', f_idx)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 1040, 930),
            'AUTONOMOUS PERIMETER INTELLIGENCE',
            'Engineered for Air-Gapped High-Security Environments',
            [
                '100% On-Device Physical AI Inference Pipeline with Zero Cloud Uplink',
                'Embedded Dual-Core Compute Architecture for Concurrent AI & Display',
                'Sub-millisecond Deterministic Deterrence & Local GPIO Actuation',
                'Real-Time Optical Telemetry with Dual Neural Threat Classification',
                'Continuous 24/7 Thermal Stability Validated Under Extended Load'
            ],
            'SYSTEM ARCHITECTURE',
            is_elevated=True,
            f_idx=f_idx
        )

        draw_caption_bar(canvas, 'Project Sentinel: Autonomous edge perimeter defense engineered for air-gapped critical infrastructure.', f_idx=f_idx)

    # =========================================================================
    # SCENE 2: 9.5s - 19.0s (Frames 285 to 569) — HARDWARE STACK & DUAL-SOC PARTITIONING
    # =========================================================================
    elif f_idx < 570:
        local_f = f_idx - 285
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        product_callouts = [
            (0.50, 0.11, '1080P WDR OPTICAL SENSOR', 'right'),
            (0.50, 0.46, '30 FPS ROUND HUD DISPLAY', 'left'),
            (0.50, 0.78, 'EDGE COMPUTE CLUSTER', 'right')
        ]
        embed_glassmorph_photo_card(
            canvas,
            photo_product,
            (1180, 110, 1820, 950),
            'HARDWARE DEPLOYMENT UNIT',
            'Physical Edge Prototype',
            product_callouts,
            f_idx=local_f
        )

        draw_kinetic_header(canvas, card_x, 142, 'EDGE HARDWARE STACK', 'Heterogeneous Compute Partitioning Architecture', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 980, 930),
            'APPLICATION SOC & REAL-TIME MCU',
            'Workload Isolation for Thermal & Latency Determinism',
            [
                'Quad-Core 64-bit ARM Cortex-A53 SoC for Neural Network Execution',
                'Ultra-Low-Power Dedicated MCU for Actuation & GPIO Hardware Control',
                'Circular 1.28-inch HUD Display Serialization via Hardware SPI',
                'Wide Dynamic Range 1080p Optical Telemetry Sensor Core',
                'Air-Gapped Embedded Design • Zero External Network Vulnerability'
            ],
            'HARDWARE PARTITIONING',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Heterogeneous compute partitioning isolates heavy neural inference from deterministic real-time MCU control.', f_idx=local_f)

    # =========================================================================
    # SCENE 3: 19.0s - 30.5s (Frames 570 to 914) — ZERO-FREEZE MULTITHREADED PIPELINE
    # =========================================================================
    elif f_idx < 915:
        local_f = f_idx - 570
        arrow_phase = (local_f % 30) / 30.0

        draw_kinetic_header(canvas, 100, 136, 'ZERO-FREEZE DECOUPLED PIPELINE', 'Asynchronous Multithreaded Processing • Zero Display Lag • Instant Triggering', local_f)

        c1_ease = ease_out_cubic(min(1.0, local_f / 25.0))
        c1_x0 = int(-400 + (80 - -400) * c1_ease)
        draw_crystal_card(
            canvas,
            (c1_x0, 275, c1_x0 + 480, 860),
            '01. CAMERA & HUD',
            'Continuous 30 FPS Stream',
            [
                '1080p High-Resolution Stream',
                'Round Circular HUD Display',
                'Dedicated Serialization Thread',
                'Zero Dropped Frames on Display',
                'Continuous Visual Telemetry'
            ],
            'STAGE 01 • INGESTION',
            is_elevated=(local_f < 110),
            f_idx=local_f
        )

        if local_f > 15:
            draw_animated_arrow(draw, (c1_x0 + 480, 560), (c1_x0 + 590, 560), arrow_phase)

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

        if local_f > 40:
            draw_animated_arrow(draw, (1170, 560), (1270, 560), arrow_phase)

        c3_ease = ease_out_cubic(min(1.0, max(0.0, (local_f - 50) / 25.0)))
        c3_x0 = int(2000 + (1270 - 2000) * c3_ease)
        draw_crystal_card(
            canvas,
            (c3_x0, 275, c3_x0 + 480, 860),
            '03. INSTANT RESPONSE',
            'Deterministic Edge Actuation',
            [
                'Preloaded Flash Waveforms in RAM',
                'DMA Direct Memory Access Bus',
                'Hardware Strobe & Actuation',
                'Instant Acoustic Deterrence',
                'Telemetry Synced to Local Log'
            ],
            'STAGE 03 • ACTUATION',
            is_elevated=(local_f >= 220),
            f_idx=local_f
        )

        draw.rounded_rectangle([180, 890, 1740, 952], radius=18, fill=(255, 255, 255, 245), outline=(56, 189, 248, 160), width=2)
        draw.text((220, 908), 'ARCHITECTURAL GUARANTEE: UI NEVER FREEZES WHILE HEAVY AI RUNS • 100% DETERMINISTIC EXECUTION', font=FONT_HEAD, fill=SLATE_900)
        draw_animated_waveform(draw, 1540, 921, 160, local_f)

        draw_caption_bar(canvas, 'Decoupled ring-buffer architecture guarantees continuous 30 FPS HUD telemetry without frame drops.', f_idx=local_f)

    # =========================================================================
    # SCENE 4: 30.5s - 41.5s (Frames 915 to 1244) — DUAL-ENGINE AI & GATED INFERENCE
    # =========================================================================
    elif f_idx < 1245:
        local_f = f_idx - 915
        arrow_phase = (local_f % 30) / 30.0

        draw_animated_neural_web_card(
            canvas,
            (1140, 110, 1840, 950),
            f_idx=local_f
        )

        draw_kinetic_header(canvas, 100, 136, 'DUAL-ENGINE NEURAL AI', 'Quantized YOLOv8 Detection & Gated ArcFace Biometrics', local_f)

        draw_crystal_card(
            canvas,
            (100, 275, 1070, 565),
            'MODEL 01: YOLOv8 THREAT CLASSIFIER',
            'INT8 Quantized Real-Time Perimeter Surveillance',
            [
                'Real-Time Detection of Unauthorized Boundary Breaches & Objects',
                'Custom INT8 Quantization optimized for DSP Vector Engines',
                'Continuous 360-degree Boundary Vector Telemetry Stream'
            ],
            'REAL-TIME THREAT AI',
            is_elevated=True,
            f_idx=local_f
        )

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

        draw_caption_bar(canvas, 'Two-stage gated scheduling reduces neural compute by 80%, preserving embedded battery life.', f_idx=local_f)

    # =========================================================================
    # SCENE 5: 41.5s - 50.5s (Frames 1245 to 1514) — INDUSTRIAL BENCHMARK & HARDWARE RIGOR
    # =========================================================================
    elif f_idx < 1515:
        local_f = f_idx - 1245
        ease_slide = ease_out_cubic(min(1.0, local_f / 26.0))
        card_x = int(-500 + (100 - -500) * ease_slide)

        vframe = get_video_frame(cap_demo, local_f, demo_fc)
        embed_crystal_video_frame(canvas, vframe, (1260, 110, 1780, 950), hud_text='LIVE RIGOROUS BENCHMARK', f_idx=local_f)

        draw_kinetic_header(canvas, card_x, 142, 'HARDWARE STRESS BENCHMARK', 'Exhibition Stress Testing & Reliability Verification', local_f)

        draw_crystal_card(
            canvas,
            (card_x, 280, card_x + 1040, 930),
            'LIVE INDUSTRIAL BENCHMARK',
            'Empirical Validation Under Extended Operational Stress',
            [
                'Validated Under Multi-Hour Continuous Autonomous Exhibition Testing',
                'Zero Memory Leaks & Zero Thermal Throttling Under Extended Inference',
                'Multithreaded Decoupled Pipeline Confirmed 100% Deterministic',
                'Physical Verification of Sub-millisecond Hardware Acoustic Triggering',
                'Production-Grade Edge Computing Ready for Industrial Deployment'
            ],
            'EMPIRICAL VALIDATION',
            is_elevated=True,
            f_idx=local_f
        )

        draw_caption_bar(canvas, 'Empirically validated under multi-hour stress testing, proving hardware stability and reliability.', f_idx=local_f)

    # =========================================================================
    # SCENE 6: 50.5s - 60.0s (Frames 1515 to 1800) — ENGINEERING SUMMARY & INTERVIEW OUTRO
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

        draw_hud_tech_bracket(hdraw, cw // 2, ch // 2, cw - 40, ch - 40, col=(56, 189, 248, 140), line_len=36, width=2)

        shimmer_x = int(-200 + (cw + 400) * ((local_f % 90) / 90.0))
        hdraw.line([(shimmer_x, 0), (shimmer_x + 110, ch)], fill=(255, 255, 255, 150), width=6)

        # Title: PROJECT SENTINEL
        bbox = hdraw.textbbox((0, 0), 'PROJECT SENTINEL', font=FONT_HERO)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, 60), 'PROJECT SENTINEL', font=FONT_HERO, fill=SLATE_900)

        # Subtitle: Physical AI & Embedded Edge Engineering
        sub_text = 'Autonomous Edge Security • Physical AI • Embedded Systems Architecture'
        bbox = hdraw.textbbox((0, 0), sub_text, font=FONT_HEAD)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, 138), sub_text, font=FONT_HEAD, fill=CYAN_DEEP)

        p_len = int(520 + 60 * math.sin(local_f * 0.1))
        hdraw.line([((cw - p_len)//2, 186), ((cw + p_len)//2, 186)], fill=(56, 189, 248, 220), width=3)
        hdraw.line([((cw - int(p_len*0.6))//2, 186), ((cw + int(p_len*0.6))//2, 186)], fill=(255, 255, 255, 255), width=2)

        # 4 Core Engineering Competency Cards for Resume & Interviews
        comp_tags = [
            ('HETEROGENEOUS COMPUTE', 'ARM64 Application SoC + Real-Time MCU Workload Isolation'),
            ('DETERMINISTIC PIPELINE', 'Multithreaded Decoupled Zero-Freeze Circular Ring Buffer'),
            ('EDGE NEURAL EFFICIENCY', 'Quantized INT8 YOLOv8 + Gated SCRFD Slashes Compute by 80%'),
            ('AIR-GAPPED ROBUSTNESS', '100% Offline Autonomy With Zero Cloud Dependency or Latency')
        ]
        
        card_y = 215
        for c_title, c_desc in comp_tags:
            hdraw.rounded_rectangle([120, card_y, cw - 120, card_y + 88], radius=16, fill=(248, 250, 252, 245), outline=(56, 189, 248, 160), width=1)
            hdraw.ellipse([145, card_y + 24, 157, card_y + 36], fill=(0, 212, 255, 255))
            hdraw.text((172, card_y + 16), c_title, font=FONT_HEAD, fill=SLATE_900)
            hdraw.text((172, card_y + 48), c_desc, font=FONT_BODY, fill=SLATE_600)
            card_y += 104

        # Bottom Engineering Badge
        btn_w = 640
        btn_x0 = (cw - btn_w) // 2
        btn_y0 = 640
        hdraw.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + 52], radius=18, fill=(255, 255, 255, 255), outline=(56, 189, 248, 200), width=2)
        call_action = 'PORTFOLIO PROJECT • EMBEDDED SYSTEMS & EDGE AI'
        bbox = hdraw.textbbox((0, 0), call_action, font=FONT_BADGE)
        tw = bbox[2] - bbox[0]
        hdraw.text(((cw - tw)//2, btn_y0 + 17), call_action, font=FONT_BADGE, fill=CYAN_DEEP)

        # Shadow
        h_shadow = Image.new('RGBA', (cw + 60, ch + 60), (0, 0, 0, 0))
        hs_draw = ImageDraw.Draw(h_shadow)
        hs_draw.rounded_rectangle([30, 30, cw + 30, ch + 30], radius=32, fill=(15, 23, 42, 35))
        h_shadow = h_shadow.filter(ImageFilter.GaussianBlur(24))
        canvas.alpha_composite(h_shadow, (cx - 30, cy - 20))
        canvas.alpha_composite(hero_card, (cx, cy))

        draw_caption_bar(canvas, 'Project Sentinel: Real-world physical AI, deterministic embedded architecture, and edge computing.', f_idx=local_f)

        if local_f > 265:
            fade_prog = (local_f - 265) / 20.0
            fade_layer = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, int(255 * fade_prog)))
            canvas.alpha_composite(fade_layer)

    return np.array(canvas.convert('RGB'))

def main():
    print(f'Starting Project Sentinel Technical Interview Showcase 60s Render...')
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
