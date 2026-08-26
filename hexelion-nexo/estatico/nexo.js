// El Nexo · pinta lo que el servidor mide. Vanilla, sin una sola libreria.
//
// Dos reglas gobiernan todo este fichero:
//   1. NO_DATA no se pinta como un valor. Va en ambar, con su causa debajo.
//   2. Si el servidor no contesta, la pagina NO se queda con lo de antes como
//      si siguiera vivo: marca su edad y lo dice. Una interfaz congelada que
//      ensena cifras viejas es peor que una vacia, porque parece que funciona.
'use strict';

const $ = s => document.querySelector(s);
const esc = s => String(s === null || s === undefined ? '' : s)
  .replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const NO_DATA = 'NO_DATA';
const hueco = v => v === NO_DATA || v === null || v === undefined;

function fila(k, v, clase, sangrada) {
  const cuerpo = hueco(v)
    ? `<span class="nodata">${NO_DATA}</span>`
    : `<span class="${clase || ''}">${esc(v)}</span>`;
  return `<div class="fila${sangrada ? ' fila--sangrada' : ''}">` +
         `<span class="k">${esc(k)}</span><span class="v">${cuerpo}</span></div>`;
}

function causa(texto) {
  return texto ? `<p class="causa">${esc(texto)}</p>` : '';
}

function pinta(id, chipTexto, chipClase, html) {
  const mod = document.getElementById(id);
  if (!mod) return;
  const chip = mod.querySelector('[data-chip]');
  chip.textContent = chipTexto;
  chip.className = 'chip ' + (chipClase || 'c-mut');
  mod.querySelector('[data-cuerpo]').innerHTML = html;
}

function sinDato(id, lectura) {
  pinta(id, NO_DATA, 'c-warn',
    `<div class="cifra nodata" style="font-size:19px">${NO_DATA}</div>` +
    causa(lectura && lectura.causa ? lectura.causa : 'el sensor no devolvio nada'));
}

// ── un pintor por tarjeta ───────────────────────────────────────────────────

const PINTORES = {

  nodos(d) {
    // Tira horizontal y no rejilla fija: cuando entre un quinto nodo, la fila
    // se alarga en vez de re-maquetarse. Es el mismo veredicto que retiro la
    // grilla 4x4 del herbier.
    const CLASE = {ONLINE: 'c-ok', CRITICO: 'c-crit', OFFLINE: 'c-mut',
                   'EN ESPERA': 'c-warn', NO_DATA: 'c-warn'};
    const tarjetas = (d.nodos || []).map(n => `
      <article class="nodo ${n.estado === 'CRITICO' ? 'nodo--critico' : ''}">
        <header><b>${esc(n.nodo)}</b>
          <span class="chip ${CLASE[n.estado] || 'c-mut'}">${esc(n.estado)}</span></header>
        <p class="nodo__metal">${esc(n.metal)}</p>
        <p class="nodo__nota">${hueco(n.nota)
          ? '<span class="nodata">' + NO_DATA + '</span>' : esc(n.nota)}</p>
        ${n.alerta ? `<p class="nodo__alerta">${esc(n.alerta)}</p>` : ''}
      </article>`).join('');
    pinta('m-nodos',
      d.en_pie + ' en pie' + (d.criticos ? ' · ' + d.criticos + ' crítico' : ''),
      d.criticos ? 'c-crit' : 'c-ok',
      `<div class="tira">${tarjetas}</div>` +
      causa('fuente: ' + d.fuente + (d.avisos.length ? ' · ' + d.avisos.join(' · ') : '')));
  },

  soberania(d) {
    // El diagrama manda: la banda focal se mueve con el nivel en vigor. Un
    // layer stack pintado a mano se quedaria diciendo «0» el dia que suba, y
    // una figura que miente es peor que ninguna figura.
    const mod = document.getElementById('m-soberania');
    mod.querySelectorAll('.banda').forEach(b => {
      const n = Number(b.dataset.nivel);
      b.classList.toggle('focal', n === d.nivel);
      b.classList.toggle('dormida', n > d.nivel);
    });
    const pie = mod.querySelector('[data-pie]');
    if (pie) {
      pie.textContent = d.cortado
        ? 'corte activo · el centinela manda sobre lo declarado en el estado'
        : 'nivel ' + d.nivel + ' en vigor · nada por encima esta concedido';
    }
    const caps = (d.capacidades || []).map(c =>
      fila(c.nombre, c.concedida ? 'concedida' : 'no concedida',
           c.concedida ? 'c-ok' : 'c-mut')).join('');
    pinta('m-soberania',
      d.cortado ? 'santuario · corte' : 'nivel ' + d.nivel,
      d.cortado ? 'c-warn' : (d.nivel === 0 ? 'c-ok' : 'c-gold'),
      caps + causa('el nivel 0 no aparece en la tabla: lo que el suelo ya hace '
                 + 'no pide permiso'));
  },

  preceptor(d) {
    const t = d.tanda || {};
    const verde = t.estado === 'ok' && t.verde;
    pinta('m-preceptor',
      verde ? (t.rancia ? 'verde · rancia' : 'verde') : NO_DATA,
      verde ? (t.rancia ? 'c-warn' : 'c-ok') : 'c-warn',
      `<div class="cifra">${t.estado === 'ok' ? esc(t.pruebas) + ' / ' + esc(t.pruebas)
        : '<span class="nodata">' + NO_DATA + '</span>'}` +
      `<small>${t.estado === 'ok' ? esc(t.suites) + ' SUITES' : 'SIN TANDA REGISTRADA'}</small></div>` +
      fila('versión', d.version) +
      fila('ficheros de la cara', d.huella ? d.huella.ficheros : NO_DATA) +
      fila('medida', t.medido ? t.medido.replace('T', ' ').slice(0, 16) : NO_DATA) +
      fila('ruta', d.ruta, 'c-mut') +
      causa(t.causa));
  },

  timers(d) {
    const filas = (d.propios || []).map(f => {
      const ok = f.resultado === 'success';
      return fila(f.unidad.replace('.timer', ''), f.proxima,
                  f.activo ? 'c-ok' : 'c-crit') +
             fila('última · ' + (hueco(f.resultado) ? 'sin estrenar' : f.resultado),
                  f.ultima, ok ? 'c-mut' : 'c-warn', true);
    }).join('');
    const sinEstrenar = (d.propios || []).filter(f => hueco(f.ultima)).length;
    pinta('m-timers', d.cuantos + ' bucles',
      sinEstrenar ? 'c-warn' : 'c-ok',
      filas + causa(
        (sinEstrenar ? sinEstrenar + ' armado(s) y sin dispararse nunca · ' : '') +
        d.cuantos_ajenos + ' timers del sistema, contados aparte'));
  },

  lora(d) {
    const ads = (d.adapters || []).map(a =>
      fila(a.nombre, a.estado === 'ok' ? (a.bytes / 1048576).toFixed(1) + ' MiB' : NO_DATA,
           a.estado === 'ok' ? 'c-ok' : '', true)).join('');
    pinta('m-lora', d.entrenados + ' adapters',
      d.entrenados ? 'c-gold' : 'c-warn',
      `<div class="cifra">${esc(d.ejemplos_totales)}<small>EJEMPLOS · ${
        esc((d.datasets || []).length)} DATASETS</small></div>` +
      fila('fase', d.fase, 'c-warn') +
      fila('con pesos', d.entrenados + ' de ' + (d.adapters || []).length) +
      ads + causa('una carpeta sin fichero de pesos no cuenta como adapter'));
  },

  cinek(d) {
    const filas = (d.registros || []).slice(0, 4).map(r =>
      fila(r.nombre, (r.bytes / 1024).toFixed(0) + ' KiB · ' + r.dias + ' d')).join('');
    pinta('m-cinek', d.quietud_dias + ' d sin tocar',
      d.quietud_dias > 7 ? 'c-warn' : 'c-ok',
      `<div class="cifra">${esc(d.quietud_dias)}<small>DÍAS DE QUIETUD</small></div>` +
      filas + causa(d.nota + ' · los registros se listan, no se leen'));
  },

  jardin(d) {
    pinta('m-jardin', 'en espera', 'c-mut',
      fila('rutas en disco', (d.rutas || []).join(' · ') || NO_DATA) +
      fila('sensores', d.sensores_declarados) +
      fila('última lectura', d.ultima_lectura) +
      causa(d.causa));
  },
};

// ── el bucle ────────────────────────────────────────────────────────────────
//
// Treinta segundos, y no menos: los sensores hablan con systemd y con el disco,
// y un panel que pregunta cada segundo deja de ser una ventana para convertirse
// en carga. Cuando la pestaña esta oculta NO se pregunta nada -- nadie esta
// mirando-- y al volver se pide de inmediato en vez de esperar al siguiente
// turno, que es lo que hace que parezca que se ha quedado colgado.

const CADA = 30000;
let ultimaBuena = null;   // Date de la ultima respuesta que llego entera
let reloj = null;

function edad() {
  if (!ultimaBuena) return null;
  return Math.round((Date.now() - ultimaBuena.getTime()) / 1000);
}

function envejecer() {
  // La degradacion honesta. La pagina NO se vacia --lo de antes sigue siendo
  // cierto de cuando se midio-- pero deja de presentarse como viva: se marca
  // entera y la cabecera dice desde cuando. Una interfaz congelada enseñando
  // cifras viejas es peor que una vacia, porque parece que funciona.
  const s = edad();
  const chip = $('#chip-conexion');
  document.body.classList.add('rancio');
  chip.textContent = 'sin lectura';
  chip.className = 'chip c-warn';
  $('#meta-medido').textContent = s === null
    ? 'el servidor no ha contestado ni una vez'
    : 'sin lectura desde hace ' + s + ' s · lo de abajo es de la ultima buena';
}

async function tick() {
  let datos;
  try {
    const r = await fetch('/api/estado', {cache: 'no-store'});
    if (!r.ok) throw new Error('estado ' + r.status);
    datos = await r.json();
  } catch (e) {
    // Ni una traza de red en la cara: no ha fallado nada que la persona pueda
    // arreglar leyendo un errno. Se dice que no hay dato y desde cuando.
    envejecer();
    return;
  }
  ultimaBuena = new Date();
  document.body.classList.remove('rancio');
  const chip = $('#chip-conexion');
  chip.textContent = 'en vivo';
  chip.className = 'chip c-ok';
  $('#meta-medido').textContent =
    'medido ' + String(datos.medido || '').replace('T', ' ').slice(0, 19);

  for (const [nombre, lectura] of Object.entries(datos.lecturas || {})) {
    const id = 'm-' + nombre;
    if (!document.getElementById(id)) continue;
    if (!lectura || lectura.estado !== 'ok' || !PINTORES[nombre]) {
      sinDato(id, lectura);
      continue;
    }
    try {
      PINTORES[nombre](lectura);
    } catch (e) {
      // Una tarjeta que revienta al pintarse no puede llevarse a las otras
      // cinco por delante, igual que un sensor caido no tumba a los demas.
      sinDato(id, {causa: 'la tarjeta no se pudo pintar con esta lectura'});
    }
  }
}

function arrancar() {
  if (reloj !== null) clearInterval(reloj);
  reloj = setInterval(tick, CADA);
}

function parar() {
  if (reloj !== null) { clearInterval(reloj); reloj = null; }
}

document.addEventListener('visibilitychange', () => {
  if (document.hidden) { parar(); return; }
  tick();        // al volver, de inmediato: esperar 30 s parece un cuelgue
  arrancar();
});

tick();
arrancar();
