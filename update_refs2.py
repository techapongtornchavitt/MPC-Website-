import os, glob

folder = r"C:\Users\Chavit\Downloads\brand guidlines mpc"

SKIP = {
    "favicon-16.png","favicon-16x16.png","favicon-32.png","favicon-32x32.png",
    "favicon-48x48.png","favicon-64.png","favicon-192.png","favicon-512.png",
    "apple-touch-icon.png","brand-logo-iwis.png","line-qr-salesco-motion.png",
    "dongbo-authorized-brand.png","dongbo-authorized-brand-2.png",
    "hs-chain-authorized-brand-2.png","kmh-authorized-brand.png","kmh-authorized-brand-2.png",
    "dongbo-chain-product.png",  # doesn't exist
}

# Build set of .webp files we actually created (by their original .png name)
webp_set = {os.path.basename(f).replace(".webp", ".png")
            for f in glob.glob(os.path.join(folder, "*.webp"))}

html_files = [f for f in glob.glob(os.path.join(folder, "*.html"))
              if "backup" not in f.lower()]

total = 0
for html_path in sorted(html_files):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Replace every .png occurrence that has a matching .webp
    # Work through all known webp-ified names
    for png_name in sorted(webp_set, key=len, reverse=True):  # longest first to avoid partial matches
        if png_name in SKIP:
            continue
        if png_name in content:
            content = content.replace(png_name, png_name.replace(".png", ".webp"))

    count = original.count(".png") - content.count(".png")
    if count > 0:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("%-45s  %d replacements" % (os.path.basename(html_path), count))
        total += count
    else:
        print("%-45s  (no changes)" % os.path.basename(html_path))

print("\nTotal additional replacements: %d" % total)
