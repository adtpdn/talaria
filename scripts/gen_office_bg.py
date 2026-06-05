#!/usr/bin/env python3
"""Generate pixel art office background tiles for Talaria 2D world."""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'html', 'assets')
os.makedirs(OUT, exist_ok=True)

# Palette — clean/modern office
WALL_BG      = (235, 235, 240, 255)
WALL_LINE    = (210, 210, 218, 255)
WALL_TRIM    = (195, 195, 205, 255)
WIN_FRAME    = (90, 90, 100, 255)
WIN_SKY_TOP  = (135, 195, 235, 255)
WIN_SKY_BOT  = (175, 215, 245, 255)
WIN_BUILDING = (110, 120, 140, 255)
WIN_BUILD_LT = (140, 155, 175, 255)
WIN_GLASS    = (160, 200, 230, 255)
CLOCK_FACE   = (250, 250, 250, 255)
CLOCK_RIM    = (80, 80, 90, 255)
CLOCK_HAND   = (50, 50, 60, 255)
POSTER_BG    = (255, 245, 220, 255)
POSTER_EDGE  = (200, 190, 170, 255)
POSTER_ART1  = (100, 160, 210, 255)
POSTER_ART2  = (210, 120, 100, 255)

DESK_TOP     = (230, 225, 215, 255)
DESK_FRONT   = (210, 205, 195, 255)
DESK_EDGE    = (180, 175, 165, 255)
DESK_LEG     = (160, 155, 148, 255)
MON_BEZEL    = (45, 45, 50, 255)
MON_SCREEN   = (60, 130, 180, 255)
MON_SCRN_LT  = (80, 160, 210, 255)
MON_STAND    = (70, 70, 78, 255)
CHAIR_BACK   = (60, 60, 68, 255)
CHAIR_SEAT   = (55, 55, 62, 255)
CHAIR_WHEEL  = (40, 40, 48, 255)
PLANT_POT    = (180, 120, 80, 255)
PLANT_LEAF   = (80, 170, 100, 255)
PLANT_LEAF2  = (60, 145, 80, 255)
CUP_BODY     = (240, 240, 245, 255)
CUP_COFFEE   = (120, 80, 50, 255)
KEYBOARD     = (200, 200, 210, 255)
KB_KEY       = (180, 180, 190, 255)

FLOOR_A      = (200, 200, 208, 255)
FLOOR_B      = (210, 210, 218, 255)
FLOOR_GROUT  = (175, 175, 185, 255)
BASEBOARD    = (170, 170, 180, 255)
BASEBOARD_HI = (190, 190, 200, 255)

T = (0, 0, 0, 0)


def draw_wall(w=80, h=24):
    """Wall with windows, clock, and poster — tileable."""
    img = Image.new('RGBA', (w, h), WALL_BG)
    d = ImageDraw.Draw(img)

    # Subtle horizontal lines
    for y in [6, 12, 18]:
        d.line([(0, y), (w-1, y)], fill=WALL_LINE)

    # Wainscoting trim at bottom
    d.rectangle([0, h-2, w-1, h-1], fill=WALL_TRIM)

    # Window 1 (left area) — 18x14 at position (4, 3)
    _draw_window(d, 4, 3, 18, 14)

    # Clock between windows (center) — at (32, 2)
    _draw_clock(d, 34, 2)

    # Window 2 (right area)
    _draw_window(d, 46, 3, 18, 14)

    # Small poster/art on far right
    _draw_poster(d, 70, 4, 8, 10)

    return img


def _draw_window(d, x, y, w, h):
    """Draw a window with frame, sky, and buildings."""
    # Frame
    d.rectangle([x, y, x+w-1, y+h-1], fill=WIN_FRAME)
    # Glass (inset 1px)
    for gy in range(y+1, y+h-1):
        t = (gy - y) / h
        r = int(WIN_SKY_TOP[0] + (WIN_SKY_BOT[0] - WIN_SKY_TOP[0]) * t)
        g = int(WIN_SKY_TOP[1] + (WIN_SKY_BOT[1] - WIN_SKY_TOP[1]) * t)
        b = int(WIN_SKY_TOP[2] + (WIN_SKY_BOT[2] - WIN_SKY_TOP[2]) * t)
        d.line([(x+1, gy), (x+w-2, gy)], fill=(r, g, b, 255))

    # Buildings silhouette
    buildings = [
        (x+2, y+h-5, 3, 4),
        (x+6, y+h-7, 2, 6),
        (x+9, y+h-4, 3, 3),
        (x+13, y+h-6, 2, 5),
    ]
    for bx, by, bw, bh in buildings:
        d.rectangle([bx, by, bx+bw-1, by+bh-1], fill=WIN_BUILDING)
        # Window lights on buildings
        if bw >= 2 and bh >= 3:
            d.point((bx+1, by+1), fill=WIN_BUILD_LT)
            if bh >= 4:
                d.point((bx, by+2), fill=WIN_BUILD_LT)

    # Crossbar
    mid_y = y + h // 2
    d.line([(x+1, mid_y), (x+w-2, mid_y)], fill=WIN_FRAME)
    mid_x = x + w // 2
    d.line([(mid_x, y+1), (mid_x, y+h-2)], fill=WIN_FRAME)


def _draw_clock(d, cx, cy):
    """Draw a small wall clock at (cx, cy), about 6x6."""
    # Rim
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                c = CLOCK_FACE if dx*dx + dy*dy <= 6 else CLOCK_RIM
                d.point((cx+dx, cy+3+dy), fill=c)
    # Hands
    d.point((cx, cy+3), fill=CLOCK_HAND)
    d.point((cx, cy+2), fill=CLOCK_HAND)  # 12 o'clock
    d.point((cx+1, cy+3), fill=CLOCK_HAND)  # 3 o'clock (short)


def _draw_poster(d, x, y, w, h):
    """Draw a small framed poster."""
    d.rectangle([x, y, x+w-1, y+h-1], fill=POSTER_EDGE)
    d.rectangle([x+1, y+1, x+w-2, y+h-2], fill=POSTER_BG)
    # Abstract art inside
    d.rectangle([x+2, y+3, x+4, y+6], fill=POSTER_ART1)
    d.rectangle([x+4, y+5, x+6, y+8], fill=POSTER_ART2)


def draw_desks(w=80, h=16):
    """Desk + monitor + chair + accessories — tileable, wall-colored above furniture."""
    img = Image.new('RGBA', (w, h), WALL_BG)
    d = ImageDraw.Draw(img)

    # Desk unit 1 — centered around x=8
    _draw_desk_unit(d, 2, h)

    # Desk unit 2 — centered around x=48
    _draw_desk_unit(d, 42, h, with_plant=True)

    return img


def _draw_desk_unit(d, x, h, with_plant=False):
    """Draw one desk with monitor, keyboard, chair, and optional plant."""
    desk_y = h - 7  # desk surface y
    desk_w = 30
    desk_h = 3

    # Chair (behind desk, slightly left)
    ch_x = x + 4
    ch_y = desk_y - 6
    d.rectangle([ch_x, ch_y, ch_x+6, ch_y+5], fill=CHAIR_BACK)
    d.rectangle([ch_x+1, ch_y+1, ch_x+5, ch_y+2], fill=(75, 75, 82, 255))
    # Chair base/wheels
    d.rectangle([ch_x+1, h-2, ch_x+5, h-1], fill=CHAIR_WHEEL)
    d.line([(ch_x+3, ch_y+5), (ch_x+3, h-2)], fill=CHAIR_WHEEL)

    # Desk surface
    d.rectangle([x, desk_y, x+desk_w-1, desk_y+desk_h-1], fill=DESK_TOP)
    d.line([(x, desk_y+desk_h-1), (x+desk_w-1, desk_y+desk_h-1)], fill=DESK_EDGE)

    # Desk front panel
    d.rectangle([x+1, desk_y+desk_h, x+desk_w-2, h-2], fill=DESK_FRONT)
    d.line([(x+1, h-2), (x+desk_w-2, h-2)], fill=DESK_EDGE)

    # Desk legs
    d.line([(x+1, desk_y+desk_h), (x+1, h-1)], fill=DESK_LEG)
    d.line([(x+desk_w-2, desk_y+desk_h), (x+desk_w-2, h-1)], fill=DESK_LEG)

    # Monitor
    mon_x = x + 12
    mon_y = desk_y - 8
    mon_w = 10
    mon_h = 7
    d.rectangle([mon_x, mon_y, mon_x+mon_w-1, mon_y+mon_h-1], fill=MON_BEZEL)
    # Screen
    d.rectangle([mon_x+1, mon_y+1, mon_x+mon_w-2, mon_y+mon_h-2], fill=MON_SCREEN)
    # Screen highlight
    d.rectangle([mon_x+2, mon_y+2, mon_x+4, mon_y+3], fill=MON_SCRN_LT)
    # Code lines on screen
    d.line([(mon_x+2, mon_y+4), (mon_x+6, mon_y+4)], fill=MON_SCRN_LT)
    d.line([(mon_x+3, mon_y+5), (mon_x+7, mon_y+5)], fill=(70, 150, 200, 255))
    # Stand
    d.rectangle([mon_x+4, mon_y+mon_h, mon_x+6, desk_y-1], fill=MON_STAND)
    # Stand base
    d.line([(mon_x+2, desk_y-1), (mon_x+8, desk_y-1)], fill=MON_STAND)

    # Keyboard on desk
    kb_x = x + 11
    kb_y = desk_y + 1
    d.rectangle([kb_x, kb_y, kb_x+8, kb_y+1], fill=KEYBOARD)
    for kx in range(kb_x+1, kb_x+8, 2):
        d.point((kx, kb_y), fill=KB_KEY)

    # Coffee cup (right side of desk)
    cup_x = x + 24
    d.rectangle([cup_x, desk_y-2, cup_x+2, desk_y-1], fill=CUP_BODY)
    d.point((cup_x+1, desk_y-3), fill=CUP_COFFEE)

    # Plant on desk (optional)
    if with_plant:
        px = x + 2
        py = desk_y - 1
        d.rectangle([px, py, px+2, py+1], fill=PLANT_POT)
        d.point((px+1, py-1), fill=PLANT_LEAF)
        d.point((px, py-2), fill=PLANT_LEAF)
        d.point((px+2, py-2), fill=PLANT_LEAF2)
        d.point((px+1, py-3), fill=PLANT_LEAF2)


def draw_floor(w=32, h=6):
    """Tiled floor with baseboard — tileable."""
    img = Image.new('RGBA', (w, h), FLOOR_A)
    d = ImageDraw.Draw(img)

    # Baseboard (top 2 rows)
    d.rectangle([0, 0, w-1, 0], fill=BASEBOARD)
    d.rectangle([0, 1, w-1, 1], fill=BASEBOARD_HI)

    # Tile pattern — checkerboard
    tile_size = 8
    for tx in range(0, w, tile_size):
        for ty in range(2, h):
            tile_idx = (tx // tile_size + (ty - 2) // tile_size) % 2
            color = FLOOR_A if tile_idx == 0 else FLOOR_B
            for px in range(tx, min(tx + tile_size, w)):
                d.point((px, ty), fill=color)

    # Grout lines
    for gx in range(0, w, tile_size):
        d.line([(gx, 2), (gx, h-1)], fill=FLOOR_GROUT)
    for gy in range(2, h, tile_size):
        if gy < h:
            d.line([(0, gy), (w-1, gy)], fill=FLOOR_GROUT)

    return img


if __name__ == '__main__':
    wall = draw_wall(80, 24)
    wall.save(os.path.join(OUT, 'office_bg_wall.png'))
    print(f'Wall: {wall.size}')

    desks = draw_desks(80, 16)
    desks.save(os.path.join(OUT, 'office_bg_desks.png'))
    print(f'Desks: {desks.size}')

    floor = draw_floor(32, 6)
    floor.save(os.path.join(OUT, 'office_bg_floor.png'))
    print(f'Floor: {floor.size}')

    print('Done — files in html/assets/')
