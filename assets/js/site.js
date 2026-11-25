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
  }
  if (seg) {
    seg.hidden = false;
    sync();
    seg.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return;
      setTheme(b.dataset.themeSet);
    });
  }

  // Easter egg: 8-bit mode, from its button or the Konami code
  function toggle8() { setTheme(root.dataset.theme === '8bit' ? 'auto' : '8bit'); }
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
