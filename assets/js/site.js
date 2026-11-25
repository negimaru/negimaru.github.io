// Progressive enhancement only: the page is complete without this file.
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.theme');
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function current() { return root.dataset.theme || (mq && mq.matches ? 'dark' : 'light'); }
  function label() { if (btn) btn.textContent = current() === 'dark' ? btn.dataset.toLight : btn.dataset.toDark; }
  if (btn) {
    btn.hidden = false;
    label();
    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (_) {}
      label();
    });
    if (mq && mq.addEventListener) mq.addEventListener('change', label);
  }
  // An earlier version of this site registered a service worker; remove it for returning visitors.
  if ('serviceWorker' in navigator && navigator.serviceWorker.getRegistrations) {
    navigator.serviceWorker.getRegistrations().then(function (rs) { rs.forEach(function (r) { r.unregister(); }); });
  }
})();
