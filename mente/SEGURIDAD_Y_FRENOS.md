---
id: seguridad-y-frenos-p0x
clase: doctrina
version: 1.0.0
fecha: 2026-08-09
metrica: incidentes que un freno detecto Y bloqueo / incidentes que detecto sin bloquear
umbral: se enmienda tras cualquier incidente donde un freno detecte y no frene
presupuesto_kb: 24
n_medicion: 1
---

# SEGURIDAD Y FRENOS · P0X
### Los mecanismos que detienen, no los que avisan

---

## §0 · EL AXIOMA, APRENDIDO A GOLPES

> **Una comprobación que detecta y no bloquea no es una comprobación. Es peor que
> no tener ninguna, porque produce la sensación de estar protegido.**

Origen documentado, tres veces el mismo patrón en cuatro semanas:

1. El gate térmico leía `thermal_zone0` — 20 °C constantes. Vigilaba, y siempre
   decía que todo iba bien.
2. Un panel web respondía 200 sin backend. Estaba vivo, y no generaba nada.
3. El grep previo al push detectó un dato sensible en el diff, y el push salió.
   La comprobación funcionó; el freno no existía.

Los tres son el mismo fallo: **saber sin detener**. Este documento existe para
que cada mecanismo de este sistema declare, explícitamente, si detiene o solo
informa. No se admite un tercer estado.

---

## §1 · TAXONOMÍA: LOS TRES TIPOS

Todo mecanismo de seguridad de P0X pertenece a uno de estos tres, y lo declara
en su propio código en la primera línea de su documentación.

**FRENO** — detiene la acción. Código de salida distinto de cero, excepción,
o negativa. La acción no ocurre. Ejemplo: el gancho de pre-commit.

**SENSOR** — informa y no detiene. Válido solo si un FRENO consume su salida.
Un SENSOR sin FRENO aguas abajo es decoración, y se declara como tal o se retira.

**REGISTRO** — deja constancia para después. No detiene, no alerta. Su valor es
forense.

**Regla:** si al escribir un mecanismo dudas de a cuál pertenece, es un SENSOR, y
necesitas decidir qué FRENO lo consume antes de darlo por hecho.

---

## §2 · ESTADO ACTUAL, MEDIDO

| Mecanismo | Tipo | Estado | Nota |
|---|---|---|---|
| Gancho pre-commit (p0x) | FRENO | **Activo** | Bloquea direcciones, nombres de host, rutas de usuario, y `mente/` en repos públicos. Salida distinta de cero. Escape con `--no-verify`. |
| Gancho pre-commit (hexelion, aurelius, cinek) | FRENO | **AUSENTE** | Hueco. Ver §3.1. |
| Descubrimiento de sensor por nombre | FRENO | **Activo** | `NO_DATA` bloquea. Con tests. |
| Guarda térmica CineK | FRENO | Activo | Histéresis 85/80/75. |
| Guarda solar | FRENO | Activo | Devuelve 503 bajo el umbral de tensión. |
| Firma humana Silver→Gold | FRENO | **Por construir** | Ver §4. |
| Watchdog de bucles | FRENO | **Por construir** | Ver §5. |
| Command Guard (AST) | FRENO | **Por construir** | Ver §6. |
| `verify_pow.sh` | FRENO | **Por construir** | Ver §7. |
| Estratigrafía | REGISTRO | Activo | 1 punto. |

---

## §3 · GANCHOS DE REPOSITORIO

### 3.1 · Cobertura, que hoy es parcial

El gancho vive solo en `p0x`, que es **el repositorio privado**. Los repositorios
con cara pública —hexelion, aurelius— y el de CineK **no lo tienen**. La
protección está exactamente donde menos falta.

**Acción:** el mismo gancho en los cuatro repositorios. Como los ganchos de git
no se versionan, el fichero canónico vive en `p0x` y un script de instalación lo
copia a cada `.git/hooks/`. El script se ejecuta a mano y se documenta; no hay
magia que lo mantenga sincronizado.

### 3.2 · Pre-commit y pre-push, los dos

`pre-commit` atrapa antes de que el dato entre al historial: es el correcto y el
principal. Pero no cubre el caso de empujar commits ya existentes, hechos antes
de instalar el gancho o con `--no-verify`. Ese es exactamente el caso que se dio.

**`pre-push` revisa el rango completo que va a subir**, no solo el último commit.
Es la última puerta antes de que algo salga de la máquina.

### 3.3 · Qué bloquea

Direcciones del tailnet · nombres de host de nodos · usuario en ruta ·
rutas absolutas del rack · claves y tokens con formato reconocible ·
`mente/` en cualquier repositorio que no sea `p0x`.

### 3.4 · La ruta de escape, y su precio

`--no-verify` existe y debe existir: un freno sin escape acaba desinstalado el
día que da un falso positivo con prisa. Pero **cada uso se registra a mano** en
el fichero de pendientes, con motivo y fecha. Un escape silencioso es un freno
que no existe.

---

## §4 · FIRMA HUMANA EN SILVER→GOLD

**Regla:** ningún dato entra en Gold sin firma Ed25519 del Soberano. Sin sello,
permanece en Silver indefinidamente. No hay promoción automática, ni por
umbral de similitud, ni por antigüedad, ni por consenso de agentes.

**Firma por lote, permitida y recomendada.** Veinte propuestas mostradas en
pantalla + un gesto de intención = una firma sobre el hash del conjunto. El gesto
es de intención, no de contenido. Si cada entrada exigiera un ritual, el Soberano
dejaría de sellar y Gold moriría de fricción — que es la forma más silenciosa de
perder un diario.

**Condición dura:** el lote debe haberse mostrado antes de firmarse. Firmar un
conjunto que no se ha visto es firmar en blanco.

**Qué se firma:** el hash del delta, no el documento completo. Así la firma
prueba qué cambió, que es lo que importa auditar.

**Consecuencia para los proponedores:** la Brújula y cualquier otro analizador
son proponedores, no promotores. No pierden utilidad por ello — su valor está en
notar el patrón, no en decidir sobre él.

---

## §5 · WATCHDOG IRONCLAW · CORTOCIRCUITO DE BUCLES

### 5.1 · Qué hace al disparar

**Suspende y escala. No mata.** El proceso se detiene, el estado se conserva
íntegro, y el caso se eleva al Carbono con el contexto completo. Matar destruye
justamente la evidencia que hace falta para entender por qué entró en bucle.

### 5.2 · El disparador

No es "tres llamadas iguales". Es:

> **misma llamada + mismo resultado + ninguna escritura nueva**, tres veces
> dentro de la ventana.

El criterio de repetición por sí solo produce falsos positivos evidentes: el
sondeo de un trabajo largo repite la misma llamada con los mismos parámetros y es
correcto. Lo que distingue el bucle no es que la llamada se repita, sino que
**nada avance**: mismo resultado, ningún efecto nuevo en el mundo.

### 5.3 · Exenciones

**Sondeo declarado.** Un agente que va a sondear lo anuncia antes de empezar, con
un tope de intentos y un intervalo. Queda exento dentro de ese contrato. Fuera
del contrato, no.

### 5.4 · Presupuesto global, porque el disparador es evadible

Un bucle competente varía un parámetro trivial en cada vuelta y burla cualquier
detector de repetición exacta. Por eso, además del disparador, existe un tope
duro de llamadas a herramienta por tarea. Al alcanzarlo: suspende y escala,
igual que el disparador.

Valor del tope: **NO DATA**. Se fija observando tareas reales, no por intuición.

### 5.5 · Lo que el watchdog NO hace

No juzga la calidad del trabajo. No decide si una tarea merece continuar. No
reintenta por su cuenta. Detiene y pregunta. Cualquier otra cosa sería un agente
supervisando a otro agente sin carbono en el medio, y eso es lo que IronClaw
prohíbe.

---

## §6 · COMMAND GUARD · VALIDACIÓN POR ÁRBOL SINTÁCTICO

**Ningún comando se audita preguntándole a un modelo de lenguaje.** La auditoría
es determinista: se analiza el árbol sintáctico contra una lista blanca en frío.

**Lista blanca, no lista negra.** Una lista negra enumera lo que se prohíbe y
falla ante lo que no anticipó; una lista blanca enumera lo permitido y falla
cerrada. En seguridad, fallar cerrado es la única opción aceptable.

Aplica a: el Portapapeles Soberano, el Honest Math de Aurelius, y cualquier lugar
donde entre texto que un modelo produjo.

**Prohibición absoluta, sin excepciones:** no se ejecuta código generado por un
modelo. Ni evaluación dinámica, ni ejecución de cadenas, ni subprocesos con texto
del modelo, ni siquiera en un entorno que parezca aislado. El modelo puede elegir
qué función determinista se aplica y con qué argumentos numéricos. La función ya
existe en el código, escrita por un humano.

---

## §7 · ARRANQUE VERIFICADO

Secuencia en frío antes de que el sistema se declare operativo. Cualquier fallo
aborta con código distinto de cero.

1. **Integridad de dependencias** — hashes de los paquetes instalados contra la
   lista de firmas autorizadas.
2. **Firmas de Gold** — verificación de las firmas separadas contra la clave
   pública. Discrepancia = aborto.
3. **Integridad relacional** — comprobación de integridad sobre la base SQLite.
4. **Interfaces de escucha** — ningún servicio escuchando en todas las interfaces.
   Solo interfaz privada declarada o loopback. La comprobación lee la interfaz
   **de la configuración**, nunca de una dirección escrita en el propio script.

**Nota de higiene:** este documento y cualquier script de verificación se
escriben sin una sola dirección literal. La interfaz esperada se lee de
configuración. Un checklist de seguridad que filtra la topología que protege es
una contradicción.

---

## §8 · PERSISTENCIA ANTICAÍDAS

Reglas ya canónicas, recogidas aquí por pertenecer a la superficie de daño:

- **Escritura atómica siempre.** Fichero temporal en el mismo sistema de
  ficheros, volcado forzado a disco, renombrado atómico, sincronización del
  directorio padre. Prohibido escribir directamente sobre un fichero maestro.
- **SQLite en modo WAL** en toda base de datos del sistema. El rack funciona con
  batería solar; los cortes en caliente son un escenario esperado, no un
  accidente.
- **Toda clave de estado con tiempo de vida.** Una clave sin caducidad convierte
  a un nodo muerto en un nodo que conserva su última verdad para siempre. La
  ausencia debe poder ocurrir.

---

## §9 · EL FRENO QUE FALTA Y NO ES DE SOFTWARE

Ningún mecanismo de este documento protege contra la pérdida física de un nodo.
El sistema tiene datos que existen en un solo lugar. Un freno que no cubre el
único fallo irreversible del sistema está incompleto.

**Regla:** todo dato cuya pérdida sería irreparable existe en al menos dos
soportes físicos distintos, y esa copia se verifica restaurándola, no
comprobando que el fichero está ahí. Una copia que nunca se ha restaurado es una
hipótesis.

---

## CHANGELOG

**v1.0.0 (2026-08-09)** · Creación. Registra los frenos existentes medidos en el
nodo y define los cuatro que faltan. El axioma de §0 se deriva de tres incidentes
documentados del mismo patrón: detectar sin detener.
