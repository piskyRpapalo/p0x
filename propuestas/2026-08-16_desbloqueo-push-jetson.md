---
id: propuesta-desbloqueo-push-jetson
titulo: Desbloqueo del push de p0x a jetson · una línea, tres opciones
tipo: operativo
clase: operativo
sistema: P0X-CORE
estado: PROPUESTA · requiere firma del Soberano
actualizado: 2026-08-16
---

# DESBLOQUEO DEL PUSH DE `p0x` A JETSON

**El push a jetson está preparado y bloqueado por una sola línea.** No lo he
arreglado por mi cuenta: es un documento de auditoría del Soberano y la guardia
de higiene es un control de doctrina, no un obstáculo que se rodea.

---

## §1 · ESTADO MEDIDO

| Comprobación | Resultado |
|---|---|
| `jetson:p0x.git` responde | **sí** · `master = 4d4130e` |
| Clave usada | `id_ed25519_soberano_git` · `auth-only` · `no-value-signing` ✅ |
| ¿Divergencia? | **no** · avance rápido limpio |
| Commits que jetson tiene y el Soberano no | **0** |
| Commits que subirían | **40** — desde `fcbf8f8` hasta `51de287` |
| Ensayo `git push --dry-run` | **BLOQUEADO** por la guardia de pre-push · 0 objetos transferidos |

**Jetson está mucho más atrás de lo que parecía.** No son los 2 o 3 commits de
esta ronda: son **40**, el más antiguo del 2026-08-09. La documentación del rack
lleva una semana entera viviendo en un solo disco, no una noche.

Remoto ya configurado (cambio local, reversible con `git remote remove jetson`):

```
jetson => jetson:p0x.git
```

---

## §2 · EL BLOQUEO · UNA LÍNEA

```
=== GUARDIA DE HIGIENE · pre-push ===
· refs/heads/master: revisando 40 commit(s) del rango
❌ BLOQUEADO: fuga de infraestructura en el rango de refs/heads/master
mente/auditorias/RACK_Y_CODICE_2026-08-09.md:59: [RUTA-HOME] ...
```

La línea es la salida de un `ls -la` dentro de un bloque literal: un symlink
cuyo destino es una ruta de montaje de un nodo del rack. <!-- guardia:permitir se describe la forma del hallazgo, sin reproducir la ruta -->

**Por qué no lo paró el pre-commit en su día, que es el dato que importa:**

| Evento | Fecha | Commit |
|---|---|---|
| Entra la línea | 2026-08-09 | `777640d` |
| Se añade la regla de los seis prefijos (D34) | 2026-08-12 | `ed292e2` |

**La línea es tres días anterior a la regla que la caza.** No es una guardia que
falló: es una guardia que se endureció después, y el pre-push —que revisa el
rango completo, no el último commit— la encuentra ahora. Es exactamente para lo
que se instaló.

---

## §3 · TRES OPCIONES · LAS TRES PROBADAS CONTRA LA GUARDIA

Probadas ejecutando la guardia sobre cada candidato, no razonadas:

| # | Opción | ¿Pasa? | Coste |
|---|---|---|---|
| **B** | Elipsis: `/mnt/` + `...` + resto de la ruta | ✅ | Altera un carácter del transcrito |
| **C** | Marcador: `/mnt/` + `<NVME>` + resto | ✅ | Altera el transcrito, pero **se ve que es un marcador** |
| **D** | Pragma `guardia:permitir <motivo>` al final de la línea | ✅ | Deja la ruta real en la historia y mete un comentario dentro de un bloque literal |
| — | `git push --no-verify` | (salta la guardia) | **Queda sin registrar.** La propia guardia lo desaconseja |

### Recomendación: **C**

- **Pasa por la vía que la guardia ya tiene prevista**, no por una excepción:
  `<NVME>` cae en su lista de PLACEHOLDERS. No se está silenciando una regla,
  se está escribiendo el dato en la forma que la regla acepta.
- **Se ve que es un marcador.** La elipsis (B) puede leerse dentro de un año
  como parte del transcrito; `<NVME>` no engaña a nadie.
- **El documento no pierde nada.** Ese apartado trata de que el symlink estaba
  **roto** (`sha256sum: No such file or directory`), no de dónde apuntaba. El
  punto de montaje exacto no sostiene ninguna afirmación del texto.
- **D deja la ruta real en la historia de un repo**, que es lo que D8 evita. Y
  un pragma dentro de un bloque de salida de terminal falsea la transcripción
  igual que un marcador, pero sin avisar de que la falsea.

**Contra la recomendación, dicho para que decidas con las dos caras:** C toca
un documento de auditoría, y un transcrito alterado es un transcrito alterado.
Si prefieres que la historia conserve el dato tal cual y llevar el coste en
forma de excepción declarada, **D es defendible** y no la discuto.

---

## §4 · LO QUE HAY QUE EJECUTAR

**Paso 1 — aplicar la opción elegida.** Para **C**, en
`mente/auditorias/RACK_Y_CODICE_2026-08-09.md`, línea 59: sustituir el nombre
del punto de montaje por `<NVME>`, dejando el resto de la ruta igual.

```bash
cd ~/p0x
git commit -am "fix(auditoria): punto de montaje a marcador · D34 es posterior a la linea"
```

**Paso 2 — comprobar antes de empujar** (no transfiere nada):

```bash
git push --dry-run jetson master
```

Debe imprimir `✅ GUARDIA OK`. Si no, **para**: no se fuerza.

**Paso 3 — el push, con tu firma:**

```bash
git push jetson master
```

**Paso 4 — verificar que llegó:**

```bash
git ls-remote jetson:p0x.git master   # debe coincidir con: git rev-parse HEAD
```

---

## §5 · UNA DECISIÓN APARTE, QUE NO ES ESTA

`p0x` tiene además un remoto **`origin` que apunta a GitHub**
(`github.com/piskyRpapalo/p0x.git`) y está **3 commits por detrás**. No lo he
tocado y no lo propongo aquí: empujar el canon a GitHub es una decisión de
superficie pública, no de respaldo, y no es lo que pediste. Se menciona solo
para que conste que existe y que no se ha movido.

---

Pendiente de firma del Soberano.
