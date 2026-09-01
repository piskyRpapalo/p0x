/* EL REFUGIO · el mapa de productos como un corte lateral del bunker.
   Contrato visual: plan_v5.md, fase V5. Cero frameworks, loopback, 32 KB.

   POR QUE UN BUNKER Y NO UN GRAFO
   -------------------------------
   La primera version fue una nube de puntos girando en 3D. Era correcta y no
   servia: un grafo de fuerzas coloca los nodos donde caben, no donde SON, y
   aqui el sitio es el argumento. En el refugio, «superficie» es lo que se ve
   desde fuera, «sotano» es el metal, y las alas son los dos productos que no
   deben mezclarse. Mirarlo ya te dice la arquitectura; no hace falta leerla.

   DE DONDE SALE CADA COSA
   -----------------------
   De `grafo.json` y de nada mas. La sala, la tribu y las fronteras son DATO.
   Un render que decide donde va cada pieza es un render que puede mentir sobre
   la arquitectura, y este dibujo existe justo para que nadie se confunda.

   PIXEL ART DE VERDAD
   -------------------
   Se pinta en un lienzo interno pequeno con coordenadas ENTERAS y se amplia
   con `imageSmoothingEnabled=false`. Ampliar un dibujo suave no da pixel art,
   da un dibujo borroso: el pixel tiene que nacer grande. Los rotulos van
   despues, a resolucion nativa y en ui-monospace, que es lo que el anexo
   tipografico manda para datos y HUD. */
(function () {
  "use strict";
  var lienzo = document.getElementById("grafo");
  var ficha = document.getElementById("grafo-ficha");
  if (!lienzo || !lienzo.getContext) return;

  var W = 320, H = 208, ESC = 1;           // el mundo, en pixeles de verdad
  var buf = document.createElement("canvas");
  buf.width = W; buf.height = H;
  var b = buf.getContext("2d");
  var cx = lienzo.getContext("2d");
  var G = null, CAJAS = [], sel = null;

  var C = {
    cielo: "#243b55", tierra: "#3a2b22", roca: "#241a15",
    suelo: "#4a3830", pared: "#1b1520", panel: "#241d2e",
    marmol: "#d8d2c4", tinta: "#0f0c14", sol: "#f0d9a0", rojo: "#c65f5f"
  };

  function tribu(n) {
    return ((G.tribus || {})[n.tribu] || {}).color || C.marmol;
  }

  /* Un cuarto: pared, suelo y marco de su tribu. Sin degradados ni sombras --
     el anexo pide bordes crudos-- y con todo en enteros para que ningun
     pixel salga a medias. */
  function cuarto(x, y, w, h, color, activo) {
    b.fillStyle = C.pared; b.fillRect(x, y, w, h);
    b.fillStyle = C.suelo; b.fillRect(x + 1, y + h - 3, w - 2, 2);
    b.strokeStyle = activo ? C.sol : color;
    b.lineWidth = 1;
    b.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
    if (activo) b.strokeRect(x + 2.5, y + 2.5, w - 5, h - 5);
  }

  function piramide(x, y, w, h) {
    b.fillStyle = C.panel;
    b.beginPath();
    b.moveTo(x + w / 2, y); b.lineTo(x + w, y + h); b.lineTo(x, y + h);
    b.closePath(); b.fill();
    b.strokeStyle = C.marmol; b.stroke();
  }

  /* El ojo del centro. Es el unico dibujo figurativo del mapa y esta a
     proposito: la piramide es la casa de esta consola. */
  function ojo(px, py) {
    b.fillStyle = C.marmol;
    b.fillRect(px - 7, py - 2, 14, 4);
    b.fillRect(px - 5, py - 4, 10, 8);
    b.fillStyle = C.tinta; b.fillRect(px - 2, py - 2, 4, 4);
    b.fillStyle = C.sol;   b.fillRect(px - 1, py - 1, 2, 2);
  }

  function escena() {
    CAJAS = [];
    b.fillStyle = C.cielo; b.fillRect(0, 0, W, 62);
    b.fillStyle = C.tierra; b.fillRect(0, 62, W, 4);
    b.fillStyle = C.roca; b.fillRect(0, 66, W, H - 66);

    piramide(94, 66, 132, 106);
    ojo(160, 96);

    var por = {};
    G.nodos.forEach(function (n) { (por[n.sala] = por[n.sala] || []).push(n); });

    // `col` apila --las salas de un ala van una encima de otra-- y `fil`
    // reparte a lo ancho. El sotano es fila y no columna porque son CAJONES:
    // asi salen en la referencia, y apilados se salian del lienzo.
    function pon(lista, x, y, w, h, sep, horizontal) {
      (lista || []).forEach(function (n, i) {
        var xx = horizontal ? x + i * (w + sep) : x;
        var yy = horizontal ? y : y + i * (h + sep);
        cuarto(xx, yy, w, h, tribu(n), sel === n.id);
        CAJAS.push({ id: n.id, x: xx, y: yy, w: w, h: h, n: n });
      });
    }
    // La topologia del plan. Cada rotulo de sala tiene su franja libre encima:
    // la primera version los pintaba sobre el primer cuarto y no se leia
    // ninguno de los dos.
    pon(por["superficie"], 8, 14, 62, 14, 3, false);
    pon(por["ala-izq"], 8, 78, 80, 19, 4, false);
    pon(por["ala-der"], 230, 78, 82, 19, 4, false);
    pon(por["centro"], 118, 112, 84, 14, 2, false);
    pon(por["sotano"], 6, 182, 58, 18, 4, true);

    // Las fronteras: un muro rojo a trazos entre los dos cuartos que NO se
    // confunden. Se pinta encima de todo porque es lo ultimo que hay que
    // dejar de ver.
    b.save(); b.setLineDash([3, 3]); b.strokeStyle = C.rojo; b.lineWidth = 2;
    G.aristas.filter(function (e) { return e.tipo === "no_es"; }).forEach(function (e) {
      var A = caja(e.de), B = caja(e.a);
      if (!A || !B) return;
      b.beginPath();
      b.moveTo(A.x + A.w / 2, A.y + A.h / 2);
      b.lineTo(B.x + B.w / 2, B.y + B.h / 2);
      b.stroke();
    });
    b.restore();
  }

  function caja(id) {
    for (var i = 0; i < CAJAS.length; i++) if (CAJAS[i].id === id) return CAJAS[i];
    return null;
  }

  function pintar() {
    if (!G) return;
    escena();
    ESC = Math.max(1, Math.floor(lienzo.width / W));
    cx.imageSmoothingEnabled = false;       // sin esto no es pixel art, es puré
    cx.fillStyle = C.roca;
    cx.fillRect(0, 0, lienzo.width, lienzo.height);
    cx.drawImage(buf, 0, 0, W, H, 0, 0, W * ESC, H * ESC);

    // Rotulos a resolucion nativa: el anexo tipografico manda ui-monospace
    // para datos y HUD, y un rotulo pixelado a mano no se lee en un telefono.
    cx.font = "10px ui-monospace,monospace";
    cx.textBaseline = "top";
    Object.keys(G.salas || {}).forEach(function (k) { });
    CAJAS.forEach(function (c) {
      cx.fillStyle = sel === c.id ? C.sol : "#e8e8ef";
      var t = c.n.nombre;
      var max = Math.floor((c.w * ESC - 6) / 6);
      if (t.length > max) t = t.slice(0, max - 1) + "…";
      cx.fillText(t, c.x * ESC + 3, c.y * ESC + 3);
    });
    // Los rotulos de sala, en el sitio que ocupan en el plano.
    cx.fillStyle = "#8a8398";
    [["SUPERFICIE", 8, 3], ["MVP", 8, 68], ["WEB", 230, 68],
     ["EL OJO", 118, 102], ["LABORATORIO", 6, 172]].forEach(function (r) {
      cx.fillText(r[0], r[1] * ESC + 2, r[2] * ESC + 2);
    });
  }

  /* La ficha dice lo que el dibujo no puede: que ES cada cosa, donde vive y
     POR QUE cada frontera existe. Una linea roja sin su motivo es un adorno. */
  function contar(id) {
    sel = id; pintar();
    var c = caja(id);
    if (!ficha || !c) return;
    var n = c.n;
    ficha.innerHTML = "";
    var h = document.createElement("h3"); h.textContent = n.nombre;
    var s = document.createElement("p"); s.className = "tenue";
    s.textContent = (G.salas[n.sala] || {}).rotulo + " · " + n.sala;
    var q = document.createElement("p"); q.textContent = n.que_es;
    var d = document.createElement("p"); d.className = "tenue";
    d.textContent = n.donde || "";
    ficha.appendChild(h); ficha.appendChild(s); ficha.appendChild(q); ficha.appendChild(d);
    var ul = document.createElement("ul");
    G.aristas.forEach(function (e) {
      if (e.de !== id && e.a !== id) return;
      var otro = e.de === id ? e.a : e.de, on = caja(otro);
      var li = document.createElement("li");
      var bb = document.createElement("b");
      bb.style.color = e.tipo === "no_es" ? C.rojo
        : ((G.tipos[e.tipo] || {}).color || "#bbb");
      bb.textContent = (G.tipos[e.tipo] || {}).que_dice || e.tipo;
      li.appendChild(bb);
      li.appendChild(document.createTextNode(
        " · " + (on ? on.n.nombre : otro) + (e.nota ? " — " + e.nota : "")));
      ul.appendChild(li);
    });
    ficha.appendChild(ul);
  }

  lienzo.addEventListener("click", function (ev) {
    var r = lienzo.getBoundingClientRect();
    var mx = (ev.clientX - r.left) * (lienzo.width / r.width) / ESC;
    var my = (ev.clientY - r.top) * (lienzo.height / r.height) / ESC;
    for (var i = 0; i < CAJAS.length; i++) {
      var c = CAJAS[i];
      if (mx >= c.x && mx <= c.x + c.w && my >= c.y && my <= c.y + c.h) {
        return contar(c.id);
      }
    }
    sel = null; pintar();
  });

  function medir() {
    // Se mide el PADRE, no el lienzo. Un canvas con `width:100%` toma su ancho
    // del hueco, pero ese hueco lo define el propio canvas hasta que se le
    // asigna uno: leerse a si mismo da siempre la escala 1 de arranque. Me
    // paso, y el mapa salia del tamano de un sello.
    // Y si el hueco sale degenerado se cae a la ventana. No es paranoia: el
    // 2026-09-01 medi `html.clientWidth === 0` en esta misma pagina --el
    // refugio se colapsa entero en algunos contextos-- y un mapa que depende
    // de que su padre este bien maquetado desaparece sin decir por que.
    var hueco = (lienzo.parentNode && lienzo.parentNode.clientWidth) || 0;
    if (hueco < W) hueco = Math.max(W, window.innerWidth || W);
    // Multiplo ENTERO del mundo: media escala parte los pixeles y el dibujo
    // deja de ser nitido, que es todo lo que tiene.
    var e = Math.max(1, Math.min(4, Math.floor(hueco / W)));
    if (lienzo.width === W * e) { pintar(); return; }
    lienzo.width = W * e; lienzo.height = H * e;
    pintar();
  }
  window.addEventListener("resize", medir);

  fetch("/api/grafo").then(function (r) { return r.json(); }).then(function (g) {
    if (!g || !g.nodos) {
      if (ficha) ficha.textContent = "NO_DATA · " + ((g && g.causa) || "sin grafo");
      return;
    }
    G = g; medir(); contar("p0x");
    // Y otra vez tras el primer pintado: en el arranque el hueco todavia no
    // tiene su ancho definitivo y la escala saldria corta.
    requestAnimationFrame(medir);
  }).catch(function (e) {
    if (ficha) ficha.textContent = "NO_DATA · el Ojo no sirvio /api/grafo: " + e.message;
  });
})();
