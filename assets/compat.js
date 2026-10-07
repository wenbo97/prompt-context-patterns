(function () {
  'use strict';
  if (!document.querySelector('[data-compat]') || !location.hash) return;
  var id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
  var anchor = document.getElementById(id);
  var target = anchor && anchor.getAttribute('data-target');
  if (target && target.charAt(0) === '/' && target !== location.pathname + location.hash) location.replace(target);
}());
