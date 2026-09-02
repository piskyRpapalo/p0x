# 🏛️ ESTADO DEL SISTEMA · PROYECTO ALEJANDRÍA
## Generado: 2026-08-30 03:43:19

## 1. SERVICIOS ACTIVOS
### Ollama
"name":"preceptor-v7-linea-b:latest"
"name":"control-base-qwen3-4b:latest"
"name":"preceptor-v7:latest"
"name":"qwen2.5:7b"
"name":"llama3.2:3b"
"name":"qwen38-limpio:latest"
"name":"oficial-inventario:latest"
"name":"qwen3:30b-a3b-instruct-2507-q4_K_M"

### API Guía
inactive
- NO_DATA: api-guia no está activa

### Agentes del Enjambre
- guardian: inactive
inactivo
- curador: inactive
inactivo
- afinador: inactive
inactivo

### Timers Systemd
Sun 2026-08-30 04:13:28 WEST          30min Sat 2026-08-29 04:10:00 WEST     23h ago guardian.timer                 guardian.service
Sun 2026-08-30 05:01:09 WEST       1h 17min Tue 2026-08-25 01:31:16 WEST           - curador.timer                  curador.service
Mon 2026-08-31 03:09:42 WEST            23h Sun 2026-08-30 03:05:07 WEST   38min ago afinador.timer                 afinador.service

## 2. PUERTOS ACTIVOS
- 100[.]81[.]82[.]34:11434 → 
- 100[.]81[.]82[.]34:9001 → users:(("python3",pid=403615,fd=6))
- 0.0.0.0:8080 → users:(("python3",pid=419514,fd=3))
- 127.0.0.1:8740 → users:(("python3",pid=475769,fd=3))

## 3. REPOSITORIOS (Commits Pendientes)
- preceptor (main): 0 commits sin push
- preceptoros-web (main): 0 commits sin push
- preceptor-internal (main): 0 commits sin push

## 4. MEMORY.DB (Cahier del Beelink)
- Engramas: 
- Tamaño: 164K

## 5. DATASETS LORA
- sft_cot_v6.jsonl: 85 líneas
- sft_cot_v7.jsonl: 109 líneas

## 6. MODELOS EN OLLAMA
preceptor-v7-linea-b:latest           fe3915193f21    2.0 GB    9 hours ago     
control-base-qwen3-4b:latest          8d492c4e355b    2.5 GB    9 hours ago     
preceptor-v7:latest                   5c460e1de9a4    2.5 GB    9 hours ago     
qwen2.5:7b                            845dbda0ea48    4.7 GB    10 hours ago    
llama3.2:3b                           a80c4f17acd5    2.0 GB    29 hours ago    
qwen38-limpio:latest                  27edeefa4f4b    16 GB     29 hours ago    
qwen3:30b-a3b-instruct-2507-q4_K_M    19e422b02313    18 GB     5 weeks ago     

## 7. GATES (Estado de Tests)
### MVP (preceptor)
.................................................................................... [ 94%]
.....................s                                                   [100%]
429 passed, 2 skipped, 167 subtests passed in 10.09s

### Web (preceptoros-web)
Ran 17 tests in 0.056s

OK

## 8. ÚLTIMOS COMMITS (p0x)
12d6d40 fix(doogee): la URL del repo nombra PreceptorOS en vez de apoyarse en un redirect
7b3980c fix(forja): los constructores de dataset apuntaban a la carpeta vieja
15b38dd refactor: symlinks actualizados tras migración aurelius-* → preceptor-*
5d10b8c docs: actualizar estado del README (15 adapters producidos)
b2127d8 chore: eliminar log sanitizado temporal (reemplazado por informe.json)

## 9. FICHEROS DE CONTINUIDAD
- NO_DATA: no hay continuidad.db

---
Fichero generado automáticamente por volcar_estado.sh
Para actualizar: ~/p0x/volcar_estado.sh
