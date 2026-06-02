import os, re, glob

folder = r"C:\Users\Chavit\Downloads\brand guidlines mpc"

# Only replace PNGs that have a corresponding .webp we just created
# Skip favicons, brand-logos, and other tiny icons we skipped converting
SKIP_NAMES = {
    "favicon-16.png","favicon-16x16.png","favicon-32.png","favicon-32x32.png",
    "favicon-48x48.png","favicon-64.png","favicon-192.png","favicon-512.png",
    "apple-touch-icon.png","brand-logo-iwis.png","line-qr-salesco-motion.png",
    "dongbo-authorized-brand.png","dongbo-authorized-brand-2.png",
    "hs-chain-authorized-brand-2.png","kmh-authorized-brand.png","kmh-authorized-brand-2.png",
}

# Build set of webp files we actually created
webp_files = {os.path.basename(f).replace(".webp",".png")
              for f in glob.glob(os.path.join(folder, "*.webp"))}

html_files = glob.glob(os.path.join(folder, "*.html"))
# Skip backup files
html_files = [f for f in html_files if "backup" not in f.lower()]

total_replacements = 0

for html_path in sorted(html_files):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    def replace_png(m):
        full = m.group(0)
        name = m.group(1)  # just the filename e.g. "bearing-product-1.png"
        if name in SKIP_NAMES:
            return full
        if name in webp_files:
            return full.replace(name, name.replace(".png", ".webp"))
        return full

    # Match any .png reference (in src=, url(, srcset=, etc.) — capture just the filename part
    content = re.sub(r'(?<=["\'/])([^"\'/ ]+\.png)', replace_png, content)

    count = original.count(".png") - content.count(".png")
    if count > 0:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("%-45s  %d replacements" % (os.path.basename(html_path), count))
        total_replacements += count
    else:
        print("%-45s  (no changes)" % os.path.basename(html_path))

print("")
print("Total .png -> .webp replacements: %d" % total_replacements)
