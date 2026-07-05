#!/usr/bin/env python3
"""audit_report.py — agrega los 4 JSON en informe + plan PROPUESTO.

Determinista: severidad y coste salen de una TABLA, cada tarea ancla su
evidencia (archivo+categoría+detalle) — cero tareas sin infracción que las
motive. Escribe mente/auditorias/AUDIT_<fecha>.md y ANEXA tareas a
PENDIENTES.md con estado=propuesta (dedup por marcador [aud:<slug>], tope
de anexo para respetar el presupuesto_kb de PENDIENTES; el resto queda en
el informe). JAMÁS ejecuta cambios sobre MDs: propone. El paso de
razonamiento acotado (síntesis ejecutiva) lo hace el modelo invocante
siguiendo el prompt fijo del final del informe.
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import MENTE, OUT

AUDITORIAS = MENTE / "auditorias"
PENDIENTES = MENTE / "feedback" / "PENDIENTES.md"
MAX_ANEXO = 8  # tareas máximas que se anexan a PENDIENTES por corrida

# categoria → (severidad, coste, acción propuesta)
TABLA = {
    "correa-mal-atada":       ("critico", "S", "reatar la correa: editor_autorizado=carbono en doctrina"),
    "changelog-reescrito":    ("critico", "S", "restaurar historia append-only desde git y re-aplicar como entrada nueva"),
    "fuga-necropolis":        ("critico", "S", "re-cablear la guardia de build_graph y regenerar el grafo"),
    "divergencia-remote":     ("critico", "S", "git pull --rebase y reconciliar antes de cualquier edición"),
    "sin-front-matter":       ("importante", "S", "añadir front-matter mínimo (id/titulo/tipo)"),
    "contrato-evolutivo-incompleto": ("importante", "S", "completar el contrato §2 (campos del carbono: que los fije David)"),
    "PODA":                   ("importante", "M", "pasada de poda §4.4: enterrar reglas sin evidencia en changelog"),
    "enlace-roto":            ("importante", "S", "corregir el enlace o crear el nodo destino"),
    "id-duplicado":           ("importante", "S", "renombrar uno de los dos ids (el id es estable: decidir cuál nació después)"),
    "arista-rota":            ("importante", "S", "regenerar grafo (ingest_mente) o corregir el enlace fuente"),
    "md-fuera-del-grafo":     ("importante", "S", "encolar re-ingesta (tsp ingest_mente.py)"),
    "nodo-sin-fuente":        ("importante", "S", "regenerar grafo; si persiste, buscar el MD borrado sin re-ingesta"),
    "esfera-sin-niveles":     ("importante", "S", "correr gen_niveles.py sobre la esfera (marcar cc-pendiente-revision)"),
    "umbral-cruzado":         ("importante", "M", "abrir lazo §3: hipótesis en changelog + re-edición propuesta"),
    "mente-sin-commit":       ("importante", "S", "commit del cambio (el commit ES el registro, §5)"),
    "runtime-trackeado":      ("importante", "S", "git rm --cached (el criterio ya está en el .gitignore)"),
    "push-pendiente":         ("importante", "S", "push al remote soberano (paracaídas)"),
    "version-no-semver":      ("menor", "S", "normalizar a MAJOR.MINOR.PATCH"),
    "editor-invalido":        ("menor", "S", "corregir a carbono|silicio-telemetria"),
    "campo-basico-ausente":   ("menor", "S", "completar id/titulo/tipo"),
    "tipo-fuera-vocabulario": ("menor", "S", "alinear al vocabulario §2 o proponer ampliarlo (con motivo)"),
    "nodo-huerfano":          ("menor", "S", "enlazar desde/hacia un nodo real o aceptar la isla con motivo"),
    "basura-en-mente":        ("menor", "S", "mover el .bak fuera de SCOPE_DIRS o borrarlo (git ya lo guarda)"),
    "grafo-ausente":          ("critico", "S", "correr ingest_mente para regenerar el grafo"),
    "repo-ausente":           ("critico", "M", "investigar: un repo soberano ha desaparecido"),
}
ORDEN = {"critico": 0, "importante": 1, "menor": 2}

PROMPT_SINTESIS = """\
<!-- PROMPT DE SÍNTESIS (para el modelo invocante — reproducible, sin intuición):
1. Lee las tareas de arriba. Para cada una comprueba que su evidencia citada
   existe en la sección EVIDENCIA. Si alguna no la tiene, táchala aquí y anótalo.
2. Escribe bajo este bloque una SÍNTESIS EJECUTIVA de máximo 6 líneas en
   español: (a) estado general en una frase, (b) los 1-3 críticos si los hay,
   (c) el patrón dominante entre importantes, (d) qué NO requiere acción
   (ruido aceptado y por qué). Prohibido: proponer tareas nuevas que no estén
   ancladas a evidencia, tocar MDs, o ejecutar nada — el plan es PROPUESTO
   y lo firma el carbono.
3. No borres este bloque: es el contrato del paso. -->
"""


def main() -> int:
    hoy = date.today().isoformat()
    auditores = {}
    for f in ("frontmatter", "grafo", "telemetria", "git"):
        p = OUT / f"{f}.json"
        auditores[f] = json.loads(p.read_text(encoding="utf-8")) if p.exists() \
            else {"error": "no corrió", "infracciones": []}

    todas = []
    for nombre, data in auditores.items():
        for i in data.get("infracciones", []):
            sev, coste, accion = TABLA.get(
                i["categoria"], ("menor", "S", "revisar manualmente"))
            todas.append({**i, "auditor": nombre, "severidad": sev,
                          "coste": coste, "accion": accion,
                          "slug": f"{i['categoria']}:{i['archivo']}"})
    todas.sort(key=lambda t: (ORDEN[t["severidad"]], t["categoria"], t["archivo"]))

    n_por_sev = {s: sum(1 for t in todas if t["severidad"] == s) for s in ORDEN}

    # ── informe ──
    AUDITORIAS.mkdir(parents=True, exist_ok=True)
    informe = AUDITORIAS / f"AUDIT_{hoy}.md"
    L = [f"# Auditoría de higiene P0X · {hoy}",
         "",
         f"skill auditar-p0x · determinista · {len(todas)} infracciones "
         f"(crítico {n_por_sev['critico']} · importante "
         f"{n_por_sev['importante']} · menor {n_por_sev['menor']})",
         "",
         "## Tareas propuestas (cada una anclada a su evidencia)",
         "",
         "| sev | tarea | evidencia | coste |",
         "|---|---|---|---|"]
    for t in todas:
        L.append(f"| {t['severidad']} | {t['accion']} | "
                 f"`{t['archivo']}` · {t['categoria']}: {t['detalle']} | "
                 f"{t['coste']} |")
    L += ["", "## Telemetría (dato, no opinión)", "```json",
          json.dumps({"por_voz": auditores["telemetria"].get("por_voz", {}),
                      "por_dominio_op": auditores["telemetria"].get("por_dominio_op", {})},
                     ensure_ascii=False, indent=1),
          "```", "", "## Evidencia completa por auditor", "```json",
          json.dumps({k: v.get("infracciones", []) for k, v in auditores.items()},
                     ensure_ascii=False, indent=1),
          "```", "", "## Síntesis ejecutiva", "", PROMPT_SINTESIS, ""]
    informe.write_text("\n".join(L), encoding="utf-8")

    # ── anexo a PENDIENTES (propuesta, dedup, tope) ──
    texto = PENDIENTES.read_text(encoding="utf-8")
    nuevas = [t for t in todas if f"[aud:{t['slug']}]" not in texto
              and t["severidad"] != "menor"][:MAX_ANEXO]
    if nuevas:
        filas = [f"\n### {hoy} · auditoría automática (skill auditar-p0x)\n",
                 "| # | Tarea propuesta | Coste | Estado |",
                 "|---|---|---|---|"]
        for k, t in enumerate(nuevas, 1):
            filas.append(f"| A{k} | **{t['accion']}** — `{t['archivo']}` "
                         f"({t['categoria']}: {t['detalle']}) "
                         f"[aud:{t['slug']}] | {t['coste']} | propuesta |")
        with open(PENDIENTES, "a", encoding="utf-8") as f:
            f.write("\n".join(filas) + "\n")

    print(f"AUDIT → {informe}")
    print(f"infracciones: {len(todas)} (c{n_por_sev['critico']}/"
          f"i{n_por_sev['importante']}/m{n_por_sev['menor']}) · "
          f"anexadas a PENDIENTES: {len(nuevas)} (dedup+tope {MAX_ANEXO}, "
          f"menores solo en el informe)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
