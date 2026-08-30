# PLAN v5 · CONTRATO VISUAL Y DE PRIORIDADES (OJO-VIVO + PRODUCTO)
Capa Alejandria: tope 32 KB/fichero. Loopback 127.0.0.1. Cero frameworks.

TOPOLOGIA (corte transversal): SUPERFICIE (cupula+sensores HEXELION) /
ALAS (MVP izq, WEB der) + CENTRO piramidal (EL OJO: ojo+busto+Acta+chat del
companero) / SOTANO (hardware medido). HUD lee estado.json; sidebar lee
Alejandria/fases.json. Nada hardcodeado; lo contrario es defecto del render.

ESTADOS: mascara=estado (verde=busy, rojo=stale, sin mascara+gris=sleep),
borde=tribu, mobiliario=ubicacion. Movimiento atado a anclas (sleep=cama,
busy=objeto de trabajo, stale=congelado).

TRIBUS: PRECEPTOR=violeta (companeros/producto) · HEXELION=phosphor
(hardware/sensores) · P0X-CORE=bronce (enjambre/ops). Marmol=cromo del Ojo.
Iconos ya existen en el Beelink: reutilizar, crear solo lo que falte.

PIPELINE: FASE A polling estado.json 60s; FASE B SSE despues.
PRESUPUESTO: sprite ~2,5KB+mascaras ~400B; sacrificio: mobiliario primero,
nunca mascaras/chat/pipeline.

FASES VISUALES: V0=mockup actual (no se tira) · V1 topologia · V2 estados
humanos · V3 mobiliario · V4 superficie+centro vivo. Una commiteable c/u.

PISTA PRODUCTO (flujo antes que forma en lo publico):
1 Terminologia · 2 Guion Instalador+pares v8 · 3 Onboarding 1 pantalla/2 caminos
· 4 Contrato agentes+QR+sprite · 5 Ojo-Vivo V1-V4 (paralelo, capa interna) ·
6 Identidad publica · 7 Tooltips+dataset.html+cURL · 8 Compresion T.papel.

TERMINOLOGIA: producto=PreceptorOS (nunca aurelius) · voz=Preceptor ·
memoria (no Cahier) · usuario elige "companero" (nunca modelo/LoRA) ·
filtro="el que tacha lo privado" · PC="fichero de doble clic" ·
Android hoy=Termux, APK declarado futuro · vinculacion="codigo de vinculacion".

DEUDA FIRMADA: renombrar empaquetado/guias aurelius→preceptoros · renombrar
selector MOA (Creador→Escritor, Guia repartido) · identidad_publica.json.

REGLAS: un commit por fase · gate verde antes/despues · sin push hasta
"Empuja a produccion" · reporte por fase (navegador, peso vs tope, NO_DATA).

---

# ANEXO VISUAL (firmado 2026-08-30)

R-WIDGET: todo texto visible vive en un panel con --panel-bg y --panel-fg
declarados, contraste >= 4.5:1. Texto flotando sobre el fondo = defecto de
render. Rige la web publica Y el Ojo.

R-TIPOGRAFIA: dos niveles, cero fuentes externas.
 DISPLAY serif local: "Iowan Old Style","Palatino Linotype",Palatino,
 "URW Palladio L","Book Antiqua",Georgia,"DejaVu Serif",serif
 -> titulos, heroes y prosa humana.
 ui-monospace sin cambio -> datos, logs, HUD, tooltips.

OJO-VIVO · recetas V1-V4
 TOPOLOGIA por filas: SUPERFICIE (cielo, cupula, sensores HEXELION) / ALAS
 (MVP izq, WEB der) + CENTRO piramidal (clip-path o bordes en angulo; ojo +
 busto + pergamino del Acta + chat del companero activo, Instalador por
 defecto) / SOTANO (hardware con barras medidas).
 ESTADOS: la MASCARA es el estado (dos <symbol> ok/bad; sleep sin mascara y
 grayscale), el BORDE es la tribu, el MOBILIARIO es la ubicacion. Bocadillo
 de log con a.log; anillo de seleccion outline 2px var(--sol).
 MOVIMIENTO semantico: sleep junto a la cama, busy junto a su objeto de
 trabajo, stale congelado. requestAnimationFrame, translate.
 HUD y FASES de estado.json y Alejandria/fases.json. Todo numero o fase
 escrita a mano = defecto del render. Cero emojis: <symbol> del sprite.
 PRESUPUESTO: sprite ~12 simbolos ~2,5 KB + mascaras ~400 B; agentes como div
 con box-shadow. Sacrificio: mobiliario primero, luego superficie; NUNCA
 mascaras, chat ni pipeline. Tope 32 KB/fichero.
 image-rendering: pixelated; shape-rendering="crispEdges"; viewBox 16x16 o
 24x24; rellenos con currentColor y variables de tribu.
 Iconos de hexelion/preceptoros/agentes YA existen en el Beelink: reutilizar.
 Un commit por fase V1-V4, gate verde antes y despues, reporte por fase.

FIRMA s0 (cierra la pregunta del acta): sensor de ausencia CORRECTO. Se
mantiene NO_DATA «especificado, no construido». No es bug del detector.

EL CENTRO: donde el Soberano habla con su Instalador. El silicio pinta el
refugio; el carbono lo habita.
