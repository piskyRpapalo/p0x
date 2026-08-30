/* El Ojo del Soberano · pinta el rack. No lo mide.
   Todo sale de /api/rack, que sirve lo que recolector.py dejo escrito. Si esta
   pagina midiera por su cuenta, se colgaria justo cuando el rack cae -- que es
   el unico momento en que hace falta. */
(function () {
  'use strict';

  var LOG = document.getElementById('log');
  var FRESCURA = document.getElementById('frescura');
  var DETALLE = document.getElementById('detalle');
  var CUERPO = document.getElementById('detalle-cuerpo');

  var HORA = 3600, DIA = 86400;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function sello(iso) {
    // [YYYY-MM-DD HH:MM] · la marca de cada linea es la HORA DE LA MEDIDA, no
    // la de ahora. Poner la hora actual en un dato viejo es como se disfraza
    // de fresco lo que no lo esta.
    var d = iso ? new Date(iso) : new Date();
    if (isNaN(d)) d = new Date();
    var p = function (n) { return String(n).padStart(2, '0'); };
    return '[' + d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) +
           ' ' + p(d.getHours()) + ':' + p(d.getMinutes()) + ']';
  }

  function clase(estado) {
    return estado === 'OK' ? 't-ok' : estado === 'RED' ? 't-red' : 't-nodata';
  }

  /* El rotulo depende del componente. «PUERTOS :: OFFLINE» para decir que hay
     un puerto expuesto dice justo lo contrario de lo que pasa, y un panel que
     miente en una palabra deja de leerse entero. */
  var ROTULOS = {
    PUERTOS:  { OK: 'LIMPIO', RED: 'EXPUESTO' },
    HUERFANOS:{ RED: 'FANTASMA' },
    MEMORIA: { OK: 'OK', RED: 'ROTA' },
    DISCO:   { OK: 'OK', RED: 'LLENO' },
    MVP_GATE:{ OK: 'GREEN', RED: 'RED' },
    WEB_GATE:{ OK: 'GREEN', RED: 'RED' }
  };
  function rotulo(estado, clave) {
    var t = ROTULOS[clave];
    if (t && t[estado]) return t[estado];
    return estado === 'OK' ? 'ONLINE' : estado === 'RED' ? 'OFFLINE' : 'NO_DATA';
  }

  function fila(marca, clave, estado, detalle) {
    return '<span class="t-sello">' + marca + '</span> ' +
           '<span class="t-clave">' + esc(clave.padEnd(9)) + '</span> :: ' +
           '<b class="' + clase(estado) + '">' + rotulo(estado, clave.trim()) + '</b>' +
           (detalle ? ' <span class="t-sello">(' + esc(detalle) + ')</span>' : '');
  }

  function plural(n, singular, sufijo) {
    return n + ' ' + singular + (n === 1 ? '' : (sufijo || 's'));
  }

  function edad(s) {
    if (s == null) return 'NO_DATA';
    if (s < 90) return s + ' s';
    if (s < 5400) return Math.round(s / 60) + ' min';
    if (s < 172800) return Math.round(s / HORA) + ' h';
    return Math.round(s / DIA) + ' d';
  }

  function pintarFrescura(d) {
    var s = d.frescura_segundos;
    FRESCURA.className = 'frescura';
    if (s == null) {
      FRESCURA.classList.add('perdida');
      FRESCURA.innerHTML = '🔴 <b>NO_DATA</b> — ' + esc(d.causa || 'sin estado.json') +
        '. Remedio: <code>' + esc(d.remedio || '~/p0x/Alejandria/verificar_sesion.sh') + '</code>';
      return;
    }
    if (s > DIA) {
      FRESCURA.classList.add('perdida');
      FRESCURA.innerHTML = '🔴 <b>STALE · contexto perdido</b> — la medida tiene ' +
        edad(s) + '. No decidas nada con esto: lee ' +
        '<code>ALEJANDRIA_ESTADO_ACTUAL.md</code> y vuelve a medir.';
    } else if (s > HORA) {
      FRESCURA.classList.add('rancia');
      FRESCURA.innerHTML = '🟠 <b>STALE</b> — la medida tiene ' + edad(s) +
        '. Ejecuta <code>~/p0x/Alejandria/verificar_sesion.sh</code>';
    } else {
      FRESCURA.classList.add('fresca');
      FRESCURA.innerHTML = '✅ Medida hace ' + edad(s) + ' · modo <code>' +
        esc(d.modo || '?') + '</code>';
    }
  }

  function pintarLog(d) {
    var c = d.componentes || {};
    var m = sello(d.generado);
    var L = [];

    var o = c.ollama || {};
    L.push(fila(m, 'OLLAMA', o.estado, o.estado === 'OK'
      ? o.modelos + ' modelos · ' + o.latencia_ms + ' ms · ' + (o.backend || '?')
      : o.causa));

    var g = c.api_guia || {};
    L.push(fila(m, 'API_GUIA', g.estado, g.estado === 'OK'
      ? ':9001 · unidad de ' + g.gestor + ' · via ' + g.alcanzado_en
      : g.causa));

    ['mvp_gate', 'web_gate'].forEach(function (k) {
      var b = c[k] || {};
      var nom = k === 'mvp_gate' ? 'MVP_GATE' : 'WEB_GATE';
      var det;
      if (b.estado === 'OK') {
        det = b.pasa + (b.salta ? '/' + b.salta + ' skip' : '') +
              (b.subtests ? ' +' + b.subtests + ' sub' : '') + ' GREEN';
        // Un gate arrastrado se declara arrastrado. Siempre.
        if (b.arrastrado) det += ' · ⏳ de hace ' + edad(b.edad_s);
      } else { det = b.causa; }
      L.push(fila(m, nom, b.estado, det));
    });

    var l = c.lora_v7 || {};
    L.push(fila(m, 'LORA_V7', l.estado, l.estado === 'OK'
      ? 'LOADED · ' + (l.adaptadores || []).join(', ') : l.causa));

    var dg = c.doogee || {};
    L.push(fila(m, 'DOOGEE', dg.estado, dg.estado === 'OK'
      ? 'connected · ' + dg.serial : dg.causa));

    var t = c.tailscale || {};
    L.push(fila(m, 'TAILNET', t.estado, t.estado === 'OK'
      ? t.online + '/' + t.total + ' en linea' : t.causa));

    var mem = c.memoria || {};
    if (mem.estado === 'OK') {
      var tab = {}; (mem.tablas || []).forEach(function (p) { tab[p[0]] = p[1]; });
      var aviso = (mem.engramas <= 1 && tab.turnos > 1)
        ? ' · ⚠ sin destilar (' + plural(tab.turnos, 'turno') + ')' : '';
      L.push(fila(m, 'MEMORIA', 'OK', plural(mem.engramas, 'engrama') + ' · FTS ' +
        (mem.fts ? 'si' : 'NO') + aviso));
    } else {
      L.push(fila(m, 'MEMORIA', mem.estado, mem.causa));
    }

    var ds = c.disco || {};
    L.push(fila(m, 'DISCO', ds.estado, ds.libre_gb + ' GB libres de ' + ds.total_gb));

    var p = c.puertos || {};
    // La condicion es «hay datos», NO «esta en verde». Con `p.estado === 'OK'`
    // el panel escondia la seccion de puertos justo cuando salia en rojo, que
    // es el unico momento en que hacia falta verla. Un panel que se calla al
    // detectar el problema es peor que no tener panel.
    if (p.lista) {
      var det = p.total + ' a la escucha · ' + p.expuestos + ' fuera de loopback';
      if ((p.sorpresas || []).length) {
        det += ' · SORPRESA: ' + p.sorpresas.map(function (x) {
          return x.addr + ' (' + x.proceso + ')'; }).join(', ');
      }
      L.push(fila(m, 'PUERTOS', p.estado, det));
      if ((p.huerfanos || []).length) {
        // Servidores cuyo shell murio. Linea propia porque es un hallazgo, no
        // una nota: nadie recuerda haberlos arrancado, y por eso siguen ahi.
        var vh = Math.max.apply(null, p.huerfanos.map(function (x) { return x.edad_s; }));
        L.push(fila(m, 'HUERFANOS', 'RED',
          p.huerfanos.length + ' × http.server sin padre · el más viejo lleva ' + edad(vh)));
      }
    }

    L.push('');
    L.push('<span class="t-sello">' + m + ' ENJAMBRE  :: oneshot — «inactive» entre disparos es el estado sano</span>');
    Object.keys(c.enjambre || {}).forEach(function (n) {
      var b = c.enjambre[n];
      L.push('  ' + '<span class="t-clave">' + esc(n.padEnd(9)) + '</span> :: ' +
        '<b class="' + clase(b.estado) + '">' + (b.estado === 'OK' ? 'SANO' : rotulo(b.estado, n)) + '</b>' +
        ' <span class="t-sello">(' + esc(b.cadencia || '?') + ' · próxima ' +
        esc(b.proxima || '?') + ')</span>');
    });

    LOG.innerHTML = L.join('\n');
  }

  function pintarDetalle(d) {
    var p = (d.componentes || {}).puertos;
    // Mismo criterio que arriba: se pinta si hay lista, en verde o en rojo.
    if (!p || !p.lista) { DETALLE.hidden = true; return; }
    var h = ['<table><thead><tr><th>Dirección</th><th>Alcance</th><th>Proceso</th>' +
             '</tr></thead><tbody>'];
    p.lista.slice().sort(function (a, b) { return (b.expuesto ? 1 : 0) - (a.expuesto ? 1 : 0); })
      .forEach(function (f) {
        h.push('<tr><td><code>' + esc(f.addr) + '</code></td><td class="' +
          (f.expuesto ? 'expuesto">🌐 expuesto' : 'local">🔒 loopback') +
          '</td><td>' + esc(f.proceso) + '</td></tr>');
      });
    h.push('</tbody></table>');
    CUERPO.innerHTML = h.join('');
    DETALLE.hidden = false;
  }

  function refrescar() {
    fetch('/api/rack', { cache: 'no-store' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        pintarFrescura(d);
        if (d.componentes) { pintarLog(d); pintarDetalle(d); }
        else { LOG.textContent = 'NO_DATA — ' + (d.causa || 'sin datos'); }
      })
      .catch(function (e) {
        // El Ojo caido se declara caido. No deja el ultimo pintado en pantalla
        // fingiendo que sigue vivo.
        FRESCURA.className = 'frescura perdida';
        FRESCURA.innerHTML = '🔴 <b>NO_DATA</b> — el Ojo no responde: ' + esc(e.message) +
          '. ¿Sigue vivo <code>ojo.py</code>?';
      });
  }

  refrescar();
  setInterval(refrescar, 60000);
})();
