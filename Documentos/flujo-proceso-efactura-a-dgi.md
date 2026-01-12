# Flujo de proceso: e‑Factura (empresa en Uruguay) → DGI

Este documento describe el flujo **punta a punta** desde que se genera una **e‑Factura** en la web del sistema de facturación de un emisor en Uruguay hasta que la información **llega a DGI**, asumiendo que el **certificado digital** requerido (para firma FEA y la integración técnica) ya está incorporado al sistema de facturación.

Incluye **mensajes**, **emisor**, **receptor** y si son **síncronos** o **asíncronos**.

---

## Actores (quién habla con quién)

- **Usuario operador**: usa la web del sistema de facturación del **emisor**.
- **Web/Frontend del emisor**: UI.
- **Backend/Motor CFE del emisor**: arma XML, valida CAE, numera, etc.
- **Módulo de firma del emisor**: firma FEA (XMLDSig) con el certificado disponible en el sistema.
- **Receptor electrónico (cliente en Uruguay)**: empresa que recibe la e‑Factura y debe responder mensajes.
- **DGI (plataforma eFactura)**: recibe sobres/reportes y devuelve acuses/estados.

---

## Reglas/formatos que condicionan el flujo (según DGI)

### 1) El CFE debe ir firmado con FEA y la Adenda no se envía a DGI

En el formato de CFE se establece:

- Todo CFE debe contener **firma electrónica avanzada (FEA)**.
- La **Adenda** puede incluirse para información comercial, pero **no se envía a DGI** y **no está incluida en la firma enviada a DGI**.

Fuente: `extracted_pdfs/Formato_CFE_v24-Publicado.txt` (sección “Introducción” y “Zonas del CFE”).

### 2) Para e‑Factura, se debe enviar a DGI “previo” al envío al receptor electrónico, y no hace falta esperar autorización online

En el formato de sobre se indica que el emisor debe **emitir y enviar a DGI** (y **previo** al envío del comprobante al receptor electrónico) las **e‑Facturas** y sus notas de corrección, entre otros, y que **no se requiere esperar una autorización on line** de DGI para enviar el CFE al receptor.

Fuente: `extracted_pdfs/Formato_Sobre_v05-Publicado.txt` (Introducción, “No se requiere esperar…”).

### 3) Canal técnico con DGI: SOAP `ws_efactura`

En la documentación técnica de servicios externos se describen (al menos) estas operaciones:

- `ws_efactura / EFACRECEPCIONSOBRE` (envío de `EnvioCFE` → `ACKSobre`)
- `ws_efactura / EFACCONSULTARESTADOENVIO` (envío de `ConsultaCFE` → `ACKCFE`)
- `ws_efactura / EFACRECEPCIONREPORTE` (envío de reporte → `ACKRepDiario`)

Fuente: `extracted_pdfs/ServiciosWebExternosFacturaElectronicaVersionPublica_23052013.txt`.

> Nota: esta fuente es un documento técnico “version pública” (2013) y el repositorio también incluye documentación de consultas/solicitudes posterior; en el flujo se conserva la nomenclatura de mensajes/operaciones porque los formatos de `ACKSobre`/`ACKCFE`/`ACKRepDiario` se mantienen como concepto en las cartillas.

### 4) Intercambio emisor ↔ receptor: mensajes de respuesta (acuse y aceptación/rechazo)

El formato de mensajes de respuesta establece que:

- Al recibir un envío, el receptor debe generar una respuesta (acuse).
- Posteriormente, deberá dar cuenta de la aceptación o rechazo de cada comprobante.
- Ese “resultado” puede venir en **uno o múltiples mensajes** (depende de procesos internos).

Fuente: `extracted_pdfs/Formato_Mensaje_de_Respuesta_v19-Publicado.txt` (Introducción).

---

## Flujo de proceso (e‑Factura → “llega a DGI”)

> Nota sobre “certificado”: en la práctica el sistema necesita material criptográfico para (a) **firmar el CFE (FEA)** y (b) autenticarse/firmar invocaciones SOAP (WS‑Security). Aquí se asume que ya está incorporado, como premisa.

| Paso | Mensaje (nombre) | Emisor → Receptor | Contenido mínimo / detalles | ¿Síncrono o asíncrono? |
|---:|---|---|---|---|
| 0 | **CAE disponible** (precondición) | DGI → Emisor (vía portal/descarga) | CAE vigente para e‑Factura (rango de numeración, vencimiento, etc.). | N/A (precondición) |
| 1 | `POST /emitir-efactura` (o equivalente) | Usuario/Frontend → Backend emisor | Datos de operación (receptor uruguayo, ítems, moneda, totales, etc.). | **Síncrono** (request/response interno) |
| 2 | **Generar CFE (XML)** tipo e‑Factura | Backend → Backend | Construye el CFE (p.ej. tipo 111), asigna serie/nro dentro del CAE, calcula montos, arma zonas. | **Síncrono** (interno) |
| 3 | **Firmar CFE (FEA/XMLDSig)** | Backend → Módulo firma | Firma avanzada sobre las zonas requeridas; **no incluye Adenda** y la Adenda **no va a DGI**. | **Síncrono** |
| 4 | **Armar Sobre a DGI (`EnvioCFE`)** | Backend → Backend | Carátula (RUC emisor, RUC receptor=DGI, id emisor del envío, cantidad CFE, fecha, **certificado X509**), + 1..250 `CFE` firmados con el **mismo cert**. | **Síncrono** |
| 5 | SOAP `ws_efactura / EFACRECEPCIONSOBRE` | Emisor → DGI | `Datain/xmlData` conteniendo `EnvioCFE` (usualmente CDATA) + WS‑Security/HTTPS. | **Síncrono** (HTTP) |
| 6 | **`ACKSobre`** (acuse del sobre) | DGI → Emisor | `Estado=AS` (recibido) o `BS` (rechazado). Si `AS`: `Token` + `Fechahora` para consulta posterior. | **Síncrono** (respuesta inmediata) |
| 7 | **Envío al receptor electrónico (cliente)** | Emisor → Receptor | Envío del CFE (y/o sobre) por medio acordado: email con XML adjunto o web service; suele incluir PDF/representación. | **Asíncrono** (típico) |
| 8 | **Mensaje de respuesta a “Sobre” (acuse)** | Receptor → Emisor | `Estado=AS/BS` para el sobre recibido (no implica aceptación comercial final del CFE). | **Asíncrono** (típico) |
| 9 | SOAP `ws_efactura / EFACCONSULTARESTADOENVIO` | Emisor → DGI | `ConsultaCFE` con `IdReceptor` + `Token` (del `ACKSobre`). | **Asíncrono (negocio)** / **síncrono (técnico)** |
| 10 | **`ACKCFE`** (resultado por comprobante) | DGI → Emisor | Por cada CFE: `Estado=AE` (recibido/aceptado por DGI) o `BE` (rechazado) + motivos. | **Síncrono** (respuesta a la consulta) |
| 11 | **Respuesta a “Consulta de Comprobantes” (comercial)** | Receptor → Emisor | Aceptación/rechazo del CFE por el receptor (puede venir en 1 o varios mensajes según procesos internos). | **Asíncrono (negocio)** |
| 12 | *(si DGI rechaza y ya se envió al receptor)* **Comunicación de anulación por rechazo DGI** | Emisor → Receptor | Mensaje de anulación (no se envía a DGI). | **Asíncrono** |
| 13 | *(cierre operativo)* SOAP `ws_efactura / EFACRECEPCIONREPORTE` + `ACKRepDiario` | Emisor ↔ DGI | Reporte Diario (firmado) y su acuse. | **Síncrono** (por envío) |

---

## ¿Cuándo “llega a DGI”?

- **Llegó a DGI (recepción de transporte)**: cuando el emisor recibe **`ACKSobre` con `Estado=AS`** (paso 6).
- **Llegó y quedó validado por DGI a nivel comprobante**: cuando el emisor obtiene **`ACKCFE` con `Estado=AE`** para ese CFE (paso 10).

---

## Detalle de mensajes clave (resumen de campos)

- **`CFE` (e‑Factura XML)**: datos de transacción + CAE + timestamp de firma + **firma FEA** (sin Adenda para DGI).
- **`EnvioCFE` (Sobre)**:
  - **Carátula**: RUC emisor, RUC receptor (**DGI** o receptor del CFE), id del envío, cantidad CFEs, fecha, **certificado X509**.
  - **Contenido**: 1..250 CFEs.
- **`ACKSobre`**:
  - `Estado`: `AS`/`BS`.
  - Si `AS`: `Token` + `Fechahora` (habilita consulta posterior).
- **`ConsultaCFE`**: `IdReceptor` + `Token`.
- **`ACKCFE`**:
  - Por CFE: tipo/serie/número/fechas + `Estado` (`AE`/`BE`) + motivos si corresponde.
- **Mensajes emisor↔receptor (respuesta)**:
  - El receptor debe acusar recepción del sobre y luego aceptar/rechazar los CFEs; puede hacerlo **en uno o varios mensajes** (depende del proceso interno del receptor).

### Comunicación de anulación (si aplica)

Cuando DGI rechaza un CFE ya enviado al receptor, el emisor debe comunicar la anulación al receptor (y **no debe enviarse a DGI**).

Fuente: `extracted_pdfs/Formato_Mensaje_de_Respuesta_v19-Publicado.txt` (sección “3.4 anulación de CFE rechazado por DGI”).

