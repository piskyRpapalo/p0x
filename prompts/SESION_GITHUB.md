# Prompt · sesión para reordenar GitHub

**Úsalo en Claude Code, no en Cowork.** Razón: hace falta el `gh` autenticado,
leer los clones locales para comprobar que nada se pierde antes de borrar, y
comparar cada repo remoto con su copia en disco. Cowork no tiene terminal ni
sistema de ficheros; escribe documentos muy bien, pero aquí lo que se necesita
es verificar y ejecutar. Si quieres que además te redacte el README de perfil
en bonito, eso sí puede salir de esta misma sesión — no hace falta partirla.

---

Copia de aquí abajo:

---

Vas a reordenar mi cuenta de GitHub (`piskyRpapalo`). `gh` ya está instalado y
autenticado.

**Lee primero, en este orden:** `~/p0x/HANDOFF.md`, `~/p0x/INVENTARIO.md` y
`~/preceptoros-web/docs/ESTADO.md`. No repitas trabajo que ya está hecho ahí.

## El objetivo

Que en mi cuenta queden **cuatro repositorios y nada más**:

1. **`piskyRpapalo`** — el README de mi perfil. Existe uno antiguo que está muy
   bien escrito: **adáptalo, no lo tires**. Hay que actualizar tres cosas —
   *skills*, conocimientos y filosofía — porque hoy mi trabajo es entrenar
   LoRAs con LoRAtelier y construir la comunidad alrededor de la web.
   Enséñamelo antes de aplicarlo.
2. **`preceptoros-web`** — público. Su README se rehízo el 2026-09-05; no lo
   toques sin decírmelo.
3. **`PreceptorOS`** — público, la app. Igual.
4. **`hexelion-nexo`** — privado por ahora. Sólo asegúrate de que su
   descripción dice lo que es.

El resto quiero quitarlos de en medio.

## Antes de borrar nada · las cuatro comprobaciones

**Borrar un repositorio en GitHub es irreversible.** No borres ninguno hasta
que, para cada uno, me traigas:

1. **Qué es y qué tiene dentro** — una línea, leída del repo, no del nombre.
2. **Si existe copia local** y dónde, con `git remote -v` y la última fecha de
   commit a cada lado. Si el remoto tiene commits que la copia local no tiene,
   dilo en voz alta: eso es material que sólo existe en GitHub.
3. **Si algo lo referencia.** `grep` en `~/p0x` y en los dos repos públicos por
   el nombre del repo y por su URL. Un enlace roto en un README público es peor
   que un repo de más.
4. **Archivar en vez de borrar**, como opción por defecto. Un repo archivado
   deja de aparecer como activo, conserva el historial y se puede desarchivar.
   Propón borrar sólo cuando yo lo pida para ese repo concreto.

## Atención con `p0x`

`p0x` es el monorepo de doctrina del rack. Su remoto canónico es
`jetson:p0x.git` y **GitHub es sólo un espejo**. No entra en la lista de los
cuatro, pero **no lo borres ni lo archives sin preguntarme explícitamente**, y
antes comprueba que `jetson` tiene todo lo que tiene `origin`. Si te digo que
lo quite, quítalo del remoto de GitHub y deja `jetson` intacto.

## Cómo trabajar

- Un repo cada vez. Me traes las cuatro comprobaciones, yo firmo, tú actúas.
- Nada de borrados en lote.
- Al terminar: descripción, *topics* y enlace del sitio en los cuatro que
  quedan, para que quien llegue de fuera —normalmente una IA— entienda qué es
  cada uno sin abrirlo.
- Cierra dejando escrito en `~/p0x/HANDOFF.md` qué se borró, qué se archivó y
  qué se quedó.
