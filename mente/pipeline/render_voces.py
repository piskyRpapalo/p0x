"""
render_voces.py — P0X mente/pipeline
Regenera /home/ubuntu/hexelion/packages/personas/{agent}.md a partir de
mente/voces/{agent}.md (fuente de verdad, clase=operativo, editada bajo el
Protocolo del MD Evolutivo). _load_persona() en hexelion_gateway.py sigue
haciendo un simple read_text() sobre packages/personas/ — cero cambios ahí;
este script es la única pieza nueva, corrida manualmente cuando cambian las
voces (cadencia distinta a la reindexación de Qdrant, por eso vive separado
de ingest_mente.py).

Ancla de versión (Protocolo §4.5): cada archivo regenerado lleva un comentario
HTML con md_id@version, para que un mismatch futuro sea detectable a simple vista.
"""
import sys
from pathlib import Path

import yaml

MENTE_ROOT = Path(__file__).resolve().parent.parent
VOCES_DIR = MENTE_ROOT / "voces"
PERSONAS_DIR = Path("/home/ubuntu/hexelion/packages/personas")

AGENTS = ("monje", "vocero", "berserker", "escriba", "alquimista", "enlace")


def _strip_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("sin front-matter YAML")
    end = lines[1:].index("---") + 1
    fm = yaml.safe_load("\n".join(lines[1:end]))
    body = "\n".join(lines[end + 1:]).strip()
    return fm, body


def render_one(agent: str) -> None:
    src = VOCES_DIR / f"{agent}.md"
    fm, body = _strip_frontmatter(src.read_text(encoding="utf-8"))
    anchor = f"<!-- fuente: mente/voces/{agent}.md @ {fm['id']}@{fm['version']} — regenerado por render_voces.py, no editar aquí directamente -->\n\n"
    dest = PERSONAS_DIR / f"{agent}.md"
    dest.write_text(anchor + body + "\n", encoding="utf-8")
    print(f"[render_voces] {agent}: {fm['id']}@{fm['version']} -> {dest}")


def main() -> None:
    for agent in AGENTS:
        render_one(agent)


if __name__ == "__main__":
    main()
