#!/usr/bin/env python3
"""ERS-2026-003 analysis: reproduces the Board 2 figures from the PPK2 files.

Sub-commands
  ppk2   FILE.ppk2 OUT.csv        per-second summary from a Power Profiler .ppk2 state file
  csv    FILE.csv  OUT.csv        per-second summary from a Power Profiler CSV export
  events FILE.csv  [LOW] [HIGH]   list runs of samples below LOW or above HIGH (uA; defaults 1300, 2000)
  stats  SUMMARY.csv A:B [A:B ...] mean of whole seconds A..B-1 from a per-second summary

Per-second summary columns: second, mean_uA, min_uA, max_uA, n (stats also accepts second, mean_uA, n; the last column is the sample count) (100,000 samples per full second at 100 kS/s).

.ppk2 format (Power Profiler v4.4.1, formatVersion 2), as read here: a zip holding
  metadata.json  {"metadata":{"samplesPerSecond":100000,"startSystemTime":<epoch ms>},"formatVersion":2}
  session.raw    consecutive 6-byte records: little-endian float32 current in uA, uint16 digital bits
  minimap.raw    display data (not used)
This layout was checked by comparing the first samples of A2_run3_off.ppk2 with A2_run3_off.csv.
"""
import sys, json, zipfile, datetime
import numpy as np

SPS = 100_000

class Acc:
    def __init__(self, nbins=4000):
        self.s = np.zeros(nbins); self.c = np.zeros(nbins)
        self.mn = np.full(nbins, np.inf); self.mx = np.full(nbins, -np.inf)
    def add(self, b, i):
        np.add.at(self.s, b, i); np.add.at(self.c, b, 1)
        np.minimum.at(self.mn, b, i); np.maximum.at(self.mx, b, i)
    def write(self, out):
        n = int((self.c > 0).sum())
        np.savetxt(out, np.c_[np.arange(n), self.s[:n] / self.c[:n], self.mn[:n], self.mx[:n], self.c[:n]],
                   delimiter=',', header='second,mean_uA,min_uA,max_uA,n', comments='', fmt='%.4f')
        tot = self.s[:n].sum() / self.c[:n].sum()
        print(f'samples {int(self.c[:n].sum())}  mean {tot:.3f} uA  min {self.mn[:n].min():.3f}  max {self.mx[:n].max():.3f}')

def ppk2(src, out):
    z = zipfile.ZipFile(src); md = json.loads(z.read('metadata.json'))
    st = md['metadata']['startSystemTime']
    print('start (UTC)', datetime.datetime.utcfromtimestamp(st / 1000).isoformat())
    rec = np.dtype([('i', '<f4'), ('b', '<u2')]); f = z.open('session.raw'); a = Acc(); n = 0; buf = b''
    while True:
        blk = f.read(60_000_000)
        if not blk: break
        buf += blk; k = len(buf) // 6
        r = np.frombuffer(buf[:k * 6], dtype=rec); buf = buf[k * 6:]
        a.add(np.arange(n, n + k) // SPS, r['i'].astype(np.float64)); n += k
    a.write(out)

def csv(src, out):
    import pandas as pd
    a = Acc()
    for ch in pd.read_csv(src, usecols=[0, 1], chunksize=5_000_000):
        t = ch.iloc[:, 0].to_numpy(); i = ch.iloc[:, 1].to_numpy()
        a.add(np.floor(t / 1000.0).astype(np.int64), i)
    a.write(out)

def events(src, low=1300.0, high=2000.0):
    import pandas as pd
    for ch in pd.read_csv(src, usecols=[0, 1], chunksize=5_000_000):
        t = ch.iloc[:, 0].to_numpy(); i = ch.iloc[:, 1].to_numpy()
        for name, sel in (('low', i < low), ('high', i > high)):
            idx = np.where(sel)[0]
            if not len(idx): continue
            for g in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
                print(f'{name}: t={t[g[0]]:.2f}..{t[g[-1]]:.2f} ms  n={len(g)}  min={i[g].min():.1f}  max={i[g].max():.1f} uA')

def stats(summary, ranges):
    d = np.loadtxt(summary, delimiter=',', skiprows=1)
    for r in ranges:
        a, b = (int(x) for x in r.split(':'))
        seg = d[a:b]; w = seg[:, -1]; print(f'{a}..{b} s: mean {(seg[:,1]*w).sum()/w.sum():.3f} uA')

if __name__ == '__main__':
    cmd, *args = sys.argv[1:]
    if cmd == 'ppk2': ppk2(*args)
    elif cmd == 'csv': csv(*args)
    elif cmd == 'events': events(args[0], *(float(x) for x in args[1:]))
    elif cmd == 'stats': stats(args[0], args[1:])
    else: sys.exit(__doc__)
