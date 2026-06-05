#!/usr/bin/env python3
"""Generate pixel-art character sprite sheets for Talaria avatars.

Each 128x128 sheet contains an 8x8 grid of 16x16 frames:
  Row 0: Idle (front-facing, 2 breathing frames repeated)
  Row 1: Working (front-facing, typing animation) — legacy
  Row 2: Walk right (4 frames + 4 mirrored)
  Row 3: Walk left  (4 frames)
  Row 4: Sitting at desk (back view, hands on keyboard, typing animation)
  Row 5: Sitting idle (back view, no typing)
  Rows 6-7: spare
"""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'html', 'assets')
os.makedirs(OUT, exist_ok=True)

T = (0, 0, 0, 0)
S = 16  # frame size

# ── Character palettes ──────────────────────────────────
CHARS = {
    'office_man': {
        'skin':       (240, 200, 165, 255),
        'skin_shade': (210, 165, 130, 255),
        'hair':       (60, 40, 25, 255),
        'shirt':      (90, 110, 180, 255),
        'shirt_dk':   (60, 80, 140, 255),
        'pants':      (50, 55, 80, 255),
        'pants_dk':   (35, 40, 60, 255),
        'shoes':      (40, 30, 20, 255),
    },
    'office_woman': {
        'skin':       (245, 210, 180, 255),
        'skin_shade': (215, 175, 140, 255),
        'hair':       (180, 60, 45, 255),
        'shirt':      (200, 70, 90, 255),
        'shirt_dk':   (160, 45, 65, 255),
        'pants':      (50, 50, 60, 255),
        'pants_dk':   (35, 35, 45, 255),
        'shoes':      (30, 25, 20, 255),
    },
    'alien': {
        'skin':       (130, 220, 140, 255),
        'skin_shade': (90, 180, 100, 255),
        'hair':       (40, 100, 50, 255),
        'shirt':      (60, 180, 90, 255),
        'shirt_dk':   (40, 140, 60, 255),
        'pants':      (40, 80, 50, 255),
        'pants_dk':   (25, 55, 30, 255),
        'shoes':      (20, 40, 25, 255),
    },
    'hacker': {
        'skin':       (220, 190, 165, 255),
        'skin_shade': (185, 150, 125, 255),
        'hair':       (30, 25, 20, 255),
        'shirt':      (50, 50, 55, 255),
        'shirt_dk':   (30, 30, 35, 255),
        'pants':      (35, 35, 40, 255),
        'pants_dk':   (20, 20, 25, 255),
        'shoes':      (15, 15, 18, 255),
    },
    'robot': {
        'skin':       (200, 215, 230, 255),
        'skin_shade': (155, 175, 195, 255),
        'hair':       (90, 110, 130, 255),
        'shirt':      (120, 170, 220, 255),
        'shirt_dk':   (80, 130, 180, 255),
        'pants':      (95, 110, 130, 255),
        'pants_dk':   (70, 85, 105, 255),
        'shoes':      (50, 60, 75, 255),
    },
}

# Chair palette (shared)
CHAIR_DK  = (40, 40, 48, 255)
CHAIR_MD  = (60, 60, 70, 255)
CHAIR_LT  = (80, 80, 90, 255)
WHEEL     = (30, 30, 35, 255)


def put(d, x, y, c):
    if 0 <= x < S and 0 <= y < S:
        d.point((x, y), fill=c)


def draw_front(d, p, frame=0, walk_pose=0):
    """Draw character facing forward.
    walk_pose: 0=stand, 1=left foot fwd, 2=right foot fwd
    """
    # Head (y=2..6)
    # Hair top
    for x in range(5, 11):
        put(d, x, 2, p['hair'])
    for x in range(4, 12):
        put(d, x, 3, p['hair'])
    # Face
    for x in range(5, 11):
        put(d, x, 4, p['skin'])
        put(d, x, 5, p['skin'])
    # Hair sides
    put(d, 4, 4, p['hair'])
    put(d, 11, 4, p['hair'])
    put(d, 4, 5, p['skin_shade'])
    put(d, 11, 5, p['skin_shade'])
    # Eyes
    put(d, 6, 4, (30, 30, 30, 255))
    put(d, 9, 4, (30, 30, 30, 255))
    # Mouth
    put(d, 7, 5, p['skin_shade'])
    put(d, 8, 5, p['skin_shade'])
    # Neck
    put(d, 7, 6, p['skin_shade'])
    put(d, 8, 6, p['skin_shade'])

    # Torso (y=7..11)
    for y in range(7, 12):
        for x in range(4, 12):
            put(d, x, y, p['shirt'])
    # Shirt shading on sides
    for y in range(7, 12):
        put(d, 4, y, p['shirt_dk'])
        put(d, 11, y, p['shirt_dk'])
    # Arms (y=7..10)
    for y in range(7, 11):
        put(d, 3, y, p['skin'])
        put(d, 12, y, p['skin'])
    put(d, 3, 10, p['skin_shade'])
    put(d, 12, 10, p['skin_shade'])

    # Pants (y=12..13)
    for y in range(12, 14):
        for x in range(4, 12):
            put(d, x, y, p['pants'])
    # Pant shading
    for y in range(12, 14):
        put(d, 7, y, p['pants_dk'])
        put(d, 8, y, p['pants_dk'])

    # Legs/shoes (y=14..15) - walk cycle
    if walk_pose == 0:
        # Standing
        for x in [4, 5, 10, 11]:
            put(d, x, 14, p['pants'])
            put(d, x, 15, p['shoes'])
    elif walk_pose == 1:
        # Left foot forward
        put(d, 4, 14, p['pants'])
        put(d, 5, 15, p['shoes'])
        put(d, 6, 15, p['shoes'])
        put(d, 10, 14, p['pants'])
        put(d, 10, 15, p['pants'])
        put(d, 11, 15, p['shoes'])
    else:
        # Right foot forward
        put(d, 4, 14, p['pants'])
        put(d, 4, 15, p['shoes'])
        put(d, 5, 15, p['pants'])
        put(d, 10, 14, p['pants'])
        put(d, 10, 15, p['shoes'])
        put(d, 11, 15, p['shoes'])


def draw_side(d, p, walk_pose=0, facing='right'):
    """Draw character walking in profile."""
    # Head
    for x in range(5, 10):
        put(d, x, 2, p['hair'])
    for x in range(5, 10):
        put(d, x, 3, p['hair'])
    for x in range(5, 10):
        put(d, x, 4, p['skin'])
        put(d, x, 5, p['skin'])
    # Hair back
    if facing == 'right':
        put(d, 4, 3, p['hair'])
        put(d, 4, 4, p['hair'])
        # Eye
        put(d, 8, 4, (30, 30, 30, 255))
        # Nose hint
        put(d, 9, 5, p['skin_shade'])
    else:
        put(d, 10, 3, p['hair'])
        put(d, 10, 4, p['hair'])
        put(d, 6, 4, (30, 30, 30, 255))
        put(d, 5, 5, p['skin_shade'])

    # Neck
    put(d, 7, 6, p['skin_shade'])
    put(d, 8, 6, p['skin_shade'])

    # Torso
    for y in range(7, 12):
        for x in range(5, 11):
            put(d, x, y, p['shirt'])
    # Back shading
    if facing == 'right':
        for y in range(7, 12):
            put(d, 5, y, p['shirt_dk'])
    else:
        for y in range(7, 12):
            put(d, 10, y, p['shirt_dk'])

    # Arm — swings with walk
    if facing == 'right':
        arm_x = 10 if walk_pose in (1, 3) else 11
    else:
        arm_x = 5 if walk_pose in (1, 3) else 4
    for y in range(7, 11):
        put(d, arm_x, y, p['skin'])
    put(d, arm_x, 10, p['skin_shade'])

    # Pants
    for y in range(12, 14):
        for x in range(5, 11):
            put(d, x, y, p['pants'])

    # Legs - walk cycle
    if walk_pose == 0:
        # Both feet together
        for x in [6, 9]:
            put(d, x, 14, p['pants'])
            put(d, x, 15, p['shoes'])
    elif walk_pose == 1:
        # Front foot forward
        if facing == 'right':
            put(d, 5, 14, p['pants'])
            put(d, 5, 15, p['shoes'])
            put(d, 9, 14, p['pants'])
            put(d, 10, 15, p['shoes'])
        else:
            put(d, 10, 14, p['pants'])
            put(d, 10, 15, p['shoes'])
            put(d, 6, 14, p['pants'])
            put(d, 5, 15, p['shoes'])
    elif walk_pose == 2:
        # Feet together (passing)
        put(d, 7, 14, p['pants'])
        put(d, 7, 15, p['shoes'])
        put(d, 8, 14, p['pants'])
        put(d, 8, 15, p['shoes'])
    else:  # walk_pose == 3
        # Back foot forward
        if facing == 'right':
            put(d, 6, 14, p['pants'])
            put(d, 5, 15, p['shoes'])
            put(d, 9, 14, p['pants'])
            put(d, 9, 15, p['shoes'])
        else:
            put(d, 9, 14, p['pants'])
            put(d, 10, 15, p['shoes'])
            put(d, 6, 14, p['pants'])
            put(d, 6, 15, p['shoes'])


def draw_sitting_back(d, p, type_frame=0):
    """Draw character sitting at desk, viewed from behind.
    type_frame: 0=hands resting, 1=left hand typing, 2=right hand typing
    Chair occupies bottom; character torso/head visible.
    """
    # Chair back (behind character) — wider than character
    for y in range(8, 14):
        for x in range(3, 13):
            put(d, x, y, CHAIR_DK)
    # Chair back highlight
    for y in range(8, 14):
        put(d, 3, y, CHAIR_MD)
        put(d, 12, y, CHAIR_MD)
    # Chair top edge
    for x in range(3, 13):
        put(d, x, 8, CHAIR_LT)

    # Head (back of head — all hair, no face)
    for x in range(5, 11):
        put(d, x, 2, p['hair'])
    for x in range(4, 12):
        put(d, x, 3, p['hair'])
    for x in range(4, 12):
        put(d, x, 4, p['hair'])
    for x in range(5, 11):
        put(d, x, 5, p['hair'])
    # Neck (small bit of skin)
    put(d, 7, 6, p['skin_shade'])
    put(d, 8, 6, p['skin_shade'])

    # Shoulders/upper back — visible above chair top
    for x in range(4, 12):
        put(d, x, 7, p['shirt'])
    # Sides of torso peek out beside chair
    put(d, 4, 8, p['shirt_dk'])
    put(d, 11, 8, p['shirt_dk'])
    put(d, 4, 9, p['shirt_dk'])
    put(d, 11, 9, p['shirt_dk'])

    # Arms reaching forward (down toward keyboard) - on top of chair
    # Left arm
    if type_frame == 1:
        # Left hand raised slightly
        put(d, 5, 11, p['shirt'])
        put(d, 5, 12, p['skin'])
        put(d, 5, 13, p['skin_shade'])
    else:
        put(d, 5, 11, p['shirt'])
        put(d, 5, 12, p['shirt'])
        put(d, 5, 13, p['skin'])
    # Right arm
    if type_frame == 2:
        put(d, 10, 11, p['shirt'])
        put(d, 10, 12, p['skin'])
        put(d, 10, 13, p['skin_shade'])
    else:
        put(d, 10, 11, p['shirt'])
        put(d, 10, 12, p['shirt'])
        put(d, 10, 13, p['skin'])

    # Chair wheels/base at bottom
    put(d, 6, 15, WHEEL)
    put(d, 7, 15, WHEEL)
    put(d, 8, 15, WHEEL)
    put(d, 9, 15, WHEEL)
    put(d, 7, 14, CHAIR_DK)
    put(d, 8, 14, CHAIR_DK)


def render_sheet(name, palette):
    """Build the 8x8 frame sheet for one character."""
    sheet = Image.new('RGBA', (128, 128), T)
    d = ImageDraw.Draw(sheet)

    # Row 0: idle (front) — 8 frames with subtle breathing variation
    for col in range(8):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        # Tiny breathing: every other frame, lift torso by 0 (no shift, just animation pose)
        draw_front(fd, palette, walk_pose=0)
        # Blink on certain frames
        if col in (3, 4):
            # eyes closed
            for x in [6, 9]:
                fd.point((x, 4), fill=palette['skin'])
            fd.point((6, 4), fill=palette['skin_shade'])
            fd.point((9, 4), fill=palette['skin_shade'])
        sheet.paste(frame, (col * S, 0 * S))

    # Row 1: working (front, typing) — legacy state
    for col in range(8):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        draw_front(fd, palette, walk_pose=0)
        # Arm movement to suggest typing
        if col % 2 == 0:
            fd.point((3, 9), fill=palette['skin_shade'])
            fd.point((12, 9), fill=palette['skin'])
        else:
            fd.point((3, 9), fill=palette['skin'])
            fd.point((12, 9), fill=palette['skin_shade'])
        sheet.paste(frame, (col * S, 1 * S))

    # Row 2: walk right
    walk_cycle = [0, 1, 2, 3, 0, 1, 2, 3]
    for col, pose in enumerate(walk_cycle):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        draw_side(fd, palette, walk_pose=pose, facing='right')
        sheet.paste(frame, (col * S, 2 * S))

    # Row 3: walk left
    for col, pose in enumerate(walk_cycle):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        draw_side(fd, palette, walk_pose=pose, facing='left')
        sheet.paste(frame, (col * S, 3 * S))

    # Row 4: sitting at desk, typing (back view)
    type_cycle = [0, 1, 0, 2, 0, 1, 0, 2]
    for col, tf in enumerate(type_cycle):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        draw_sitting_back(fd, palette, type_frame=tf)
        sheet.paste(frame, (col * S, 4 * S))

    # Row 5: sitting idle (back, no typing)
    for col in range(8):
        frame = Image.new('RGBA', (S, S), T)
        fd = ImageDraw.Draw(frame)
        draw_sitting_back(fd, palette, type_frame=0)
        sheet.paste(frame, (col * S, 5 * S))

    sheet.save(os.path.join(OUT, f'{name}.png'))
    return sheet


if __name__ == '__main__':
    for name, palette in CHARS.items():
        render_sheet(name, palette)
        print(f'{name}.png: 128x128')
    print('Done.')
