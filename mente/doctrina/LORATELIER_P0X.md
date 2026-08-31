---
id: loratelier-p0x
titulo: LorAtelier — el negocio es el proceso, no el volumen
tipo: doctrina
clase: doctrina
version: 1.0.0
editor_autorizado: carbono
metrica_exito: "cero LoRA publicado sin doble puerta y firma; cero dato de usuario que viaje sin su firma Ed25519; la cola real siempre publicada"
umbral_reedicion: "cierre de cualquiera de las cuatro decisiones abiertas (D1-D4), o llegada de la Forja a produccion"
enlaces:
  - doctrina-p0x-producto
  - instrucciones-p0x
  - orquesta-modelos-p0x
estado: contexto filosofico · NO es una funcionalidad en construccion
aplazado_hasta: cerrar el Agora (dominio 1)
firmado: 2026-08-31
---

# LorAtelier

**Contexto, no encargo.** Esto se escribe para que exista antes de que haga
falta: el dia que se construya el boton «corregir esta respuesta» en el Agora,
la decision de que hacer con esa correccion ya estara tomada aqui y no se
improvisara en caliente. Hasta entonces no toca codigo.

## La distincion que sostiene el negocio

El ecosistema PreceptorOS **no es una fabrica de LoRAs. Es un atelier.**

| | Vende | Y por tanto |
|---|---|---|
| **Fabrica** | volumen · «tu LoRA en 5 minutos» | miente sobre la cola |
| **Atelier** | proceso · «tu IA mejora con tus correcciones firmadas, y tus datos no viajan sin tu firma» | **publica la cola** |

La cola publicada no es transparencia decorativa: es la misma regla de los
honest sensors aplicada al negocio. Una cola oculta es una cifra publicada que
nadie puede reproducir, y este proyecto lleva cuatro puertas cazando
exactamente eso.

## Las tres capas

1. **La Boveda** (la app, dominio 2) · memoria firmada + Privacy Gateway +
   companeros locales. Cero nube.
2. **El Agora** (la web publica, dominio 1) · probador, tablon firmado, Call
   Center de agentes. Nada se carga sin boton.
3. **HEXELION** (el rack privado, dominio 3) · enjambre de bucles + Forja LoRA
   + Ojo del Soberano. La fabrica disciplinada.

## El flywheel: Medallion aplicado a LoRAs

- **BRONZE** — correcciones del usuario, firmadas Ed25519, **inmutables**.
- **SILVER** — dataset curado: Curador + Privacy Gateway + checker de doctrina.
- **GOLD** — LoRA que pasa **doble puerta** (doctrina + aceptacion del usuario)
  y ademas la firma del carbono.
- **DEAD_PATH** — candidatos que regresan. **Archivados con causa, no
  borrados.** Un descarte sin causa se repite; con causa, se aprende.

## El meta-bucle

El Curador detecta un cluster de correcciones que no encaja en ningun companero
y **propone uno nuevo** en Bronze. El carbono firma crearlo.

El ecosistema se especializa solo. **Nunca sin firma.**

## Las cuatro decisiones abiertas · solo carbono

| | Pregunta | Por que no la puede cerrar el silicio |
|---|---|---|
| **D1** | Propiedad del LoRA: ¿exportable por el usuario o del ecosistema? | Define si el producto es una herramienta o una plataforma |
| **D2** | ¿Se paga con dinero, con datos firmados, o ambos? | Es el contrato con quien usa el producto |
| **D3** | Cola maxima del Jetson | Define la escasez REAL, y la cola se publica |
| **D4** | ¿Que pasa con un LoRA publicado si su autor se va? | Es una promesa a terceros, no una politica interna |

Mientras esten abiertas, nada de LorAtelier entra en produccion. La pieza
estrategica --el boton de corregir-- es el combustible: **sin combustible no
hay fabrica**, pero encenderla antes de responder a D1 y D2 seria pedir datos
sin saber que se hara con ellos.
