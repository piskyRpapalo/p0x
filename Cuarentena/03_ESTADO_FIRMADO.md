---
id: estado-firmado-ronda
titulo: Estado firmado y frentes aparcados
tipo: operativo
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
caduca: 2026-09-10
actualizado: 2026-08-10
---

# ESTADO FIRMADO
### Punto de partida, no verdad verificada. Ante duda, se comprueba en disco.

> **Regla de caducidad.** Pasada la fecha `caduca`, este documento deja de ser punto de partida y todo su contenido pasa a `NO_DATA` hasta que el Soberano lo refresque. Un estado sin fecha es una mentira con retraso.
>
> **Regla de origen.** Lo marcado *(informado)* lo dijo el Soberano y **no está verificado en disco**. Un agente no puede citarlo como hecho medido; puede citarlo como declaración del Soberano.

---

## §1 · DECISIONES FIRMADAS

| ID | Decisión |
|---|---|
| **D1** | `CineK_Studio` es el repositorio oficial de CineK. `cinek_automatico` queda archivado. |
| **D2** | Corrección hacia adelante para el riesgo de `config.py`. No se reescribe historia. Revisar/rotar sensibles si aplica. |
| **D3** | Dashboard v2 oficial en `hexelion/dashboard`, servido en `localhost:5173/ui/`. El entorno `:8001` queda descartado hasta nueva decisión. |
| **D4** | Push del commit `35b2553` autorizado tras revisión de diff. Push normal, nunca forzado. |
| **D5** | `planta_brote.webp` autorizado como placeholder provisional. No cuenta como foto real elegida por K. |
| **D6** | K firma Gold en Herbier **cuando entienda que firma**. Hasta entonces no se declara Gold firmado por K. |
| **D7** | Anclaje pospuesto hasta que el dashboard MVP esté funcional. |

## §2 · ESTADO TÉCNICO *(informado por el Soberano · no verificado)*

- Historial local limpiado por reset a origen y cherry-pick selectivo. Basura eliminada del historial antes del push.
- Dos commits anclados: estructura NFC + datos tomate-cherry, y `plantas.ts` conectado a JSON reales.
- Guardia pre-push validó integridad. Push a `origin/nexo-carbono-dashboard-20260623` correcto; rama sincronizada.
- Estructura NFC plug-and-play lista. Pegatinas NFC probadas con el móvil de K y funcionan. **Tags NFC físicos pendientes.**
- Datos mínimos creados: `tomate-cherry.json`, medallón de K, Aurelius hermano.
- Herbier: estructura de datos lista; UI necesita anclarse. **Widgets del dashboard pendientes.**
- ESP32 con sensores funcionando, pero **sus datos no están en el dashboard**.
- Cámara en el Vigía funcional.
- P (hermano del Soberano) probó Aurelius desde España y funcionó. Creación de su perfil **aparcada** para esta ronda.
- J y A: usuarios potenciales futuros. `NO_DATA`.

## §3 · FUENTES DECLARADAS PARA VERIFICACIÓN DE BORDE

| Nombre declarado | Resolución | Estado |
|---|---|---|
| `axl345` | Muy probablemente **ADXL345** (acelerómetro I2C). **No se corrige por cuenta propia.** | `PENDIENTE_CONFIRMACION` |
| `apklvsr` | **No resoluble.** No corresponde a ningún dispositivo conocido del inventario. | **`NO_DATA` — bloquea** |
| `bme680` | BME680 (temperatura, humedad, presión, gas). | `PENDIENTE_VERIFICACION_EN_DISCO` |
| `camara` | Cámara en el nodo Vigía. Modelo e interfaz sin declarar. | `PENDIENTE_VERIFICACION_EN_DISCO` |

**Regla:** ningún agente adivina qué es `apklvsr`, ni lo sustituye por el dispositivo que le parezca más plausible. Mientras no lo confirme el Soberano, la verificación de borde está **BLOQUEADA** y así debe reportarse.

**Forma de la verificación** — por cada fuente, cinco campos y nada más:
`existe` · `visible por la Aduana` · `esquema definido` · `última medición real` · `estado: OK / NO_DATA / ERROR / BLOQUEADO`

Un agente documental **no puede ver un sensor**. Solo puede ver el rastro que un sensor deja en disco: un fichero, un log, una línea de telemetría con timestamp. Si no hay rastro, la respuesta correcta es `NO_DATA`, y eso es un resultado válido y útil — no un fracaso de la ronda.

## §4 · FRENTES APARCADOS (no se proponen, no se planifican, no se mencionan como próximos pasos)

Proyecto Custodia · mesh · multiusuario por ID · impresora 3D · métricas energéticas (hasta que haya enchufes inteligentes) · bombas de agua y cajas hexelion · contenedor Docker para P o Raspberry Pi · RAG local · MQTT como canon.

## §5 · PERSONAS

- **K** — no escribe código. Copia enlaces y busca carpetas. Toda solución para K es manual, simple y verificable sin terminal. Tiene autoridad sobre los datos de su jardín; el control técnico por ID se aplaza. Firma Gold en Herbier cuando entienda qué firma.
- **Soberano** — firma decisiones, revisa diffs, autoriza push, decide prioridades, decide borrado o archivado.
- **Claude Code** — mide, construye, commitea, prepara. No publica, no fuerza, no declara canon, no ejecuta lo irreversible sin firma.

## §6 · OBJETIVO POSTERIOR (declarado, NO para esta ronda)

Cuando Le Jardin tenga CineK o Herbier activo y Aurelius sus partes funcionales, la prioridad será construir herramientas locales para Aurelius y usarlo de verdad. **No se construye ahora. No se abre ese frente.**

## D8 · VISIBILIDAD DE RED PARA COWORK (firmado 2026-08-11)
- Las IPs tailnet y LAN son visibles para Cowork: necesarias para proponer arquitectura y filtro Edge real.
- Las keys (JWT, tokens, contraseñas, URLs firmadas) son secreto: nunca se transcriben a POST_VERIFICACION.
- Token JWT de "Del Barrido al Borde" declarado quemado (viajó a Qwen/Claude/Gemini).
- El Soberano sigue siendo human-in-the-loop: firma toda acción irreversible.
- Las IPs son pasajeras; los métodos de defensa cambiarán; la doctrina no.

## VERIFICACIÓN RAÍZ P0X (2026-08-11)
- Escaneo de keys en toda la raíz p0x (excluyendo Cuarentena, .git, node_modules, dist): dos coincidencias.
- Ambas en /home/pisky/p0x/deploy/comun/hooks/test_guardia.py, líneas 90 y 92.  # guardia:permitir ruta-local-documentacion-D8
- Confirmado como fixtures de test (tuplas de casos de prueba con etiqueta TOKEN-PROVEEDOR).
- AKIAIOSFODNN7EXAMPLQ es el placeholder literal de la documentación AWS.  # guardia:permitir placeholder-AWS-D10
- Decisión: ignorar. No son credenciales vivas. Se declaran en POST_VERIFICACION_R00 como datos de test verificados.
- Pre-check de la raíz: VERDE. Cero keys reales.

## D9 · CANON BLUEPRINT (2026-08-11)
- v1.3.0 (raíz) sigue siendo canon hasta que v1.5 sea firmado.
- v1.4 (Cuarentena) queda declarado borrador histórico sin autoridad.
- Se redactará v1.5 grounded en el estado verificado actual (R00, 03_, HASHES_R00).
- Cláusula de grounding: toda afirmación de v1.5 sobre software, rutas o versiones cita fuente (ruta+hash o D-id); sin fuente = NO_DATA. CC verifica antes de la firma.
- v1.4 se usa solo como referencia de estructura, nunca como fuente de hechos.

## D10 · TEST_FUGA (2026-08-11)
- test_fuga.md reconocido por el Soberano: canario antiguo, inofensivo.
- Enterrado en necropolis/ con motivo; original eliminado tras copia.

## D11 · HASHES_R00 (2026-08-11, ENMENDADO 2026-08-11)
- Causa real: la linea base NUNCA estuvo rota. sha256sum -c separa por doble espacio; el formato era correcto desde el principio.
- Lo roto fue la verificacion del auditor en R01 (awk '{print $2}'), no el artefacto. D11 se firmo sobre una alarma falsa generada por el Preceptor.
- La regeneracion fue inocua. La regla se mantiene con motivo corregido: no protege de bases mal escritas; protege de auditores que verifican mal.
- Regla futura: toda linea base se re-ejecuta con sha256sum -c (herramienta nativa, no awk) antes de usarse como autoridad.
- Evidencia enterrada conservada en necropolis/HASHES_R00_roto_evidencia.txt.
## D12 · TERCER BLUEPRINT v1.2.0 (mente/doctrina)
- Clasificado borrador histórico sin autoridad. No se mueve hasta que una ronda decida la casa de la doctrina.

## D13 · VERSIONADO DEL MOVIMIENTO mente→Cuarentena
- Cuarentena/ entra en git; los 9 borrados de mente/ quedan registrados como movimiento. Reversible por historia.

## D14 · R00 ARCHIVADO
- Línea 5 corregida a FIRMADO en docs/post_verificacion/.

## D15 · CANON v1.5 COMO ENVOLTORIO
- v1.5 = canon de sistema; v1.3.0 = canon visual íntegro, sin editar.
- v1.5 se firma en raíz como BLUEPRINT_SISTEMA_P0X_v1.5.md.
- v1.4 y v1.2.0 quedan como borradores históricos.

## D16 · STDERR VISIBLE (2026-08-11)
- git add con 2>/dev/null oculto el fallo del index.lock; misma familia que el sed de R00.
- Regla: ningun comando de git o de verificacion se ejecuta con stderr suprimido.

## D17 · ENMIENDA D11 (2026-08-11)
- D11 reescrito con causa real: verificacion del auditor rota, no la base.

## D18 · AGUJERO GUARDIA (pendiente 2026-08-12)
- Exencion D8/D10 evalua por linea, no por regla. Token ghp_ pasa si la linea tiene /home/pisky/.  # guardia:permitir ruta-local-documentacion-D8
- Requiere refactor a evaluacion por regla + test rojo TOKEN-PROVEEDOR x RUTA-HOME.
- El Preceptor aplico el parche tras directiva explicita del Soberano (D23 firmada).

## D19 · EXCEPCION INNECESARIA (pendiente 2026-08-12)
- guardia:permitir 0.0.0.0:8050 en p0x-paper-manifest-v2.txt fue innecesaria (no habia exposicion).
- Quitar excepcion y revisar edicion humana del archivo.

## D20 · DEL BARRIDO ENTERRADO (2026-08-11)
- Restaurado desde bdf2595 a necropolis/ con tumba. Doctrina absorbida en canon.

## D21 · CRASH-LOOP AURELIUS-INTERFAZ (cola)
- ~29953 reinicios segun PENDIENTES.md. Hallazgo operativo real. Ronda dedicada futura.

## D22 · ARCHIVO diez (cola)
- 0 bytes, origen NO_DATA. Basura evidente o investigar en ronda futura.

## D23 · EXENCION GUARDIA POR RUTA (opcion A) (2026-08-12)
- D8 se interpreta como exencion DOCUMENTAL acotada: Cowork puede citar IPs/rutas en sus entregables (salida/, docs/post_verificacion/).
- NO autoriza commits con IPs/rutas fuera de esas carpetas.
- 04_CONTRATO §3.5 queda intacto: cero rutas de usuario, cero IPs tailnet en nada publicable.
- Exencion por regla: D8 exime IP-RFC1918/RUTA-HOME/DOMINIO-PRIVADO/NODO-*; NUNCA TOKEN-PROVEEDOR ni IP-TAILNET.
- Suite de tests a verde sin rendirse (no mover BLOQUEAN a PASAN).

## D25 · ENMIENDA D21 (2026-08-12)
- Crash-loop de aurelius-interfaz CERRADO el 2026-08-01 con prueba en PENDIENTES.md (seccion CERRADO, 416-423).
- D21 se firmo sobre cita sin seccion. Ver D28.

## D26 · ENMIENDA D19 (2026-08-12)
- Premisa de D19 falsa: exposicion 0.0.0.0:8050 real en deploy/soberano/aurelius-interfaz.service (ExecStart, linea 12).
- El grep de R02 no incluia *.service. Afirmo "no hay bind" sobre barrido incompleto.

## D27 · ENDURECIMIENTO AURELIUS-INTERFAZ (abierto 2026-08-12)
- Item abierto: bind a 0.0.0.0:8050 contra doctrina de Red de Confianza (tailnet/mTLS), y unidad sin StartLimitBurst/StartLimitIntervalSec.  # guardia:permitir exposicion-documentada-D27
- Severidad: activa si ss en soberano muestra LISTEN hoy; latente si inactivo.
- La sesion Cowork no tiene runtime de soberano (sandbox bwrap); datos de runtime los aporta el Soberano o CC en maquina real.
- Remedio via spec de Claude Code tras firma: bind a tailnet/loopback + limite de arranques.

## D28 · CITA CON SECCION (2026-08-12)
- Toda cita de documento tri-estado (PENDIENTES.md u otro con ABIERTO/CERRADO) incluye el encabezado de seccion de la linea.
- Cita sin seccion = NO_DATA. Regla mecanica, no atencional.
- Barridos de higiene: sin filtro de extension (la forma del error de R02/R04).
