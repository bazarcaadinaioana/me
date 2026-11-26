"""Crea un foglio di anteprima di pagine del PDF. Uso: python3 anteprima.py file.pdf out.png p1 p2 ..."""
import sys, subprocess, tempfile, glob, os
from PIL import Image
pdf, out, pages = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
d = tempfile.mkdtemp(); ims = []
for p in pages:
    subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "60", "-png", pdf, f"{d}/p{p:04d}"], check=True)
    ims.append(Image.open(sorted(glob.glob(f"{d}/p{p:04d}*.png"))[0]))
w, h = ims[0].size; cols = 4; rows = (len(ims) + 3) // 4
c = Image.new("RGB", (w * cols, h * rows), "white")
for i, im in enumerate(ims): c.paste(im, ((i % cols) * w, (i // cols) * h))
c.save(out); print(out)
