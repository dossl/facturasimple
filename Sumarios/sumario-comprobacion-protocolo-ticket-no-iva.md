# Sumario de comprobación: “protocolo” de envío de e‑Ticket no IVA (exterior) a DGI

Este documento reproduce la **última respuesta** (comprobación contra fuentes locales del repo) para aclarar si un e‑Ticket “se envía dos veces” a DGI.

---

## Verificación en fuentes: ¿“se envía dos veces” el e‑Ticket?

**No exactamente.** Según las fuentes, lo que ocurre es:

### 1) Envío del e‑Ticket (la “info del ticket”): 1 envío + 1 consulta posterior

- **Se envía el e‑Ticket una vez** dentro de un **Sobre** (XML `EnvioCFE`) a DGI vía `ws_efactura / EFACRECEPCIONSOBRE`.
- DGI responde en esa misma llamada con un **acuse del sobre** (`ACKSobre`) diciendo si el sobre fue aceptado/rechazado.
- **Si el sobre fue aceptado**, el emisor **debe consultar** luego el estado de los CFE incluidos, usando `ws_efactura / EFACCONSULTARESTADOENVIO`, y DGI devuelve `ACKCFE` con el estado por comprobante (AE/BE/…).

Esto está explícito en el doc de servicios: “en caso de ser aceptado el sobre, luego el usuario deberá consultar el estado…” y que esa consulta devuelve la respuesta por CFE/CFC.

```198:209:extracted_pdfs/ServiciosWebExternosFacturaElectronicaVersionPublica_23052013.txt
ws_efactura / EFACRECEPCIONSOBRE
Dado un XML con un Sobre, con uno o varios CFE, el servicio devuelve un XML de respuesta del sobre,
determinando si el mismo fue aceptado o no. En caso de ser aceptado el sobre, luego el usuario deberá
consultar el estado de los diferentes CFE/CFC incluidos en él.
...
ws_efactura / EFACCONSULTARESTADOENVIO
... se especifica, para cada CFE/CFC incluido en el sobre, si los mismos fueron aceptados, rechazados u observados.
```

**Conclusión**: aquí hay “dos fases”, pero **la segunda fase no re‑envía el ticket**; es una **consulta** del resultado.

### 2) Reporte Diario (fin del día): es otro envío, pero no es el ticket

El **Reporte Diario** es un **archivo distinto** que “contiene información por tipo de CFE/CFC” (resúmenes, montos totales, consumo diario, etc.). No es el XML del e‑Ticket.

```185:228:extracted_pdfs/Formato_Reporte_CFE_v13.2-Publicado.txt
REPORTE DIARIO DE INFORMACIÓN DE LOS CFE UTILIZADOS
...
Este reporte contiene información por tipo de Comprobante Fiscal Electrónico (CFE) certificado así como por tipo de Comprobante Fiscal de Contingencia (CFC).
...
B) Resumen: Es la zona donde se informa para cada tipo de comprobante:
• Los montos totales ... correspondientes a los CFE y CFC emitidos ...
• El consumo diario total de los CFE emitidos y anulados. No se incluye el consumo de CFC.
```

Además, el instructivo deja claro que se debe **generar y enviar el Reporte Diario**, que “recoge” los comprobantes enviados (recibidos y rechazados), pero no dice que se re‑envíen los CFEs completos:

```198:203:extracted_pdfs/Instructivo_Ingreso_Regimen_CFE_v18.txt
• Generar y enviar el Reporte Diario correspondiente:
o La totalidad de los comprobantes enviados (recibidos y rechazados) ... deben estar recogidos en el reporte.
```

---

## Resumen en una frase

- **El e‑Ticket (XML CFE) se envía una vez** (dentro de `EnvioCFE`), luego se **consulta** el resultado (`ACKCFE`); y aparte, al cierre, se envía un **Reporte Diario** que **resume** lo emitido (no re‑manda el ticket).

