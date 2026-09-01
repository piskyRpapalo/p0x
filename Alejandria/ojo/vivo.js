/* El Ojo-Vivo · V1 topologia. Sin frameworks y sin build.
 *
 * LA REGLA QUE MANDA EN ESTE FICHERO
 * ----------------------------------
 * Ninguna cifra, ninguna fase y ningun nombre de nodo se escribe aqui. Todo
 * valor visible sale de /api/rack, /api/fases, /api/identidad o /api/acta, y
 * lo que no venga se pinta NO_DATA con su causa. Un numero a mano en el
 * render es un sensor que miente sin que nadie lo note: el panel sigue
 * verde cuando el rack ya no lo esta.
 *
 * Lo que SI vive aqui es la TOPOLOGIA -- que cuarto va en que ala y de que
 * tribu es. Eso no es un dato medido: es el plano del refugio, y el plano lo
 * pone el contrato visual, no el recolector.
 *
 * FASE A: polling cada 60 s (plan_v5). SSE es FASE B y no esta aqui.
 */
"use strict";

var REFRESCO_MS = 60000;

/* --- utilidades de pintura ------------------------------------------- */

function el(tag, clase, texto) {
  var n = document.createElement(tag);
  if (clase) n.className = clase;
  if (texto !== undefined && texto !== null) n.textContent = String(texto);
  return n;
}

function icono(id) {
  var s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  s.setAttribute("class", "ic");
  s.setAttribute("aria-hidden", "true");
  var u = document.createElementNS("http://www.w3.org/2000/svg", "use");
  u.setAttribute("href", "#" + id);
  s.appendChild(u);
  return s;
}

/* NO_DATA es un valor de primera clase, no un hueco. Se pinta con su causa
   para que quien lo lea sepa si falta el sensor o falla la medida. */
function nodata(causa) {
  var s = el("span", "nodata", "NO_DATA");
  if (causa) s.title = causa;
  return s;
}

function fila(clave, valor, clase) {
  var d = el("div", "dato");
  d.appendChild(el("span", "k", clave));
  var v = el("span", "v" + (clase ? " " + clase : ""));
  if (valor === undefined || valor === null || valor === "") {
    v.appendChild(nodata("el recolector no dejo este campo escrito"));
  } else if (valor instanceof Node) {
    v.appendChild(valor);
  } else {
    v.textContent = String(valor);
  }
  d.appendChild(v);
  return d;
}

function sello(estado) {
  var e = estado || "NO_DATA";
  var c = e === "OK" ? "ok" : (e === "RED" ? "red" : "nodata");
  return el("span", "sello " + c, e);
}

function vaciar(n) { while (n.firstChild) n.removeChild(n.firstChild); }

/* --- EL PLANO DEL REFUGIO --------------------------------------------
 * Estructura, no medida: que cuarto, en que ala, de que tribu y que campos
 * del componente enseña. Los VALORES los pone estado.json.
 * Tribus: preceptor = compañeros y producto · hexelion = hardware y
 * sensores · core = enjambre y operaciones.
 */
var ALA_IZQ = [
  { comp: "memoria", titulo: "Memoria", tribu: "preceptor", ic: "i-memoria",
    campos: [["engramas", "engramas"], ["índice FTS", "fts"], ["ruta", "ruta"]] },
  { comp: "ollama", titulo: "Inferencia", tribu: "preceptor", ic: "i-chip",
    campos: [["compañeros", "modelos"], ["latencia", "latencia_ms", " ms"],
             ["backend", "backend"], ["residentes", "residentes"]] },
  { comp: "lora_v7", titulo: "Afinado", tribu: "preceptor", ic: "i-chip",
    campos: [["adaptadores", "adaptadores"]] },
  { comp: "mvp_gate", titulo: "Gate del MVP", tribu: "core", ic: "i-gate",
    campos: [["pasa", "pasa"], ["salta", "salta"], ["subtests", "subtests"]] },
  { comp: "enjambre", titulo: "Enjambre", tribu: "core", ic: "i-gate",
    agentes: true, campos: [] }
];

var ALA_DER = [
  { comp: "api_guia", titulo: "Ágora · API Guía", tribu: "preceptor", ic: "i-agora",
    campos: [["puerto", "puerto"], ["gestor", "gestor"],
             ["unidad", "unidad"], ["alcanzada en", "alcanzado_en"]] },
  { comp: "web_gate", titulo: "Gate de la web", tribu: "core", ic: "i-gate",
    campos: [["pasa", "pasa"]] },
  { comp: "repos", titulo: "Repos", tribu: "core", ic: "i-repo", arboles: true,
    campos: [["sin empujar", "pendientes_total"]] }
];

/* Longitud de una lista o valor tal cual: el recolector escribe unas veces
   un numero y otras la lista entera, y el render no debe inventarse cual. */
function medida(v, sufijo) {
  if (v === undefined || v === null) return null;
  if (Array.isArray(v)) return v.length ? v.length + (sufijo || "") : "ninguno";
  if (typeof v === "boolean") return v ? "sí" : "no";
  return String(v) + (sufijo || "");
}

/* Peor estado de un grupo. Un cuarto con tres agentes no tiene un `estado`
   propio en estado.json: lo tiene cada agente. Si uno esta en rojo, el
   cuarto esta en rojo -- promediar estados es como promediar temperaturas
   de un incendio y una nevera. */
function peor(lista) {
  if (!lista.length) return "NO_DATA";
  if (lista.indexOf("RED") >= 0) return "RED";
  if (lista.indexOf("NO_DATA") >= 0 || lista.indexOf("OK") < 0) return "NO_DATA";
  return "OK";
}

/* Un agente del enjambre es `Type=oneshot`: entre disparos esta `inactive` y
   ESE es su estado sano (decision 2 del Soberano). Por eso aqui se pinta el
   RESULTADO y la proxima cita, y no se pinta `is-active` en ninguna parte:
   es la propiedad que no informa, y pintarla fabrica rojos que no existen. */
/* V2 · la cara del agente. Tres estados y ni uno mas, porque tres son los que
   el dato distingue: OK, RED, y no lo se. El contrato visual hablaba de
   busy/stale/sleep; eso describe procesos que corren, y estos son `oneshot`
   que casi siempre estan parados y sanos. Se pinta lo medido. */
function mascara(estado) {
  if (estado !== "OK" && estado !== "RED") return null;   // sin dato: sin cara
  var ns = "http://www.w3.org/2000/svg";
  var svg = document.createElementNS(ns, "svg");
  svg.setAttribute("class", "mascara " + (estado === "OK" ? "ok" : "mal"));
  svg.setAttribute("aria-hidden", "true");
  var use = document.createElementNS(ns, "use");
  use.setAttribute("href", estado === "OK" ? "#i-mascara-ok" : "#i-mascara-mal");
  svg.appendChild(use);
  return svg;
}

function agente(nombre, a) {
  var v = el("span");
  var m = mascara(a.estado);
  if (m) {
    v.appendChild(m);
  } else {
    // El hueco se DIBUJA. Un espacio en blanco se lee como un fallo de
    // maquetado; un recuadro punteado y gris se lee como «aqui no hay medida».
    v.className = "sin-mascara";
    v.appendChild(el("i", "hueco-cara"));
  }
  v.appendChild(el("b", a.estado === "OK" ? "v ok" : "v red",
    a.resultado || a.estado || "NO_DATA"));
  v.appendChild(el("span", "entrega",
    (a.cadencia || "cadencia NO_DATA") + " · próxima " + (a.proxima || "NO_DATA")));
  // El bocadillo: lo que el bucle dijo de si mismo en su ultimo latido.
  if (a.nota_latido) v.appendChild(el("span", "bocadillo", a.nota_latido));
  return fila(nombre, v);
}

function cuarto(plano, comps) {
  var c = comps ? comps[plano.comp] : null;
  var estado = !c ? "NO_DATA" : (plano.agentes
    ? peor(Object.keys(c).map(function (k) { return c[k].estado; }))
    : c.estado);
  var art = el("article", "cuarto tribu-" + plano.tribu);
  var h = el("h3");
  h.appendChild(icono(plano.ic));
  h.appendChild(el("span", null, plano.titulo));
  h.appendChild(sello(estado));
  art.appendChild(h);
  var cuerpo = el("div", "cuerpo");

  if (!c) {
    cuerpo.appendChild(fila("componente", nodata(
      "estado.json no trae `" + plano.comp + "`; remedio: verificar_sesion.sh")));
    art.appendChild(cuerpo);
    return art;
  }
  if (c.causa) cuerpo.appendChild(fila("causa", c.causa, "red"));

  plano.campos.forEach(function (f) {
    cuerpo.appendChild(fila(f[0], medida(c[f[1]], f[2])));
  });

  if (plano.agentes) {
    Object.keys(c).forEach(function (nombre) {
      cuerpo.appendChild(agente(nombre, c[nombre]));
    });
  }

  /* Los repos son un mapa de arboles, no una lista de campos: cada arbol
     dice su rama y cuanto lleva sin empujar. */
  if (plano.arboles && c.arboles) {
    Object.keys(c.arboles).forEach(function (nombre) {
      var a = c.arboles[nombre];
      var sinPush = a.sin_push;
      cuerpo.appendChild(fila(nombre, a.rama + " · " + medida(sinPush) + " sin push",
        sinPush ? "red" : "ok"));
    });
  }
  art.appendChild(cuerpo);
  return art;
}

/* --- HUD -------------------------------------------------------------- */

function cifra(rot, valor, mala) {
  var s = el("span", "cifra" + (mala ? " mala" : ""));
  s.appendChild(el("span", "rot", rot));
  if (valor === undefined || valor === null) s.appendChild(nodata());
  else s.appendChild(el("b", null, valor));
  return s;
}

function pintarHud(d) {
  var c = d.componentes || {};
  var caja = document.getElementById("hud-cifras");
  vaciar(caja);
  var rojos = Object.keys(c).filter(function (k) { return c[k].estado === "RED"; }).length;
  var nd = Object.keys(c).filter(function (k) { return c[k].estado === "NO_DATA"; }).length;
  caja.appendChild(cifra("nodo", d.nodo));
  caja.appendChild(cifra("rojos", rojos, rojos > 0));
  caja.appendChild(cifra("no_data", nd, nd > 0));
  caja.appendChild(cifra("gate MVP", c.mvp_gate ? c.mvp_gate.pasa : null));
  caja.appendChild(cifra("gate web", c.web_gate ? c.web_gate.pasa : null));
  caja.appendChild(cifra("compañeros", c.ollama ? c.ollama.modelos : null));
}

function pintarFrescura(d) {
  var p = document.getElementById("frescura");
  var s = d.frescura_segundos;
  p.className = "frescura panel";
  if (s === null || s === undefined) {
    p.textContent = "NO_DATA · " + (d.causa || "sin sello de tiempo") +
      " · remedio: " + (d.remedio || "verificar_sesion.sh");
    p.classList.add("perdida");
    return;
  }
  var min = Math.floor(s / 60);
  var texto = min < 1 ? s + " s" : (min < 60 ? min + " min" : Math.floor(min / 60) + " h " + (min % 60) + " min");
  p.textContent = "Medido hace " + texto + " · modo " + (d.modo || "?") +
    " · generado " + (d.generado || "?");
  p.classList.add(s < 900 ? "fresca" : (s < 7200 ? "rancia" : "perdida"));
}

/* --- SUPERFICIE ------------------------------------------------------- */

function pintarCielo(c) {
  var art = document.getElementById("c-tailnet");
  var cuerpo = art.querySelector(".cuerpo");
  vaciar(cuerpo);
  var h = art.querySelector("h3");
  var viejo = h.querySelector(".sello");
  if (viejo) h.removeChild(viejo);
  var t = c.tailscale;
  h.appendChild(sello(t ? t.estado : "NO_DATA"));
  if (!t) {
    cuerpo.appendChild(fila("tailnet", nodata("estado.json no trae `tailscale`")));
    return;
  }
  cuerpo.appendChild(fila("en línea", medida(t.online) + " de " + medida(t.total),
    t.online ? "ok" : "red"));
  /* Los nombres de los nodos se pintan; sus direcciones NO. La tabla de
     direcciones de la tailnet esta en D8_JAMAS y el guardia de higiene la
     rechaza sin excepcion -- tampoco dentro de una consola de loopback. */
  cuerpo.appendChild(fila("despiertos", (t.nodos_online || []).join(" · ")));
  cuerpo.appendChild(fila("dormidos", (t.nodos_offline || []).join(" · ")));
}

/* --- SOTANO ----------------------------------------------------------- */

function barra(pct) {
  var b = el("div", "barra");
  var i = el("i");
  i.style.width = Math.max(0, Math.min(100, pct)) + "%";
  if (pct >= 90) i.className = "mala"; else if (pct >= 70) i.className = "tibia";
  b.appendChild(i);
  return b;
}

function pintarSotano(c) {
  var caja = document.getElementById("sotano-cuerpo");
  vaciar(caja);

  var disco = el("article", "cuarto tribu-hexelion");
  var hd = el("h3");
  hd.appendChild(icono("i-disco"));
  hd.appendChild(el("span", null, "Disco del nodo"));
  hd.appendChild(sello(c.disco ? c.disco.estado : "NO_DATA"));
  disco.appendChild(hd);
  var cd = el("div", "cuerpo");
  if (c.disco && c.disco.total_gb) {
    var usado = c.disco.total_gb - c.disco.libre_gb;
    cd.appendChild(fila("libre", c.disco.libre_gb + " GB de " + c.disco.total_gb + " GB"));
    cd.appendChild(barra(100 * usado / c.disco.total_gb));
  } else {
    cd.appendChild(fila("disco", nodata("estado.json no trae `disco`")));
  }
  disco.appendChild(cd);
  caja.appendChild(disco);

  var puertos = el("article", "cuarto tribu-core");
  var hp = el("h3");
  hp.appendChild(icono("i-candado"));
  hp.appendChild(el("span", null, "Puertos"));
  hp.appendChild(sello(c.puertos ? c.puertos.estado : "NO_DATA"));
  puertos.appendChild(hp);
  var cp = el("div", "cuerpo");
  if (c.puertos) {
    if (c.puertos.causa) cp.appendChild(fila("causa", c.puertos.causa, "red"));
    cp.appendChild(fila("escuchando", medida(c.puertos.total)));
    cp.appendChild(fila("fuera de loopback", medida(c.puertos.expuestos),
      c.puertos.expuestos ? "red" : "ok"));
    cp.appendChild(fila("huérfanos", medida(c.puertos.huerfanos)));
  } else {
    cp.appendChild(fila("puertos", nodata("estado.json no trae `puertos`")));
  }
  puertos.appendChild(cp);
  caja.appendChild(puertos);

  var doogee = el("article", "cuarto tribu-hexelion");
  var hg = el("h3");
  hg.appendChild(icono("i-chip"));
  hg.appendChild(el("span", null, "Doogee"));
  hg.appendChild(sello(c.doogee ? c.doogee.estado : "NO_DATA"));
  doogee.appendChild(hg);
  var cg = el("div", "cuerpo");
  cg.appendChild(fila("conexión", c.doogee ? c.doogee.conexion : null));
  /* La RAM por nodo del rack NO se pinta: el recolector no la mide todavia.
     Dibujar una barra sin fuente es exactamente el defecto que el contrato
     llama «numero escrito a mano». */
  cg.appendChild(fila("RAM por nodo", nodata(
    "el recolector no mide RAM de nodos remotos; remedio: anadir el sensor")));
  doogee.appendChild(cg);
  caja.appendChild(doogee);
}

/* --- CENTRO: el Acta y el compañero ----------------------------------- */

function pintarActa(d) {
  var cuerpo = document.querySelector("#c-acta .cuerpo");
  vaciar(cuerpo);
  if (!d || d.estado !== "OK") {
    cuerpo.appendChild(fila("acta", nodata(d ? d.causa : "sin respuesta")));
    return;
  }
  cuerpo.appendChild(fila("cadena", d.cadena_sana ? "sana" : "ROTA",
    d.cadena_sana ? "ok" : "red"));
  var ms = (d.mensajes || []).slice(-3).reverse();
  cuerpo.appendChild(fila("mensajes", (d.mensajes || []).length));
  ms.forEach(function (m) {
    var caja = el("div", "msg");
    caja.appendChild(el("span", "de " + (m.de || ""), m.de || "?"));
    caja.appendChild(el("span", " ", " " + (m.ts || "")));
    caja.appendChild(el("p", "humano", m.humano || ""));
    cuerpo.appendChild(caja);
  });
}

function pintarCompanero(d) {
  var cuerpo = document.querySelector("#c-companero .cuerpo");
  vaciar(cuerpo);
  cuerpo.appendChild(fila("por defecto", d && d.por_defecto));
  cuerpo.appendChild(fila("elegido", d && d.elegido ? d.elegido :
    nodata(d ? d.causa : "sin respuesta")));
  var p = el("p", "prosa", d && d.nota ? d.nota : "");
  cuerpo.appendChild(p);
}

/* --- MARGEN: fases e identidad ---------------------------------------- */

function claseEstado(e) {
  var t = (e || "").toLowerCase();
  if (t.indexOf("curso") >= 0) return "curso";
  if (t.indexOf("hecha") >= 0 || t.indexOf("cerrada") >= 0) return "hecha";
  return "pend";
}

function pintarFases(d) {
  var cuerpo = document.querySelector("#p-fases .cuerpo");
  vaciar(cuerpo);
  if (!d || d.estado !== "OK" || !d.fases) {
    cuerpo.appendChild(fila("fases", nodata(d ? d.causa : "sin respuesta")));
    if (d && d.remedio) cuerpo.appendChild(fila("remedio", d.remedio));
    return;
  }
  d.fases.forEach(function (f) {
    var caja = el("div", "fase");
    caja.appendChild(el("b", null, f.nombre));
    caja.appendChild(el("span", "est " + claseEstado(f.estado), " " + (f.estado || "")));
    caja.appendChild(el("span", "entrega", f.entrega || ""));
    cuerpo.appendChild(caja);
  });
  cuerpo.appendChild(el("p", "prosa", "Fuente: " + (d.fuente || "?")));
}

function pintarIdentidad(d) {
  var cuerpo = document.querySelector("#p-identidad .cuerpo");
  vaciar(cuerpo);
  if (!d || d.estado !== "OK") {
    cuerpo.appendChild(fila("identidad", nodata(d ? d.causa : "sin respuesta")));
    if (d && d.remedio) cuerpo.appendChild(fila("remedio", d.remedio));
    return;
  }
  var i = d.identidad || {};
  Object.keys(i).forEach(function (k) {
    var v = i[k];
    if (Array.isArray(v)) {
      cuerpo.appendChild(fila(k, v.length ? v.join(" · ") : "ninguna"));
      return;
    }
    if (/^https?:/.test(String(v))) {
      var a = el("a", null, String(v));
      a.href = v; a.rel = "noreferrer noopener"; a.target = "_blank";
      cuerpo.appendChild(fila(k, a));
      return;
    }
    cuerpo.appendChild(fila(k, v));
  });
  cuerpo.appendChild(el("p", "prosa",
    "Lo que el Soberano publica de si mismo. Sale de identidad_publica.json: " +
    "si aqui aparece algo que no deberia ser publico, el fichero es el sitio " +
    "donde se quita, no esta pantalla."));
}

/* --- ciclo ------------------------------------------------------------ */

function traer(ruta) {
  return fetch(ruta, { cache: "no-store" })
    .then(function (r) { return r.json(); })
    .catch(function (e) {
      return { estado: "NO_DATA", causa: "no se pudo leer " + ruta + ": " + e,
               remedio: "¿esta vivo ojo.py?" };
    });
}

function refrescar() {
  traer("/api/rack").then(function (d) {
    pintarFrescura(d);
    if (d.estado === "NO_DATA") return;
    var c = d.componentes || {};
    pintarHud(d);
    pintarCielo(c);
    var izq = document.getElementById("ala-izq");
    var der = document.getElementById("ala-der");
    vaciar(izq); vaciar(der);
    ALA_IZQ.forEach(function (p) { izq.appendChild(cuarto(p, c)); });
    ALA_DER.forEach(function (p) { der.appendChild(cuarto(p, c)); });
    pintarSotano(c);
    seleccionable();          // los cuartos nuevos tambien se pueden mirar
  });
  traer("/api/acta").then(pintarActa);
  traer("/api/fases").then(pintarFases);
  traer("/api/identidad").then(pintarIdentidad);
  traer("/api/companero").then(pintarCompanero);
}

refrescar();
setInterval(refrescar, REFRESCO_MS);

/* --- V2 · la seleccion ---------------------------------------------------
   El anillo del contrato visual no servia de nada mientras nada pudiera
   recibirlo: `.cuarto:focus-visible` y `.cuarto.sel` estaban en la hoja y
   ningun cuarto era enfocable, asi que era CSS que no podia aparecer jamas.

   Se resuelve con `tabindex` en vez de con un manejador de teclas propio: el
   navegador ya sabe recorrer, y reimplementar las flechas seria romper el
   recorrido que quien usa un lector de pantalla ya tiene aprendido. El clic
   solo marca; NO abre nada, porque el Ojo no ejecuta -- ninguna puerta se abre
   sin la palabra del Soberano, y eso vale tambien para su consola. */
var SELECCIONADO = null;

function seleccionable() {
  // IDEMPOTENTE a proposito: `refrescar()` reconstruye las alas cada ciclo,
  // asi que esto corre una y otra vez sobre los cuartos fijos del marcado. Sin
  // la marca, cada pasada colgaria otro par de oyentes sobre los mismos nodos
  // y en una hora habria cientos. Una fuga de memoria lenta en una consola que
  // se deja abierta todo el dia es justo la que nadie atribuye a su causa.
  Array.prototype.forEach.call(document.querySelectorAll(".cuarto"), function (c) {
    if (c.dataset.selEnchufado) return;
    c.dataset.selEnchufado = "1";
    if (!c.hasAttribute("tabindex")) c.setAttribute("tabindex", "0");
    c.addEventListener("click", function () { marcar(c); });
    c.addEventListener("focus", function () { marcar(c); });
  });
  // La seleccion sobrevive al repintado. Los cuartos de las alas se destruyen
  // y se crean de nuevo cada ciclo: sin esto, el anillo se caeria solo cada
  // pocos segundos y quien estuviera mirando un cuarto lo perderia sin tocar
  // nada.
  if (SELECCIONADO) {
    var vuelto = document.getElementById(SELECCIONADO);
    if (vuelto) vuelto.classList.add("sel");
  }
}

function marcar(cual) {
  Array.prototype.forEach.call(document.querySelectorAll(".cuarto.sel"),
    function (c) { if (c !== cual) c.classList.remove("sel"); });
  cual.classList.add("sel");
  SELECCIONADO = cual.id || null;
}
