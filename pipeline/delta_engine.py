#!/usr/bin/env python3
"""delta_engine.py — P0X misión OBSERVAR (Bloque B, núcleo).

Transcript → delta clasificado contra la mente (Qdrant `mente`):

  MAP       1 llamada LLM por ventana (~450 tok) → claims relevantes al FOCO
  RETRIEVE  embed `search_query:` (reusa mente/pipeline/embed.py) + Qdrant top-k
  CLASSIFY  híbrido: score>=umbral_ya_sabido → YA_SABIDO con citas [id#chunk];
            score<=umbral_nuevo → NUEVO; zona gris → juez LLM (retry 1,
            fallback NUEVO+flag). CONEXIÓN si >=2 ids distintos >= umbral.
  REDUCE    2 llamadas: destino (esfera existente/nueva, slugs validados) +
            redacción del cuerpo en español.

El front-matter y la sección "Lo que ya sabías" se ensamblan en PYTHON —
jamás YAML del modelo. keep_alive:0 en la última llamada (libera RAM).
Scores crudos persistidos en delta.json para calibrar umbrales con dato.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import date
from pathlib import Path

import yaml

PIPE = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPE))
sys.path.insert(0, str(PIPE.parent / "mente" / "pipeline"))

import observar_lib as ol  # noqa: E402
from embed import embed_text  # noqa: E402
from to_qdrant import COLLECTION, get_client  # noqa: E402

CFG = yaml.safe_load((PIPE / "delta_config.yaml").read_text(encoding="utf-8"))
OLLAMA = "http://localhost:11434/api/chat"
ESFERAS_DIR = PIPE.parent / "mente" / "esferas"

_llm_calls = 0
_thermal_cb = None  # inyectado por el runner: se invoca cada 10 llamadas LLM
_pacing_cb = None   # inyectado por el runner (#20): antes de CADA llamada LLM


def set_thermal_callback(cb) -> None:
    global _thermal_cb
    _thermal_cb = cb


def set_pacing_callback(cb) -> None:
    global _pacing_cb
    _pacing_cb = cb


def _slug(texto: str) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:48] or "sin-titulo"


def esferas_reales() -> list[str]:
    return sorted(p.stem for p in ESFERAS_DIR.glob("*.md"))


def _llm(prompt: str, dom: str, op: str, keep_alive="5m") -> tuple[str, dict]:
    """Llamada LLM con telemetría lengua.jsonl y guard térmico inyectado."""
    global _llm_calls
    _llm_calls += 1
    if _pacing_cb:
        _pacing_cb()  # pacing primero: el guard de abajo mide temp ya enfriada
    if _thermal_cb and _llm_calls % 10 == 0:
        _thermal_cb()
    body = json.dumps({
        "model": CFG["model"],
        "messages": [{"role": "user", "content": prompt}],
        "stream": False, "keep_alive": keep_alive,
        "options": {"temperature": CFG["temperature"],
                    "num_ctx": CFG["num_ctx"]},
    }).encode()
    t0 = time.time()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        resp = json.loads(r.read())
    ms = int((time.time() - t0) * 1000)
    content = resp.get("message", {}).get("content", "")
    ol.telemetria_lengua(dom, op, resp.get("prompt_eval_count", 0),
                         resp.get("eval_count", 0),
                         valida=bool(content), ms=ms)
    return content, resp


def _json_del_modelo(s: str):
    """Extrae el primer objeto JSON de una respuesta de modelo. None si no hay."""
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.S)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        i, j = s.find("{"), s.rfind("}")
        if 0 <= i < j:
            try:
                return json.loads(s[i:j + 1])
            except json.JSONDecodeError:
                return None
    return None


# ── 1 · Transcript → ventanas ───────────────────────────────────────────────

def cargar_transcript(video_id: str) -> str:
    p = ol.transcript_path(video_id)
    if p is None:
        raise FileNotFoundError(f"sin transcript para {video_id}")
    if p.suffix == ".txt":
        return p.read_text(encoding="utf-8")
    data = json.loads(p.read_text(encoding="utf-8"))
    segs = data.get("transcription") or []
    return " ".join(s.get("text", "").strip() for s in segs)


def ventanas(texto: str) -> list[str]:
    """Ventanas de ~ventana_tokens (aprox 0.75 palabras/token). Sin
    SemanticChunker a propósito: coste de embed prohibitivo en habla."""
    palabras = texto.split()
    paso = max(50, int(CFG["ventana_tokens"] * 0.75))
    return [" ".join(palabras[i:i + paso])
            for i in range(0, len(palabras), paso)]


# ── 2 · MAP: claims por ventana ─────────────────────────────────────────────

PROMPT_MAP = """Eres el extractor de afirmaciones del motor delta de P0X.

FOCO del Soberano (criterio de relevancia): {foco}

VENTANA {idx}/{total} del transcript:
---
{ventana}
---

Extrae las afirmaciones sustantivas de ESTA ventana relevantes al FOCO.
Responde SOLO con JSON válido, sin markdown:
{{"claims": [{{"texto": "afirmación en español, autocontenida", "relevancia_foco": 0.0}}]}}
Máximo 6 claims por ventana. relevancia_foco entre 0 y 1. Si nada es relevante: {{"claims": []}}"""


def map_claims(job_id: str, texto: str, foco: str) -> list[dict]:
    vs = ventanas(texto)
    claims: list[dict] = []
    for i, v in enumerate(vs):
        if len(claims) >= CFG["max_claims"]:
            ol.log_runner(job_id, f"MAP: cap max_claims={CFG['max_claims']} alcanzado en ventana {i}")
            break
        ol.sobre_alfabeto(job_id, "delta", "ingesta",
                          {"src": f"ventana:{i}", "vs": "mente"},
                          "{claims:[{texto,relevancia_foco}]}")
        content, _ = _llm(PROMPT_MAP.format(foco=foco, idx=i + 1,
                                            total=len(vs), ventana=v),
                          "ingesta", "delta")
        parsed = _json_del_modelo(content)
        lote = (parsed or {}).get("claims")
        if not isinstance(lote, list):
            ol.log_runner(job_id, f"MAP ventana {i}: JSON inválido, descartada")
            continue
        for c in lote:
            t = (c.get("texto") or "").strip() if isinstance(c, dict) else ""
            if t:
                claims.append({"texto": t,
                               "relevancia_foco": c.get("relevancia_foco"),
                               "ventana": i})
    return claims[:CFG["max_claims"]]


# ── 3 · RETRIEVE + CLASSIFY ────────────────────────────────────────────────

PROMPT_JUEZ = """Eres el juez de novedad del motor delta de P0X.

CONOCIMIENTO EXISTENTE (pasajes recuperados de la mente, con su score):
---
{ctx}
---

CLAIM a clasificar: "{claim}"

¿El conocimiento existente ya contiene la sustancia de este claim?
Responde SOLO con JSON válido: {{"veredicto": "YA_SABIDO" | "NUEVO", "razon": "una frase en español"}}"""


def clasificar(job_id: str, claims: list[dict]) -> list[dict]:
    client = get_client()
    for c in claims:
        vec = embed_text(c["texto"], prefix="search_query: ")
        # query_points: .search() fue retirado en qdrant-client modernos
        hits = client.query_points(collection_name=COLLECTION,
                                   query=vec.tolist(),
                                   limit=CFG["top_k"],
                                   with_payload=True).points
        vecinos = [{
            "id": h.payload.get("id") or h.payload.get("path"),
            "chunk": h.payload.get("chunk_index"),
            "score": round(float(h.score), 4),
            "texto": (h.payload.get("text") or "")[:400],
        } for h in hits]
        c["vecinos"] = vecinos
        top = vecinos[0]["score"] if vecinos else 0.0
        ids_conexion = {v["id"] for v in vecinos
                        if v["score"] >= CFG["umbral_conexion"] and v["id"]}
        c["conexion"] = sorted(ids_conexion) if len(ids_conexion) >= 2 else []
        if top >= CFG["umbral_ya_sabido"]:
            c["clase"] = "YA_SABIDO"
            c["citas"] = [f"[{v['id']}#{v['chunk']}]" for v in vecinos
                          if v["score"] >= CFG["umbral_ya_sabido"]]
        elif top <= CFG["umbral_nuevo"]:
            c["clase"] = "NUEVO"
        else:
            c["clase"] = _juez(job_id, c, vecinos)
    return claims


def _juez(job_id: str, claim: dict, vecinos: list[dict]) -> str:
    ctx = "\n".join(f"[{v['id']}#{v['chunk']}] (score {v['score']}) {v['texto']}"
                    for v in vecinos)
    ol.sobre_alfabeto(job_id, "eval", "ingesta",
                      {"src": "claim", "vs": "mente", "k": CFG["top_k"]},
                      "{veredicto,razon}")
    for intento in range(1 + CFG["juez_reintentos"]):
        content, _ = _llm(PROMPT_JUEZ.format(ctx=ctx, claim=claim["texto"]),
                          "ingesta", "eval")
        parsed = _json_del_modelo(content)
        v = ((parsed or {}).get("veredicto") or "").upper()
        if v in ("YA_SABIDO", "NUEVO"):
            claim["juez"] = {"veredicto": v,
                             "razon": (parsed or {}).get("razon"),
                             "intento": intento}
            if v == "YA_SABIDO":
                claim["citas"] = [f"[{x['id']}#{x['chunk']}]" for x in vecinos[:2]]
            return v
    claim["juez"] = {"veredicto": None, "razon": "sin JSON válido",
                     "juez_fallback": True}
    ol.log_runner(job_id, "JUEZ fallback → NUEVO (JSON inválido tras retry)")
    return "NUEVO"


# ── 4 · REDUCE: destino + redacción ────────────────────────────────────────

PROMPT_DESTINO = """Eres el bibliotecario del motor delta de P0X.

ESFERAS EXISTENTES (slugs reales): {slugs}

AFIRMACIONES NUEVAS destiladas de un video (FOCO: {foco}):
{lista}

Decide el destino del conocimiento nuevo. Responde SOLO con JSON válido:
{{"accion": "nota_sobre_esfera" | "crear_esfera",
  "esfera": "slug de la lista si nota_sobre_esfera; slug nuevo corto si crear_esfera",
  "titulo": "título en español del delta",
  "razon": "una frase"}}"""

PROMPT_CUERPO = """Eres el redactor del motor delta de P0X. Escribe en español, sobrio y denso.

FOCO del Soberano: {foco}
TÍTULO del delta: {titulo}

AFIRMACIONES NUEVAS (no estaban en la mente):
{nuevos}

CONEXIONES detectadas (claims que tocan >=2 nodos existentes):
{conexiones}

Redacta SOLO el cuerpo markdown del delta (sin front-matter, sin título H1):
1) Sección "## Lo nuevo": prosa que integre las afirmaciones nuevas, fiel a ellas, sin inventar.
2) Sección "## Conexiones propuestas": si hay conexiones, una línea por conexión explicando el puente; si no, escribe "Ninguna detectada.".
Nada más."""


def reduce_delta(job_id: str, claims: list[dict], foco: str,
                 video_id: str, titulo_video: str) -> tuple[str, dict]:
    nuevos = [c for c in claims if c["clase"] == "NUEVO"]
    sabidos = [c for c in claims if c["clase"] == "YA_SABIDO"]
    conexiones = [c for c in claims if c["conexion"]]
    slugs = esferas_reales()

    destino = {"accion": "nota_sobre_esfera", "esfera": slugs[0] if slugs else "edge-ai",
               "titulo": titulo_video or f"Delta {video_id}",
               "razon": "fallback: sin claims nuevos o destino inválido"}
    if nuevos:
        lista = "\n".join(f"- {c['texto']}" for c in nuevos[:20])
        ol.sobre_alfabeto(job_id, "delta", "ingesta",
                          {"src": f"claims:{len(nuevos)}", "vs": "esferas"},
                          "{accion,esfera,titulo,razon}")
        content, _ = _llm(PROMPT_DESTINO.format(slugs=", ".join(slugs),
                                                foco=foco, lista=lista),
                          "ingesta", "delta")
        parsed = _json_del_modelo(content) or {}
        accion = parsed.get("accion")
        esfera = _slug(str(parsed.get("esfera") or ""))
        if accion == "nota_sobre_esfera" and esfera in slugs:
            destino = {"accion": accion, "esfera": esfera,
                       "titulo": parsed.get("titulo") or destino["titulo"],
                       "razon": parsed.get("razon")}
        elif accion == "crear_esfera" and esfera and esfera not in slugs:
            destino = {"accion": accion, "esfera": esfera,
                       "titulo": parsed.get("titulo") or destino["titulo"],
                       "razon": parsed.get("razon")}
        else:
            ol.log_runner(job_id, f"DESTINO inválido del modelo ({accion!r}/{esfera!r}) → fallback")

    cuerpo = "## Lo nuevo\n\nNada nuevo frente a la mente actual.\n\n## Conexiones propuestas\n\nNinguna detectada.\n"
    if nuevos:
        txt_nuevos = "\n".join(f"- {c['texto']}" for c in nuevos)
        txt_conex = "\n".join(
            f"- \"{c['texto'][:120]}\" toca: {', '.join(c['conexion'])}"
            for c in conexiones) or "(ninguna)"
        # última llamada LLM del job → keep_alive 0 libera la RAM del modelo
        content, _ = _llm(PROMPT_CUERPO.format(foco=foco,
                                               titulo=destino["titulo"],
                                               nuevos=txt_nuevos,
                                               conexiones=txt_conex),
                          "ingesta", "render", keep_alive=0)
        if content.strip():
            cuerpo = content.strip() + "\n"

    # ── Ensamblado 100% Python (jamás YAML del modelo) ──
    hoy = date.today().isoformat()
    if destino["accion"] == "crear_esfera":
        delta_id = f"esfera-{destino['esfera']}"
        destino_rel = f"esferas/{destino['esfera']}.md"
        tipo = "esfera"
    else:
        delta_id = f"obs-{video_id.lower()}-{destino['esfera']}"
        destino_rel = f"corpus/observaciones/{video_id}-{_slug(destino['titulo'])}.md"
        tipo = "observacion"

    fm = "\n".join([
        "---",
        f"id: {delta_id}",
        f"titulo: {json.dumps(destino['titulo'], ensure_ascii=False)}",
        f"tipo: {tipo}",
        "capa_codice: factual",
        "enlaces:",
        *([f"  - {destino['esfera']}"] if destino["accion"] == "nota_sobre_esfera" else ["  []"]),
        "nivel: stub",
        f"fuente: \"youtube:{video_id}\"",
        f"actualizado: {hoy}",
        "---",
    ])
    ya_sabias = "\n".join(
        f"- \"{c['texto'][:160]}\" — {' '.join(c.get('citas') or [])} "
        f"(score {c['vecinos'][0]['score'] if c['vecinos'] else 'n/a'})"
        for c in sabidos) or "(nada — todo el contenido relevante era nuevo)"

    delta_md = (
        f"{fm}\n\n# {destino['titulo']}\n\n"
        f"> **FOCO del Soberano (literal):** {foco}\n\n"
        f"{cuerpo}\n"
        f"## Lo que ya sabías\n\n{ya_sabias}\n"
    )
    sidecar = {
        "job_id": job_id, "video_id": video_id,
        "accion": destino["accion"], "esfera": destino["esfera"],
        "destino_rel": destino_rel, "titulo": destino["titulo"],
        "razon_destino": destino.get("razon"),
        "n_claims": len(claims), "n_nuevos": len(nuevos),
        "n_ya_sabidos": len(sabidos), "n_conexiones": len(conexiones),
        "umbrales": {k: CFG[k] for k in
                     ("umbral_ya_sabido", "umbral_nuevo", "umbral_conexion")},
        "model": CFG["model"],
        "claims": claims,  # scores crudos completos para calibrar
    }
    return delta_md, sidecar


# ── Entrada del runner ─────────────────────────────────────────────────────

def generar_delta(job_id: str) -> None:
    state = ol.leer_state(job_id)
    if state is None:
        raise FileNotFoundError(f"job {job_id} sin state.json")
    video_id, foco = state["video_id"], state["comentario"]
    titulo_video = ""
    info = PIPE.parent / "corpus" / video_id / "audio.info.json"
    if info.exists():
        try:
            titulo_video = json.loads(info.read_text())["title"]
        except (json.JSONDecodeError, KeyError, OSError):
            pass

    texto = cargar_transcript(video_id)
    ol.log_runner(job_id, f"transcript: {len(texto.split())} palabras, "
                          f"{len(ventanas(texto))} ventanas")
    # Checkpoints de fase: un re-encolado térmico reanuda donde murió en vez
    # de rehacer MAP+CLASSIFY (~45 min de CPU) y chocar contra el mismo muro.
    clasificados = ol.leer_checkpoint(job_id, "claims_classify.json")
    if clasificados is not None:
        claims = clasificados
        nuevos = sum(1 for c in claims if c["clase"] == "NUEVO")
        ol.log_runner(job_id, f"CLASSIFY en cache — skip ({nuevos} nuevos / "
                              f"{len(claims) - nuevos} ya sabidos)")
    else:
        claims = ol.leer_checkpoint(job_id, "claims_map.json")
        if claims is not None:
            ol.log_runner(job_id, f"MAP en cache — skip ({len(claims)} claims)")
        else:
            claims = map_claims(job_id, texto, foco)
            ol.guardar_checkpoint(job_id, "claims_map.json", claims)
            ol.log_runner(job_id, f"MAP: {len(claims)} claims")
        claims = clasificar(job_id, claims)
        ol.guardar_checkpoint(job_id, "claims_classify.json", claims)
        nuevos = sum(1 for c in claims if c["clase"] == "NUEVO")
        ol.log_runner(job_id, f"CLASSIFY: {nuevos} nuevos / "
                              f"{len(claims) - nuevos} ya sabidos")
    delta_md, sidecar = reduce_delta(job_id, claims, foco, video_id, titulo_video)

    d = ol.job_dir(job_id)
    (d / "delta.md").write_text(delta_md, encoding="utf-8")
    (d / "delta.json").write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
    ol.log_runner(job_id, f"REDUCE: {sidecar['accion']} → {sidecar['destino_rel']}")
