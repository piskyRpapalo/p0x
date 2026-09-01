/* El Second Brain · el mapa de productos, en 3D y sin una sola libreria.

   POR QUE EXISTE
   --------------
   El canon del nodo dice «Hexelion != Aurelius != P0X, jamas confundir». Esa
   frase vive en prosa, y una frase en prosa hay que ACORDARSE de ella. Aqui la
   confusion es geometria: las aristas `no_es` se pintan en rojo y a trazos,
   igual de visibles que las que unen. Una sesion que salta de la app a la web
   puede seguir la linea sin cruzarla.

   POR QUE 3D A MANO Y NO UNA LIBRERIA
   -----------------------------------
   Tres razones, en orden. La casa no mete frameworks. El Ojo es loopback y
   tiene que abrir sin red. Y lo que hace falta de verdad --situar en el
   espacio, girar y proyectar-- son treinta lineas: una matriz de rotacion, una
   division por la profundidad y ordenar por z antes de pintar. Traerse tres
   megas para eso seria pagar en dependencias lo que cuesta en aritmetica.

   LA PROFUNDIDAD SIGNIFICA ALGO
   -----------------------------
   No es decoracion: cada capa es un nivel de abstraccion. z=0 el todo (P0X),
   z=1 los productos, z=2 sus caras y servicios, z=3 el metal. Se lee de dentro
   hacia fuera, que es como esta construido el organismo. */
(function () {
  "use strict";
  var lienzo = document.getElementById("grafo");
  var ficha = document.getElementById("grafo-ficha");
  if (!lienzo || !lienzo.getContext) return;

  var cx = lienzo.getContext("2d");
  var G = null, N = [], sel = null;
  // Giro inicial: ni de frente --las capas se taparian-- ni de perfil.
  var giroY = -0.55, giroX = 0.32, arrastre = null;
  var quieto = window.matchMedia
    ? matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };

  /* Cada capa es un anillo a su profundidad. El reparto por angulo es
     determinista --indice entre total-- y no aleatorio: el mapa tiene que
     salir IGUAL en cada recarga, o nadie construye memoria visual de el. */
  function situar(g) {
    var porCapa = {};
    g.nodos.forEach(function (n) {
      (porCapa[n.z] = porCapa[n.z] || []).push(n);
    });
    N = [];
    Object.keys(porCapa).forEach(function (z) {
      var fila = porCapa[z], radio = z === "0" ? 0 : 60 + Number(z) * 52;
      fila.forEach(function (n, i) {
        var a = (i / fila.length) * Math.PI * 2;
        N.push({
          d: n,
          x: Math.cos(a) * radio,
          y: (Number(z) - 1.5) * 62,
          z0: Math.sin(a) * radio
        });
      });
    });
  }

  function porId(id) {
    for (var i = 0; i < N.length; i++) if (N[i].d.id === id) return N[i];
    return null;
  }

  /* Rotar en Y, luego en X, y dividir por la profundidad. La `p` de la
     perspectiva se guarda: sirve para el tamano del punto y para ordenar. */
  function proyectar(n, w, h) {
    var cy = Math.cos(giroY), sy = Math.sin(giroY);
    var x1 = n.x * cy - n.z0 * sy, z1 = n.x * sy + n.z0 * cy;
    var cxx = Math.cos(giroX), sxx = Math.sin(giroX);
    var y1 = n.y * cxx - z1 * sxx, z2 = n.y * sxx + z1 * cxx;
    var p = 420 / (420 + z2);
    return { X: w / 2 + x1 * p, Y: h / 2 + y1 * p, p: p, z: z2 };
  }

  function pintar() {
    var w = lienzo.width, h = lienzo.height;
    cx.clearRect(0, 0, w, h);
    if (!G) return;
    var pos = {};
    N.forEach(function (n) { pos[n.d.id] = proyectar(n, w, h); });

    // Las aristas primero y de atras hacia delante, para que las de delante
    // tapen y el volumen se lea.
    G.aristas.slice().sort(function (a, b) {
      return (pos[b.de].z + pos[b.a].z) - (pos[a.de].z + pos[a.a].z);
    }).forEach(function (e) {
      var A = pos[e.de], B = pos[e.a], t = G.tipos[e.tipo] || {};
      if (!A || !B) return;
      var vivo = !sel || sel === e.de || sel === e.a;
      cx.save();
      cx.globalAlpha = vivo ? 0.85 : 0.12;
      cx.strokeStyle = t.color || "#888";
      // `no_es` a trazos y mas gruesa: una frontera tiene que verse ANTES
      // que un parentesco, porque es la que se cruza por error.
      cx.lineWidth = e.tipo === "no_es" ? 2.2 : 1.1;
      if (e.tipo === "no_es") cx.setLineDash([5, 4]);
      cx.beginPath(); cx.moveTo(A.X, A.Y); cx.lineTo(B.X, B.Y); cx.stroke();
      cx.restore();
    });

    N.slice().sort(function (a, b) { return pos[b.d.id].z - pos[a.d.id].z; })
      .forEach(function (n) {
        var P = pos[n.d.id], r = Math.max(3, 7 * P.p);
        var vivo = !sel || sel === n.d.id || vecino(n.d.id);
        cx.save();
        cx.globalAlpha = vivo ? 1 : 0.2;
        cx.beginPath(); cx.arc(P.X, P.Y, r, 0, Math.PI * 2);
        cx.fillStyle = n.d.id === sel ? "#f0d9a0" : COLOR[n.d.capa] || "#bbb";
        cx.fill();
        cx.font = Math.round(11 * P.p + 3) + "px ui-monospace,monospace";
        cx.fillStyle = "#e8e8ef";
        cx.fillText(n.d.nombre, P.X + r + 4, P.Y + 4);
        cx.restore();
        n.P = P; n.r = r;
      });
  }

  var COLOR = { todo: "#f0d9a0", producto: "#8f7bd6", cara: "#4fb286",
                servicio: "#e0a458", metal: "#9c9c9c" };

  function vecino(id) {
    if (!sel) return false;
    for (var i = 0; i < G.aristas.length; i++) {
      var e = G.aristas[i];
      if ((e.de === sel && e.a === id) || (e.a === sel && e.de === id)) return true;
    }
    return false;
  }

  /* La ficha no repite el dibujo: dice lo que el dibujo no puede decir --que
     ES cada cosa y donde vive-- y, sobre todo, POR QUE cada frontera existe.
     Una arista roja sin su motivo es un adorno. */
  function contar(id) {
    sel = id;
    var n = porId(id);
    if (!ficha || !n) return;
    ficha.innerHTML = "";
    var t = document.createElement("h3");
    t.textContent = n.d.nombre;
    ficha.appendChild(t);
    var q = document.createElement("p");
    q.textContent = n.d.que_es;
    ficha.appendChild(q);
    var d = document.createElement("p");
    d.className = "tenue"; d.textContent = n.d.donde || "";
    ficha.appendChild(d);
    var ul = document.createElement("ul");
    G.aristas.forEach(function (e) {
      if (e.de !== id && e.a !== id) return;
      var otro = e.de === id ? e.a : e.de;
      var on = porId(otro);
      var li = document.createElement("li");
      var b = document.createElement("b");
      b.style.color = (G.tipos[e.tipo] || {}).color || "#bbb";
      b.textContent = (G.tipos[e.tipo] || {}).que_dice || e.tipo;
      li.appendChild(b);
      li.appendChild(document.createTextNode(
        " · " + (on ? on.d.nombre : otro) + (e.nota ? " — " + e.nota : "")));
      ul.appendChild(li);
    });
    ficha.appendChild(ul);
    pintar();
  }

  // --- girar con el raton, y tocar para seleccionar -----------------------
  lienzo.addEventListener("pointerdown", function (ev) {
    arrastre = { x: ev.clientX, y: ev.clientY, movido: false };
    lienzo.setPointerCapture(ev.pointerId);
  });
  lienzo.addEventListener("pointermove", function (ev) {
    if (!arrastre) return;
    var dx = ev.clientX - arrastre.x, dy = ev.clientY - arrastre.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) arrastre.movido = true;
    giroY += dx * 0.008;
    giroX = Math.max(-1.2, Math.min(1.2, giroX + dy * 0.006));
    arrastre.x = ev.clientX; arrastre.y = ev.clientY;
    pintar();
  });
  lienzo.addEventListener("pointerup", function (ev) {
    var era = arrastre; arrastre = null;
    if (!era || era.movido) return;          // arrastrar no es seleccionar
    var r = lienzo.getBoundingClientRect();
    var mx = (ev.clientX - r.left) * (lienzo.width / r.width);
    var my = (ev.clientY - r.top) * (lienzo.height / r.height);
    var cerca = null, dmin = 26;
    N.forEach(function (n) {
      if (!n.P) return;
      var d = Math.hypot(n.P.X - mx, n.P.Y - my);
      if (d < dmin) { dmin = d; cerca = n.d.id; }
    });
    if (cerca) contar(cerca); else { sel = null; pintar(); }
  });

  function medir() {
    var r = lienzo.getBoundingClientRect();
    lienzo.width = Math.max(320, Math.round(r.width));
    lienzo.height = Math.max(260, Math.round(r.width * 0.62));
    pintar();
  }
  window.addEventListener("resize", medir);

  fetch("/api/grafo").then(function (r) { return r.json(); }).then(function (g) {
    if (!g || !g.nodos) {
      if (ficha) ficha.textContent = "NO_DATA · " + ((g && g.causa) || "sin grafo");
      return;
    }
    G = g; situar(g); medir(); contar("p0x");
    // Un giro lento solo si nadie ha pedido quietud, y se para al tocar: el
    // movimiento aqui sirve para leer el volumen, no para adornar.
    if (!quieto.matches) {
      setInterval(function () {
        if (!arrastre) { giroY += 0.0016; pintar(); }
      }, 50);
    }
  }).catch(function (e) {
    if (ficha) ficha.textContent = "NO_DATA · el Ojo no sirvio /api/grafo: " + e.message;
  });
})();
