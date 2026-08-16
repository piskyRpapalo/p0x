---
id: estado-firmado-ronda
titulo: Estado firmado y frentes aparcados
tipo: operativo
clase: doctrina
version: 1.1.0
editor_autorizado: carbono
caduca: 2026-09-10
actualizado: 2026-08-16
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
- Confirmado como fixtures de test (tuplas de casos de prueba con etiqueta <TOKEN-DE-PROVEEDOR>).
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

## D29 · HUERFANO_8050 ELIMINADO (2026-08-12)
- pid 2411: servir_interfaz.py --host 0.0.0.0 --puerto 8050; iniciado 2026-08-11 06:54; ppid 2314.
- Identificado con ps/cmdline y matado por el Soberano; ss confirma PUERTO_LIBRE.
- Exposicion activa eliminada. Exposicion latente permanece en la unit (D27, spec CC pendiente).
- Precedente aplicado: dump1090 murio por la misma doctrina (Red de Confianza, necropolis 3.1).

## D30 · CAUSA ESTRUCTURAL DE LOS HUERFANOS (2026-08-12)
- Padre del pid 2411: systemd --user (2314), con la unit en inactive: patron de daemonizacion (el PID principal sale; systemd pierde al hijo).
- Explica el crash-loop de 2026-08-01 y el huerfano de hoy: cada stop/restart deja un servidor huerfano en :8050.
- El fix D27 debe incluir rastreo del proceso real (foreground o Type=forking+PIDFile), ademas del bind acotado y el StartLimit.

## D31 · CANON DE ENFOQUE ARQUITECTONICO (2026-08-12)
- Todo documento nuevo declara `sistema:` con uno de cinco valores: MVP, PRECEPTOR, HEXELION, P0X-CORE, COMPARTIDO. Sin etiqueta = propuesta incompleta.
- Clausula de alcance: la convencion rige para documentos nuevos; el canon existente se cualifica cuando se toque por otro motivo. Un documento firmado no queda en falta por una regla posterior a su firma.
- "Aurelius" solo no identifica nada: se escribe Aurelius-MVP o Aurelius-Preceptor.
- Vocabulario por audiencia: MVP en ingles de industria (su lector es cualquiera); Preceptor en espanol concreto (su lector es el Soberano). Ningun termino cruza; dos nombres para un componente es traduccion, no duplicacion.
- Los identificadores citados por un expediente firmado no se renombran: romperia una prueba sellada por hash o exigiria tabla de traduccion permanente.
- La lista solarpunk queda ARCHIVADA: no es canon, no es cola, no tiene fecha.
- Medido: los 9 terminos del MVP tienen cero colisiones en el arbol; 6 nombres del Preceptor colisionaban, 4 contra canon visual firmado. Reemplazos verificados antes de proponerse.

## D32 · TRANSITO · NADA CONSERVA SU VERDAD AL CAMBIAR DE SITIO (2026-08-12)
- Enmienda del principio de reutilizacion: "un modulo usado vale mas que diez especificados, siempre que se reaudite su politica al cambiarlo de sitio". El lexico es parte de la politica.
- Aplica tambien al cambio de modo de invocacion dentro del mismo fichero, no solo al cambio de repositorio.
- Todo transito declara origen, destino y verificacion; la verificacion se ejecuta EN EL DESTINO.
- Todo POST_VERIFICACION lleva seccion TRANSITOS con tabla origen/destino/verificacion.
- Los hashes cubren una region delimitada por marcadores; las firmas van fuera, para que firmar no invalide el sello.
- Rondas paralelas: las lecciones que cruzan viven en un anexo de sitio unico, leido no transcrito, con test en destino. Ningun agente escribe en el anexo ni en el repo del otro. Hallazgo cruzado = PARO y reporte, no parche.
- Anexo de la ronda VERSIONES1+FASE0: `Cuarentena/salida/ANEXO_LECCIONES_CRUZADAS.md`, sha256 del cuerpo entre marcadores = 0939b9ea1568df12407c7808cf469ee803d08dfcaeaa0da14cfb0ab01cfcb5d3.
- Regla de desbloqueo: divergencia de hash exige diff contra la fuente. Diferencia entre marcadores = PARO. Diferencia fuera de marcadores o de extraccion = re-ejecutar el comando literal, registrar incidente y CONTINUAR. Un PARO falso ensena a desactivar el freno.
- Origen: nueve correcciones propias en la serie; ninguna fue mentira, todas fueron cambio de contexto sin reauditar.

## D33 · ANTICIPACION · MECANISMOS, NO FALLOS (2026-08-12)
- Nunca anticipar fallos especificos: una regla no ganada por colision es especulacion.
- Si anticipar mecanismos de respuesta: la Ley de Desobediencia Verificable y la clausula de revision son de esta clase.
- Matiz: se puede anticipar un fallo concreto cuando ya se sufrio en un contexto vecino. No es especulacion, es generalizacion de una colision medida.
- El canon de P0X crece por colision, no por reflexion. Cada regla tiene una herida detras.

## D34 · PUNTO CIEGO DE RUTAS ABSOLUTAS (2026-08-12)
- La regla de ruta de la guardia cubria /home/<usuario>, ~<usuario> y rutas de Windows. NO cubria /mnt, /srv, /opt, /var, /media.
- Reproducido: tres lineas con rutas bajo /mnt, /srv y /home; solo detecta la de /home.
- Enmienda: extender la regla a los cinco prefijos, con un caso rojo por prefijo en la suite.
- ::1 y 127.0.0.1 quedan como casos PASAN explicitos con test: loopback no es dato sensible y ya estaba en verde por casualidad.
- Rangos del verificador de publicacion: incluir fc00::/7, que cubre el rango IPv6 de la red superpuesta. ::1 fuera de prohibidos.
- Medido: 13 rutas absolutas distintas invisibles para la guardia en el arbol; 3 de ellas en skills/auditar-p0x.

## D35 · CADUCIDAD DE CONFIANZA (2026-08-12)
- Todo mecanismo critico declara `revisar_antes_de:` con fecha literal. Un test verde es una medicion pasada, no presente.
- Mecanismo critico que caduca: BLOQUEA. Mecanismo no critico que caduca: informa.
- Lista firmada de criticos: la guardia, los ganchos pre-commit y pre-push, el auditor de transitos, y los hashes del registro sellado.
- Primer `revisar_antes_de:` critico: la guardia, 2026-09-12.
- Registro de puntos ciegos conocidos: fichero con lo que la guardia NO cubre, de revision obligatoria al tocarla. "64/64 verde" dice lo que hay; el registro dice lo que falta.
- Metatest: bateria roja de agujeros ya cerrados, ejecutada al modificar la guardia. Regresion de atencion, no solo de codigo.
- Origen: el punto ciego de D34 llevaba ahi desde el origen de la guardia y se uso como criterio de publicabilidad sin dudarlo, precisamente porque estaba probada.

## D36 · ARCHIVO DE CINEK-AUTOMATICO (2026-08-12)
- D1 firmo que cinek_automatico queda archivado y CineK_Studio es el repositorio oficial. El repo seguia activo como privado.
- Accion: Archived con motivo en el README, no description nueva. Archivar, no borrar.
- NO_DATA: CineK_Studio no aparece entre los seis repos del perfil. Su ausencia se declara y queda por resolver.

## D37 · AUDITORIA EXTERNA CON CADUCIDAD (2026-08-12)
- Cada estacion, o en cada publicacion, se audita hacia afuera: repositorios publicos, puertos en escucha, unidades activas y sus enlaces, ACLs efectivas.
- Motivo: el rigor de la serie miraba hacia dentro. Un candado nuevo en una puerta interior se instala y se verifica en una tarde; comprobar la puerta de la calle exige mirar algo ya dado por hecho.
- Inventario de puertas sin revisar al firmar: el repositorio espejo (contenido), ocho unidades de servicio con enlaces desconocidos, una caza interrumpida en un arbol antiguo, y la validez de unas credenciales citadas en documentos viejos.
- El auditor externo entra en el roadmap de La Lupa.
- Auditor chat->disco: toda decision firmada que no conste en disco es hallazgo. Forma minima: lista de D-ids esperados frente a presentes.

## D38 · DIFERIMIENTO DEL REPOSITORIO ESPEJO (2026-08-12)
- Estado: PRIVADO. Exposicion detenida. El borrado y la recreacion limpia quedan DIFERIDOS, no abandonados.
- Disparador de reapertura: cuando exista el export curado ejecutable, o la revision del 2026-09-12, lo que ocurra primero.
- Medido: el arbol publicado coincidia entrada por entrada con el privado (19 de 19); 27 hallazgos de guardia en 15 ficheros mas 13 rutas absolutas invisibles; el mayor deposito no era deploy/ sino mente/, con 30 hallazgos y 15 rutas.
- Confirmado: cero credenciales reales publicadas. Nada criptografico que rotar.
- Causa estructural: un espejo de un arbol privado no puede ser seguro, porque su proposito es copiar. La correccion es export curado con lista blanca y guardia en la ruta de destino.
- Hallazgo: el repositorio nacio como cara publica escrita a mano y un push de arbol completo la sobrescribio. La correccion es volver a lo que era su primer commit.
- NO_DATA: numero de commits y coincidencias del historial publicado. Nunca medido. La cifra de 3680 corresponde al arbol privado, no al publicado.
- Rescate de capturas: cancelado por el Soberano, que posee copias en otro lugar.

## D39 · NO SE ROTAN LAS DIRECCIONES · RIESGO RESIDUAL ACEPTADO (2026-08-12)
- Decision: no se rota el rack. Se acepta el riesgo residual, con motivo escrito.
- Motivo 1: cero forks y una estrella; probabilidad de clon hostil baja.
- Motivo 2: una direccion de la red superpuesta sin identidad autorizada no abre la malla. Lo expuesto es inventario, no acceso.
- Motivo 3: el inventario no es rotable, solo despublicable.
- Motivo 4: coste operativo de rotar el rack mayor que el riesgo residual.
- Revision: 2026-09-12. Si para entonces existe el export curado ejecutable, la decision pasa a borrar y recrear, y la rotacion queda sin objeto.
- Se registra la decision de NO actuar con su razon, para que en la revision se discuta y no se descubra.

## D40 · PODA ESTACIONAL (2026-08-12)
- Cada estacion se revisan los mecanismos. Lo que nadie pueda explicar de memoria, o que nunca haya disparado, es candidato a fusion o archivo.
- La estructura crece por colision y se poda por estacion.
- Indicador firmado: una regla que no se puede explicar de memoria existe en disco pero no en el sistema.
- Criterio operativo: leer en voz alta las veinte reglas de `ANEXO_VEINTE_REGLAS.md` y anotar las que no salgan. Lo que falle dos estaciones seguidas se fusiona o se archiva.
- Primera poda: 2026-09-12, misma fecha que la caducidad de la guardia y la revision de D38 y D39.

## D41 · ARCHIVO DE RAZONAMIENTO Y PARTIDA GUARDADA (2026-08-12)
- Nace un archivo de razonamiento fuera de git con cabecera "memoria, no canon". Su existencia no depende de rellenarlo.
- Primer contenido: la lista de D-ids esperados, que es el artefacto del que lee el auditor chat->disco.
- `ANEXO_PARTIDA_GUARDADA.md` queda firmado como mapa de memoria del sistema. Sus nueve autocorrecciones no se editan ni se suavizan: son el argumento del documento.
- Sera el contenido inicial del repositorio de doctrina cuando se publique, no un texto nuevo escrito para la ocasion.
- `ANEXO_VEINTE_REGLAS.md`, una pagina, es el instrumento de relectura semanal y el criterio de la poda de D40.


## D43 · FALSOS POSITIVOS EN PROSA (2026-08-12)
- Extender la regla de rutas a /mnt /srv /opt /var /media (D34) crea
  falsos positivos inmediatos en prosa que cita esos prefijos. Todo
  entregable que los mencione requiere guardia:permitir declarado con
  motivo. La lección viaja fuera del anexo sellado (D32) para no
  invalidar el hash de las lecciones compartidas.

## D44 · BUCLE ROJO-SABOTAJE-VERDE COMO PROTOCOLO OBLIGATORIO (2026-08-12)
- Protocolo obligatorio, no opcional: primero todos los tests fallan; despues se rompen A PROPOSITO tres invariantes propias y se comprueba que la suite lo detecta; solo entonces verde.
- El sabotaje es un MODO PERMANENTE del propio codigo, ejecutable por bandera, no un gesto manual hecho una vez. Convierte "12/12 verde" en una afirmacion con contenido en lugar de un numero.
- Regla que lo sostiene: un test que pasa desde el principio es un test que no fue disenado para detectar una rotura especifica. Candidata a `ANEXO_VEINTE_REGLAS.md`.
- Si una invariante rota NO es detectada, ESE es el fallo, y el fallo es del test: se reescribe el test, no se toca el modulo. El sabotaje trabaja siempre sobre copia.
- Procedencia doble e independiente: el bucle ejecutado a mano sobre la memoria de M2 (0/12 esqueleto vacio -> 12/12 implementado -> 3/12 saboteando tres invariantes -> 12/12 restaurado) y el documento externo del Prompt Maestro. Se adopta por la coincidencia de dos procedencias, no por la autoridad de la fuente (D46).
- Texto de origen: `Cuarentena/salida/VEREDICTO_PROMPT_MAESTRO.md` §1 y §5.1.

## D45 · DEPENDENCIA FINA · UNA SALIDA NO SE CONSUME HASTA QUE EL AUDITOR LA VALIDA (2026-08-12)
- Los agentes de una ronda corren en paralelo, pero ninguna salida entra como entrada de otro hasta que el auditor la valida.
- Refina la regla vigente de D32 ("hallazgo cruzado = PARO"), que solo cubria el caso de conflicto. Esta cubre el caso normal, que es el frecuente.
- El grano es la salida, no la ronda: no se espera a que todo termine, se espera a que este validado lo que se va a consumir.
- Origen: seccion 4 del Prompt Maestro AI-AI. Se adopta la regla; su aparato de citas se descarta entero (D46).
- Texto de origen: `Cuarentena/salida/VEREDICTO_PROMPT_MAESTRO.md` §1 (cierre) y §5.3.

## D46 · VEREDICTO DEL PROMPT MAESTRO AI-AI · ESTRUCTURA SI, AUTORIDAD NO (2026-08-12)
- Clasificacion R00: `EXTERNO_NO_VERIFICADO` en su grado mas severo. Se aprovecha la ESTRUCTURA y se descarta la CITA, como manda `02 §3`.
- DECLARADOS INEXISTENTES, medido: `NVIDIA OpenShell` (30 menciones entre variantes) no es un producto de NVIDIA — la casa tiene Container Toolkit, Triton, NIM y TensorRT. `NVIDIA NemoClaw` (4 menciones) tampoco existe. Toda la seccion de ejecucion en el borde se apoya en una plataforma inventada, y sobre ella el documento declara una "obligacion etica": la forma retorica mas peligrosa del texto, un supuesto no verificado convertido en deber.
- Citas de empresas homonimas, no de este proyecto: `docs.hexagonppm.com` x12 es Hexagon PPM, software industrial; `nexo.com` x7 es una plataforma de criptoprestamos. Coinciden con HEXELION y el Nexo en la silaba y en nada mas. Con 33 enlaces de YouTube y 17 de LinkedIn en el resto, el aparato de 66 paginas no aporta ninguna autoridad.
- NIVELES N0-N4: **DECLARADOS NO FIRMADOS.** El documento los presenta como "una escala ya definida y acordada". Cero apariciones en las decisiones firmadas al medirlo. Citarlos como canon es un error de categoria.
- Medallon Bronze/Silver/Gold: el documento se ancla a el como cimiento existente; los tres directorios no estaban en el arbol al medirlo.
- RECHAZADO: "sin depender de decisiones externas para tareas que los agentes pueden resolver de forma autonoma". El Soberano no es una dependencia externa: es quien firma el valor. Un documento que lo llama externo ha invertido el suelo.
- RECHAZADO: siete agentes en paralelo. Coordinar dos costo hoy un anexo con sello, una regla de desbloqueo y un PARO real; siete son veintiun pares de posible interferencia.
- ADOPTADO ademas de D44 y D45: `AG-*` como convencion de identificador de agente en un prompt. Util y sin colision.
- Texto de origen: `Cuarentena/salida/VEREDICTO_PROMPT_MAESTRO.md` §2, §4 y §5.

## D47 · HUECO D42 · REVERSION DELIBERADA (2026-08-12)
- D42 fue `PODA ESTACIONAL`, anexado por orden literal y revertido la misma tarde, en la ronda VERSIONES1.
- Motivo de la reversion: duplicaba D40, que ya se titula igual y contiene lo mismo MAS el indicador firmado, el criterio operativo de relectura y la fecha de la primera poda. D42 era un restatement estrictamente mas pobre de canon existente.
- Como se revirtio: restauracion del respaldo previo. `diff` contra el estado post-D41: IDENTICO. D40 nunca se toco.
- El numero NO se reutiliza. Reciclar un D-id retirado rompe toda cita futura y hace que dos decisiones distintas compartan identidad. La numeracion salta de D41 a D43 a proposito.
- Diferencia con D24, y por que importa: D24 es `NO_DATA` porque no se SABE que fue; D42 es `NO_DATA` porque se sabe exactamente que fue y se decidio que no fuera.
- Consecuencia mecanica, firmada aqui: el auditor chat->disco distingue `HUECO_PREEXISTENTE` de `HUECO_NUEVO`. El primero informa; el segundo BLOQUEA mientras su motivo no conste en ESTE documento. Explicarlo en el archivo de razonamiento no basta: ese fichero es memoria, no prueba, y lo edita el mismo proceso al que se audita. Esta entrada es la que cierra el hueco D42.

## D49 · PREDICCION CINEK REESCRITA (2026-08-12)
- La prediccion firmada perdida se reescribio de memoria y quedo VERSIONADA en bronze/. Commit efb8397.
- La perdida original: bronze/, silver/ y gold/ nunca estuvieron bajo seguimiento; cero commits los anadieron.
- Regla ganada: un directorio sin seguimiento en el primer nivel es hallazgo del auditor, no una nota de git status.

## D51 · REFERENCIA CRUZADA · M-D51 en aurelius-mvp (2026-08-12)
- Frontera cerrada: cualquier excepcion del redactor es FronteraSinFiltro, no solo su ausencia.
- Contenido verificado por el Soberano en clon limpio. Cowork no lee ese repositorio: declaracion, no medicion.

## D52 · REFERENCIA CRUZADA · M-D52 en aurelius-mvp (2026-08-12)
- Modo sabotaje como mecanismo permanente del codigo, no gesto manual de sesion.

## D53 · REFERENCIA CRUZADA · M-D53 en aurelius-mvp (2026-08-12)
- README de M2 el Agua, producto publico.

## D54 · TUMBA DE LA COPIA DIVERGENTE (2026-08-12)
- La copia del producto en Cuarentena/salida/ paso a necropolis/tumbas/aurelius-mvp-m2/ con TUMBA.md. Commit 28f838a.
- Cierra el riesgo de dos verdades sobre el mismo codigo. Manda el repositorio del producto.

## D55 · LIMPIEZA DE ESTRUCTURA ANIDADA EN LA TUMBA (2026-08-12)
- Commit ed248ef. Sin cambio de contenido.

## D56 · FIRMA DEL MANIFEST DE RONDA (2026-08-12)
- MANIFEST.yaml firmado por carbono. Commit fa8e8f2.

## D58 · REFERENCIA CRUZADA · M-D58 · exenciones del guardian en el producto (2026-08-12)
- Guardian instalado en el repositorio del producto y .guardia_exento declarado.

## D59 · REFERENCIA CRUZADA · M-D59 · lexico sintetico (2026-08-12)
- El respaldo de lexico para test es SINTETICO: ninguna palabra real del lexico vigilado viaja al repositorio publico.
- En produccion la ausencia del lexico sigue siendo frontera cerrada. La asimetria es deliberada y esta probada.

## D60 · REFERENCIA CRUZADA · M-D60 · perfil y preguntas humanas (2026-08-12)
- Tabla profile aditiva: no toca engrams ni exige migracion del CHECK de origin.

## D61 · REFERENCIA CRUZADA · M-D61 · neutralizacion de termino vigilado (2026-08-12)

## D62 · REFERENCIA CRUZADA · M-D62 · cierre de M2 con el manifiesto (2026-08-13)
- El hash cubre solo el cuerpo entre marcadores; la firma va fuera para que firmar no invalide el sello.
- Firmar no muta la memoria. Sin nombre, signed_by NO_DATA y la firma es valida. Verificar es recalcular.
- El manifiesto guarda huellas, nunca el texto de los recuerdos.

## D63 · EL TEMPLE · CARACTER DE AURELIUS (2026-08-13)
- preceptor/El_Temple.md, sistema PRECEPTOR. Commit 928a98f. NO viaja al repositorio publico.
- El tono (ritmo, pausas, elecciones) SI es del producto: es texto y temporizacion.

## D64 · SERIES DE NUMERACION SEPARADAS (2026-08-13)
- p0x usa serie D. El producto usa serie M. Sin colision.
- El canon de p0x registra las decisiones del producto como referencia cruzada cuando hay evidencia legible.
- Origen: dos registros de cambios acunaban identificadores de decision de forma independiente.
- Regla ganada: un registro de cambios no es un registro de decisiones. git log cuenta que se movio; el canon cuenta que se decidio.

## D65 · IDENTIFICADORES NUNCA ACUNADOS (2026-08-13)
- D48, D50 y D57 no existen en canon ni en ningun commit. No se rellenan y no son huecos de perdida.
- D24 y D42 siguen declarados como huecos previos.

## D66 · E1 · NUCLEO PURO Y GERENTE OPCIONAL (2026-08-13)
- El nucleo no sabe que modelo es el gerente: solo detecta si algo responde al CONTRATO.
- Inyeccion, nunca importacion dentro del nucleo. El gerente es camino principal, jamas el unico.

## D67 · FRONTERA ASIMETRICA HACIA EL GERENTE (2026-08-13)
- El nucleo redacta SIEMPRE, tambien hacia el gerente. No se cree ninguna declaracion de localidad.
- Politicas Core (claves, tokens, claves privadas): no cruzan NUNCA, ni pedido. Es D8_JAMAS traducido al producto.
- Politicas Custom (direcciones, rutas, nombres de maquina): redactadas por defecto, liberables POR SESION.
- El levantamiento NOMBRA el dato ante la persona, se declara, se registra y es reversible.
- Motivo de la asimetria: un suelo que hay que levantar para trabajar se levanta siempre. Medido en casa: 55 lineas con pragma en 26 ficheros, cada una con motivo legitimo.
- Vocabulario: en el producto quien levanta es "la persona". "Soberano" solo en el canon de p0x y del Preceptor.

## D68 · E5 · PORTAPAPELES SOBERANO, ACOTADO A LA RED (2026-08-13)
- Nada sale automatico POR RED. El gerente queda fuera por construccion, no por confianza.
- El gerente es proceso hijo por entrada y salida estandar. El CONTRATO NUNCA es HTTP a localhost: un puerto local es indistinguible de un tunel.
- La localidad se impone, no se cree.

## D69 · E6 · CAPA BORRADORES (2026-08-13)
- El gerente escribe en BORRADORES (drafts), tabla aparte. Nunca en engrams. Ninguna migracion del CHECK de origin.
- Estados: pendiente, promovido, descartado. Columnas, no borrados. La capa NO se vacia nunca.
- El recordatorio cuando se llena es un CONTADOR VISIBLE, no una purga.
- La promocion a memoria firmada es acto exclusivo de la persona. IronClaw se conserva: el gerente escribe por quien no puede; la persona firma.
- El nombre "plata/silver" queda reservado al Medallon: 02_CANON_OPERATIVO §1 lo define y lo nombra seis veces.

## D70 · REDEFINICION DEL PRODUCTO, CON SU PORQUE (2026-08-13)
- Aurelius-MVP no es un producto de privacidad: es una herramienta para organizar datos y empezar un proyecto, con un programa de aprendizaje.
- La accesibilidad es requisito, no opcion. Voz como entrada para quien no puede escribir.
- Por que la frontera se endurece a la vez que el producto deja de venderse como privacidad: una herramienta de accesibilidad se usa justo cuando la persona NO PUEDE revisar lo que sale. Quien dicta por voz no esta leyendo el prompt antes de enviarlo. El suelo protege a quien no puede vigilar.
- Esta justificacion va en la misma entrada a proposito: separada, la frontera se leeria en un ano como resto de una etapa superada.

## D71 · E7 · INSTALACION COMO ECOSISTEMA (2026-08-13)
- Los dispositivos son parte del perfil de la persona y su ambiente. Migrar a hardware nuevo es funcion de primera clase.
- Umbral de capacidad: lo aporta la persona buscando las caracteristicas de su equipo. Desconocido -> NO_DATA -> modo reducido. Nada de umbrales por intuicion.
- Voz: escuchar primero, hablar despues. STT prioritario, TTS condicional. Capacidad negociada, no caracteristica.

## D72 · DIAPOSITIVAS COMO EJE TRANSVERSAL (2026-08-13)
- Nuevo lenguaje de onboarding de todas las misiones siguientes: el usuario pasa de consumidor a productor.
- Lo que toque documentos ya firmados se re-verifica. Un eje que modifica misiones firmadas sin re-verificarlas convierte "firmado" en decorativo.

## D73 · INCIDENTE DE NO PERSISTENCIA (2026-08-13)
- Reproducido: dos recuerdos guardados con mensaje "Saved", interrupcion con Ctrl+C, contador posterior sobre la base real -> vacio.
- Causa reproducida por Cowork sobre la copia enterrada: abrir() envolvia la sesion entera en una transaccion y capturaba BaseException con rollback. KeyboardInterrupt es BaseException. La interrupcion descartaba todas las escrituras.
- "Saved" se imprimia porque la lectura ocurria dentro de la misma transaccion: verdad dentro, mentira fuera.
- Autoria: el fallo es de Cowork, en codigo que escribio. Decima correccion propia de la serie y la unica que destruyo trabajo real del Soberano, dos veces.
- Arreglo verificado: commit por escritura, antes de devolver. Si la funcion devuelve, esta en disco.
- Regla 1: respaldo de SQLite son los tres ficheros (db, -wal, -shm) o la API de backup. Un cp del db solo NO es respaldo. Esto explica que el respaldo tambien estuviera vacio.
- Regla 2: "Saved" solo se imprime tras commit. Una interrupcion no deja una mentira. Con test rojo que lo impone desde otra conexion, porque en la misma conexion el test veria el error como acierto.
- Regla 3: la unica memoria del usuario se respalda antes de todo toque de esquema. Hoy se perdieron filas por el diario WAL. Queda con su cicatriz.


## D74 · EL IDIOMA ES LA PRIMERA PREGUNTA (2026-08-13)
- La primera pregunta de la sesion es el idioma: English o Espanol, y se hace EN LOS DOS a la vez. Preguntar en un idioma que la persona no ha elegido ya es elegirlo por ella.
- Se guarda en el perfil (clave `language`), al lado de device y name. Un idioma ya contestado no se vuelve a preguntar: misma regla que el resto del perfil.
- No elegir NO se guarda como "en". Queda en NO_DATA y la sesion corre en ingles. El perfil distingue a quien eligio ingles de quien no eligio nada; escribir "en" por defecto convertiria una ausencia en una respuesta.
- Los textos viven en un solo diccionario de dos columnas, no en condicionales repartidos: una traduccion que falta es una clave que falta, y un test la encuentra antes que la persona.
- Efecto lateral firmado en la misma ronda: una sola gramatica para elegir. Las preguntas numeradas aceptan numeros y solo numeros, el enunciado lo dice, y el rechazo nombra los que valen. Antes convivian [y/N] y opciones numeradas en la misma sesion, y el Soberano escribio "yes" tres veces antes de entender que se esperaba un "1".

## D75 · TODA CAPA QUE HABLE O PIENSE ES PROCESO HIJO (2026-08-13)
- Toda capa que hable o piense es proceso hijo por entrada y salida estandar. Ningun servicio HTTP en localhost: un puerto local es indistinguible de un tunel. La voz no es excepcion.
- Origen: la residencia de voz medida en la fragua (681 ms) corre como servicio HTTP en localhost. Es exactamente la forma que D68 cerro para el gerente, y entraba al MVP por la puerta de atras como "capa aparte". Se cierra aqui, con nombre.
- Consecuencia para Piper: se invoca como programa, escribiendo a salida estandar, no como servicio. Bajo esta forma su licencia GPL no toca el nucleo Apache-2.0: es programa invocado, no codigo enlazado. La separacion no es un detalle de empaquetado, es lo que hace legitima la mezcla.
- Consecuencia para llama-tts: viaja en la MISMA compilacion Vulkan b10068 que ya esta en el metal, y habla por entrada y salida estandar por construccion. Cumple D75 sin instalar nada, sin dependencia GPL y sin segunda cadena de suministro. Queda declarado como candidato de voz de primera clase, a comparar de oido contra Piper cuando los seis clips esten en el Beelink. Si el oido no distingue, gana el que no anade dependencia.
- Lo que esta regla NO dice: no prohibe la red al usuario ni al Camino. Prohibe que una capa del MVP se hable a si misma por socket y llame a eso localidad.
- Por que el modelo pequeno, dicho aqui para que dentro de un ano no parezca un error: el pequeno se eligio porque CABE y porque el Camino incluye el telefono. No se eligio por velocidad — medido en este metal, genera un 12% mas lento que el 30B-A3B en Vulkan, porque un MoE de 3B activos corre mas que un denso de 4B. Donde si gana es sin GPU (x3,1 de prefill, +39% de generacion) y en tamano (2,32 GiB contra 17,3), que es exactamente el escenario del telefono.

## D76 · LA VOZ, LOS FILTROS Y EL PROGRESO MEDIDO (2026-08-14)
- Voz firmada: es_ES-sharvard-medium, HABLANTE 0. El modelo trae dos y la firma es sobre el 0; regenerar con el 1 queda prohibido sin nueva firma.
- Dos filtros de habla, defecto `rapido`: rapido dice lo minimo cierto; `lector` anade un parrafo de historia DETRAS de la respuesta, nunca en su lugar y nunca mas de uno. Son modificadores que se anaden al final del caracter: un filtro que sustituye al caracter no es un filtro, es otro personaje.
- Lore publico con gusto solarpunk, y su regla dura: el vocabulario de control NO cruza a la cara publica (D67). La capa pasa los dos guardianes con cero. El filtro es literal y caza incluso palabras usadas como nombre comun; se reescriben, no se exceptuan. Tampoco entra historia inventada: quien adorna con datos falsos ensena a no comprobar, que es lo contrario de lo que el producto ensena.
- Hijo residente: residente NO es servicio. Son procesos hijos con sus tuberias abiertas, sin puerto y sin nada escuchando; si el supervisor muere, mueren con el. Medido en este metal: arranque 1,36 s UNA vez por conversacion, turno medio 1,82 s, contra 4,57 s por frase en el modo de disparo unico. D75 intacto.
- Boton de audio en la cara, presente desde el primer arranque, junto a idioma, Pizarra y Camino. El texto se muestra SIEMPRE; el boton solo decide si ademas suena. La voz se GRABA al generar la pagina, con el proceso hijo, y viaja incrustada: al abrir la cara no se lanza nada ni se conecta nada. Solo suenan las lineas fijas y solo en espanol; lo que no puede sonar se declara en el propio boton en vez de callarse.
- El Camino muestra los ocho peldanos desde 0. Progreso MEDIDO: cada peldano ensena que lo da por hecho. M1 se declara NO MEDIBLE porque el cerebro no vive dentro del fichero, y M3-M7 se quedan en sin empezar en vez de inventarse un estado. Una barra de progreso que muestra lo que no puede medir es una barra falsa, y en cuanto la persona lo descubre deja de creerse el resto de la pantalla.
- Instalacion limpia: clonar y ejecutar. Sin paquete, sin servicio, sin cuenta. En el primer arranque estan el idioma, la cara, el boton de audio y las misiones a cero. Verificado sobre un clon virgen, no supuesto.
- LoRA de voz propio: se entrenara EN EL BEELINK, no en la fragua, y no antes de que el Soberano lo firme. Cuando lo firme, lo primero es una prueba de una hora que diga si este metal entrena un LoRA de 4B en horas o en dias — antes de preparar dataset.

## D77 · LO QUE UN MODELO PEQUENO NO PUEDE HACER, Y QUIEN PREGUNTA (2026-08-14)
- Un modelo pequeno no anade historia: pedirsela es pedirle que la fabrique. La historia la pega el PROGRAMA, literal, desde un fichero revisado. Medido contra el 4B: pedida en el prompt, invento tres origenes incompatibles del mismo hecho en tres respuestas seguidas; entregada en un bloque con etiqueta, aprendio a imitar la etiqueta y a inventarse el bloque cuando faltaba. Nombrar un marcador ensena a producir el marcador.
- De ahi la division: `rapido` es modificador de prompt y funciona; `lector` NO puede serlo. Lo dice la medida, no la preferencia.
- El lector callado se CUENTA. Quedarse en silencio cuando ninguna pieza encaja es la conducta correcta, pero un silencio que nadie cuenta no se distingue de una cobertura que no existe. Una linea por conversacion en telemetria.
- PUENTE CON LA CARA: se mantiene terminal-entra / cara-sale. Ni socket ni fichero-por-turno. Funciona hoy y D75 queda limpio.
- «Que la pagina pregunte» queda APLAZADO a la UI local real: una interfaz que sea ella misma un proceso, y no una pagina abierta con doble clic. Una pagina servida desde el disco no puede recibir de un proceso local sin un puerto, y el puerto es lo que D75 cierra. No es una limitacion que se arregle con ingenio: es la forma del medio. Esa UI es la siguiente pieza, no un bloqueo de la actual.
- Lo que se OYE se limpia; lo que se MUESTRA no se toca. Los dos espacios de fin de linea y los saltos del modelo son marcas para los ojos: dichos en voz alta producen silencios a mitad de idea. La limpieza quita marcas, jamas palabras — misma regla que el tono: se puede cambiar cuando se dice algo, nunca que se dice.
- El arquetipo se carga AL ARRANCAR el hijo residente. Editar el fichero del caracter no cambia una conversacion en curso: hay que cerrar y volver a abrir. Es correcto —el caracter no debe mutar a media charla— y se escribe aqui para que nadie edite el texto, no vea ningun cambio, y concluya que el arquetipo no se usa.

---

> **BLOQUE D78-D80 · FIRMADO POR EL SOBERANO · 2026-08-16.**
> Redactado por Claude Code desde evidencia medida y **firmado por Pisky** en
> la respuesta de cierre de ronda M-D80. §5 de este documento dice que Claude
> Code «no declara canon»: no lo declaro — lo redacte, y la firma es suya. Cada afirmacion lleva de
> donde sale. Lo que no se pudo medir se dice, no se rellena.
>
> **Aviso de numeracion.** El canon y los mensajes de commit del producto NO
> coinciden en dos sitios, y no se corrige la historia para taparlo:
> el commit `6d3f379` lleva la etiqueta «M-D79» y contiene lo que aqui son
> D78 (parte), D78b, D79 y D79b; y el commit `fd518b6` lleva «M-D80b» y es lo
> que aqui es D80c. Manda este documento; la etiqueta del commit es como quedo
> escrita en su momento.

## D78 · EL GENERADOR DE LEITMOTIVS VIAJA CON EL REPO Y ES DETERMINISTA (2026-08-16)
- La musica de M3 se FABRICA en la maquina de quien juega. No se descarga y no viaja como binario: viaja el generador. Commits `6b354c8` (lo trae al arbol, +49 lineas) y `6d3f379` (lo hace determinista, 171 lineas tocadas).
- Que viaje con el repo solo significa algo si es DETERMINISTA, y hasta esta entrada no lo era: el ruido de fondo salia de `hash(str(i))`, y el hash de `str` en Python esta aleatorizado por proceso (`PYTHONHASHSEED`). Dos ejecuciones en la MISMA maquina daban sha256 distintos; dos clones, sonidos distintos.
- Arreglo: `random.Random` sembrado con el NOMBRE de la sala. `random.Random(cadena)` siembra por sha512 del texto y no lo toca `PYTHONHASHSEED`. La misma sala suena igual en todas partes y para siempre; dos salas distintas suenan distinto.
- `asegurar()` la llama `fuga.ejecutar()` al entrar en M3, porque un clon limpio no tenia sonidos hasta que alguien ejecutara el generador a mano — que es justo lo que un generador que viaja con el repo venia a evitar.
- Y no bloquea: disco lleno o de solo lectura, M3 se hace igual. La musica es adorno del relato, no requisito. Misma regla que la voz y el oido.
- Nada se escribe AL IMPORTAR el modulo. Un modulo que escribe en la casa de la persona solo por ser importado no se puede probar sin tocarla.
- Verificado: `test_leitmotivs.py`, 13 pruebas, incluido el sha256 de los seis WAV.

## D78b · EL APAGADO DE HARDWARE ES DEL PRODUCTO, NO DE CADA SUITE (2026-08-16)
- `silencio.py` (commit `6d3f379`, +63 lineas). Tres puertas y las tres se cierran juntas: microfono (`oido`), sintesis (`voz`) y altavoz (`fuga._reproducir_wav`).
- Una sola variable: `AURELIUS_SIN_HARDWARE=1`. Va por ENTORNO y no por mock en memoria a proposito, porque tiene que cruzar a los procesos hijo: `test_idioma` arranca `aurelius.py` como subproceso y un mock no cruza esa frontera.
- Origen con cicatriz: ya paso una vez en `test_fuga` (D77) y se arreglo DENTRO de esa suite. Se sube al producto para que la siguiente suite no lo repita. Una tanda que graba la habitacion de quien la corre tarda minutos, escucha lo que no le han dado, y ademas no prueba lo que dice probar: si la respuesta entra por el microfono, el guion de teclado no se usa nunca.
- No es «modo test». Es una declaracion sobre la MAQUINA, como `estado.json`: vale igual para un servidor sin tarjeta de sonido o para quien no quiere que un programa le encienda el microfono. Los dos son casos reales y ninguno es una prueba.
- Verificado: `test_silencio.py`, 9 pruebas.

## D79 · UNA SOLA GRAMATICA PARA ELEGIR, POR VOZ Y POR TECLADO (2026-08-16)
- `numero_dicho(texto, cuantas)` en `fuga.py:103` (commit `6d3f379`). Es la continuacion directa de D74, que ya habia firmado una sola gramatica para las preguntas numeradas; aqui esa gramatica pasa a ser LA MISMA por los dos canales de entrada.
- `None` NO significa «no entendi, tira con el defecto». Significa «esto no es un numero», y quien llama tiene que rechazarlo EN VOZ ALTA nombrando los que valen.
- Un fuera de rango tambien es `None`: decir «siete» cuando hay cuatro opciones es tan invalido como decir «Carlos», y merece el mismo rechazo. Un fuera de rango que cae al defecto en silencio es la version educada de no escuchar.
- Acepta digitos y palabras, y solo si el texto ES el numero: «el 3» vale, «tengo 3 hijos» no es una eleccion, es una frase.
- Verificado: casos 25, 26, 27 y 28 de `test_fuga.py` (numero por voz, rechazo hablado, misma gramatica por teclado, y el defecto DICHO al agotar intentos).

## D79b · EL PERMISO DEL GERENTE: FILA AUSENTE VALE 'NO', Y SE COMPRUEBA DENTRO (2026-08-16)
- `permiso_concedido(db)` y `perfil_para_gerente(db)` en `fuga.py:157` y `:177` (commit `6d3f379`).
- Fila ausente = `no`. Nunca un error y nunca otro defecto: una base recien creada, una fila que jamas se escribio y una sesion que se corto antes de la pregunta tienen que dar TODAS la misma respuesta, y tiene que ser la que no entrega nada. Solo un `si` explicito abre la puerta.
- La comprobacion vive DENTRO del camino de lectura, no en quien llama. Esa es la diferencia entre un permiso y una costumbre: en el llamante, bastaria un llamante nuevo que no la conociera — y siempre hay un llamante nuevo.
- Sin permiso LEVANTA (`SinPermiso`), no devuelve un diccionario vacio. Vacio se confunde con «no contesto nada», y son cosas distintas: una es no tener datos y la otra es tenerlos y que no sean tuyos.
- `NO_DATA` se entrega tal cual cuando hay permiso: la ausencia tambien es del perfil.
- Verificado: casos 19 a 24 de `test_fuga.py`, incluido el que exige que la comprobacion este dentro del camino de lectura y el que impide que abandonar la sala 3 deje un permiso suelto.

## D79c · EL RANGO DE INTERPRETES SE MIDE, SE DECLARA Y NO BLOQUEA (2026-08-16)
- Commits `1ee1b3f` (la cabecera de `bin/pruebas` declara interprete y ruta) y `e531b5b` (`interprete.py` + `test_interprete.py`, 6 pruebas).
- Regla: una cifra sin su maquina es un rumor con decimales. `bin/pruebas` imprime `python3 -V` y su ruta ANTES de correr nada, para que salga aunque la tanda se corte a la mitad.
- El rango vive en UN sitio (`interprete.py`) y lo consumen el producto y la tanda. Si viviera en los dos, el dia que se pruebe una version nueva habria que acertar dos veces, y bastaria fallar una para que el README prometiera un rango y el programa declarara otro.
- Fuera del rango: se DECLARA por salida de error, en los dos idiomas — ocurre antes de que nadie haya elegido idioma — y se SIGUE. Fuera del rango probado no significa roto, significa sin dato; negarse a arrancar convertiria una ausencia de medida en un veredicto, que es lo que este arbol no hace en ningun otro sitio.
- El README publica lo que se CORRIO, con su arbol y su sistema, y no un intervalo de compatibilidad: nadie ha corrido la suite en 3.12, asi que la tabla no dice que funcione ahi.
- Medido: 3.10.12 y 3.14.4, ambos VERDE. La medida vieja de Ubuntu 22.04 sobre `73f7bc6` (217/217) se declara en fila aparte de la de hoy en vez de fundirse con ella.

## D80 · UN SOLO ESCRITOR DEL PERFIL, CON ON CONFLICT (2026-08-16)
- `guardar_perfil(c, pares, commit=True)` en `memory.py` (commit `5f56b15`). Es el UNICO sitio del arbol con SQL de `profile`. `escribir_perfil` — que ya existia y ya usaba `ON CONFLICT` — pasa a delegar, para que no haya dos escritores que puedan separarse con el tiempo.
- `fuga.py:802` era el unico escritor que se saltaba la puerta: `INSERT OR REPLACE INTO profile`, que borra la fila entera y mete otra, de modo que toda columna que la sentencia no nombre vuelve a su DEFAULT. Es un DELETE con otro nombre, y la regla de cero DELETE no tiene excepcion para cuando es una sola fila. El mismo motivo ya estaba escrito en `_marcar_sala_entrada`; faltaba aplicarlo aqui.
- `commit=False` para lotes: la Fuga vuelca el perfil de una sala entero o no lo vuelca. Un commit por clave habria convertido esa promesa en media sala escrita y roto el criterio 2 de M3.
- LO QUE ESTA ENTRADA NO AFIRMA, y se escribe aqui para que nadie lo cuente al reves: la correccion es PREVENTIVA, no reparadora. Medido: `profile` tiene hoy exactamente `key`, `value`, `updated_at`, y la sentencia vieja las nombraba las tres. No se perdio ningun dato. Lo que se arregla es que haya un solo escritor y que la sentencia siga siendo correcta el dia que `profile` gane una columna.
- La prueba (caso 22 de `test_memory.py`) se monta sobre una clave que YA EXISTE y una columna extra con valor distinto de su DEFAULT. Las dos condiciones hacen falta: con clave nueva no hay conflicto y las dos sentencias escriben lo mismo — medido, las dos dan `x` — de modo que el caso daria verde con la mala dentro. Un test que pasa con el bug dentro no es un test.
- Leccion de metodo, de la misma familia que las tres anteriores del Preceptor: el prompt afirmaba que `memory.py` no tenia pareja de `leer_perfil`. La tenia (`escribir_perfil`, `memory.py:237`, +20 llamantes, presente ya en `12d6071`). El error fue buscar `def guardar_perfil` — el nombre supuesto — en vez de `def .*perfil`, la funcion que hace el trabajo. Una busqueda con la forma de la suposicion confirma la suposicion. Ejecutado al pie de la letra habria creado un segundo escritor con la misma semantica y otro nombre.

## D80b · LO QUE APAGA UNA GUARDIA Y LO QUE LOS CRITERIOS NO MIDEN, EN LA RAIZ (2026-08-16)
- `EXCEPCIONES.md` (commit `2c2c163`) y `LIMITES_DEL_CRITERIO.md` (commit `bd52d76`), los dos en la RAIZ del producto y versionados. Comprobado: `git ls-files '*.md'` da siete e incluye a ambos.
- Van a la raiz y no a `docs/` porque `docs/` esta en `.gitignore` linea 7 — por un motivo escrito dentro y correcto, que no se toca — y `git ls-files docs/` da 0. Un registro que no esta versionado no es un registro.
- `EXCEPCIONES.md`: una fila por pragma que apaga una guardia — fichero, linea, pragma, motivo, fecha. Hoy hay uno: `voz.py:43`, introducido en `73f7bc6`. El motivo dice por que ESA linea es segura (un prefijo de gestor de paquetes es igual en cualquier maquina y no describe a nadie), no que la guardia moleste. Queda escrita la orden que reconcilia la tabla con el arbol.
- `LIMITES_DEL_CRITERIO.md`: tres partes. (a) que verifican los 10 criterios de M3, uno por fila, mas los sabotajes 6/6 que les dan valor. (b) QUE NO VERIFICAN: ninguno comprueba que la persona salga sabiendo algo que no sabia al entrar, que era la razon de construir M3. Un 10/10 verde es compatible con alguien que recorre las seis salas y sale igual que entro. Sin disculpa y sin promesa: nada de «criterio 11 pendiente», que seria sustituir una medida que falta por una intencion. (c) el acta del rojo del 2026-08-16.
- Esto es doctrina de producto, no de proceso: el titular no afirma mas que la seccion que lo sostiene, y donde no hay seccion se dice que no la hay.

## D80c · TMPDIR FIJADO, Y EL ACTA DEL ROJO ENMENDADA (2026-08-16)
- Commit `fd518b6` (etiquetado «M-D80b» en su mensaje; ver el aviso de numeracion arriba). `bin/pruebas` fija `export TMPDIR="${TMPDIR:-/var/tmp}"` antes de cualquier operacion, con guarda: si no existe o no se puede escribir, para con codigo 2. <!-- guardia:permitir /var/tmp es prefijo de sistema (FHS), no el home de nadie; es el dato medido de D80c -->
- Motivo medido: `/tmp` en el Soberano es tmpfs de 29 GB — RAM — y `/var/tmp` es el NVMe. `TMPDIR` no estaba puesto, asi que `tempfile` resolvia a `/tmp` y las tandas escribian en RAM sin que nadie lo hubiera elegido ni quedara constancia. Dos tandas con el mismo numero podian no haber corrido en el mismo sitio; las salidas lo prueban (`/tmp/fuga_8dqsdn_b` en una, `/var/tmp/fuga_ligpbeb8` en otra). <!-- guardia:permitir /var/tmp es prefijo de sistema (FHS), no el home de nadie; es el dato medido de D80c -->
- ENMIENDA AL ACTA DEL ROJO, sin borrar lo anterior: el disco queda descartado (541 GB libres, cero eventos de `ENOSPC` o E/S en el journal de toda la semana, y los seis positivos del grep eran nombres de ficheros de Chromium). NO queda descartada la presion de memoria sobre `/tmp`. Un tmpfs lleno devuelve `ENOSPC` sin dejar rastro en el journal y sin disparar `oom-kill`, asi que la ausencia de registro no lo excluye: el cero es evidencia contra el disco y no es evidencia contra la RAM.
- Se corrige ademas una frase que argumentaba en la direccion contraria: «`TemporaryDirectory` ni siquiera toca el disco» se habia escrito COMO apoyo del descarte, y es el flanco. Que el temporal viviera en RAM no aleja las pruebas del problema.
- Esto NO identifica el mecanismo. Cierra una indeterminacion: si el rojo vuelve, vuelve en un sitio conocido, con espacio medido y estable. `TMPDIR` se imprime ahora en la cabecera junto al interprete, por el mismo motivo que el: «donde escribio» es parte de la maquina.
- Consecuencia honesta: las tandas anteriores a este commit corrieron en el sitio sospechoso. No las invalida, pero la serie comparable empieza aqui.

## D80d · INCIDENTE DE BORRADO DEL CLON DE TRABAJO (2026-08-16)
- Que paso: `~/p0x/aurelius-mvp` desaparecio durante una sesion. El sintoma que confundio fue que hasta `true` devolvia 1 sin salida — no es que los comandos fallaran, es que ningun comando puede arrancar en un directorio que no existe. Se resuelve con `cd`, no reviviendo nada.
- Que NO se perdio, medido en el momento: `p0x` entero y sano (canon, blueprints, doctrina, `Cuarentena/salida/` con 44 ficheros). El producto estaba empujado a GitHub (`6b354c8..73f7bc6`), asi que `git clone` lo devolvia entero. `~/.aurelius/` — lo unico irreemplazable y sin copia — intacto.
- Origen del riesgo: un `purge` de `python3.12` seguido de `autoremove -y`. La gravedad dependia de la distribucion (en 22.04 el 3.12 venia de `deadsnakes` y purgarlo no toca el sistema; en 24.04 el 3.12 ES el sistema). Se resolvio mirando `/var/log/apt/history.log` en vez de adivinar. <!-- guardia:permitir /var/tmp es prefijo de sistema (FHS), no el home de nadie; es el dato medido de D80c -->
- Leccion 1: lo unico sin copia es `~/.aurelius/`. Todo lo demas tiene remoto. El orden de comprobacion lo decide una sola pregunta — ¿esto tiene copia en algun sitio? — y se mira primero lo que no la tiene.
- Leccion 2: `autoremove` es el comando que hace el dano en cascada. No se ejecuta otro «por si acaso» mientras se diagnostica.
- Leccion 3 (la que costo la tarde): el rojo que siguio al borrado no era del codigo. Mismo clon y mismo commit en otra maquina daban VERDE. La cifra no viajaba con su interprete, y de ahi sale D79c.
- Pendiente y declarado: la prueba de recuperacion HECHA A PROPOSITO — borrar, restaurar desde el remoto, cronometrar y exigir verde — sigue sin hacerse. Es el unico test que mediria lo unico que el producto promete: que te lo llevas y vuelve.

## D80e · ESTADO VERIFICADO AL CIERRE DE LA RONDA (2026-08-16)
- Producto en `fd518b6`, arbol limpio, empujado a `origin/main` (`github.com/piskyRpapalo/aurelius`), remoto comprobado igual al local.
- **224/224 VERDE, salida 0**, 13 suites, 6 corredores, sabotajes 4/4 y 6/6.
- Reproducido de forma INDEPENDIENTE por el Preceptor sobre el arbol `5a86cc6`, en otra maquina y otro interprete (3.10.12): 224/224, salida 0. Tercera reproduccion independiente de una cifra de Claude Code en esta serie y la tercera que sale exacta.
- ACOTACION: esa reproduccion independiente es de `5a86cc6`. El commit `fd518b6` (D80c) solo esta verificado en el Soberano, en 3.14.4 y en 3.10.12. No se cuenta como verificado fuera hasta que lo este.
- El canon `p0x` NO esta empujado a `jetson`. Todo lo de esta ronda vive en un solo disco.

## D80f · EL NUMERO DEL TEST ES EL DEL CRITERIO, Y EL RANGO SON CINCO PUNTOS (2026-08-16)
- Commit `7d0a72d` del producto. Cierra dos de las tres deudas que el Soberano puso al firmar M3 (§4.2.b y §3.d de su respuesta de cierre).
- NUMERACION: `test_07` cubria el criterio 8, `test_08` el 7, `test_09` el 10 y `test_10` el 9. Nada fallaba por eso — los diez pasaban — y por eso duro: solo se ve auditando, y quien auditase por el numero del metodo concluiria que faltan criterios que estan. Renombrados los cuatro.
- Renombrar no basta porque volveria a torcerse. `test_00_el_numero_del_test_es_el_del_criterio` lo comprueba POR INTROSPECCION: lee el numero del metodo y el que declara su docstring y exige que sean el mismo, y exige ademas que esten los diez — una renumeracion que borrase uno dejaria la primera comprobacion en verde con nueve. No se usa lista escrita a mano: seria otra cosa mas que se puede desincronizar del arbol, el mismo fallo con un fichero mas.
- Verificado en los dos sentidos: verde sobre el arbol arreglado y ROJO sobre una copia donde se deshace el arreglo. Un test que pasa con el bug dentro no es un test.
- INTERPRETES: `uv run --python X.Y ./bin/pruebas` funciona. 225/225 salida 0 en 3.10.12, 3.11.16, 3.12.13, 3.13.15 y 3.14.4. El intervalo inferido de D79c pasa a CINCO PUNTOS MEDIDOS.
- Lo que fallaba era la invocacion, no `uv`: `unittest discover` corre 145 de 225 — no encuentra las cinco suites con corredor propio, que es lo que el README ya advertia — imprime su informe por salida de error mientras los casos imprimen por salida estandar, y termina en 0. De ahi que la salida mostrase el final de una fuga y ningun recuento. Un verde que cubre el 64% y no lo dice es exactamente el fallo que `bin/pruebas` existe para impedir.
- Lo que sigue SIN cubrir y se declara: las cuatro medidas con `uv` fijan el INTERPRETE, no la distribucion, y corrieron en una sola maquina. Una segunda maquina es otra medida.
- `CIERRE_M3.md` pasa a FIRMADA y conserva la trampa de numeracion como cicatriz cerrada, no borrada.
