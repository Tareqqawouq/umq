#!/usr/bin/env python3
"""Draws the truck-mounted drilling rig artwork used for the app icon and the start screen.

Writes dev/icon.svg (square, for icons) and dev/splash.svg (tall, for the start screen).
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))


def rig(ox, oy, s):
    """Truck-mounted rig, side view, cab on the left, mast raised at the rear. Ground line at y=0."""
    def P(x, y):
        return '%.1f,%.1f' % (ox + x * s, oy + y * s)

    def rect(x, y, w, h, fill, rx=0, extra=''):
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"%s/>' % (ox + x * s, oy + y * s, w * s, h * s, rx * s, fill, extra)

    def line(x1, y1, x2, y2, col, w):
        return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (ox + x1 * s, oy + y1 * s, ox + x2 * s, oy + y2 * s, col, w * s)

    def poly(pts, fill, extra=''):
        return '<polygon points="%s" fill="%s"%s/>' % (' '.join(P(x, y) for x, y in pts), fill, extra)

    def wheel(x):
        return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#14191c"/>' % (ox + x * s, oy - 46 * s, 46 * s) +
                '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#5d666b"/>' % (ox + x * s, oy - 46 * s, 22 * s) +
                '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#2b3236"/>' % (ox + x * s, oy - 46 * s, 9 * s))

    o = []
    # shadow
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#000" opacity=".35"/>' % (ox + 430 * s, oy + 4 * s, 470 * s, 16 * s))
    # ---- mast (rear), lattice tower
    mx0, mx1, top, base = 650, 730, -760, -100
    o.append(poly([(mx0, base), (mx1, base), (mx1 - 6, top), (mx0 + 6, top)], 'url(#mastShade)'))
    for x in (mx0, mx1):
        o.append(line(x + (6 if x == mx0 else -6) * 0, base, x + (6 if x == mx0 else -6), top, '#e6d6ac', 9))
    y = base
    step = 52
    k = 0
    while y - step >= top:
        a, b = y, y - step
        xl0, xr0 = mx0 + 6 * (base - a) / (base - top), mx1 - 6 * (base - a) / (base - top)
        xl1, xr1 = mx0 + 6 * (base - b) / (base - top), mx1 - 6 * (base - b) / (base - top)
        o.append(line(xl1, b, xr1, b, '#d6c49a', 5))
        o.append(line(xl0, a, xr1, b, '#c4b285', 4) if k % 2 == 0 else line(xr0, a, xl1, b, '#c4b285', 4))
        y = b
        k += 1
    # crown block
    o.append(rect(mx0 - 18, top - 34, (mx1 - mx0) + 36, 36, '#2e3b44', 4))
    o.append(rect(mx0 - 10, top - 48, (mx1 - mx0) + 20, 16, '#ff7a1a', 3))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffd27a"/>' % (ox + (mx0 + mx1) / 2 * s, oy + (top - 60) * s, 7 * s))
    # drill string inside mast + top drive
    cx = (mx0 + mx1) / 2
    o.append(line(cx, -420, cx, -6, '#c7ced2', 12))
    o.append(line(cx, top + 10, cx, -470, '#3b4850', 4))
    o.append(rect(cx - 40, -500, 80, 86, '#ff7a1a', 8))
    o.append(rect(cx - 40, -500, 80, 18, '#d9600f', 6))
    o.append(rect(cx - 26, -414, 52, 22, '#2e3b44', 4))
    # casing / wellhead at ground
    o.append(rect(cx - 26, -30, 52, 34, '#6c767c', 4))
    o.append(rect(cx - 40, -40, 80, 14, '#8d979c', 3))
    # rear platform + jacks
    o.append(rect(600, -136, 190, 26, '#3a464d', 3))
    for x in (612, 770):
        o.append(rect(x - 7, -112, 14, 112, '#5d666b'))
        o.append(rect(x - 22, -10, 44, 10, '#3a464d', 2))
    # hydraulic ram raising the mast
    o.append(line(470, -120, mx0 + 4, -430, '#9aa3a8', 20))
    o.append(line(470, -120, 560, -260, '#d6dbde', 12))
    # ---- chassis
    o.append(rect(70, -150, 600, 34, '#2b3236', 4))
    # deck equipment: power pack + mud pump + pipe rack
    o.append(rect(250, -270, 170, 120, '#f2efe6', 6))
    o.append(rect(250, -270, 170, 22, '#ff7a1a', 6))
    for i in range(5):
        o.append(rect(270 + i * 28, -235, 14, 70, '#c9c4b6', 3))
    o.append(rect(430, -230, 130, 80, '#4b8fb3', 6))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#2f6f90"/>' % (ox + 495 * s, oy - 190 * s, 24 * s))
    for i in range(4):
        o.append(rect(250 + 0, -300 - i * 14, 330, 12, '#b9c0c4', 6))
    o.append(rect(560, -310, 14, 160, '#5d666b'))
    o.append(rect(246, -310, 14, 40, '#5d666b'))
    # exhaust stack
    o.append(rect(222, -360, 14, 120, '#4a5358', 3))
    # ---- cab (left)
    o.append(poly([(-40, -130), (-40, -395), (-26, -412), (196, -412), (204, -130)], '#1f4fa8'))
    o.append(rect(-30, -470, 210, 62, '#1f4fa8', 14))
    o.append(rect(-24, -385, 96, 100, '#1d3346', 6))
    o.append(rect(86, -385, 96, 100, '#1d3346', 6))
    o.append(rect(-50, -330, 14, 70, '#2b3236', 3))
    o.append(rect(-44, -240, 260, 20, '#163c80'))
    o.append(rect(-50, -170, 70, 26, '#2b3236', 4))
    o.append(rect(-52, -214, 18, 30, '#ffe7a8', 4))
    o.append(rect(150, -262, 40, 8, '#9aa3a8', 3))
    # fuel tank + steps
    o.append(rect(100, -150, 90, 46, '#9aa3a8', 10))
    # wheels
    for x in (40, 420, 520):
        o.append(wheel(x))
    # mud flaps / fenders
    o.append(rect(-20, -112, 120, 10, '#14191c', 5))
    o.append(rect(368, -112, 210, 10, '#14191c', 5))
    return ''.join(o)


DEFS = '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0d1b26"/><stop offset=".45" stop-color="#1f3a4f"/><stop offset=".72" stop-color="#c8673a"/><stop offset=".86" stop-color="#f3a649"/><stop offset="1" stop-color="#f7c46b"/>
</linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2c4"/><stop offset=".55" stop-color="#ffd27a"/><stop offset="1" stop-color="#ffb14a" stop-opacity="0"/></radialGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5236"/><stop offset="1" stop-color="#2a1d16"/></linearGradient>
<linearGradient id="mastShade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d6c49a" stop-opacity=".14"/><stop offset="1" stop-color="#ff7a1a" stop-opacity=".05"/></linearGradient>
</defs>'''


def scene(w, h, horizon, sun, rig_xy, rig_s):
    sx, sy, sr = sun
    rx, ry = rig_xy
    dunes = ('<path d="M0 %d C %d %d %d %d %d %d C %d %d %d %d %d %d L %d %d L 0 %d Z" fill="#8a5a3a" opacity=".85"/>' %
             (horizon - 10, w * .2, horizon - 70, w * .38, horizon - 60, w * .55, horizon - 18, w * .7, horizon + 10, w * .85, horizon - 80, w, horizon - 30, w, h, h))
    dunes2 = ('<path d="M0 %d C %d %d %d %d %d %d L %d %d L 0 %d Z" fill="url(#ground)"/>' %
              (horizon + 20, w * .35, horizon - 20, w * .7, horizon + 40, w, horizon + 5, w, h, h))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">' % (w, h) + DEFS +
            '<rect width="%d" height="%d" fill="url(#sky)"/>' % (w, h) +
            '<circle cx="%d" cy="%d" r="%d" fill="url(#sun)"/>' % (sx, sy, sr) +
            dunes + dunes2 + rig(rx, ry, rig_s) + '</svg>')


# square icon: rig centred, mast reaching near the top
icon = scene(1024, 1024, 760, (690, 330, 230), (205, 905), 0.92)
open(os.path.join(HERE, 'icon.svg'), 'w').write(icon)
# maskable icon: same scene, rig smaller and centred so round/squircle masks keep all of it
open(os.path.join(HERE, 'icon-maskable.svg'), 'w').write(scene(1024, 1024, 730, (660, 360, 210), (250, 840), 0.72))
# start screen (portrait)
splash = scene(1080, 1920, 1380, (760, 760, 300), (150, 1560), 1.05)
open(os.path.join(HERE, 'splash.svg'), 'w').write(splash)
# start screen (landscape: computers, tablets on their side)
open(os.path.join(HERE, 'splash-wide.svg'), 'w').write(scene(1920, 1080, 800, (1380, 470, 260), (1010, 960), 0.95))
print('wrote icon.svg and splash.svg')
