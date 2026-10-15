import sys, os, datetime
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
S=sys.argv[1]; OUT=os.path.join(S,'build','fig'); D=os.environ.get('ERS003_DATA','/mnt/user-data/uploads/Bench Evidence')
NAVY='#12263a'; COPPER='#b56a2d'; SLATE='#7a8b99'; LSLATE='#c3ccd4'; RULE='#d4d9de'; INK='#1a1a1a'; MUTED='#5e6b77'; RED='#a8323a'; GREEN='#2e7d4f'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.edgecolor':RULE,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED})
def load(n): return np.loadtxt(os.path.join(D,n),delimiter=',',skiprows=1)
def clean(ax):
    for s in ['top','right']: ax.spines[s].set_visible(False)
    ax.grid(color='#eef1f4',linewidth=0.6); ax.set_axisbelow(True)

# ---- Fig 1 (updated value) ----
fig,ax=plt.subplots(figsize=(7.2,3.4),dpi=220)
rows=[('BG95-M3  ·  header current, off (STATUS, VDD-EXT)',1539,NAVY,'1.539 mA'),
      ('BG95-M3  ·  Quectel power-off leakage (avg)',12.99,SLATE,'12.99 µA'),
      ('BG95-M3  ·  Quectel PSM (avg)',3.89,LSLATE,'3.89 µA'),
      ('SIM7080G  ·  header current, off (PWRKEY, STA LED)',1886,NAVY,'1.886 mA'),
      ('SIM7080G  ·  SIMCom power-off (max)',15,SLATE,'15 µA'),
      ('SIM7080G  ·  SIMCom PSM (typ)',3,LSLATE,'3 µA')]
ys=[4.9,4.2,3.5,2.2,1.5,0.8]
for (lab,v,c,t),y in zip(rows,ys):
    ax.barh(y,v-1,left=1,height=0.52,color=c,edgecolor='white',linewidth=2)
    ax.text(v*1.3,y,t,va='center',ha='left',color=INK,fontsize=8.5,fontweight='bold' if c==NAVY else 'normal')
ax.set_xscale('log'); ax.set_xlim(1,2e4); ax.set_ylim(0.3,5.6)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows],fontsize=8,color=INK)
ax.set_xlabel('Current (µA, logarithmic scale)',fontsize=8.5)
ax.grid(axis='x',which='both',color='#eef1f4',linewidth=0.6); ax.set_axisbelow(True)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.tick_params(axis='y',length=0)
def bracket(y1,y2,x,txt):
    ax.annotate('',xy=(x,y1),xytext=(x,y2),arrowprops=dict(arrowstyle='<->',color=COPPER,lw=1.2))
    ax.text(x*1.15,(y1+y2)/2,txt,color=COPPER,fontsize=8,va='center',fontweight='bold')
ax.text(1.05,5.35,"Question 1: header reading against the module's own power-off figure",fontsize=7.5,color=MUTED)
bracket(4.9,4.2,4500,'≈118×'); bracket(2.2,1.5,4500,'≥125×')
plt.tight_layout(); fig.savefig(os.path.join(OUT,'fig1_comparison.png'),facecolor='white'); plt.close(fig)

# ---- Fig R2: run 2 timeline ----
r=load('A2_run2_1s_summary.csv'); t0=datetime.datetime(2026,10,14,20,33,18,604000)
x=[t0+datetime.timedelta(seconds=float(k)) for k in r[:,0]]
fig,ax=plt.subplots(figsize=(7.4,3.5),dpi=220)
ax.fill_between(x,np.maximum(r[:,2],100)/1000,r[:,3]/1000,color=LSLATE,alpha=0.6,lw=0,label='per-second min to max')
ax.plot(x,r[:,1]/1000,color=NAVY,lw=1.0,label='per-second mean')
ax.set_yscale('log'); ax.set_ylim(0.5,3000); ax.set_ylabel('Header current (mA, log)')
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')); ax.set_xlabel('Time, 14 October 2026 (WAT)')
def mark(sec,txt,y,col=COPPER,ha='left'):
    tx=t0+datetime.timedelta(seconds=sec); ax.axvline(tx,color=col,lw=0.8,ls='--')
    ax.text(tx+datetime.timedelta(seconds=8 if ha=='left' else -8),y,txt,color=col,fontsize=7,ha=ha,va='center')
mark(433,'20:40:32 (operator: probe slip):\n1.02 A spike, drop to\noff level (no QPOWD)',600,RED,'right')
mark(960,'',1500,RED); ax.text(t0+datetime.timedelta(seconds=1100),1500,'20:49:18 and 20:50:39 (operator:\nprobe slips): to 1.68 A',color=RED,fontsize=7,va='center')
mark(1053,'20:50:51 module back on,\nno operator power cycle',10,MUTED)
mark(1309,'20:55:08\nAT+QPOWD=1',150,GREEN)
ax.text(t0+datetime.timedelta(seconds=150),40,'on, 26.26 mA',fontsize=7.5,color=NAVY)
ax.text(t0+datetime.timedelta(seconds=1450),2.6,'off, 1.539 mA',fontsize=7.5,color=NAVY)
clean(ax); ax.legend(loc='lower left',fontsize=7,frameon=False)
plt.tight_layout(); fig.savefig(os.path.join(OUT,'figR2_run2_timeline.png'),facecolor='white'); plt.close(fig)

# ---- Fig R3: run 3 per-second means ----
r=load('A2_run3_off_1s_summary.csv'); t0=datetime.datetime(2026,10,14,21,27,9,203000)
x=[t0+datetime.timedelta(seconds=float(k)) for k in r[:,0]]
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.4,3.0),dpi=220,gridspec_kw={'width_ratios':[3,1.2]})
a1.plot(x,r[:,1]/1000,color=NAVY,lw=0.7)
for (a,b),col in zip([(0,600),(600,1200),(1200,1800)],[COPPER]*3):
    mm=r[a:b,1].mean()/1000; a1.plot([x[a],x[b-1]],[mm,mm],color=COPPER,lw=1.6)
    a1.text(x[a+300],1.5448,f'{mm:.4f} mA',ha='center',fontsize=7,color=COPPER)
a1.set_ylim(1.532,1.546); a1.set_ylabel('1 s mean (mA)'); a1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')); a1.set_xlabel('Time (WAT)')
a1.set_title('1,800 one-second means; 10-minute averages in copper',fontsize=7.5,color=MUTED,loc='left'); clean(a1)
a2.axhspan(1.4535,1.6065,color='#e6efe9'); a2.axhline(1.53,color=SLATE,lw=1,ls='--'); a2.plot([0.5],[1.5388],'o',color=NAVY)
a2.text(0.62,1.548,'run 3\n1.539 mA',fontsize=7,va='center',color=NAVY); a2.text(0.05,1.522,'September 2026\nreference: 1.53 mA',fontsize=7,color=SLATE,va='top')
a2.text(0.05,1.60,'pre-set band\n±5 %',fontsize=7,color=GREEN,va='top')
a2.set_xlim(0,1.2); a2.set_ylim(1.44,1.62); a2.set_xticks([]); a2.set_title('Against criterion',fontsize=7.5,color=MUTED,loc='left'); clean(a2)
plt.tight_layout(); fig.savefig(os.path.join(OUT,'figR3_run3.png'),facecolor='white'); plt.close(fig)

# ---- Fig A4 ----
r=load('A4_uart_disconnect_1s_summary.csv')[:300]
fig,ax=plt.subplots(figsize=(7.4,2.6),dpi=220)
ax.plot(r[:,0],r[:,1]/1000,color=NAVY,lw=0.9)
for a,b in [(0,76),(79,169),(172,300)]:
    mm=r[a:b,1].mean()/1000; ax.plot([a,b-1],[mm,mm],color=COPPER,lw=1.6); ax.text((a+b)/2,mm-0.0035,f'{mm:.4f} mA',ha='center',fontsize=7,color=COPPER)
for s,t in [(77.6,'77.6 s transient\n(peak 25.9 mA, 0.6 ms)'),(170,'170 s transient')]:
    ax.axvline(s,color=RED,lw=0.8,ls='--'); ax.text(s+3,1.553,t,fontsize=7,color=RED,va='top')
ax.set_ylim(1.530,1.560); ax.set_xlim(0,300); ax.set_xlabel('Seconds from Start (≈ 22:31 WAT)'); ax.set_ylabel('1 s mean (mA)')
ax.set_title('UART wires off pins 29/30 at ≈ 22:32, back at ≈ 22:34 (operator times, to the minute)',fontsize=7.5,color=MUTED,loc='left'); clean(ax)
plt.tight_layout(); fig.savefig(os.path.join(OUT,'figA4_uart.png'),facecolor='white'); plt.close(fig)
print('ok')
