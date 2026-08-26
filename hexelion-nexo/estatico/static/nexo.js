// El Nexo · treinta lineas, y ninguna decide nada.
//
// El servidor manda secciones de HTML ya compuestas por un flujo de eventos.
// Aqui solo se colocan. No hay plantillas, no hay estado, no hay framework: lo
// que antes eran siete pintores y doscientas lineas de JS vive ahora en Python,
// donde el escapado ocurre una vez y sobre el dato crudo.
//
// `EventSource` es del navegador. Cero bytes descargados, cero dependencias que
// auditar, y una reconexion automatica que nadie tiene que escribir.
'use strict';

const $ = s => document.querySelector(s);
let ultimoLatido = null;

function envejecer() {
  // Lo medido sigue siendo cierto de cuando se midio, asi que no se borra --
  // pero la pagina deja de presentarse como viva. El ojo lee la perdida de
  // color como «esto ya no esta pasando» sin leer una palabra.
  document.body.classList.add('rancio');
  const chip = $('#chip-conexion');
  chip.textContent = 'sin flujo';
  chip.className = 'chip c-warn';
  const s = ultimoLatido ? Math.round((Date.now() - ultimoLatido) / 1000) : null;
  $('#meta-medido').textContent = s === null
    ? 'el flujo no ha llegado a abrirse'
    : 'sin latido desde hace ' + s + ' s · lo de abajo es de la ultima lectura';
}

const flujo = new EventSource('/api/flujo');

for (const seccion of document.querySelectorAll('main section[id]')) {
  flujo.addEventListener(seccion.id, ev => { seccion.innerHTML = ev.data; });
}

flujo.addEventListener('latido', ev => {
  ultimoLatido = Date.now();
  document.body.classList.remove('rancio');
  const chip = $('#chip-conexion');
  chip.textContent = 'en vivo';
  chip.className = 'chip c-ok';
  $('#meta-medido').textContent = 'medido ' + String(ev.data).replace('T', ' ').slice(0, 19);
});

flujo.onerror = envejecer;

// Si el latido deja de llegar, la cara lo nota aunque el socket siga abierto:
// una conexion viva que no habla es indistinguible de una muerta, y solo el
// reloj las separa.
setInterval(() => {
  if (ultimoLatido && Date.now() - ultimoLatido > 70000) envejecer();
}, 10000);
