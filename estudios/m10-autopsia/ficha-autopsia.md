## 1. Ficha tecnica de autopsia

**Modelo del dispositivo:** M10-EM-2  
**Vendedor:** Simatop  
**Ecosistema:** Tuya  
**Chip:** BK7231N (Comprobar el chip y sensor abriendo el aparato)  
**Driver de medición:** BL0937 (Verificar la fuentes fisica)  
**Compatible con CloudCutter:** No compatible (Firmware de Tuya pacheteado después de febrero 2022)  
**Gemelo declarado:** F1s202-EU, Chip BK7231N  
**Chip y sensor leidos abriendo el aparato; no hay via software para confirmarlos sin flashear. (Flasheo prohibido por decision del carbono)**

## 2. Prompt reutilizable para futuros intentos de liberacion OTA

Por favor, sigue este protocolo:

1. No tocar el M10 fisicamente
2. No flashear nada mas 
3. No buscar mas vias de extraccion (UART cerrado por el carbono)
4. Utilice un gemelo compatible y válido (F1s202-EU, Chip BK7231N)

Por favor no intentes más cambios ni descargas al dispositivo M10-EM-2.

## 3. Entrada para LA_NECROPOLIS.md (causa, intento, reemplazo)

```markdown
---

### Causa

El dispositivo M10-EM-2 se encuentra en un estado de autopsia, debido a que su chip BK7231N no está disponible en el sistema operativo Tuya. El dispositivo ha sido liberado a través de un gemelo declarado (F1s202-EU) con el mismo modelo y tipo de chip BK7231N.

### Intento

Este intento se realiza después de haber comprobado la autopsia completa del dispositivo, utilizando un gemelo compatible y válido. El reemplazo será necesario para seguir adelante con la liberación OTA del dispositivo, ya que el software original no puede ser utilizada directamente debido a las restricciones técnicas impuestas por Tuya.

### Reemplazo

El reemplazo consistirá en:

1. Comprobar y validarlo en una fábrica de confianza.
2. Flashear la nueva versión del software para asegurarse de que todo está correctamente configurado.
3. Instalar el nuevo dispositivo en su sitio original o en un segundo lugar.

Por favor, no se intentará realizar ningún cambio físico ni desplegar cambios adicionales al M10-EM-2 ya que la liberación OTA debe ser realizada siguiendo estos pasos y protocolos establecidos.
```