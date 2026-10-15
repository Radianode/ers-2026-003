import sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; OUT=os.path.join(S,'build','fig'); BE=os.path.join(S,'be')
NAVY='#12263a'; COPPER='#b56a2d'; SLATE='#7a8b99'; LSLATE='#c3ccd4'; RULE='#d4d9de'; INK='#1a1a1a'; MUTED='#5e6b77'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':RULE,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED})

fig,ax=plt.subplots(figsize=(7.2,4.6),dpi=220); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
def box(x,y,w,h,t,fc='white',ec=NAVY,tc=INK,fs=7.6,ls='-'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.25,rounding_size=0.8',fc=fc,ec=ec,lw=1.1,ls=ls))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=tc)
steps=['1  Module vendor figures: document, version, table, statistic',
 '2  Topology from the board schematic (not continuity)',
 '3  Every source and sink on the node; measure open inputs',
 '4  Module state from signals independent of current',
 '5  Off-state current: ≥10 min, hands off, raw data analysed',
 '6  Disconnect I/O at the module side',
 '7  Compare like with like (off vs power-off figure)']
y=94
for i,s in enumerate(steps):
    box(2,y-9,62,8,s,fc='#f4f6f8' if i%2==0 else 'white',fs=7.0)
    if i<len(steps)-1: ax.annotate('',xy=(33,y-11.2),xytext=(33,y-9.3),arrowprops=dict(arrowstyle='->',color=MUTED,lw=0.9))
    y-=11.4
box(69,22,30,14,'8  Ratio ≫ 1\nReport at system level.\nSubtraction does not rescue it.',ec=COPPER,tc=INK,fs=7.4)
box(69,3,30,14,'9  Separate board from\nmodule: network-confirmed\nPSM vs PSM figure',fs=7.0)
ax.annotate('',xy=(69,29),xytext=(64.4,20),arrowprops=dict(arrowstyle='->',color=COPPER,lw=1.1))
ax.annotate('',xy=(84,17.6),xytext=(84,21.6),arrowprops=dict(arrowstyle='->',color=MUTED,lw=0.9))
fig.savefig(os.path.join(OUT,'fig7_procedure.png'),facecolor='white',bbox_inches='tight'); plt.close(fig)