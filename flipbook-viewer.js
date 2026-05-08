/* =========================================================
   flipbook-viewer.js  —  Motion Plus Corporation
   Premium PDF viewer with real page-flip animation
   ---------------------------------------------------------
   Works on: local file:// · http:// · https://
   No CDN. No CORS issues. Zero setup.

   Features:
   ✓ Animated page-flip when navigating (prev / next)
   ✓ Keyboard arrows: ← → | PageUp PageDown | F = fullscreen
   ✓ Touch / swipe support on mobile
   ✓ Download button
   ✓ Error fallback → open in new tab
   ✓ Auto-wires any element with  data-pdf="file.pdf"
       and optional  data-pdf-title="Title"

   Public API:
     FlipbookViewer.open(pdfUrl, title)
     FlipbookViewer.close()
   ========================================================= */

(function () {
  'use strict';

  /* ── State ───────────────────────────────────────────── */
  var curPdfUrl = '';
  var curTitle  = '';
  var curPage   = 1;
  var domBuilt  = false;
  var flipping  = false;
  var touchX0   = 0;
  var touchY0   = 0;

  /* ── DOM refs ────────────────────────────────────────── */
  var elOverlay, elTitle, elIframe, elLoader, elFullBtn;
  var elIframeWrap, elPageInd, elPrevBtn, elNextBtn;

  /* ── Inline SVG icons ────────────────────────────────── */
  var SVG = {
    expand:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>' +
      '<line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>',
    compress:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/>' +
      '<line x1="10" y1="14" x2="3" y2="21"/><line x1="21" y1="3" x2="14" y2="10"/></svg>',
    download:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>' +
      '<polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    newtab:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>' +
      '<polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
    close:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    doc:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>' +
      '<polyline points="14 2 14 8 20 8"/></svg>',
    prev:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<polyline points="15 18 9 12 15 6"/></svg>',
    next:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"' +
      ' stroke-linecap="round" stroke-linejoin="round">' +
      '<polyline points="9 18 15 12 9 6"/></svg>'
  };

  /* ═══════════════════════════════════════════════════════
     Build modal DOM (runs once)
  ═══════════════════════════════════════════════════════ */
  function buildDom() {
    if (domBuilt) return;
    domBuilt = true;

    elOverlay = document.createElement('div');
    elOverlay.className = 'fbv-overlay';
    elOverlay.setAttribute('role', 'dialog');
    elOverlay.setAttribute('aria-modal', 'true');
    elOverlay.setAttribute('aria-label', 'Document viewer');

    elOverlay.innerHTML =
      '<div class="fbv-viewer" id="fbv-viewer">' +

        /* ── Top toolbar ── */
        '<div class="fbv-toolbar">' +
          '<div class="fbv-toolbar-left">' +
            '<div class="fbv-doc-icon">' + SVG.doc + '</div>' +
            '<span class="fbv-title" id="fbv-title"></span>' +
          '</div>' +
          '<div class="fbv-toolbar-actions">' +
            '<button class="fbv-icon-btn" id="fbv-fullscreen"' +
              ' title="Fullscreen (F)" aria-label="Toggle fullscreen">' + SVG.expand + '</button>' +
            '<span class="fbv-sep"></span>' +
            '<button class="fbv-icon-btn" id="fbv-newtab"' +
              ' title="Open in new tab" aria-label="Open in new tab">' + SVG.newtab + '</button>' +
            '<button class="fbv-download-btn" id="fbv-download"' +
              ' title="Download PDF" aria-label="Download PDF">' +
              SVG.download + '<span>Download</span>' +
            '</button>' +
            '<span class="fbv-sep"></span>' +
            '<button class="fbv-icon-btn" id="fbv-close"' +
              ' title="Close (Esc)" aria-label="Close viewer">' + SVG.close + '</button>' +
          '</div>' +
        '</div>' +

        /* ── PDF iframe ── */
        '<div class="fbv-iframe-wrap" id="fbv-iframe-wrap">' +
          '<div class="fbv-loader" id="fbv-loader">' +
            '<div class="fbv-spinner"></div>' +
            '<span class="fbv-loader-label">Loading document…</span>' +
          '</div>' +
          '<div class="fbv-error-panel" id="fbv-error-panel">' +
            '<svg class="fbv-error-icon" width="38" height="38" viewBox="0 0 24 24"' +
              ' fill="none" stroke="currentColor" stroke-width="2"' +
              ' stroke-linecap="round" stroke-linejoin="round">' +
              '<circle cx="12" cy="12" r="10"/>' +
              '<line x1="12" y1="8" x2="12" y2="12"/>' +
              '<line x1="12" y1="16" x2="12.01" y2="16"/>' +
            '</svg>' +
            '<p class="fbv-error-msg">Could not display this document in the browser.</p>' +
            '<button class="fbv-error-link" id="fbv-fallback-btn">Open PDF in new tab →</button>' +
          '</div>' +
          '<iframe class="fbv-iframe" id="fbv-iframe" title="PDF Viewer"' +
            ' allowfullscreen="true" webkitallowfullscreen="true"></iframe>' +
        '</div>' +

        /* ── Bottom navigation bar ── */
        '<div class="fbv-nav-bar">' +
          '<button class="fbv-nav-btn" id="fbv-prev" aria-label="Previous page">' +
            SVG.prev + '<span>Previous</span>' +
          '</button>' +
          '<span class="fbv-page-indicator" id="fbv-page-ind">Page <strong>1</strong></span>' +
          '<span class="fbv-nav-hint">← → arrow keys · swipe</span>' +
          '<button class="fbv-nav-btn" id="fbv-next" aria-label="Next page">' +
            '<span>Next</span>' + SVG.next +
          '</button>' +
        '</div>' +

      '</div>'; /* /fbv-viewer */

    document.body.appendChild(elOverlay);

    /* ── Cache element refs ── */
    elTitle      = document.getElementById('fbv-title');
    elIframe     = document.getElementById('fbv-iframe');
    elLoader     = document.getElementById('fbv-loader');
    elFullBtn    = document.getElementById('fbv-fullscreen');
    elIframeWrap = document.getElementById('fbv-iframe-wrap');
    elPageInd    = document.getElementById('fbv-page-ind');
    elPrevBtn    = document.getElementById('fbv-prev');
    elNextBtn    = document.getElementById('fbv-next');

    /* ── Event listeners ── */

    /* Close */
    document.getElementById('fbv-close').addEventListener('click', closeViewer);
    elOverlay.addEventListener('click', function (e) {
      if (e.target === elOverlay) closeViewer();
    });

    /* Download — strips hash before downloading */
    document.getElementById('fbv-download').addEventListener('click', function () {
      var a = document.createElement('a');
      a.href     = baseUrl();
      a.download = curTitle || 'document.pdf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });

    /* Open in new tab */
    document.getElementById('fbv-newtab').addEventListener('click', function () {
      window.open(baseUrl(), '_blank', 'noopener,noreferrer');
    });

    /* Error fallback */
    document.getElementById('fbv-fallback-btn').addEventListener('click', function () {
      window.open(baseUrl(), '_blank', 'noopener,noreferrer');
    });

    /* Fullscreen toggle */
    elFullBtn.addEventListener('click', toggleFullscreen);
    document.addEventListener('fullscreenchange',       syncFullscreenIcon);
    document.addEventListener('webkitfullscreenchange', syncFullscreenIcon);

    /* Page flip buttons */
    elPrevBtn.addEventListener('click', function () { flipPage(-1); });
    elNextBtn.addEventListener('click', function () { flipPage(1);  });

    /* Keyboard navigation */
    document.addEventListener('keydown', function (e) {
      if (!elOverlay.classList.contains('fbv-open')) return;
      switch (e.key) {
        case 'Escape':    closeViewer();      return;
        case 'f': case 'F': toggleFullscreen(); return;
        case 'ArrowRight': case 'PageDown':
          e.preventDefault(); flipPage(1);  break;
        case 'ArrowLeft': case 'PageUp':
          e.preventDefault(); flipPage(-1); break;
      }
    });

    /* Touch / swipe */
    elIframeWrap.addEventListener('touchstart', function (e) {
      touchX0 = e.touches[0].clientX;
      touchY0 = e.touches[0].clientY;
    }, { passive: true });

    elIframeWrap.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - touchX0;
      var dy = e.changedTouches[0].clientY - touchY0;
      /* Only register as a horizontal swipe */
      if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) {
        flipPage(dx < 0 ? 1 : -1);
      }
    }, { passive: true });

    /* Iframe load → hide spinner */
    elIframe.addEventListener('load', function () {
      setTimeout(function () {
        if (elLoader) elLoader.classList.add('fbv-hide');
      }, 320);
    });
  }

  /* ─── Helper: base URL without hash ─────────────────── */
  function baseUrl() {
    return curPdfUrl.split('#')[0];
  }

  /* ═══════════════════════════════════════════════════════
     Page-flip animation + navigation
  ═══════════════════════════════════════════════════════ */
  function flipPage(direction) {
    if (flipping) return;

    var newPage = curPage + direction;
    if (newPage < 1) {
      nudgeEdge('start');
      return;
    }

    flipping = true;

    /* ── Build the paper overlay ── */
    var flipperEl           = document.createElement('div');
    var flipperPage         = document.createElement('div');
    flipperEl.className     = 'fbv-flipper fbv-flipper--' + (direction > 0 ? 'fwd' : 'back');
    flipperPage.className   = 'fbv-flipper-page';
    flipperEl.appendChild(flipperPage);
    elIframeWrap.appendChild(flipperEl);

    /* ── At animation midpoint, change the actual page ── */
    setTimeout(function () {
      curPage = newPage;
      setIframePage(curPage);
      renderPageIndicator();
    }, 210);

    /* ── After animation completes, clean up ── */
    setTimeout(function () {
      if (flipperEl.parentNode) {
        flipperEl.parentNode.removeChild(flipperEl);
      }
      flipping = false;
    }, 480);
  }

  /* Brief horizontal nudge when already at first page */
  function nudgeEdge(side) {
    var viewer = document.getElementById('fbv-viewer');
    if (!viewer) return;
    viewer.style.transition = 'transform 0.08s ease-out';
    viewer.style.transform  = 'translateX(' + (side === 'start' ? '8px' : '-8px') + ')';
    setTimeout(function () {
      viewer.style.transform = 'translateX(0)';
      setTimeout(function () {
        viewer.style.transition = '';
      }, 130);
    }, 80);
  }

  /* Update iframe src with  #page=N  fragment */
  function setIframePage(page) {
    elIframe.src = baseUrl() + '#page=' + page;
  }

  /* Update the page-N indicator and prev button state */
  function renderPageIndicator() {
    elPageInd.innerHTML = 'Page <strong>' + curPage + '</strong>';
    elPrevBtn.disabled  = (curPage <= 1);
    elNextBtn.disabled  = false; /* Can't know total without PDF.js; let viewer handle it */
  }

  /* ═══════════════════════════════════════════════════════
     Open viewer
  ═══════════════════════════════════════════════════════ */
  function openViewer(pdfUrl, title) {
    buildDom();

    /* Strip any pre-existing hash from the stored URL */
    curPdfUrl = pdfUrl.split('#')[0];
    curTitle  = title || decodeURIComponent(
      pdfUrl.split('/').pop().replace(/[?#].*/, '')
    );
    curPage  = 1;
    flipping = false;

    /* Update title bar */
    elTitle.textContent = curTitle;

    /* Reset panels */
    elLoader.classList.remove('fbv-hide');
    document.getElementById('fbv-error-panel').classList.remove('fbv-show');
    elIframe.style.display = 'block';
    renderPageIndicator();

    /* Load the PDF */
    elIframe.src = '';
    setTimeout(function () {
      elIframe.src = curPdfUrl + '#page=1';

      /* 8-second fallback: show error if iframe never fires "load" */
      var timer = setTimeout(function () {
        if (elLoader && !elLoader.classList.contains('fbv-hide')) {
          elLoader.classList.add('fbv-hide');
          document.getElementById('fbv-error-panel').classList.add('fbv-show');
          elIframe.style.display = 'none';
        }
      }, 8000);

      elIframe.addEventListener('load', function () {
        clearTimeout(timer);
      }, { once: true });
    }, 55);

    /* Show the overlay */
    elOverlay.classList.add('fbv-open');
    document.body.style.overflow = 'hidden';
  }

  /* ═══════════════════════════════════════════════════════
     Close viewer
  ═══════════════════════════════════════════════════════ */
  function closeViewer() {
    elOverlay.classList.remove('fbv-open');
    document.body.style.overflow = '';

    /* Exit fullscreen if active */
    if (document.fullscreenElement || document.webkitFullscreenElement) {
      var exitFs = document.exitFullscreen || document.webkitExitFullscreen;
      if (exitFs) exitFs.call(document);
    }

    /* Clear iframe after close animation to stop PDF rendering */
    setTimeout(function () {
      if (elIframe) elIframe.src = '';
    }, 320);
  }

  /* ═══════════════════════════════════════════════════════
     Fullscreen
  ═══════════════════════════════════════════════════════ */
  function toggleFullscreen() {
    if (document.fullscreenElement || document.webkitFullscreenElement) {
      var exitFs = document.exitFullscreen || document.webkitExitFullscreen;
      if (exitFs) exitFs.call(document);
    } else {
      var req = elOverlay.requestFullscreen || elOverlay.webkitRequestFullscreen;
      if (req) req.call(elOverlay);
    }
  }

  function syncFullscreenIcon() {
    if (!elFullBtn) return;
    var isFs = !!(document.fullscreenElement || document.webkitFullscreenElement);
    elFullBtn.innerHTML = isFs ? SVG.compress : SVG.expand;
  }

  /* ═══════════════════════════════════════════════════════
     Auto-wire all  [data-pdf]  elements on the page
  ═══════════════════════════════════════════════════════ */
  function wireElements() {
    var els = document.querySelectorAll('[data-pdf]');
    for (var i = 0; i < els.length; i++) {
      (function (el) {
        el.addEventListener('click', function (e) {
          e.preventDefault();
          openViewer(
            el.getAttribute('data-pdf'),
            el.getAttribute('data-pdf-title') || ''
          );
        });
      })(els[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireElements);
  } else {
    wireElements();
  }

  /* ── Public API ── */
  window.FlipbookViewer = { open: openViewer, close: closeViewer };

})();
