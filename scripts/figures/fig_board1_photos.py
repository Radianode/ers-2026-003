"""Figure 4: Waveshare HAT measurement configuration (crops, labelled outside the images; IMEI value and QR code redacted, otherwise unaltered).
Usage: python3 fig_board1_photos.py ATTACH_20260826.jpg HAT_20261015_STA_OFF.png HAT_20261015_STA_ON.jpg out.jpg
Inputs: the ERS-2026-002 attachment photograph (26 Aug 2026) and two photographs of the 15 Oct 2026 re-measurement
(module off, STA LED dark; module on, STA LED lit).
"""
import sys
from PIL import Image, ImageDraw, ImageFont
A, D, L, OUT = sys.argv[1:5]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
NAVY = (18, 38, 58); MUTED = (94, 107, 119)
att = Image.open(A).convert('RGB'); dk = Image.open(D).convert('RGB'); lt = Image.open(L).convert('RGB')
# Opaque redaction of SIM7080G unit identifiers (IMEI value, QR code), in source-photo pixels.
# In the 26 August photograph the module is rotated about 45 degrees, so polygons are used.
GREY = (58, 62, 66)
_a = ImageDraw.Draw(att)
_a.polygon([(502.0, 955.0), (507.5, 963.5), (557.0, 920.0), (550.0, 910.0)], fill=GREY)   # IMEI value
_a.polygon([(547.5, 936.5), (572.5, 907.0), (605.5, 932.5), (577.5, 964.5)], fill=GREY)   # QR code
_d = ImageDraw.Draw(dk)
_d.rectangle((398, 1066, 476, 1084), fill=GREY)   # IMEI value
_d.rectangle((442, 1095, 501, 1158), fill=GREY)   # QR code
_l = ImageDraw.Draw(lt)
_l.rectangle((398, 1060, 470, 1076), fill=GREY)   # IMEI value
_l.rectangle((439, 1083, 496, 1142), fill=GREY)   # QR code
pa = att
pb = att.crop((296, 776, 728, 1200)).resize((864, 848))
pc = dk.crop((60, 940, 680, 1265))
pd = lt.crop((90, 935, 710, 1260))
def panel(img, w, title, note):
    img = img.resize((w, int(img.height * w / img.width)))
    head = 92; p = Image.new('RGB', (w, img.height + head), 'white'); dd = ImageDraw.Draw(p)
    dd.text((0, 4), title, font=FB, fill=NAVY); dd.text((0, 46), note, font=F, fill=MUTED)
    p.paste(img, (0, head)); return p
Lp = panel(pa, 900, '(a) Attachment, 26 August 2026', 'PPK2 output connected to the HAT supply header')
Rp = panel(pb, 900, '(b) Detail of (a)', 'USB connector empty; P2 jumper 5V–VCC; PWR LED lit')
Cp = panel(pc, 900, '(c) 15 October 2026, module off', 'PWR LED lit; STA LED dark; PWR–P7 open')
Dp = panel(pd, 900, '(d) 15 October 2026, module on', 'PWR LED and STA LED lit')
top = max(Lp.height, Rp.height)
out = Image.new('RGB', (900 + 40 + 900, top + 40 + max(Cp.height, Dp.height)), 'white')
out.paste(Lp, (0, 0)); out.paste(Rp, (940, 0)); out.paste(Cp, (0, top + 40)); out.paste(Dp, (940, top + 40))
out.save(OUT, quality=85)
print(out.size)
