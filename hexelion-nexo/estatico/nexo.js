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

  soberania(d) {
    const escalera = (d.niveles || []).map(n =>
      `<div class="peldano${n.activo ? ' activo' : ''}${n.n === 0 ? ' suelo' : ''}">` +
      `<b>${n.n}</b><span>${esc(n.nombre)}</span></div>`).join('');
    const caps = (d.capacidades || []).map(c =>
      fila(c.nombre, c.concedida ? 'concedida' : 'no concedida',
           c.concedida ? 'c-ok' : 'c-mut', true) ).join('');
    pinta('m-soberania',
      d.cortado ? 'santuario · corte activo' : 'nivel ' + d.nivel,
      d.cortado ? 'c-warn' : (d.nivel === 0 ? 'c-ok' : 'c-gold'),
      `<div class="cifra">Nivel ${esc(d.nivel)}<small>${esc(d.nombre)}</small></div>` +
      `<div class="escalera">${escalera}</div>` +
      `<div style="margin-top:12px">${caps}</div>` +
      causa(d.cortado
        ? 'el centinela o la bandera mandan sobre lo declarado en el estado'
        : 'ninguna capacidad por encima del suelo esta concedida'));
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

async function tick() {
  let datos;
  try {
    const r = await fetch('/api/estado', {cache: 'no-store'});
    if (!r.ok) throw new Error('estado ' + r.status);
    datos = await r.json();
  } catch (e) {
    // Ni una traza de red en la cara. Se dice que no hay dato y desde cuando.
    const chip = $('#chip-conexion');
    chip.textContent = 'sin lectura';
    chip.className = 'chip c-warn';
    $('#meta-medido').textContent =
      'el servidor no contesta · lo de abajo es de la ultima lectura buena';
    return;
  }
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
    try { PINTORES[nombre](lectura); } catch (e) { sinDato(id, {causa: 'la tarjeta no se pudo pintar'}); }
  }
}

tick();
