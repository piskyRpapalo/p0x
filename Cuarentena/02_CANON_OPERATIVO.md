---
id: canon-operativo-reestructura
titulo: Canon operativo de la reestructuración de p0x
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "cero escrituras en silver/gold sin esquema validado; cero afirmaciones sin evidencia en disco en los POST_VERIFICACION"
umbral_reedicion: "dos rondas consecutivas con hallazgos que este canon no sepa clasificar"
presupuesto_kb: 20
n_medicion: 2
changelog:
  - "v1.0.0 (2026-08-10, propuesta del Preceptor; canoniza el Soberano): nace del filtrado de dos informes externos y del prompt de Cowork del Soberano. Cambios frente a esos insumos: (a) el filtro de borde deja de llamarse Aurelius; (b) se desambigua bronce/plata/oro documental frente a datos; (c) se elimina MQTT como supuesto; (d) se secuencian las rondas."
actualizado: 2026-08-10
---

# CANON OPERATIVO DE LA REESTRUCTURACIÓN
### Lo que rige mientras p0x se ordena. Deriva del suelo de P0X; no lo sustituye.

---

## §0 · HERENCIA DEL SUELO (no se enmienda aquí)

1. **IronClaw.** Ningún bucle autónomo firma valor. El humano cierra cada bucle de valor y tiene acceso visual al dato con el que firma.
2. **Soberanía del dato.** Todo local. El Soberano lee, exporta, corrige o borra cuando quiera.
3. **Sensores honestos.** La ausencia se declara. `NO_DATA` no es cero, no es null implícito, no es el último valor conocido.
4. **Grounding.** Solo se cita lo que está literalmente en disco. Inventar un estado, una ruta o una medición es la peor violación posible.
5. **Honestidad sin hype.** Dato real sobre teatro. Un objetivo de diseño no es una medición.

## §1 · MEDALLÓN (capas de DATO)

| Capa | Rol | Regla dura |
|---|---|---|
| **bronze** | Ingesta cruda | Inmutable, append-only, idempotente. Cero lógica de negocio. Se guarda tal como llegó, incluso si llegó mal. |
| **silver** | Limpieza | Tipado, validado contra esquema, deduplicado. Ninguna escritura sin esquema. |
| **gold** | Consumo | Agregado, listo para dashboard o producto. **Todo gold debe poder reconstruirse desde bronze.** Si no puede, no es gold. |

**Regla de paso:** una capa nunca lee de dos capas por debajo. Silver lee bronze; gold lee silver. El dashboard lee gold (y, provisionalmente y declarándolo, silver).

**Métricas de calidad:** "cero escrituras inválidas" y "bajo overhead" son **objetivos de diseño**, no resultados. Mientras no exista contador, se escribe `NO_DATA`.

### §1.1 · Desambiguación obligatoria (colisión real detectada)

En el corpus de P0X existen ficheros que usan **bronce / plata / oro como niveles de profundidad documental** (fundamentos → detalle → experto). Eso choca de frente con las capas de dato y confundirá a cualquier agente que busque por esas palabras.

**Regla:** bronze/silver/gold quedan reservados **exclusivamente** para el ciclo de vida del dato, bajo `datos/`. La profundidad documental usa el vocabulario que ya existe en el canon de P0X: `basico | medio | experto`. Ningún documento nuevo usa metales para hablar de profundidad.

## §2 · LA ADUANA (el filtro de borde)

El componente que decide qué entra al sistema se llama **la Aduana** (`aduana`).

**No se llama Aurelius.** Aurelius es el preceptor local del Soberano — un producto pedagógico con su propio repositorio, su modelo y su doctrina. Colgarle además el papel de portero de datos garantiza que, dentro de seis meses, ni un humano ni un modelo sepan de cuál de los dos se está hablando al leer una línea de log. El *canon* de honestidad se conserva entero; solo cambia la etiqueta del componente.

*(El ID `aduana` queda reservado. No entra en el Alfabeto hasta que el componente exista en disco: la regla de admisión exige que el ID nombre algo real.)*

**Qué es la Aduana:**
- **Determinista. Cero LLM.** Validación contra esquema, rangos, tipos, deduplicación por hash. Un modelo de lenguaje decidiendo qué dato entra es exactamente el fallo que este diseño existe para evitar.
- **Bloqueante.** Una comprobación que detecta y no bloquea no es una comprobación. Payload inválido → no entra a bronze: va a `rechazados/` con motivo y timestamp.
- **Trazable.** Todo rechazo se conserva. Un rechazo silencioso es peor que un dato sucio.

**Qué ahorra** (y solo se afirma con medición): cómputo, almacenamiento, transmisión, tiempo humano, repeticiones. Sin contador → `NO_DATA`.

**Estado actual:** la Aduana no existe. Cualquier documento que hable de "el filtro Edge funcionando" describe una aspiración. Se declara `NO_DATA` y se propone su forma mínima.

## §3 · TAXONOMÍA DOCUMENTAL

Cada documento de la cuarentena recibe **una clasificación** y **una acción**.

**Clasificación:** `UTIL_DOCTRINA` · `UTIL_OPERATIVO` · `UTIL_HISTORICO` · `RUIDO` · `EXTERNO_NO_VERIFICADO` · `CONTRADICE_FIRMADO` · `OBSOLETO` · `NO_DATA` · `SECRETO_POSIBLE`

**Acción:** `EXTRAER` · `CONSOLIDAR` · `ARCHIVAR` · `NO_USAR` · `REVISAR_SOBERANO`

**Criterio de `EXTERNO_NO_VERIFICADO`:** un documento que apoya sus afirmaciones en enlaces web, redes sociales, blogs o foros. Su **estructura** puede aprovecharse (una matriz de auditoría es una matriz de auditoría venga de donde venga); su **autoridad**, no. Se extrae la forma y se descarta la cita.

## §4 · ORDEN DE TRABAJO INNEGOCIABLE

```
0. Verificar acceso, estado y documentos
1. Barrido de software residual
2. Estructura modular Medallón
3. Conectar los datos que YA funcionan
4. Arreglar lo roto
5. Pulido visual — solo con orden explícita
```

**No se salta el orden. No se empieza por lo visual. No se abre un frente nuevo si hay uno roto bloqueando valor real.**

**Heurística de prioridad:** *qué, cerrado, desbloquea más con menos construcción.* No se prioriza lo bonito ni lo interesante: lo que produce uso real, verificación real o desbloqueo real.

## §5 · SUPUESTOS PROHIBIDOS

Estos aparecen en los informes externos y **no son canon**. Nombrarlos como si lo fueran es una violación de grounding:

- **MQTT** como transporte de sensores. No verificado, no firmado. Ningún plan lo asume.
- **RAG local** en gold. Aparcado.
- **Multiusuario por ID / carpetas por persona.** Aparcado.
- **Mesh, Azure, capa "Platinum", contenedores para terceros, impresora 3D, bombas.** Aparcados.
- **Vulnerabilidades concretas de herramientas de IA** citadas desde la web. No verificables desde aquí → `EXTERNO_NO_VERIFICADO`. La mitigación real no es citar un CVE: es que la herramienta no tenga permiso de escritura fuera de su carpeta.

## §6 · HIGIENE Y SECRETOS

- IPs de tailnet, hostnames, rutas con nombre de usuario, claves y tokens: **`[SECRETO]`**, nunca transcritos.
- Una URL que lleve un parámetro tipo `?key=…`, `?token=…` o similar **es un secreto**, aunque venga dentro de una cita bibliográfica. Se reporta y no se copia.
- Ningún documento de esta carpeta se publica ni se sube a un repositorio público sin una pasada de limpieza firmada.

## §7 · DEFINICIONES

- **ACTIVE** — vivo, útil, verificable, alineado con la arquitectura actual.
- **DEPRECATED** — ya no se usa, pero tiene valor histórico o de reversión. **Se archiva, no se borra.**
- **BASURA** — accidental, temporal o inequívocamente inútil: cachés, logs temporales, duplicados muertos, artefactos generados por error. Solo se elimina tras firma.
- **NO_DATA** — ausente, no verificado, no disponible. Se declara.
- **RUIDO** — no ayuda a decidir ni a ejecutar.
- **SECRETO_POSIBLE** — puede contener credenciales. No se transcribe.

---

> **Cierre.** Este documento es clase=doctrina: un agente puede proponer enmendarlo con motivo y changelog. Solo el Soberano lo canoniza, y lo canoniza con un commit.
