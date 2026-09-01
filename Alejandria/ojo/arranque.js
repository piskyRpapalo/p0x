/* El arranque de sesion, pintado para quien abre esta consola.

   ESTA PAGINA ES PARA UNA IA. El Ojo-Vivo (/vivo) es el juego, para una
   persona; esto es informacion en lenguaje de maquina: reglas, fronteras,
   recursos y rutas. Por eso aqui no hay dibujos, ni animacion, ni color que
   signifique algo que el texto no diga tambien.

   Y NO SE ESCRIBE NADA A MANO. Todo sale de /api/arranque, que a su vez
   compone arranque.json, recursos.json y las aristas `no_es` de grafo.json.
   Una frontera copiada en el HTML seria una segunda verdad sobre el mismo
   hecho: el dia que cambie el mapa, la copia mentiria y nadie lo notaria. */
(function () {
  "use strict";
  var caja = document.getElementById("ia-cuerpo");
  if (!caja) return;

  function bloque(titulo, texto) {
    var h = document.createElement("h3");
    h.textContent = titulo;
    var p = document.createElement("pre");
    p.className = "terminal";
    p.textContent = texto;
    caja.appendChild(h); caja.appendChild(p);
  }

  fetch("/api/arranque").then(function (r) { return r.json(); }).then(function (d) {
    caja.innerHTML = "";
    var a = d.lee_esto_primero || {};

    // 1 · QUE CEREBRO ERES. Va primero porque decide si puedes tocar canon.
    var c = d.cerebro || {};
    bloque("cerebro", "P0X_BRAIN=" + (c.P0X_BRAIN || "<no puesto>") +
                      "\n" + (c.eres || "NO_DATA"));

    // 2 · LAS FRONTERAS. Antes que las reglas: confundir dos productos no se
    //     arregla siguiendo bien una regla, se arregla no confundiendolos.
    var f = d.fronteras_que_no_se_cruzan;
    bloque("fronteras que no se cruzan", Array.isArray(f)
      ? f.map(function (x) {
          return x.esto + "  !=  " + x.no_es + "\n    " + x.por_que;
        }).join("\n\n")
      : "NO_DATA · " + ((f && f.causa) || "sin grafo"));

    // 3 · LAS REGLAS, con su comando: una regla sin forma de comprobarla es
    //     una creencia, y este rack no publica creencias.
    var reglas = a.las_seis_reglas_que_mas_se_rompen || [];
    bloque("reglas que mas se rompen", reglas.map(function (r) {
      return r.regla + "\n    " + r.por_que + "\n    $ " + (r.comando || "");
    }).join("\n\n"));

    // 4 · QUE TIENES A MANO. Solo el titular y su estado: el detalle entero
    //     vive en /api/recursos, y repetirlo aqui seria peso sin dato nuevo.
    var rec = (d.lo_que_tienes_a_mano || {}).recursos || [];
    bloque("recursos", rec.map(function (r) {
      return r.estado.padEnd(8) + " " + r.recurso;
    }).join("\n") + "\n\n(el detalle y los comandos: GET /api/recursos)");

    // 5 · EL PULSO. Lo unico de esta pagina que caduca.
    var w = (d.rack_ahora || {}).consumo_w || {};
    var o = (d.rack_ahora || {}).ollama_vivo || {};
    bloque("rack ahora", "consumo_w  " + (w.estado === "MEDIDO"
        ? w.valor + " W" : "NO_DATA · " + (w.causa || "")) +
      "\nmodelos    " + (o.estado === "OK" ? (o.nombres || []).join(", ")
                                           : "NO_DATA · " + (o.causa || "")));

    bloque("rutas", (a.primer_comando || "") +
      "\nGET /api/arranque   esto mismo, en JSON" +
      "\nGET /api/recursos   que tienes a mano, y como se comprueba" +
      "\nGET /api/grafo      el mapa de productos: nodos, aristas, fronteras" +
      "\nGET /api/rack       snapshot + consumo_w y ollama_vivo EN VIVO" +
      "\nGET /api/glosario   que significa la jerga del panel" +
      "\n/vivo               el Ojo-Vivo: el juego, para una persona");
  }).catch(function (e) {
    caja.textContent = "NO_DATA · /api/arranque no contesto: " + e.message;
  });
})();
