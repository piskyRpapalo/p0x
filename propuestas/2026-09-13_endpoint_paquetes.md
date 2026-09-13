# Propuesta · el endpoint que recibe los paquetes firmados

**Propose-only.** El Ágora vive en `deploy/fragua/agora_api.py`, o sea en
**la-fragua**, y desde `soberano` eso es propose-only por canon. Se escribe aquí;
lo aplica quien tenga esa consola.

**Firmado por el Soberano el 2026-09-13**, con estas palabras:

> *«si un usuario actúa en la web durante una hora de paquetes, debe tener una
> posibilidad de enviarlas. El Rack se ocupa del reto. Es human in the loop, pero
> accesibilidad a review»*

---

## Lo primero: qué cambia y qué no

**No cambia la promesa.** La web sigue sin rastrear, sin cuenta y sin telemetría.
Lo que viaja lo **manda la persona pulsando un botón**, va firmado con su clave, y
lleva `consent: 1` puesto por ella en el momento de enviarlo.

**No cambia el human-in-the-loop.** Este endpoint **no publica nada**. Encola. Lo
que entra espera a que una persona lo mire, igual que el dataset del laboratorio
espera la firma del Soberano.

**Sí cambia una cosa, y hay que decirla:** hasta hoy el contenido de una
corrección no salía del aparato de nadie. A partir de aquí sale — **cuando se
pulsa**. Por eso el botón dice antes lo que hace, y por eso `consent` nace en 0 y
solo sube al enviar.

---

## Lo que ya está hecho, en la web

`public/assets/enviar.js`, desplegado hoy, habla **el protocolo que el Ágora ya
tiene**:

1. `GET /api/v1/reto` → nonce de un solo uso, 300 s de vida.
2. Firma `pseudonimo|clave_publica|reto` con Ed25519 en el navegador.
3. `POST /api/v1/paquetes` con la firma, la clave pública y los pares.

Y **degrada diciendo la verdad**: hoy ese POST devuelve 404, y la página lo dice
con su código y ofrece la exportación. El día que el endpoint exista, el botón
funciona **sin tocar la web**.

---

## Lo que falta, y va en la-fragua

```python
# En deploy/fragua/agora_api.py, junto a los demas endpoints.
#
# NO PUBLICA. Encola. Es la diferencia entre un buzon y un tablon, y aqui hace
# falta un buzon: el Agora declara «escritura cerrada: todavia no modera», y
# recibir no es publicar.
class PaqueteEntra(BaseModel):
    pseudonimo: str
    clave_publica: str = Field(pattern=r"^[0-9a-fA-F]{64}$")
    reto: str
    firma: str
    esquema: str
    pares: list[dict]


@app.post(f"/api/{VERSION}/paquetes", status_code=202)
def recibir_paquetes(p: PaqueteEntra):
    # 202 y no 201: Accepted, no Created. Lo que llega NO existe todavia para
    # nadie -- espera revision. Un 201 prometeria que ya esta publicado.
    if not verificar(p.pseudonimo, p.clave_publica, p.reto, p.firma):
        raise HTTPException(401, {"estado": "NO_DATA",
                                  "causa": "la firma no cubre ese reto"})
    # EL TOPE ES POR PETICION, NO POR PERSONA. Contar por identidad exigiria
    # guardar quien manda cuanto, y eso es justo el registro que esta casa no
    # lleva. Un tope por peticion protege el disco sin saber de nadie.
    if len(p.pares) > 200:
        raise HTTPException(413, {"estado": "NO_DATA",
                                  "causa": "mas de 200 pares en una peticion"})
    destino = DATOS / "paquetes"          # guardia:permitir ruta del nodo destino
    destino.mkdir(parents=True, exist_ok=True)
    # El nombre lleva la huella de la clave y NO el pseudonimo: el pseudonimo se
    # elige y puede repetirse; la huella no.
    huella = hashlib.sha256(bytes.fromhex(p.clave_publica)).hexdigest()[:16]
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    fichero = destino / f"{sello}-{huella}.json"
    fichero.write_text(json.dumps(p.model_dump(), ensure_ascii=False), "utf-8")
    return {"estado": "EN_COLA", "recibidos": len(p.pares),
            "fichero": fichero.name,
            "aviso": "recibido y en cola de revision. No se ha publicado nada."}
```

**El usuario de la-fragua es `ubuntu`, no `pisky`.** Los paquetes van a
`/mnt/nvme/agora_db/paquetes/` <!-- guardia:permitir la ruta del nodo destino ES el contenido de la propuesta -->
salvo que `AGORA_DATOS` diga otra cosa. Escrito entero y sin `~`, que se expande
al usuario que ejecuta y es justo donde se cuela el error.

---

## De la Fragua al laboratorio · la review

Lo que se encola **no entra solo** en la pool. El camino es el que ya existe y
está probado:

1. Los ficheros bajan de la-fragua al rack (el mismo canal por el que se traen
   las medidas; propose-only en el otro sentido).
2. `hexelion/laboratorio/ingesta.py` los verifica **uno a uno**: firma Ed25519
   contra la clave pública que traen, `canonico` contra `par`, `consent: 1`, y
   sin duplicar.
3. Lo que no pasa se anota en `progreso/rechazos.md` **con su causa**.
4. Lo que pasa entra a la pool y espera el ciclo de `turnos.py`, que sigue
   terminando en la bandeja de firmas.

**Tres puertas antes de que nada cuente**, y ninguna es automática del todo: el
rack recibe, el laboratorio verifica, y el carbono firma.

---

## Lo que este endpoint NO hace, escrito para que no se pida después

- **No responde qué se hizo con tu paquete.** Eso es el canal de recibos, y no
  existe. Se declara `NO_DATA` en la web.
- **No cuenta por persona.** Ni cupos, ni reputación, ni historial. Contar exige
  guardar quién eres, y aquí nadie lo guarda.
- **No modera.** Recibe. La moderación está en
  `config/agora-niveles.json`, sin firmar, con sus tres decisiones pendientes.
