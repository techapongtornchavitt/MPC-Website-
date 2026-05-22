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
