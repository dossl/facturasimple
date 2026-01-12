# Flujo de proceso: E‑Ticket exento (sin IVA) emitido al exterior → DGI

Este documento describe el **flujo punta a punta** desde que se genera un **E‑Ticket** en la web del sistema de facturación hasta que la información queda **recibida/aceptada por DGI**, suponiendo que el **certificado digital del emisor** está incorporado al sistema y que el comprobante es **exento de IVA** por corresponder a una operación “al exterior”.

> Convención: se listan los pasos con **mensajes**, **emisor**, **receptor** y si son **síncronos** o **asíncronos** (en términos de interacción técnica y/o de negocio).

---

## Actores

- **Operador (usuario)**: persona que emite el E‑Ticket en la web.
- **Web/Frontend del sistema**: UI donde se carga la venta y se solicita emitir.
- **Backend / Motor de facturación (CFE)**: construye el CFE, aplica CAE, calcula montos, etc.
- **Módulo de firma (FEA)**: firma el CFE con el certificado del emisor.
- **DGI (plataforma eFactura)**: recibe sobres/reportes y emite acuses.
- **Cliente en el exterior**: receptor no-electrónico (recibe PDF/email/portal).
- **Sitio web del emisor**: publicación/verificación del e‑Ticket (requerido para e‑Tickets).

---

## Premisas / configuración del comprobante

- **Tipo de comprobante**: E‑Ticket (CFE).
- **Tratamiento “exento por exterior”**:
  - A nivel ítem, se marca como **exportación y asimiladas** usando `IndFact = 10`.
  - A nivel totales, se utiliza el acumulador **exportación/asilimilados** `MntExpoyAsim` (manteniendo IVA en 0 donde corresponda).
- **Firma**:
  - El CFE se firma con **Firma Electrónica Avanzada (FEA)**.
  - Si el CFE incluye **Adenda**, **no se envía a DGI**.

---

## Flujo principal (emisión → recepción/aceptación en DGI)

### 1) Solicitud de emisión en la web

- **Mensaje**: `POST /emitir-eticket` (o equivalente; request interno del sistema)
- **Emisor → Receptor**: Operador → Web/Frontend → Backend
- **Sincronía**: **Síncrono**
- **Detalles**:
  - Datos del emisor, receptor (exterior), fecha, moneda, ítems, montos.
  - Indicadores para “exento/exterior” que el motor convertirá al XML (ej. `IndFact=10`).

### 2) Generación del CFE (XML) en el motor de facturación

- **Mensaje**: “Generar CFE E‑Ticket (XML)”
- **Emisor → Receptor**: Backend → Backend
- **Sincronía**: **Síncrono**
- **Detalles**:
  - Asignación de **Serie/Nro** conforme CAE vigente (precondición).
  - Generación del detalle de ítems con `IndFact=10`.
  - Cálculo de totales (incluyendo `MntExpoyAsim` si aplica) y consistencia general.

### 3) Firma electrónica avanzada del CFE (FEA)

- **Mensaje**: “Firmar CFE (XMLDSig/FEA)”
- **Emisor → Receptor**: Backend → Módulo de firma/certificado
- **Sincronía**: **Síncrono**
- **Detalles**:
  - Se firma el CFE con el certificado incorporado al sistema.
  - La **Adenda** (si existe) se trata como información no enviada a DGI.

### 4) Publicación / verificación del e‑Ticket + entrega al cliente exterior

- **Mensajes**:
  - Publicación interna: “Publicar e‑Ticket en sitio web del emisor”
  - Entrega externa: “Enviar PDF/Link por email/portal”
- **Emisor → Receptor**:
  - Backend → Sitio web del emisor
  - Backend → Cliente exterior
- **Sincronía**:
  - Publicación: típicamente **síncrona** (o encolada internamente, según arquitectura).
  - Envío al cliente: generalmente **asíncrono** (email/portal).
- **Detalles**:
  - La representación impresa del e‑Ticket incluye **URL del emisor** para verificación.
  - Puede incluir QR/código de seguridad para consulta.

### 5) Construcción del Sobre para DGI (`EnvioCFE`)

- **Mensaje**: `EnvioCFE` (XML de sobre)
- **Emisor → Receptor**: Backend → Backend
- **Sincronía**: **Síncrono**
- **Detalles del mensaje** (carátula + CFEs):
  - **Carátula**: `RutReceptor`, `RUCEmisor`, `Idemisor`, `CantCFE`, `Fecha`, `X509Certificate`
  - **Contenido**: lista `CFE` (máx. 250 por sobre)
  - Un **solo certificado** para todos los CFE del mismo sobre (coherencia de firma).

### 6) Envío del sobre a DGI (Recepción de sobre)

- **Mensaje**: SOAP `ws_efactura / EFACRECEPCIONSOBRE`
  - Request: `Datain` conteniendo el XML `EnvioCFE` (usual: dentro de CDATA)
- **Emisor → Receptor**: Sistema de facturación → DGI
- **Sincronía**: **Síncrono**
- **Detalles**:
  - Seguridad: **WS-Security** (certificados + firma digital) + HTTPS.

### 7) Respuesta inmediata de DGI al envío del sobre (`ACKSobre`)

- **Mensaje**: `ACKSobre` (XML)
- **Emisor → Receptor**: DGI → Sistema de facturación
- **Sincronía**: **Síncrono** (respuesta del `EFACRECEPCIONSOBRE`)
- **Detalles del mensaje**:
  - `Detalle/Estado`:
    - `AS`: Sobre recibido
    - `BS`: Sobre rechazado
  - `MotivosRechazo` si `BS`.
  - `ParamConsulta` si `AS`, con:
    - `Token`
    - `Fechahora` (momento desde el que puede consultarse el resultado final por CFE)

### 8) Consulta del estado final de los CFE del sobre (resultado diferido)

- **Mensaje**: SOAP `ws_efactura / EFACCONSULTARESTADOENVIO`
  - Request: `ConsultaCFE` incluyendo el `Token` recibido en `ACKSobre/ParamConsulta`
- **Emisor → Receptor**: Sistema de facturación → DGI
- **Sincronía**:
  - **Asíncrono (de negocio)**: se ejecuta **después** del envío del sobre, cuando corresponde (p.ej. desde `Fechahora`).
  - **Síncrono (técnico)**: cada consulta es request/response HTTP.

### 9) Respuesta de DGI con estado por comprobante (`ACKCFE`)

- **Mensaje**: `ACKCFE` (XML)
- **Emisor → Receptor**: DGI → Sistema de facturación
- **Sincronía**: **Síncrono** (respuesta del `EFACCONSULTARESTADOENVIO`)
- **Detalles del mensaje**:
  - Se informan los comprobantes del sobre (`TipoCFE`, `Serie`, `NroCFE`, `TmstCFE`, etc.).
  - `Estado` por CFE:
    - `AE`: Comprobante recibido (aceptado)
    - `BE`: Comprobante rechazado (incluye `MotivosRechazoCF`)
  - Para este caso, el “final feliz” es **`AE`** para el E‑Ticket.

---

## Cierre operativo recomendado (Reporte Diario)

Aunque el “llegó a DGI” queda cubierto al obtener `ACKCFE` con `AE`, la operativa completa del régimen implica el **Reporte Diario**:

### 10) Envío del Reporte Diario a DGI

- **Mensaje**: SOAP `ws_efactura / EFACRECEPCIONREPORTE`
- **Emisor → Receptor**: Sistema de facturación → DGI
- **Sincronía**: **Síncrono**
- **Detalles**:
  - Reporte diario consolidado (firmado).

### 11) Respuesta de DGI al Reporte Diario (`ACKRepDiario`)

- **Mensaje**: `ACKRepDiario` (XML)
- **Emisor → Receptor**: DGI → Sistema de facturación
- **Sincronía**: **Síncrono**
- **Detalles**:
  - `Detalle/Estado` + `MotivosRechazo` (si corresponde).

---

## Estados finales (resumen)

- **Sobre recibido por DGI**: `ACKSobre/Detalle/Estado = AS`
- **E‑Ticket recibido/aceptado por DGI**: `ACKCFE/ACKCFE_Det/Estado = AE`
- **Si hay rechazo**:
  - Rechazo de sobre: `ACKSobre/Detalle/Estado = BS` + `MotivosRechazo`
  - Rechazo de CFE: `ACKCFE_Det/Estado = BE` + `MotivosRechazoCF`

