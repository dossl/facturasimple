# Regla: Evidencia y citas (eFactura Uruguay / DGI / ABITAB)

## Alcance

Aplicar esta regla cuando el trabajo involucre **trámites**, **normativa**, o **implementación técnica** de **facturación electrónica (CFE)** en Uruguay (DGI / eFactura), especialmente si se usa documentación en `Fuentes-Gub.uy/`, `Documentos/` o material descargado de `efactura.dgi.gub.uy`.

## Regla de evidencia (obligatoria)

- **No supongas nada.** Solo afirmes requisitos, pasos, obligaciones o conclusiones cuando exista **evidencia segura** en una fuente disponible en el repo o una página oficial descargada.
- Si hay **contradicción** entre fuentes, usa la **más reciente** (por fecha de impresión/versión indicada en la fuente) y explica brevemente el criterio.

## Regla de citas (obligatoria)

- Cuando cites documentación, hazlo con precisión como: **(documento, p.X, P.Y)** donde:
  - **p.X** = número de página.
  - **P.Y** = número de párrafo (bloque) dentro de esa página, según extracción a texto.
- Si el documento fue transcripto por OCR, indícalo explícitamente: **(OCR)**.

## Fuentes preferidas en este repo para citación

- **PDFs con extracción por página/párrafo**: usar los `.txt` generados en `extracted_pdfs/` que contienen separadores `=== PAGE N ===` y párrafos `[P#]`.
- **PDFs escaneados**: si no hay texto embebido, usar los `.txt` generados por OCR en `extracted_pdfs/*_OCR.txt` y citar igual por página/párrafo, indicando **(OCR)**.

## Ejemplo de estilo de cita (formato)

- “Todo CFE que se emita, debe contener una firma electrónica avanzada…” (`Formato_CFE_v24-Publicado.pdf`, p.16, P1)

