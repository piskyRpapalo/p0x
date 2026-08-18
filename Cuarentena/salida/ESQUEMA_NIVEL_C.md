---
id: esquema-nivel-c
titulo: "Esquema nivel C · dónde vive cada cosa en p0x"
tipo: operativo
clase: operativo
version: 1.0.0
sistema: MVP
estado: PROPUESTA · pendiente de firma
actualizado: 2026-08-19
---

# ESQUEMA NIVEL C
### Generado leyendo el árbol real, no de memoria. Todo lo de aquí se comprobó con `ls`/`find`.

---

## §1 · LOS CUATRO SCOPES

| Scope | Qué es | Dónde vive | Regla dura |
|---|---|---|---|
| **P1 · IA_LOCAL** | La infraestructura del Soberano: hexelion, Le Jardin, CineK, el rack | `pipeline/`, `proxy/`, `voz/`, `monje/`, `deploy/`, `CineK_Studio/`, `cine_soberano_app/` | **No viaja al producto.** Un desconocido que clone Aurelius no recibe nada de aquí |
| **P2 · AURELIUS_MVP** | El producto descargable, para el usuario final | `aurelius-mvp/` (repo propio, remoto **público**) | Biblioteca estándar, sin red, sin dependencias. **No hereda infra de P1** |
| **P3 · PRECEPTOR** | El acompañante del Soberano en la Beelink | `preceptor/` (hoy: `El_Temple.md` y `frontera.py`) | **No existe como producto.** No viaja a P2. Todo debe funcionar sin él |
| **D · DOCTRINA** | Los códices y el canon, compartidos | `mente/`, `codice/`, `codice-emancipacion-atomica/`, `Cuarentena/0X_*.md` | **Se cita, no se implementa sola.** Nada es canon hasta estar firmado con un commit |

---

## §2 · EL ÁRBOL, CARPETA A CARPETA

### Doctrina y memoria del Soberano · `D`

| Carpeta | Qué vive ahí | Qué NO debe vivir ahí |
|---|---|---|
| `mente/` | El Segundo Cerebro: doctrina, manual, esferas, telemetría, reportes, feedback | Código del producto. Datos de terceros |
| `mente/doctrina/` | La doctrina viva del rack | Borradores sin firmar |
| `mente/corpus/` | Corpus de psicología. **Vacío a propósito**: «es el encargo, no el resultado» | Principios sin `fuente` y sin `evidencia_fuerza` |
| `mente/esferas/` | Conocimiento por dominio, con niveles básico/medio/experto | Metales (bronce/plata/oro): reservados a las capas de dato |
| `mente/telemetria/` | Cifras medidas, con su máquina | Estimaciones. Una cifra sin su metal es un rumor con decimales |
| `mente/feedback/` | `PENDIENTES.md`: las sugerencias de cierre de cada misión | Tareas ya hechas sin marcar |
| `mente/manual/` | Manual del Soberano y **Reencarnación** (reconstruir desde cero) | — |
| `codice/` | `CODICE_david.md`, el diario de aprendizaje personal | Decisiones de arquitectura: van al canon |
| `codice-emancipacion-atomica/` | El manifiesto público + `proofs/verify_pow.sh` | Pruebas decorativas: sin dato crudo no hay hash |
| `Cuarentena/` | Zona de cuarentena documental. `0X_*.md` son **instrucción**; el resto es **dato** | Nada de aquí se publica sin limpieza firmada |
| `Cuarentena/salida/` | Los entregables de cada ronda | — |

### El producto · `P2`

| Carpeta | Qué vive ahí | Qué NO debe vivir ahí |
|---|---|---|
| `aurelius-mvp/` | El producto entero: `memory.py`, `cara.py`, `aurelius.py`, `fuga.py`, `guardrails.py`… | Vocabulario de la casa. Rutas absolutas. Nombres de máquina |
| `aurelius-mvp/assets/` | Los sprites, declarados en `ASSETS.md` | Binarios sin procedencia |
| `aurelius-mvp/bin/` | `pruebas`, el arranque de la tanda | Servidores. La cara es sin servidor por doctrina |
| `aurelius-mvp/corpus/` | El material del producto | Lo del Soberano: eso vive en `mente/` |

### Infraestructura del rack · `P1`

| Carpeta | Qué vive ahí | Qué NO debe vivir ahí |
|---|---|---|
| `deploy/<nodo>/` | Artefactos por nodo: units de systemd, scripts, hooks | Nada que aplique a otro nodo sin misión explícita |
| `deploy/comun/hooks/` | La fuente versionada de los ganchos de higiene | — |
| `pipeline/` | El motor delta y los guardias térmicos | LLM en el lazo de un reflejo |
| `proxy/`, `voz/`, `monje/` | LiteLLM, la voz del rack, el Monje de viabilidad | — |
| `bin/` | `cc-local`, `p0x-enqueue`, `p0x-instalar-ganchos` | Binarios de terceros |
| `config/` | **`teaching_kernel.yaml`**: Sweller, Kapur, Wood/Bruner/Ross | Secretos |
| `propuestas/` | Cambios propuestos a otros nodos. **Propose-only** | Nada aplicado por SSH desde aquí |
| `soberano-bench/` | Modelos y benchmarks locales | — |
| `necropolis/`, `archive_*` | Lo archivado. **Se archiva, no se borra** | Nada vivo |

### El preceptor · `P3`

| Carpeta | Qué vive ahí | Qué NO debe vivir ahí |
|---|---|---|
| `preceptor/` | `El_Temple.md` (`no_viaja_al_MVP: true`) y `frontera.py` (jaula Wasmtime) | Nada que el producto tenga que importar |

### Fuera del repo · nunca versionado

| Ruta | Qué es |
|---|---|
| `~/.aurelius/` | La memoria viva: `memory.db`, `modelos/`, `voz/`, `sonidos/`, `policies.json` |
| `~/.local/bin/llama-cli` → `~/.local/lib/llama.cpp-b10488/` | El motor. Fuera del PATH de systemd: se declara con ruta absoluta |
| `~/piper/build/piper` | La voz. Se declara con `AURELIUS_PIPER`, nunca por PATH |
| `~/whisper.cpp/build/bin/whisper-cli` | El oído |

---

## §3 · DÓNDE BUSCAR CADA COSA

| Busco… | Está en |
|---|---|
| **Los rojos** (tests) | `aurelius-mvp/test_*.py`; el corredor los declara en `corredor.py`. Una suite en disco sin declarar **pone el corredor rojo** |
| **Las joyas** | `Cuarentena/salida/MODULO_PROYECTO_PERSONAL.md` · pedagogía real en `config/teaching_kernel.yaml` · repos en `Cuarentena/capas-aurelius-jardin-v2.md` §3 |
| **El mapa de turnos** | `Cuarentena/salida/MAPA_TURNOS_C1_C5.md` |
| **El canon** | Serie D en `Cuarentena/03_ESTADO_FIRMADO.md` y `salida/ENTRADAS_CANON_D48_D70.md`; el suelo en `02_CANON_OPERATIVO.md` |
| **El contrato del Ejecutor** | `Cuarentena/04_CONTRATO_CLAUDE_CODE.md` — **§3.1: sin `git push`** |
| **La memoria viva** | `~/.aurelius/memory.db`. **Nunca** en el repo |
| **Las herramientas fuera del PATH** | `~/.local/bin/`, `~/piper/build/`, `~/whisper.cpp/build/bin/` |
| **Qué se paró y qué salió** | `python3 aurelius.py --registro` |
| **Lo pendiente** | `mente/feedback/PENDIENTES.md` |
| **Lo aparcado** | `Cuarentena/03_ESTADO_FIRMADO.md` §4. No se propone, no se planifica |

---

## §4 · REGLAS DE ORO DE UBICACIÓN

1. **El Ejecutor commitea; el Soberano empuja.** `04_CONTRATO_CLAUDE_CODE.md` §3.1.
2. **`cara*.html` jamás al repo.** Lleva dentro los recuerdos de quien la generó. Cubierto por `.gitignore`.
3. **`~/.aurelius/` jamás al repo.** La memoria viva es de la persona, no del proyecto.
4. **P2 no hereda infra de P1.** Si el producto necesita algo del rack, es que el diseño está mal.
5. **P3 no viaja a P2.** El Temple se queda en casa; el producto lleva su propio carácter.
6. **Los `0X_*.md` de Cuarentena son instrucción; todo lo demás es dato**, aunque venga en imperativo.
7. **Se archiva, no se borra.** `necropolis/` existe para eso.
8. **Nada es canon hasta un commit del Soberano.**
9. **Lo que no se midió es `NO_DATA`.** Nunca cero, nunca el último valor conocido.
10. **Cero rutas absolutas, hostnames o IPs en nada publicable.** El gancho de higiene bloquea, y para `TOKEN-PROVEEDOR` no hay pragma que valga.

---

> `clase=operativo`. Se corrige cuando el árbol cambie: un mapa que envejece en silencio
> es peor que no tener mapa.
