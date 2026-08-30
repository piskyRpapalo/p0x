/* «Cómo funciona el enjambre» · el glosario vivo.
   Modulo aparte y no un bloque mas de ojo.js: el nucleo esta a 268 bytes del
   tope de D1-bis, y la respuesta correcta a un fichero lleno es partirlo. */
(function () {
  'use strict';
  var O = window.Ojo, caja = document.getElementById('glosario-cuerpo');
  if (!caja) return;

  var MARCA = { OK: '', NO_DATA: '⬜ ' };

  fetch('/api/glosario', { cache: 'no-store' })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.estado === 'NO_DATA') {
        caja.innerHTML = '<p class="tenue">⬜ ' + O.esc(d.causa || '') + '</p>';
        return;
      }
      var h = ['<p class="glos-entrada">' + O.esc(d.entrada) +
               '</p><p class="t-sello">Medido el ' + O.esc(d.medido) + '</p>'];
      d.entradas.forEach(function (e) {
        h.push('<details class="glos"><summary>' + (MARCA[e.estado] || '') +
               '<b>' + O.esc(e.termino) + '</b></summary>' +
               '<p>' + O.esc(e.que_hace) + '</p>' +
               (e.nota ? '<p class="glos-nota">' + O.esc(e.nota) + '</p>' : '') +
               '<p class="t-sello">dónde verlo</p>' +
               '<pre class="glos-cmd">' + O.esc(e.donde_verlo) + '</pre>' +
               '<p class="t-sello">fuente: <code>' + O.esc(e.fuente) +
               '</code></p></details>');
      });
      caja.innerHTML = h.join('');
    })
    .catch(function (e) {
      caja.innerHTML = '<p class="t-red">NO_DATA — el glosario no cargó: ' +
        O.esc(e.message) + '</p>';
    });
})();
