// Progressive enhancement only: the page is complete without this file.
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.theme');
  function store(v) { try { localStorage.setItem('theme', v); } catch (_) {} }
  function apply(theme) {
    if (theme === 'light') root.dataset.theme = 'light'; else delete root.dataset.theme;
    if (btn) btn.setAttribute('aria-label', theme === 'light' ? btn.dataset.toDark : btn.dataset.toLight);
  }
  if (btn) {
    btn.hidden = false;
    apply(root.dataset.theme === 'light' ? 'light' : 'dark');
    btn.addEventListener('click', function () {
      var next = root.dataset.theme === 'light' ? 'dark' : 'light';
      apply(next); store(next);
    });
  }
  // An earlier version of this site registered a service worker; remove it for returning visitors.
  if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
    navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister(); }); });
  }
})();
