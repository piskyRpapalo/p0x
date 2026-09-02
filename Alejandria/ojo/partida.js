/* CARGAR PARTIDA · el save game, pintado para quien acaba de llegar.

   POR QUE ESTA ARRIBA DEL TODO Y NO EN UN <details>. Lo que esta plegado no se
   lee: el glosario entero lleva semanas plegado al final de esta pagina y la
   Doctrina Caza-Nido acabo escrita TRES VECES ahi dentro sin que nadie lo
   viera. Una sesion fria no abre acordeones -- lee lo primero, decide, y toca.
   Asi que los cuatro pilares se pintan abiertos y antes que nada.

   NO SE ESCRIBE NI UNA PALABRA AQUI. Todo sale de /api/arranque, que a su vez
   resuelve los terminos que nombra arranque.json contra glosario.json. Este
   fichero decide el ORDEN y la FORMA; el contenido no es suyo. Si algun dia
   este render y el glosario dijeran cosas distintas, este estaria mintiendo.

   Y SI FALTA UN PILAR, SE VE. La API devuelve {falta, causa, remedio} en el
   sitio donde iba la entrada; aqui eso se pinta en rojo y con su remedio, no
   se filtra. Una partida con tres pilares que parece completa es exactamente
   el fallo que este panel existe para no tener. */
(function () {
  "use strict";
  var caja = document.getElementById("partida-cuerpo");
  if (!caja) return;

  function el(t, c, x) {
    var n = document.createElement(t);
    if (c) n.className = c;
    if (x !== undefined && x !== null) n.textContent = String(x);
    return n;
  }

  /* Una entrada del glosario, o el hueco que dejo. */
  function entrada(e, grado) {
    if (!e) return el("p", "t-nodata", "NO_DATA · sin entrada");
    var caja1 = el("div", "pilar" + (e.falta ? " pilar-falta" : ""));
    if (e.falta) {
      caja1.appendChild(el(grado || "h3", "t-red", "FALTA · " + e.falta));
      caja1.appendChild(el("p", "t-nodata", e.causa || ""));
      caja1.appendChild(el("p", "tenue", "remedio: " + (e.remedio || "")));
      return caja1;
    }
    var h = el(grado || "h3", null, e.termino);
    if (e.estado) {
      var s = el("span", "pilar-estado t-" + String(e.estado).toLowerCase(),
                 e.estado);
      h.appendChild(document.createTextNode(" "));
      h.appendChild(s);
    }
    caja1.appendChild(h);
    caja1.appendChild(el("p", null, e.que_hace || ""));
    if (e.nota) caja1.appendChild(el("p", "tenue", e.nota));
    if (e.donde_verlo) {
      // El comando va en <pre> y copiable: la regla de esta consola es que si
      // no hay comando que lo ensene, no es conocimiento. Enterrarlo en prosa
      // es la forma educada de no tenerlo.
      var pre = el("pre", "terminal", "$ " + e.donde_verlo);
      pre.tabIndex = 0;
      caja1.appendChild(pre);
    }
    if (e.fuente) caja1.appendChild(el("p", "tenue pilar-fuente", e.fuente));
    return caja1;
  }

  function seccion(titulo, nodos) {
    caja.appendChild(el("h3", "partida-rotulo", titulo));
    nodos.forEach(function (n) { caja.appendChild(n); });
  }

  fetch("/api/arranque").then(function (r) { return r.json(); }).then(function (d) {
    var p = d.cargar_partida;
    caja.innerHTML = "";
    if (!p || p.estado === "NO_DATA") {
      caja.appendChild(el("p", "t-red", "NO_DATA · " +
        ((p && p.causa) || "/api/arranque no trae cargar_partida")));
      if (p && p.remedio) caja.appendChild(el("p", "tenue", "remedio: " + p.remedio));
      return;
    }
    if (p.que_es) caja.appendChild(el("p", "tenue", p.que_es));

    seccion("Los cuatro pilares",
            (p.los_cuatro_pilares || []).map(function (e) { return entrada(e); }));

    // De donde vienes y a donde vas, juntos: la mision siguiente sin lo que ya
    // se hizo se relee como trabajo por hacer que ya esta hecho.
    seccion("De donde vienes", [entrada(p.de_donde_vienes)]);
    seccion("A donde vas", [entrada(p.a_donde_vas)]);

    // Lo que esa mision necesita tener delante. Va PEGADO a la mision y no en
    // las trampas: una pieza que ya existe y no se sabe que existe se
    // reconstruye, que es la forma cara de perder una sesion entera.
    if ((p.y_para_eso_lee || []).length) {
      seccion("Y para eso, lee",
              p.y_para_eso_lee.map(function (e) { return entrada(e); }));
    }

    // Las trampas van en <details> --y solo estas-- porque son muchas y no
    // hay que leerlas todas hoy: hay que saber que estan cuando algo muerda.
    caja.appendChild(el("h3", "partida-rotulo", "Lo que te va a morder"));
    (p.lo_que_te_va_a_morder || []).forEach(function (e) {
      var det = document.createElement("details");
      det.className = "glos";
      var sum = document.createElement("summary");
      sum.textContent = e.falta ? "FALTA · " + e.falta : e.termino;
      det.appendChild(sum);
      det.appendChild(entrada(e, "h4"));
      caja.appendChild(det);
    });
  }).catch(function (e) {
    caja.textContent = "NO_DATA · /api/arranque no contesto: " + e.message;
  });
})();
