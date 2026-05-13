/* =========================================================
   animations.js  —  Motion Plus Corporation
   Scroll-reveal · Stat counters · Eyebrow line reveals
   ---------------------------------------------------------
   Design philosophy (Emil Kowalski):
     • Only transform & opacity — both GPU composited
     • Custom easing via CSS variables
     • Stagger 70 ms between grid siblings
     • Respects prefers-reduced-motion
     • Every animation triggers once, never re-hides
   ========================================================= */

(function () {
  'use strict';

  var prefersReduced =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ──────────────────────────────────────────────────────
     HELPERS
  ────────────────────────────────────────────────────── */

  /* Elements inside these containers are excluded from reveal logic
     because they have their own entrance animations already */
  var EXCLUDED_PARENTS = ['.hero', '.inner-hero'];

  function isExcluded(el) {
    return EXCLUDED_PARENTS.some(function (sel) {
      return !!el.closest(sel);
    });
  }

  function tagReveal(el, delay) {
    if (isExcluded(el)) return;
    if (el.hasAttribute('data-reveal')) return;
    el.setAttribute('data-reveal', '');
    if (delay && delay > 0) el.setAttribute('data-delay', String(delay));
  }

  /* ──────────────────────────────────────────────────────
     1. SCROLL-REVEAL
     IntersectionObserver watches [data-reveal] elements.
     When they enter the viewport, .is-visible is added and
     the CSS transition (opacity + translateY → 0) fires.
  ────────────────────────────────────────────────────── */

  /* Reveal as single block */
  var SINGLE_SELECTORS = [
    '.section-header',
    '.since2004-inner',
    '.expertise-split',
    '.line-qr-block',
    '.cta-block',
  ].join(', ');

  /* Grid/flex parents — immediate children get staggered */
  var STAGGER_CONTAINERS = [
    '.brands-grid',
    '.solution-cards',
    '.grid-3',
    '.grid-4',
    '.partners-grid',
    '.gallery-grid',
    '.value-cards',
    '.stats-bar-grid',
    '.since2004-stats',
    '.cta-btns',
  ];

  /* Lists — <li> children get staggered */
  var LIST_SELECTORS = ['.feature-list'];

  function initReveal() {
    /* ── Single-block reveals ── */
    document.querySelectorAll(SINGLE_SELECTORS).forEach(function (el) {
      tagReveal(el, 0);
    });

    /* ── Two-col sections (not already inside a [data-reveal]) ── */
    document.querySelectorAll('.two-col').forEach(function (el) {
      if (!isExcluded(el) && !el.closest('[data-reveal]')) {
        tagReveal(el, 0);
      }
    });

    /* ── Staggered grid children ── */
    STAGGER_CONTAINERS.forEach(function (containerSel) {
      document.querySelectorAll(containerSel).forEach(function (parent) {
        if (isExcluded(parent)) return;
        var children = Array.from(parent.children).filter(function (c) {
          return !c.classList.contains('stat-item-divider') &&
                 getComputedStyle(c).display !== 'none';
        });
        children.forEach(function (child, idx) {
          tagReveal(child, Math.min(idx, 6));
        });
      });
    });

    /* ── Staggered list items ── */
    LIST_SELECTORS.forEach(function (listSel) {
      document.querySelectorAll(listSel).forEach(function (list) {
        if (isExcluded(list)) return;
        Array.from(list.children).forEach(function (li, idx) {
          tagReveal(li, Math.min(idx, 5));
        });
      });
    });

    /* ── Create observer ── */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -48px 0px',
    });

    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      io.observe(el);
    });
  }

  /* ──────────────────────────────────────────────────────
     2. STAT COUNTER ANIMATION
     When a number enters the viewport it counts up from 0
     to its target value using ease-out cubic timing.
     A subtle pop keyframe fires when it reaches the final
     value so the number feels like it "lands".
  ────────────────────────────────────────────────────── */

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function parseStat(text) {
    /* Match: "500+" → { num: 500, suffix: "+" }
              "20"   → { num: 20,  suffix: ""  }
              "SEA"  → null (skip non-numeric)  */
    var m = text.trim().match(/^(\d+(?:\.\d+)?)(.*)/);
    return m ? { num: parseFloat(m[1]), suffix: m[2] } : null;
  }

  function runCounter(el) {
    var parsed = parseStat(el.textContent);
    if (!parsed || parsed.num === 0) return;

    var target   = parsed.num;
    var suffix   = parsed.suffix;
    var duration = 1000;    /* ms — fast enough to feel snappy */
    var startTs  = null;

    /* Keep the static value accessible to screen readers */
    el.setAttribute('aria-label', target + suffix);

    function tick(ts) {
      if (!startTs) startTs = ts;
      var progress = Math.min((ts - startTs) / duration, 1);
      var current  = Math.round(easeOutCubic(progress) * target);
      el.textContent = current + suffix;
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = target + suffix;   /* ensure exact final value */
        el.classList.add('stat-popped');    /* CSS pop keyframe */
      }
    }
    requestAnimationFrame(tick);
  }

  function initCounters() {
    var els = document.querySelectorAll([
      '.stat-item-num',
      '.since2004-stat-num',
      '.since2004-num',
    ].join(', '));

    if (!els.length) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          runCounter(entry.target);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.55 });

    els.forEach(function (el) { io.observe(el); });
  }

  /* ──────────────────────────────────────────────────────
     3. SECTION EYEBROW LINE REVEAL
     Each .section-eyebrow (outside hero areas) gets:
       .eyebrow-anim   → added immediately (enables CSS clip-path start state)
       .eyebrow-visible → added on viewport enter (fires the CSS transition)

     The ::before and ::after decorative lines grow from
     clip-path: inset(0 100% 0 0) to inset(0 0 0 0).
     clip-path is GPU composited — no paint, no layout.
  ────────────────────────────────────────────────────── */

  function initEyebrows() {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('eyebrow-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    document.querySelectorAll('.section-eyebrow').forEach(function (el) {
      if (isExcluded(el)) return;
      el.classList.add('eyebrow-anim');
      io.observe(el);
    });
  }

  /* ──────────────────────────────────────────────────────
     4. INIT
     Counters run regardless of prefers-reduced-motion
     (number changes are not vestibular/motion-sickness
     triggers — only spatial animations are).
     Everything else is gated behind the preference.
  ────────────────────────────────────────────────────── */

  /* ── Header scroll state — applies .scrolled to .site-header on all pages ── */
  function initHeaderScroll() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    function updateHeader() {
      header.classList.toggle('scrolled', window.pageYOffset > 40);
    }
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
  }

  function init() {
    if (!prefersReduced) {
      initReveal();
      initEyebrows();
    }
    initCounters(); /* numbers count up even in reduced-motion mode */
    initHeaderScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
