---
id: esfera-edge-ai
titulo: Edge-AI / LLMs locales
tipo: esfera
capa_codice: factual
enlaces:
  - redes-linux
  - aprendizaje
nivel: practicante
evidencia_fuerza: null
fuente: null
actualizado: 2026-07-03
descripcion_niveles:
  basico: "Se ejecutan modelos de inteligencia artificial directamente en los equipos locales, sin necesidad de usar internet o servidores lejanos."
  medio: "Los modelos de lenguaje (LLMs) y de procesamiento de voz se corren localmente en equipos como Ollama o con herramientas como whisper.cpp, usando cálculos rápidos en hardware local. Esto permite procesar datos como audio o texto sin depender de servidores en la nube, y se aplica en servicios como Faro y en la ingesta de audio verificada."
  experto: "Los modelos de lenguaje local (LLMs) y de procesamiento de voz (como whisper.cpp con OpenBLAS) operan en el rack, utilizando infraestructura local como Ollama en la-fragua/la-torre o pipelines como SmolVLM→RKNN en construcción. Este enfoque descentralizado evita dependencia de la nube y forma la base de cómputo para servicios de valor (Faro/Gateway) y para la tubería de ingesta (nomic-embed-text). El sistema ya opera en producción diaria mediante proxy LiteLLM, cola task-spooler y verificación de audio."
generado_por: cc-pendiente-revision
---

# Edge-AI / LLMs locales

LLMs y modelos locales corriendo en el rack (Ollama en la-fragua/la-torre,
whisper.cpp con OpenBLAS, pipeline SmolVLM→RKNN en construcción) sin depender
de nube. Es la base de cómputo que sostiene tanto los servicios de valor
(Faro/Gateway) como esta misma tubería de ingesta (nomic-embed-text).

Nivel practicante: ya opera en producción diaria (proxy LiteLLM, cola
task-spooler, ingesta de audio verificada). *[corrige]*