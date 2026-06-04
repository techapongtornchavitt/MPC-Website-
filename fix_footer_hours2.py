import os

folder = r"C:\Users\Chavit\Downloads\brand guidlines mpc"

HOURS_ITEM = '\n          <div class="footer-contact-item"><span class="footer-contact-label" data-i18n="footer-hours-lbl">Business Hours</span><div class="footer-hours-grid"><span data-i18n="footer-mon-fri">Mon — Fri</span><span data-i18n="footer-hours-wkday">8:30 AM — 5:00 PM</span><span data-i18n="footer-sat">Saturday</span><span data-i18n="footer-hours-sat">9:00 AM — 3:00 PM</span></div></div>'

# Single-line format pages
ANCHOR_SINGLE = '<div class="footer-contact-item"><span class="footer-contact-label" data-i18n="footer-email-lbl">Email</span><span class="footer-contact-value"><a href="mailto:contact@motionpluscorp.com">contact@motionpluscorp.com</a></span></div>'

pages = ["belt.html", "coupling.html", "oil-seal.html", "pe-1000.html", "kmh-conveyor-pipe.html"]

for page in pages:
    path = os.path.join(folder, page)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "footer-hours-lbl" in content:
        print("SKIP (already has hours): %s" % page)
        continue
    if ANCHOR_SINGLE not in content:
        print("WARN anchor not found: %s" % page)
        continue
    new_content = content.replace(ANCHOR_SINGLE, ANCHOR_SINGLE + HOURS_ITEM, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("OK: %s" % page)
