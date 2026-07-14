#!/usr/bin/env python3
"""prune_backups.py — política de retención para .backups/ (tarea #60).

Los backups manuales `<nombre>.bak-<AAAAMMDDHHMMSS>` se acumulan sin límite.
Esta herramienta conserva, POR PREFIJO de archivo, los últimos N backups, y
además cualquier backup más nuevo que MAX_DIAS — lo que sea MÁS GENEROSO
(se conserva si CUALQUIERA de las dos reglas dice conservar). Nunca borra un
archivo que no encaje en el patrón `.bak-<timestamp>`.

Seguro por defecto: DRY-RUN. Solo borra con --apply. Solo LECTURA del resto
del sistema; jamás toca nada fuera de --dir.

Uso:
  python3 bin/prune_backups.py                 # dry-run sobre /mnt/nvme/p0x/.backups
  python3 bin/prune_backups.py --apply         # aplica de verdad
  python3 bin/prune_backups.py --keep 200 --dias 60 --dir /ruta/.backups
"""
import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

BAK = re.compile(r"^(?P<prefijo>.+)\.bak-(?P<ts>\d{8,14})$")
DEFAULT_DIR = Path("/mnt/nvme/p0x/.backups")


def parse_ts(ts: str):
    for fmt in ("%Y%m%d%H%M%S", "%Y%m%d%H%M", "%Y%m%d"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def plan(directorio: Path, keep: int, dias: int):
    ahora = datetime.now()
    frontera = ahora - timedelta(days=dias)
    grupos = defaultdict(list)  # prefijo -> [(ts, path)]
    ignorados = []
    for p in directorio.iterdir():
        if not p.is_file():
            continue
        m = BAK.match(p.name)
        if not m:
            ignorados.append(p)  # no encaja el patrón → jamás se toca
            continue
        ts = parse_ts(m.group("ts")) or datetime.fromtimestamp(p.stat().st_mtime)
        grupos[m.group("prefijo")].append((ts, p))

    conservar, borrar = [], []
    for _prefijo, items in grupos.items():
        items.sort(key=lambda x: x[0], reverse=True)  # más nuevo primero
        for i, (ts, p) in enumerate(items):
            reciente = ts >= frontera
            dentro_de_n = i < keep
            (conservar if (reciente or dentro_de_n) else borrar).append(p)
    return conservar, borrar, ignorados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    ap.add_argument("--keep", type=int, default=200, help="backups por prefijo a conservar")
    ap.add_argument("--dias", type=int, default=60, help="edad bajo la cual siempre se conserva")
    ap.add_argument("--apply", action="store_true", help="borra de verdad (por defecto: dry-run)")
    a = ap.parse_args()

    if not a.dir.is_dir():
        print(f"✗ no existe el directorio: {a.dir}", file=sys.stderr)
        return 1

    conservar, borrar, ignorados = plan(a.dir, a.keep, a.dias)
    modo = "APLICANDO" if a.apply else "DRY-RUN"
    print(f"[{modo}] {a.dir}  (keep={a.keep}/prefijo, edad<{a.dias}d)")
    print(f"  conservar: {len(conservar)}   borrar: {len(borrar)}   ignorados (no-patrón): {len(ignorados)}")
    for p in borrar:
        print(f"  - {'borrado' if a.apply else 'borraría'}: {p.name}")
        if a.apply:
            p.unlink()
    if not borrar:
        print("  nada que borrar — dentro de la política.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
