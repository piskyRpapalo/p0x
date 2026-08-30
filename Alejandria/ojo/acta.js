/* «El Acta» · los mensajes de coordinación, con sus dos caras.
   La humana se lee; la de máquina se despliega. El badge de la cadena es lo
   primero: un acta que no verifica no vale como acta. */
(function () {
  'use strict';
  var O = window.Ojo, caja = document.getElementById('acta-cuerpo');
  if (!caja) return;

  function badge(m) {
    return '<span class="acta-de acta-' + O.esc(m.de) + '">' + O.esc(m.de) +
           '</span> <span class="t-sello">→ ' + O.esc((m.para || []).join(', ')) +
           ' · ' + O.esc(m.tipo) + '</span>';
  }

  fetch('/api/acta', { cache: 'no-store' })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.estado === 'NO_DATA') {
        caja.innerHTML = '<p class="tenue">⬜ ' + O.esc(d.causa || '') +
          (d.remedio ? ' · <code>' + O.esc(d.remedio) + '</code>' : '') + '</p>';
        return;
      }
      var h = [];
      h.push(d.cadena_sana
        ? '<p class="acta-ok">✅ Cadena verificada · ' +
          O.plural(d.mensajes.length, 'mensaje') + '</p>'
        : '<p class="t-red"><b>🔴 CADENA ROTA</b><br>' +
          d.problemas.map(O.esc).join('<br>') + '</p>');

      // El mas reciente primero: lo ultimo dicho es lo que importa al abrir.
      d.mensajes.slice().reverse().forEach(function (m) {
        h.push('<article class="acta-msg">' +
          '<header>' + badge(m) + ' <span class="t-sello">' +
          O.esc((m.ts || '').replace('T', ' ').slice(0, 16)) + '</span>' +
          (m.firma_requerida ? ' <b class="acta-firma">firma</b>' : '') +
          '</header>' +
          '<p>' + O.esc(m.humano) + '</p>' +
          '<p class="t-sello">fuente: ' + O.esc((m.fuente || []).join(' · ')) + '</p>' +
          '<details><summary class="t-sello">la cara de máquina</summary>' +
          '<pre class="acta-json">' +
          O.esc(JSON.stringify(m.maquina, null, 1)) + '</pre></details>' +
          '</article>');
      });
      caja.innerHTML = h.join('');
    })
    .catch(function (e) {
      caja.innerHTML = '<p class="t-red">NO_DATA — el acta no cargó: ' +
        O.esc(e.message) + '</p>';
    });
})();
