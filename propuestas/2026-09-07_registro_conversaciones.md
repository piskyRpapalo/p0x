# Propuesta · el registro de conversaciones y la AI revisora

**Propose-only.** El API del Ágora vive en `deploy/fragua/agora_api.py`, o sea en
**la-fragua**, y desde `soberano` eso es propose-only por canon. El endpoint se
escribe aquí; lo aplica quien tenga esa consola.

---

## Lo primero, porque cambia si esto se hace o no

**Hoy la web le dice al visitante que no hay registro.** No es una suposición: está
en el `SYSTEM` del modelo que atiende, palabra por palabra —*«No hay cuenta ni
registro, y aquí cada visita empieza en blanco»*— y es lo que el modelo responde
cuando alguien pregunta.

Y `corregir.js` lo dice más fuerte todavía, en su propia cabecera:

> *«NO ES TELEMETRÍA, Y NO POR PROMESA SINO POR CONSTRUCCIÓN: aquí dentro no hay
> un `fetch`, ni un `XMLHttpRequest`, ni un `sendBeacon`. **El gate lo comprueba
> leyendo este fichero.**»*

El paso 3.2 del encargo —un `fetch` fire-and-forget tras cada respuesta— guarda
`user_prompt` y `model_response` **enteros** en un servidor. Eso no es «solo
patrones»: es el contenido. Y las preguntas de la gente traen datos personales
sin que nadie se lo proponga, porque para pedir ayuda hay que contar el caso.

**No estoy diciendo que no se haga.** Es tu producto y tus testers, y hay una
razón buena para hacerlo: sin conversaciones reales no hay forma de arreglar el
modelo. Lo que digo es que **hacerlo en silencio convierte al producto en lo que
existe para combatir**. Un sitio que promete no registrar y registra no tiene un
problema de privacidad: tiene un problema de verdad.

**El arreglo cuesta una frase**, y esta casa ya la sabe escribir: *se dice
antes*. Tres condiciones, y con ellas la propuesta de abajo es coherente con
todo lo demás:

1. **El `SYSTEM` del modelo deja de decir que no hay registro** y pasa a decir
   qué se guarda y para qué. Un `ollama create`.
2. **La página lo dice donde se escribe**, junto al campo del chat, no en un
   documento legal que nadie abre.
3. **Se puede decir que no.** Un interruptor en la rueda de ajustes, apagado o
   encendido según decidas — pero que exista. Sin él, «soberanía» es una palabra
   del cabecero.

Mientras eso no esté, **el gancho del frontend no se ha escrito**. El endpoint y
el revisor sí: no mueven ni un dato de nadie hasta que alguien los conecte.

---

## Lo que YA está hecho y funcionando, aquí

`scripts/revisor_ia.py`, probado hoy de punta a punta:

- SQLite en `~/.preceptoros/conversaciones.db` **con FTS5**, y el esquema lo crea
  el propio guion.
- Lee hasta 50 sin revisar, se las pasa a **`llama3.2:3b`** en la Ollama de esta
  máquina —2 GB, y **no** `preceptor-v7`, que pesa lo mismo pero está entrenado
  para decir `NO_DATA`, que es la conducta que arruina un análisis—.
- Escribe **añadiendo** a `mente/revision_conversaciones.md`, nunca reescribe.
- Marca las revisadas. Si el modelo no devuelve JSON, **no marca nada**: se
  reintenta en la pasada siguiente en vez de perder el lote.
- `--buscar TEXTO` da la búsqueda FTS5 en la terminal.
- Sin `--ejecutar` cuenta y para.

Ni una llamada fuera de `127.0.0.1`. Se ve en el diff, no en una promesa.

**Y ya ha servido para algo.** En su primera pasada, sobre seis conversaciones
reales de anoche, sugirió por su cuenta: *«Agregar una instrucción para que el
asistente indique cuando el usuario ya ha instalado el software y no lo repita»*
— el fallo exacto que llevo toda la sesión persiguiendo.

## Lo que falta, y va en la-fragua

```python
# En deploy/fragua/agora_api.py, junto a los demas endpoints.
#
# APPEND-ONLY: solo INSERT. No hay UPDATE ni DELETE, igual que `dead_path.jsonl`.
# Un registro que se puede editar no es un registro, es un borrador.
@app.post(f"/api/{VERSION}/conversation-log", status_code=201)
def registrar_conversacion(c: ConversacionEntra):
    with sqlite3.connect(BASE_CONV) as con:
        con.execute(
            "INSERT INTO conversaciones (timestamp, model_used, user_prompt,"
            " model_response, user_hash, session_id) VALUES (?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"),
             c.model_used, c.user_prompt, c.model_response,
             c.user_hash, c.session_id))
    return {"guardado": True}
```

**Y el usuario de la-fragua es `ubuntu`, no `pisky`.** Lo dice `~/.ssh/config`
(`Host la-fragua` → `User ubuntu`), y aquí importa de verdad porque este endpoint
sí escribe en el home de allá: la base va en **`/home/ubuntu/.preceptoros/`** <!-- guardia:permitir la ruta del nodo destino ES el contenido de la propuesta -->
**`conversaciones.db`**, y no en el home de este nodo. Escrito con la ruta entera y no
con `~`, que se expande al usuario que ejecuta y es justo donde se cuela el
error. Si el API corre bajo systemd, su unidad lleva `User=ubuntu` y
`Group=ubuntu` — eso es una unidad de SISTEMA en la Fragua, distinta de la
unidad `--user` del buzón del Soberano, donde `User=` ni siquiera está
permitido.

El esquema es el mismo de `scripts/revisor_ia.py` — se copia de ahí, no se
reescribe: dos esquemas para la misma tabla es el sitio donde un día se pierde
un campo.

**Y el cron NO se propone todavía.** El canon pide firma explícita para cada
unidad, una por una, y anotarla en `deploy/soberano/unidades.md`. El revisor se
ejecuta a mano hasta que se vea funcionar unas cuantas veces; cronificarlo es un
paso aparte y posterior.

---

## Lo que se verificó y no hacía falta arreglar

- **Las pestañas no están caídas.** `/es/community.html`, `/es/benchmark.html` e
  `/es/instalar.html` devuelven **307** —Cloudflare quitando el `.html`— y acaban
  las tres en **200**. `/comunidad`, `/loratelier` y `/taller` dan 404 porque
  nunca existieron: el menú usa `/es/community`, `/es/benchmark`, `/es/instalar`.
  Crear placeholders habría gastado el presupuesto de 9/9 páginas para arreglar
  algo que funciona.
- **No han llegado firmas de testers porque no hay dónde.** `/api/v1/medidas`
  sigue en **404**. La consulta del encargo no puede correr: la tabla no está
  vacía, no existe.
- **Catppuccin Mocha no se ha aplicado.** El canon visual firmado es la v3.0
  «Liquid Glass» —violeta, oro y bronce, con `--radius` y `backdrop-filter`— y
  hay un test del gate que lo hace cumplir. Meter una paleta ajena habría puesto
  el gate en rojo y roto la identidad. Las tarjetas nuevas usan los tokens de la
  casa.
