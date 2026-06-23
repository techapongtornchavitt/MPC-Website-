/* ================================================================
   interactions.js — Motion Plus Corporation
   Scroll progress bar + page transitions + cursor glow
   No dependencies. Safe to defer.
================================================================ */
(function () {
  'use strict';

  /* ──────────────────────────────────────────────────────────────
     1. SCROLL PROGRESS BAR
  ────────────────────────────────────────────────────────────── */
  var bar = document.createElement('div');
  bar.id = 'mpc-scroll-bar';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  window.addEventListener('scroll', function () {
    var scrolled = window.scrollY;
    var total    = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (total > 0 ? (scrolled / total) * 100 : 0) + '%';
  }, { passive: true });

  /* ──────────────────────────────────────────────────────────────
     2. CURSOR GLOW  (desktop / fine-pointer devices only)
  ────────────────────────────────────────────────────────────── */
  if (window.matchMedia('(pointer: fine) and (hover: hover)').matches) {
    var glow = document.createElement('div');
    glow.className = 'mpc-cursor-glow';
    glow.setAttribute('aria-hidden', 'true');
    document.body.appendChild(glow);

    document.addEventListener('mousemove', function (e) {
      glow.style.transform =
        'translate(' + (e.clientX - 260) + 'px,' + (e.clientY - 260) + 'px)';
    }, { passive: true });
  }

  /* ──────────────────────────────────────────────────────────────
     2. PAGE TRANSITIONS  — fade-out before navigation
  ────────────────────────────────────────────────────────────── */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a) return;

    var href = a.getAttribute('href');

    /* Skip: new tab, download, empty, anchor-only, mailto, tel, external */
    if (
      !href ||
      a.target === '_blank' ||
      a.hasAttribute('download') ||
      href.charAt(0) === '#' ||
      href.startsWith('mailto:') ||
      href.startsWith('tel:') ||
      href.startsWith('javascript:') ||
      (href.indexOf('://') !== -1 && href.indexOf('motionpluscorp.com') === -1)
    ) return;

    e.preventDefault();
    document.body.classList.add('mpc-fading');

    var dest = href;
    setTimeout(function () {
      window.location.href = dest;
    }, 230);
  });

})();

/* ================================================================
   GDPR Cookie Consent Banner
   Shows once, stores preference in localStorage.
================================================================ */
(function () {
  if (localStorage.getItem('mpc-cookie-consent')) return;

  var css = document.createElement('style');
  css.textContent =
    '.mpc-cookie{position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#0b1a2e;border-top:1px solid rgba(255,255,255,.1);padding:1rem 1.5rem;display:flex;align-items:center;justify-content:center;gap:1.2rem;flex-wrap:wrap;font-family:Nunito,Calibri,Arial,sans-serif;font-size:.85rem;color:rgba(255,255,255,.75);animation:mpcCkSlide .4s ease}' +
    '.mpc-cookie p{margin:0;max-width:600px;line-height:1.5}' +
    '.mpc-cookie a{color:#7ec8e3;text-decoration:underline}' +
    '.mpc-ck-btns{display:flex;gap:.5rem;flex-shrink:0}' +
    '.mpc-ck-btn{border:none;border-radius:100px;padding:.55rem 1.3rem;font-size:.82rem;font-weight:700;cursor:pointer;transition:all .2s;font-family:inherit}' +
    '.mpc-ck-accept{background:#0056a4;color:#fff}' +
    '.mpc-ck-accept:hover{background:#003d7a}' +
    '.mpc-ck-decline{background:transparent;color:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.2)}' +
    '.mpc-ck-decline:hover{border-color:rgba(255,255,255,.4);color:#fff}' +
    '@keyframes mpcCkSlide{from{transform:translateY(100%)}to{transform:translateY(0)}}' +
    '@media(max-width:600px){.mpc-cookie{flex-direction:column;text-align:center;padding:1rem}.mpc-ck-btns{width:100%;justify-content:center}}';
  document.head.appendChild(css);

  var bar = document.createElement('div');
  bar.className = 'mpc-cookie';
  bar.setAttribute('role', 'dialog');
  bar.setAttribute('aria-label', 'Cookie consent');
  bar.innerHTML =
    '<p>We use cookies to improve your experience and analyse site traffic. By clicking "Accept", you consent to our use of cookies.</p>' +
    '<div class="mpc-ck-btns">' +
    '<button class="mpc-ck-btn mpc-ck-accept">Accept</button>' +
    '<button class="mpc-ck-btn mpc-ck-decline">Decline</button>' +
    '</div>';
  document.body.appendChild(bar);

  bar.querySelector('.mpc-ck-accept').addEventListener('click', function () {
    localStorage.setItem('mpc-cookie-consent', 'accepted');
    bar.remove();
  });
  bar.querySelector('.mpc-ck-decline').addEventListener('click', function () {
    localStorage.setItem('mpc-cookie-consent', 'declined');
    bar.remove();
  });
})();
