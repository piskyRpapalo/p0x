#!/usr/bin/env python3
"""audit_git.py — higiene de los repos soberanos.

Por repo (p0x, hexelion, hexelion-lab):
- MDs de mente/ modificados sin commit (el commit ES el registro, §5)
- archivos trackeados que el .gitignore ya excluye (runtime por error)
- divergencia con el remote soberano (fetch + ahead/behind)
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_lib import escribir, infraccion

REPOS = {
    "p0x": Path("/mnt/nvme/p0x"),
    "hexelion": Path.home() / "hexelion",
    "hexelion-lab": Path.home() / "hexelion-lab",
}


def git(repo: Path, *args):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout.strip()


def main() -> int:
    inf = []
    estado = {}
    for nombre, repo in REPOS.items():
        if not (repo / ".git").exists():
            inf.append(infraccion(str(repo), "repo-ausente",
                                  f"{nombre}: no es un repo git"))
            continue
        # sucio
        _, porcelain = git(repo, "status", "--porcelain")
        sucios = [l for l in porcelain.splitlines() if l.strip()]
        for l in sucios:
            ruta = l[3:]
            if nombre == "p0x" and ruta.startswith("mente/"):
                inf.append(infraccion(f"{nombre}:{ruta}", "mente-sin-commit",
                                      f"cambio en la mente sin commitear ({l[:2].strip()})"))
        # runtime trackeado que gitignore excluye
        _, ignorados = git(repo, "ls-files", "-i", "-c", "--exclude-standard")
        for ruta in ignorados.splitlines():
            if ruta:
                inf.append(infraccion(f"{nombre}:{ruta}", "runtime-trackeado",
                                      "trackeado pero el .gitignore lo excluye"))
        # divergencia con el remote soberano
        rc, _ = git(repo, "fetch", "-q", "origin")
        rama_rc, rama = git(repo, "branch", "--show-current")
        div = None
        if rc == 0 and rama:
            rc2, counts = git(repo, "rev-list", "--left-right", "--count",
                              f"origin/{rama}...HEAD")
            if rc2 == 0 and counts:
                behind, ahead = (int(x) for x in counts.split())
                div = {"behind": behind, "ahead": ahead}
                if behind:
                    inf.append(infraccion(nombre, "divergencia-remote",
                                          f"{behind} commits POR DETRÁS de "
                                          f"origin/{rama} — otro silicio/nodo "
                                          f"empujó; reconciliar antes de tocar"))
                if ahead:
                    inf.append(infraccion(nombre, "push-pendiente",
                                          f"{ahead} commits sin empujar a "
                                          f"origin/{rama} (paracaídas caído)"))
        estado[nombre] = {"rama": rama or "?", "sucios": len(sucios),
                          "divergencia": div}

    escribir("git.json", {"auditor": "git", "repos": estado,
                          "infracciones": inf})
    return 0


if __name__ == "__main__":
    sys.exit(main())
