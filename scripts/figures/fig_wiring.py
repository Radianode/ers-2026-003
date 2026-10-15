"""Figure 8: DIP40CORE-A connections during the 14 October 2026 session (drawn from the session record).
Usage: python3 fig_wiring.py out.png"""
import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
OUT = sys.argv[1]
NAVY = '#12263a'; COPPER = '#b56a2d'; INK = '#1a1a1a'; MUTED = '#5e6b77'; LIGHT = '#f4f6f8'; RED = '#a8323a'; BLUE = '#2b5d8a'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
fig, ax = plt.subplots(figsize=(7.6, 3.9), dpi=220)
ax.set_xlim(0, 200); ax.set_ylim(0, 102); ax.axis('off')

def box(x, y, w, h, title, sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.5', fc=LIGHT, ec=NAVY, lw=1.1))
    ax.text(x + w / 2, y + h - 4, title, ha='center', va='top', fontsize=8.2, fontweight='bold', color=NAVY)
    if sub: ax.text(x + w / 2, y + h - 9.5, sub, ha='center', va='top', fontsize=6.6, color=MUTED)

def pin(x, y, label, side):
    ax.plot([x], [y], marker='o', ms=2.6, color=INK)
    if side == 'L': ax.text(x + 2, y, label, ha='left', va='center', fontsize=7.2, color=INK)
    else: ax.text(x - 2, y, label, ha='right', va='center', fontsize=7.2, color=INK)

def wire(pts, col=INK, lw=1.1, ls='-'):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=col, lw=lw, ls=ls, solid_capstyle='round')

# boxes: x, y, w, h
box(2, 44, 36, 46, 'PPK2', 'source meter\n3,800 mV')
box(58, 14, 46, 76, 'DIP40CORE-A', 'BG95-M3 on carrier')
box(126, 14, 30, 76, 'TXS0108E', 'level shifter')
box(170, 14, 29, 76, 'Raspberry\nPi 4', None)

# PPK2 terminals
pin(38, 64, 'VOUT', 'R'); pin(38, 54, 'GND', 'R')
# BG95 left pins
Y = {'VBAT': 74, 'GND': 62, 'VIN': 50}
pin(58, 64, '39  VBAT', 'L'); pin(58, 54, '40  GND', 'L'); pin(58, 44, '2  VIN (not connected)', 'L')
# BG95 right pins
pin(104, 72, 'VDD-EXT  32', 'R'); pin(104, 36, 'MAIN-TXD  29', 'R'); pin(104, 26, 'MAIN-RXD  30', 'R')
# converter pins
pin(126, 72, 'VA', 'L'); pin(126, 62, 'OE', 'L'); pin(126, 36, 'A', 'L'); pin(126, 26, 'A', 'L'); pin(126, 18, 'GND', 'L')
pin(156, 72, 'VB', 'R'); pin(156, 36, 'B', 'R'); pin(156, 26, 'B', 'R')
# Pi pins
pin(170, 72, '3.3 V', 'L'); pin(170, 36, 'RXD', 'L'); pin(170, 26, 'TXD', 'L'); pin(170, 18, 'GND', 'L')

# supply and ground
wire([(38, 64), (58, 64)], COPPER, 1.8); ax.text(48, 66, 'supply', ha='center', fontsize=6.6, color=COPPER)
wire([(38, 54), (58, 54)], INK, 1.4)
ax.plot([52, 58], [44, 44], color=RED, lw=1.0); ax.plot([52], [44], marker='o', ms=3.2, mfc='white', mec=RED)
# I/O supply for the converter's A side, OE tied to VA
wire([(104, 72), (126, 72)], BLUE)
wire([(120, 72), (120, 62), (126, 62)], BLUE)
ax.plot([120], [72], marker='o', ms=2.4, color=BLUE)
# VB from the Pi
wire([(156, 72), (170, 72)], BLUE)
# UART paths
wire([(104, 36), (126, 36)]); wire([(156, 36), (170, 36)])
wire([(104, 26), (126, 26)]); wire([(156, 26), (170, 26)])
ax.annotate('', xy=(122, 39.5), xytext=(108, 39.5), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.8))
ax.annotate('', xy=(108, 29.5), xytext=(122, 29.5), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.8))
# common ground rail below the boxes
wire([(45, 54), (45, 6), (192, 6)], INK, 1.0)
wire([(126, 18), (122, 18), (122, 6)], INK, 1.0)
wire([(170, 18), (166, 18), (166, 6)], INK, 1.0)
ax.plot([45], [54], marker='o', ms=2.4, color=INK)
ax.text(192, 8, 'common ground', ha='right', va='bottom', fontsize=6.4, color=MUTED)
fig.savefig(OUT, facecolor='white', bbox_inches='tight', pad_inches=0.05); plt.close(fig)
