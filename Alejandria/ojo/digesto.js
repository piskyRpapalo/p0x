/* «El Enlace dice» · el último digesto, con su frescura y su estante.
   La marca BRONZE va arriba y en grande: quien lee tiene que saber de un
   vistazo si está leyendo una medida o una redacción. */
(function () {
  'use strict';
  var O = window.Ojo, caja = document.getElementById('digesto-cuerpo');
  if (!caja) return;

  fetch('/api/digesto', { cache: 'no-store' })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.estado === 'NO_DATA') {
        caja.innerHTML = '<p class="tenue">⬜ ' + O.esc(d.causa || '') +
          (d.remedio ? '<br>Remedio: <code>' + O.esc(d.remedio) + '</code>' : '') +
          '</p>';
        return;
      }
      var h = ['<p class="t-sello">' + O.esc(d.fichero) + ' · hace ' +
               O.esc(O.edad(d.frescura_segundos)) + '</p>'];
      h.push(d.bronze
        ? '<p class="dig-bronze"><b>BRONZE · en cuarentena.</b> La prosa la ' +
          'redactó un modelo local a partir de hechos medidos. Los hechos son ' +
          'Silver; la prosa, no.</p>'
        : '<p class="tenue">⬜ Sin paráfrasis: solo hechos medidos.</p>');
      // Markdown minimo y a mano: traer una libreria por cuatro encabezados
      // seria la primera peticion externa de esta consola.
      h.push('<div class="dig-cuerpo">' + d.cuerpo.split('\n').map(function (l) {
        if (l.indexOf('## ') === 0)
          return '<h4>' + O.esc(l.slice(3)) + '</h4>';
        if (l.indexOf('- ') === 0 || l.indexOf('| ') === 0)
          return '<p class="dig-linea">' + O.esc(l.replace(/^[-|] ?/, '')) + '</p>';
        return l.trim() ? '<p>' + O.esc(l) + '</p>' : '';
      }).join('') + '</div>');
      caja.innerHTML = h.join('');
    })
    .catch(function (e) {
      caja.innerHTML = '<p class="t-red">NO_DATA — el digesto no cargó: ' +
        O.esc(e.message) + '</p>';
    });
})();
