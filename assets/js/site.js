// Progressive enhancement only: the page is complete without this file.
(function () {
  var root = document.documentElement;

  // Theme: Light / Dark / Auto (follows the system)
  var seg = document.querySelector('.seg');
  var play8 = document.querySelector('.play8');
  function sync() {
    var cur = root.dataset.theme || 'auto';
    if (seg) seg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeSet === cur)); });
    if (play8) play8.setAttribute('aria-pressed', String(cur === '8bit'));
  }
  function setTheme(v) {
    if (v === 'auto') { delete root.dataset.theme; try { localStorage.removeItem('theme'); } catch (_) {} }
    else { root.dataset.theme = v; try { localStorage.setItem('theme', v); } catch (_) {} }
    sync();
    if (typeof images8 === 'function') images8();
  }
  if (seg) {
    seg.hidden = false;
    sync();
    seg.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return;
      setTheme(b.dataset.themeSet);
    });
  }

  // Easter egg: 8-bit mode, from its button or the Konami code.
  // Images are re-drawn at 96px wide in a four-tone palette; the originals come back on exit.
  var PAL = [[18, 13, 6], [107, 63, 18], [217, 149, 74], [255, 194, 102]];
  function pixelate(img) {
    if (img.dataset.src) return;
    var go = function () {
      try {
        var w = 96, h = Math.max(1, Math.round(w * img.naturalHeight / img.naturalWidth));
        var cv = document.createElement('canvas'); cv.width = w; cv.height = h;
        var cx = cv.getContext('2d'); cx.drawImage(img, 0, 0, w, h);
        var d = cx.getImageData(0, 0, w, h), px = d.data;
        for (var i = 0; i < px.length; i += 4) {
          var l = (0.299 * px[i] + 0.587 * px[i + 1] + 0.114 * px[i + 2]) / 256;
          var c = PAL[Math.min(3, Math.floor(l * 4))];
          px[i] = c[0]; px[i + 1] = c[1]; px[i + 2] = c[2];
        }
        cx.putImageData(d, 0, 0);
        img.dataset.src = img.currentSrc || img.src;
        img.src = cv.toDataURL();
      } catch (_) {}
    };
    img.loading = 'eager';
    if (img.complete && img.naturalWidth) go(); else img.addEventListener('load', go, { once: true });
  }
  function restore(img) { if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; } }
  function images8() {
    var on = root.dataset.theme === '8bit';
    document.querySelectorAll('main img').forEach(on ? pixelate : restore);
  }
  function blip() {
    try {
      var A = window.AudioContext || window.webkitAudioContext; if (!A) return;
      var ac = blip.ac || (blip.ac = new A()), o = ac.createOscillator(), g = ac.createGain(), t = ac.currentTime;
      o.type = 'square'; o.frequency.setValueAtTime(660, t); o.frequency.setValueAtTime(990, t + 0.07);
      g.gain.setValueAtTime(0.04, t); g.gain.setValueAtTime(0, t + 0.15);
      o.connect(g); g.connect(ac.destination); o.start(t); o.stop(t + 0.16);
    } catch (_) {}
  }
  function toggle8() {
    var on = root.dataset.theme !== '8bit';
    setTheme(on ? '8bit' : 'auto');
    if (on) blip();
  }
  if (play8) { play8.hidden = false; play8.addEventListener('click', toggle8); }
  var hint = document.querySelector('.konami'); if (hint) hint.hidden = false;
  var code = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'], pos = 0;
  document.addEventListener('keydown', function (ev) {
    var t = ev.target; if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    var k = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key;
    pos = k === code[pos] ? pos + 1 : (k === code[0] ? 1 : 0);
    if (pos === code.length) { pos = 0; toggle8(); }
  });
  sync();
  images8();

  // Table of contents: mark the section being read
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.hash.slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute('aria-current'); });
        var a = byId[en.target.id]; if (a) a.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  // An earlier version of this site registered a service worker; remove it for returning visitors.
  if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
    navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister(); }); });
  }
})();
