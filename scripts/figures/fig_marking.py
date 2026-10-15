"""Figure 6: Quectel BG95-M3 module on the DIP40CORE-A breakout, from photograph A1_1_BG95_marking.jpg (14 October 2026).
Usage: python3 fig_marking.py A1_1_BG95_marking.jpg out.jpg
  (a) board context: crop of the photograph at original scale
  (b) package marking: crop of the module area, enlarged x3 with Lanczos resampling
Crops, a uniform enlargement, and opaque redaction of the serial-number value, IMEI value and QR code; no other change to the image. Labels are drawn outside the images."""
import sys
from PIL import Image, ImageDraw, ImageFont
SRC, OUT = sys.argv[1:3]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
NAVY = (18, 38, 58); MUTED = (94, 107, 119); COPPER = (181, 106, 45)
im = Image.open(SRC).convert('RGB')
# Opaque redaction of unit identifiers (source-photo pixels): serial-number value, IMEI value, QR code.
# Model, Q1 code, LA variant, SKU and regulatory markings are left as photographed.
REDACT = [(542, 596, 700, 612), (552, 613, 706, 629), (647, 686, 726, 758)]
_d = ImageDraw.Draw(im)
for b in REDACT: _d.rectangle(b, fill=(58, 62, 66))
CTX = (405, 365, 800, 1095)          # whole breakout board
MARK = (488, 492, 748, 768)          # module package with its marking
ctx = im.crop(CTX)
mark = im.crop(MARK); mark = mark.resize((mark.width * 3, mark.height * 3), Image.LANCZOS)
# scale context panel to the close-up's height
H = mark.height
ctx = ctx.resize((int(ctx.width * H / ctx.height), H), Image.LANCZOS)
# outline of the close-up area on the context panel
sx = ctx.width / (CTX[2] - CTX[0]); sy = H / (CTX[3] - CTX[1])
d = ImageDraw.Draw(ctx)
d.rectangle(((MARK[0] - CTX[0]) * sx, (MARK[1] - CTX[1]) * sy, (MARK[2] - CTX[0]) * sx, (MARK[3] - CTX[1]) * sy), outline=COPPER, width=4)
head = 96; gap = 40
out = Image.new('RGB', (ctx.width + gap + mark.width, H + head), 'white')
dd = ImageDraw.Draw(out)
dd.text((0, 4), '(a) Board context', font=FB, fill=NAVY)
dd.text((0, 48), 'Outline: area in (b)', font=F, fill=MUTED)
dd.text((ctx.width + gap, 4), '(b) Package marking', font=FB, fill=NAVY)
dd.text((ctx.width + gap, 48), 'Enlarged three times', font=F, fill=MUTED)
out.paste(ctx, (0, head)); out.paste(mark, (ctx.width + gap, head))
out.save(OUT, quality=92)
print(out.size)
