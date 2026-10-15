import sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
S=sys.argv[1]; OUT=os.path.join(S,'build','fig')
NAVY='#12263a'; COPPER='#b56a2d'; SLATE='#7a8b99'; RULE='#d4d9de'; INK='#1a1a1a'; MUTED='#5e6b77'; LIGHT='#f4f6f8'; RED='#a8323a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8})
def new(w,h):
    fig,ax=plt.subplots(figsize=(w,h),dpi=220); ax.set_xlim(0,100); ax.set_ylim(0,100*h/w); ax.axis('off'); return fig,ax
def box(ax,x,y,w,h,t,fc='white',ec=NAVY,fs=7.2,ls='-',tc=INK,ha='center'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=0.7',fc=fc,ec=ec,lw=1.0,ls=ls))
    ax.text(x+w/2 if ha=='center' else x+1.2,y+h/2,t,ha=ha,va='center',fontsize=fs,color=tc,linespacing=1.25)
def wire(ax,pts,col=INK,lw=1.0,ls='-'):
    xs,ys=zip(*pts); ax.plot(xs,ys,color=col,lw=lw,ls=ls,solid_capstyle='round')
def lab(ax,x,y,t,col=MUTED,fs=6.6,ha='center',va='bottom'):
    ax.text(x,y,t,color=col,fontsize=fs,ha=ha,va=va)

# ---------- Net diagram, Board 1 (from D5) ----------
fig,ax=new(7.4,3.6); ax.set_ylim(0,55)
wire(ax,[(18,30),(96,30)],COPPER,3); lab(ax,57,31.5,'VBAT net (shared)',COPPER,7.2)
box(ax,1,25,15,10,'Header H1\npin 1',fc=LIGHT); wire(ax,[(16,30),(18,30)],COPPER,3)
items=[(22,'Module VBAT\npins 34, 35\n(SIM7080G)'),(40,'PWR LED\nvia R12 1 kΩ\nto GND'),(58,'U2 RT9193-33\nLDO, EN = VIN\n→ 3V3 → P2'),(78,'D1 B5819WS\n(cathode on\nVBAT)')]
for x,t in items:
    wire(ax,[(x+5,30),(x+5,22)],INK); box(ax,x,8,10+0 if False else 12,14,t,fs=6.4)
box(ax,74,40,20,10,'U1 MP1482 buck from 5 V\n(USB / Pi header);\nanode side of D1',fs=6.2,ls='--')
wire(ax,[(90,40),(90,24),(90,15),(90,15)],INK,0.9,'--'); wire(ax,[(90,15),(90,15)],INK)
box(ax,22,40,26,10,'STA LED via R13 1 kΩ,\ndriven by module STATUS (pin 42)',fs=6.3,ls='--')
lab(ax,50,1,'Redrawn by Radianode from the Waveshare SIM7080X Cat-M/NB-IoT HAT schematic. Simplified; not a reproduction.',MUTED,6.2)
fig.savefig(os.path.join(OUT,'figN1_board1_net.png'),facecolor='white',bbox_inches='tight'); plt.close(fig)

# ---------- Net diagram, Board 2 (from D6) ----------
fig,ax=new(7.4,4.0); ax.set_ylim(0,60)
wire(ax,[(18,34),(97,34)],COPPER,3); lab(ax,80,35.5,'VBAT net (single node, shared with the module)',COPPER,7.2)
box(ax,1,29,15,10,'Header\npin 39',fc=LIGHT); wire(ax,[(16,34),(18,34)],COPPER,3)
items=[(20,'Module VBAT\nBB 32/33\nRF 52/53'),(33,'C8, C9 100 µF\nC1 to C7'),(46,'D2 LED\nvia R2\n10 kΩ\n(est. 0.1–\n0.2 mA)'),(59,'U7 FB\ndivider\nR26 15 kΩ\n+ R27 3.9 kΩ\n(est. 0.20 mA)'),(72,'D3 NET\nLED via\nR6 1 kΩ,\nQ2-switched'),(85,'R7 "0R/NC"\n→ module\nUSB_VBUS')]
for x,t in items:
    wire(ax,[(x+5.5,34),(x+5.5,26)],INK); box(ax,x,10,11.5,16,t,fs=6.0)
box(ax,40,46,30,11,'U7 JW5033H buck\nSW via L3 4.7 µH to VBAT',fs=6.4)
wire(ax,[(55,46),(55,34)],INK)
box(ax,4,46,24,11,'Header pin 2 VIN\n(unconnected at test;\nread 3.333 V, back-powered)',fs=6.2,ec=RED)
wire(ax,[(28,51.5),(40,51.5)],RED,1.0,'--'); lab(ax,34,52.3,'U7 input',RED,6.2)
box(ax,74,46,23,11,'R1 4.7 kΩ / C21 1 nF\non module PWRKEY\n(auto-start network;\nPCBA specification, note 7)',fs=6.1,ls='--')
lab(ax,50,3,'Redrawn by Radianode from DIP40CORE-A BG95 (20230417). Simplified; not a reproduction. Currents are estimates from component values.',MUTED,6.0)
fig.savefig(os.path.join(OUT,'figN2_board2_net.png'),facecolor='white',bbox_inches='tight'); plt.close(fig)
print('ok')
