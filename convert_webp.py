import os, glob, sys
from PIL import Image

folder = r"C:\Users\Chavit\Downloads\brand guidlines mpc"
pngs = glob.glob(os.path.join(folder, "*.png"))

SKIP = {
    "favicon-16.png","favicon-16x16.png","favicon-32.png","favicon-32x32.png",
    "favicon-48x48.png","favicon-64.png","favicon-192.png","favicon-512.png",
    "apple-touch-icon.png","brand-logo-iwis.png","line-qr-salesco-motion.png",
    "dongbo-authorized-brand.png","dongbo-authorized-brand-2.png",
    "hs-chain-authorized-brand-2.png","kmh-authorized-brand.png","kmh-authorized-brand-2.png",
}

results = []
total_before = 0
total_after = 0

for p in sorted(pngs):
    name = os.path.basename(p)
    if name in SKIP:
        results.append("SKIP  " + name)
        continue
    size_before = os.path.getsize(p)
    out = p.replace(".png", ".webp")
    try:
        img = Image.open(p).convert("RGBA")
        img.save(out, "webp", quality=82, method=6)
        size_after = os.path.getsize(out)
        saving = (1 - size_after/size_before)*100
        total_before += size_before
        total_after += size_after
        results.append("OK    %5dKB -> %5dKB  (%2.0f%% saved)  %s" % (
            size_before//1024, size_after//1024, saving, name))
    except Exception as e:
        results.append("FAIL  %s: %s" % (name, e))

for r in results:
    print(r)

print("")
print("TOTAL before: %d KB" % (total_before//1024))
print("TOTAL after:  %d KB" % (total_after//1024))
print("TOTAL saved:  %d KB  (%.0f%%)" % ((total_before-total_after)//1024, (1-total_after/total_before)*100))
