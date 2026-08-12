#!/usr/bin/env bash
# auditar-p0x · corre los 4 auditores deterministas + agregador.
# Salidas: mente/auditorias/out/*.json, AUDIT_<fecha>.md, anexo a PENDIENTES.
set -u
S="$(cd "$(dirname "$0")/scripts" && pwd)"
rc=0
for a in frontmatter grafo telemetria git dids; do
  python3 "$S/audit_$a.py" || { echo "auditor $a FALLÓ (rc=$?)"; rc=1; }
done
python3 "$S/audit_report.py" || rc=1
exit $rc
