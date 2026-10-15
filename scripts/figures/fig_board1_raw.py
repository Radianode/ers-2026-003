"""Figure 2: Waveshare HAT header current. (a) 15 October 2026 recording 2 (300 s): module off, started and powered down with PWRKEY.
(b) 26 August 2026 capture (10 s) previously reported in ERS-2026-002.
Usage: python3 fig_board1_raw.py OCT_RECORDING_2.csv AUG_CAPTURE.csv out.png
Prints the window statistics quoted in the report. Window means exclude 1 s either side of each transition."""
import sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OCT, AUG, OUT = sys.argv[1:4]
NAVY='#12263a'; COPPER='#b56a2d'; MUTED='#5e6b77'; RULE='#d4d9de'; INK='#1a1a1a'; BAND='#9fb0bf'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.edgecolor':RULE,'xtick.color':MUTED,'ytick.color':MUTED})
FS = 100000
def load(p): return pd.read_csv(p, usecols=[1], dtype={'Current(uA)': 'float32'}).iloc[:, 0].to_numpy(np.float64)
o = load(OCT); n = (len(o) // 1000) * 1000
ms = o[:n].reshape(-1, 100).mean(1)                       # 1 ms means
on = np.where(ms > 5000)[0]; t_on, t_off = on[0] / 1000, (on[-1] + 1) / 1000
pre = o[:int((t_on - 1) * FS)]; post = o[int((t_off + 1) * FS):n]; mid = o[int(t_on * FS):int(t_off * FS)]
print(f'power-on {t_on:.3f} s; power-down {t_off:.3f} s')
print(f'before: {len(pre)/FS:.1f} s, mean {pre.mean()/1000:.4f} mA; on: mean {mid.mean()/1000:.2f} mA, max {mid.max()/1000:.1f} mA; after: {len(post)/FS:.1f} s, mean {post.mean()/1000:.4f} mA')
a = load(AUG); print(f'26 Aug: n {len(a):,}, mean {a.mean()/1000:.3f} mA, max {a.max()/1000:.3f} mA')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.2), dpi=220, gridspec_kw={'height_ratios': [1.35, 1]})
c = o[:n].reshape(-1, 1000); t = np.arange(c.shape[0]) / 100
ax1.fill_between(t, c.min(1) / 1000, c.max(1) / 1000, color=BAND, lw=0, label='min to max per 10 ms')
ax1.plot(t, c.mean(1) / 1000, color=NAVY, lw=0.6, label='10 ms mean')
ax1.set_yscale('log'); ax1.set_xlim(0, n / FS); ax1.set_ylim(1, 400)
for x, lab in ((t_on, 'PWRKEY: power-on'), (t_off, 'PWRKEY: power-down')):
    ax1.axvline(x, color=COPPER, lw=0.9, ls='--'); ax1.text(x - 2, 280, lab, color=COPPER, fontsize=7.5, ha='right', va='top')
ax1.text(t_on / 2, 2.6, f'Module off\n{pre.mean()/1000:.3f} mA', ha='center', fontsize=7.8, color=INK, fontweight='bold')
ax1.text((t_on + t_off) / 2, 4.2, f'Module on\n{mid.mean()/1000:.1f} mA mean', ha='center', fontsize=7.8, color=INK)
ax1.annotate(f'Off\n{post.mean()/1000:.3f} mA', xy=((t_off + n / FS) / 2, 1.95), xytext=(n / FS + 6, 3.2), ha='left', fontsize=7.8, color=INK, fontweight='bold',
             annotation_clip=False, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax1.set_ylabel('Header current (mA, log)'); ax1.set_xlabel('Time from start of recording (s)')
ax1.set_title('(a)  15 October 2026, recording 2: source meter, 3,800 mV, 100 kS/s', fontsize=8.5, color=NAVY, loc='left', fontweight='bold')
ax1.legend(frameon=False, fontsize=7, loc='center left', bbox_to_anchor=(0.0, 0.62))
k = 1000; m = (len(a) // k) * k; ac = a[:m].reshape(-1, k); ta = np.arange(ac.shape[0]) / 100
ax2.fill_between(ta, ac.min(1) / 1000, ac.max(1) / 1000, color=BAND, lw=0)
ax2.plot(ta, ac.mean(1) / 1000, color=NAVY, lw=1.0)
ax2.axhline(a.mean() / 1000, color=COPPER, lw=1, ls='--')
ax2.text(10.05, a.mean() / 1000, f' {a.mean()/1000:.3f} mA\n 10 s mean', color=COPPER, va='center', fontsize=7.8, fontweight='bold')
ax2.set_xlim(0, 10); ax2.set_ylim(1.9, 2.2); ax2.set_xlabel('Time (s)'); ax2.set_ylabel('Header current (mA)')
ax2.set_title('(b)  26 August 2026, ERS-2026-002 capture: supply voltage and instrument mode not recorded', fontsize=8.5, color=NAVY, loc='left', fontweight='bold')
for ax in (ax1, ax2):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#eef1f4', which='both'); ax.set_axisbelow(True)
plt.tight_layout(); fig.savefig(OUT, facecolor='white'); plt.close(fig)
