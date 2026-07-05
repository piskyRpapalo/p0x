#!/usr/bin/env python3
"""Benchmark de cerebro batch para el motor delta (Bloque A, misión OBSERVAR).

Compara candidatos instruct en la fragua con cargas realistas del motor delta:
  1) MAP    — extraer claims JSON de una ventana de transcript real (~1800 tok).
  2) JUEZ-A — clasificar un claim sembrado como YA_SABIDO (contexto lo contiene).
  3) JUEZ-B — clasificar un claim sembrado como NUEVO (contexto no lo contiene).

Mide tok/s de prompt y eval (campos nativos de Ollama), RAM del modelo
(`ollama ps`), disciplina JSON y acierto de clasificación. Guard térmico:
zone0 >80°C al arrancar => exit 75 (re-encolar). keep_alive=0 al terminar.

Uso: bench_delta.py <modelo> [<modelo>...]   (resultados en out/bench_delta.json)
"""
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "out"
OLLAMA = "http://localhost:11434"
THERMAL = pathlib.Path("/sys/class/thermal/thermal_zone0/temp")
TMAX_START = 80.0

TRANSCRIPT = (BASE.parent / "corpus/cGhI8tGY0Gw/transcript.txt").read_text(encoding="utf-8")

FOCO = ("Me interesa cómo la IA física conecta percepción y acción, y qué "
        "implicaciones tiene para un organismo soberano con sensores propios.")

PROMPT_MAP = f"""Eres el extractor de afirmaciones del motor delta de P0X.

FOCO del Soberano: {FOCO}

TRANSCRIPT (ventana):
---
{TRANSCRIPT}
---

Extrae las afirmaciones sustantivas del transcript relevantes al FOCO.
Responde SOLO con JSON válido, sin markdown, con este esquema exacto:
{{"claims": [{{"texto": "afirmación en español, autocontenida", "relevancia_foco": 0.0}}]}}
Máximo 12 claims. relevancia_foco entre 0 y 1. Nada fuera del JSON."""

CTX_SABIDO = """[doctrina-ai-interna#2] La ausencia de dato es información: un feed caído
se reporta como "fuente caída" o "sin dato", jamás como cero. Todo número citado
debe nombrar su clave de origen. La invención de significado está prohibida.
[voz-monje#1] El Monje vigila la física del sistema (temperatura, consumo, UPS)
y solo responde desde su contrato de datos; "no lo sé" es respuesta correcta."""

CLAIM_SABIDO = ("Cuando un sensor deja de emitir, el sistema debe reportar la ausencia "
                "de dato explícitamente en lugar de rellenar con un valor cero.")

CTX_NUEVO = CTX_SABIDO
CLAIM_NUEVO = ("Los modelos de IA física entrenados en simulación pueden transferir "
               "políticas de manipulación a robots reales ajustando la aleatorización "
               "de dominios durante el entrenamiento.")

PROMPT_JUEZ = """Eres el juez de novedad del motor delta de P0X.

CONOCIMIENTO EXISTENTE (pasajes recuperados de la mente):
---
{ctx}
---

CLAIM a clasificar: "{claim}"

¿El conocimiento existente ya contiene la sustancia de este claim?
Responde SOLO con JSON válido: {{"veredicto": "YA_SABIDO" | "NUEVO", "razon": "una frase en español"}}"""


def temp_c() -> float:
    return int(THERMAL.read_text().strip()) / 1000.0


def ollama_chat(model: str, prompt: str, keep_alive="5m") -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"temperature": 0.1, "num_ctx": 6144},
    }).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.loads(r.read())


def ram_model() -> str:
    try:
        out = subprocess.run(["ollama", "ps"], capture_output=True, text=True,
                             timeout=10).stdout.strip().splitlines()
        return out[1] if len(out) > 1 else "(vacío)"
    except Exception as e:  # noqa: BLE001 — benchmark: cualquier fallo se anota
        return f"(error: {e})"


def parse_json_strict(s: str):
    s = s.strip()
    if s.startswith("```"):
        s = s.strip("`\n")
        if s.startswith("json"):
            s = s[4:]
    try:
        return json.loads(s), s.strip().startswith("{")
    except json.JSONDecodeError:
        i, j = s.find("{"), s.rfind("}")
        if 0 <= i < j:
            try:
                return json.loads(s[i:j + 1]), False
            except json.JSONDecodeError:
                pass
    return None, False


def run_case(model: str, name: str, prompt: str, keep_alive="5m") -> dict:
    t0 = temp_c()
    resp = ollama_chat(model, prompt, keep_alive)
    content = resp.get("message", {}).get("content", "")
    parsed, clean = parse_json_strict(content)
    pe_c = resp.get("prompt_eval_count", 0)
    pe_d = resp.get("prompt_eval_duration", 1)
    ev_c = resp.get("eval_count", 0)
    ev_d = resp.get("eval_duration", 1)
    return {
        "caso": name,
        "prompt_tok": pe_c, "prompt_tok_s": round(pe_c / (pe_d / 1e9), 2),
        "eval_tok": ev_c, "eval_tok_s": round(ev_c / (ev_d / 1e9), 2),
        "total_s": round(resp.get("total_duration", 0) / 1e9, 1),
        "json_valido": parsed is not None,
        "json_limpio": clean,
        "temp_inicio_c": t0, "temp_fin_c": temp_c(),
        "ram_modelo": ram_model(),
        "parsed": parsed,
        "content_raw": content if parsed is None else None,
    }


def bench_model(model: str) -> dict:
    res = {"modelo": model, "casos": []}
    c1 = run_case(model, "map_extraccion", PROMPT_MAP)
    claims = (c1["parsed"] or {}).get("claims")
    c1["n_claims"] = len(claims) if isinstance(claims, list) else None
    c1["claims_muestra"] = claims[:3] if isinstance(claims, list) else None
    c1.pop("parsed")
    res["casos"].append(c1)

    c2 = run_case(model, "juez_ya_sabido",
                  PROMPT_JUEZ.format(ctx=CTX_SABIDO, claim=CLAIM_SABIDO))
    v2 = ((c2["parsed"] or {}).get("veredicto") or "").upper()
    c2["veredicto"], c2["acierto"] = v2, v2 == "YA_SABIDO"
    c2["razon"] = (c2["parsed"] or {}).get("razon")
    c2.pop("parsed")
    res["casos"].append(c2)

    c3 = run_case(model, "juez_nuevo",
                  PROMPT_JUEZ.format(ctx=CTX_NUEVO, claim=CLAIM_NUEVO),
                  keep_alive=0)
    v3 = ((c3["parsed"] or {}).get("veredicto") or "").upper()
    c3["veredicto"], c3["acierto"] = v3, v3 == "NUEVO"
    c3["razon"] = (c3["parsed"] or {}).get("razon")
    c3.pop("parsed")
    res["casos"].append(c3)

    res["json_ok"] = all(c["json_valido"] for c in res["casos"])
    res["aciertos_juez"] = sum(1 for c in res["casos"] if c.get("acierto"))
    res["eval_tok_s_media"] = round(
        sum(c["eval_tok_s"] for c in res["casos"]) / len(res["casos"]), 2)
    return res


def main() -> int:
    t = temp_c()
    if t > TMAX_START:
        print(f"THERMAL_GUARD: zone0={t}°C > {TMAX_START} -> re-encolar", flush=True)
        return 75
    modelos = sys.argv[1:]
    if not modelos:
        print("uso: bench_delta.py <modelo> [...]")
        return 2
    OUT.mkdir(exist_ok=True)
    resultados = {"fecha": time.strftime("%Y-%m-%dT%H:%M:%S"),
                  "temp_arranque_c": t, "modelos": []}
    for m in modelos:
        print(f"== bench {m} (zone0 {temp_c()}°C)", flush=True)
        resultados["modelos"].append(bench_model(m))
    resultados["temp_final_c"] = temp_c()
    dest = OUT / "bench_delta.json"
    dest.write_text(json.dumps(resultados, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
