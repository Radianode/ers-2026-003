"""Figure 1: PPK2 operating-mode evidence, from three Power Profiler v4.4.1 screenshots.
Usage: python3 fig_mode.py OCT14_RUN2_SCREENSHOT.png SEPT_SOURCE_METER_SCREENSHOT.png AMPERE_METER_REFERENCE.png out.png
  (a) 14 October 2026 DIP40CORE-A session, run 2 recording in progress (A2_1_run2_screen_t67s.png)
  (b) September 2026 DIP40CORE-A capture (1.5mA.png)
  (c) ampere-meter reference view (ppk2_2.png)
Crops only; no pixel content is altered. Panel letters and callouts are drawn outside the images."""
import sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
A, B, C, OUT = sys.argv[1:5]
NAVY = '#12263a'; COPPER = '#b56a2d'; MUTED = '#5e6b77'; RULE = '#d4d9de'
plt.rcParams.update({'font.family': 'DejaVu Sans'})
SIDE = (0, 84, 262, 412)                       # side panel: mode, supply, sampling
a = Image.open(A).convert('RGB').crop(SIDE)
alog = Image.open(A).convert('RGB').crop((262, 844, 700, 866))   # log line: 20:20:59.186 Mode: Source meter
b = Image.open(B).convert('RGB').crop(SIDE)
c = Image.open(C).convert('RGB').crop(SIDE)
clog = Image.open(C).convert('RGB').crop((262, 938, 640, 958))   # log line: Mode: Ampere meter

fig = plt.figure(figsize=(7.4, 4.3), dpi=220)
W, H = 0.215, 0.60; Y = 0.20
axa = fig.add_axes([0.01, Y, W, H]); axb = fig.add_axes([0.355, Y, W, H]); axc = fig.add_axes([0.72, Y, W, H])
axal = fig.add_axes([0.01, 0.06, 0.30, 0.05]); axcl = fig.add_axes([0.72, 0.06, 0.27, 0.05])
for ax, im in ((axa, a), (axb, b), (axc, c), (axal, alog), (axcl, clog)):
    ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values(): s_.set_color(RULE)
def head(x, t, sub):
    fig.text(x, 0.92, t, fontsize=8.6, color=NAVY, fontweight='bold'); fig.text(x, 0.865, sub, fontsize=7.2, color=MUTED)
head(0.01, '(a)  14 October 2026', 'DIP40CORE-A, run 2 recording')
head(0.355, '(b)  September 2026', 'DIP40CORE-A off-state capture')
head(0.72, '(c)  Reference view', 'Ampere-meter mode')
fig.text(0.01, 0.125, 'Application log, 20:20:59 (before run 2)', fontsize=7, color=MUTED)
fig.text(0.72, 0.125, 'Application log entry for (c)', fontsize=7, color=MUTED)
def call(ax, y, txt):
    ax.annotate(txt, xy=(260, y), xytext=(278, y), fontsize=6.6, color=COPPER, ha='left', va='center',
                arrowprops=dict(arrowstyle='->', color=COPPER, lw=0.8), annotation_clip=False)
call(axa, 62, 'Source meter\n(greyed during\nrecording)'); call(axa, 104, '3,800 mV'); call(axa, 238, '100 kS/s')
call(axb, 62, 'Source meter'); call(axb, 104, '3,800 mV'); call(axb, 238, '100 kS/s')
for ax, w in ((axal, 438), (axcl, 378)):
    ax.add_patch(Rectangle((1, 1), w - 3, 19, fill=False, ec=COPPER, lw=1.1))
fig.savefig(OUT, facecolor='white'); plt.close(fig)
