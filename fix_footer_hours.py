import os, glob

folder = r"C:\Users\Chavit\Downloads\brand guidlines mpc"

# The hours block to insert (after the email contact-item closing div)
HOURS_BLOCK = """          <div class="footer-contact-item">
            <span class="footer-contact-label" data-i18n="footer-hours-lbl">Business Hours</span>
            <div class="footer-hours-grid">
              <span data-i18n="footer-mon-fri">Mon — Fri</span><span data-i18n="footer-hours-wkday">8:30 AM — 5:00 PM</span>
              <span data-i18n="footer-sat">Saturday</span><span data-i18n="footer-hours-sat">9:00 AM — 3:00 PM</span>
            </div>
          </div>"""

# The anchor: end of the email contact-item block
# Pattern that exists in all product pages (email line + two closing divs)
EMAIL_ANCHOR = '            <span class="footer-contact-value"><a href="mailto:contact@motionpluscorp.com">contact@motionpluscorp.com</a></span>\n          </div>\n        </div>'

# What to replace it with (same anchor + hours block before closing </div>)
EMAIL_WITH_HOURS = ('            <span class="footer-contact-value"><a href="mailto:contact@motionpluscorp.com">contact@motionpluscorp.com</a></span>\n'
                    '          </div>\n'
                    + HOURS_BLOCK + '\n'
                    '        </div>')

pages = [
    "bearing.html","belt.html","coupling.html","hs-conveyor-chains.html",
    "iwis-chains.html","iwis-conveyor-chains.html","dongbo-chains.html",
    "uno-chains.html","sprockets-pulley.html","forged-chains.html",
    "cement-chains.html","palm-oil-chains.html","sugar-mill-chains.html",
    "kmh-conveyor-pipe.html","oil-seal.html","pe-1000.html",
    "trio-forged-chain.html","uno-forged-chain.html",
]

for page in pages:
    path = os.path.join(folder, page)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if hours already present
    if "footer-hours-lbl" in content:
        print("SKIP (already has hours): %s" % page)
        continue

    if EMAIL_ANCHOR not in content:
        print("WARN (anchor not found): %s" % page)
        continue

    new_content = content.replace(EMAIL_ANCHOR, EMAIL_WITH_HOURS, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("OK: %s" % page)
