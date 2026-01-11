A continuación se documentan **los trámites** y **las acciones técnicas** que aparecen en las **fuentes oficiales** disponibles en este repositorio (PDFs descargados de `efactura.dgi.gub.uy` + `Documentos/tramites.md`) para operar un sistema/sitio web de **Comprobantes Fiscales Electrónicos (CFE)** en Uruguay, con **Firma Electrónica Avanzada (FEA)**, usando certificados vinculados a **ABITAB**, y en un esquema reconocido por **DGI**.

> **Regla de evidencia**: no se incluyen requisitos o pasos que no puedan sustentarse en las fuentes disponibles.  
> **Citas**: se citan por **PDF / página / párrafo** (P#) cuando el texto fue extraíble; el documento de ABITAB está en PDF “escaneado” y fue transcripto por OCR, indicando igualmente **página y párrafo**.

---

## Fuentes utilizadas (locales)

- `Fuentes-Gub.uy/Instructuvos-DGI/Instructivo_Ingreso_Regimen_CFE_v18.pdf` (impresión 15/10/2025).
- `Fuentes-Gub.uy/Instructuvos-DGI/Instructivo_Actualizacion_Datos_SW_v03.pdf` (impresión 17/11/2022).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Formato_CFE_v24-Publicado.pdf` (impresión 30/06/2023).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Formato_Sobre_v05-Publicado.pdf` (impresión 10/06/2024).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Formato_Reporte_CFE_v13.2-Publicado.pdf` (impresión 30/06/2023).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Formato_CAE_v05-Publicado.pdf` (impresión 29/05/2020).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Formato_Mensaje_de_Respuesta_v19-Publicado.pdf` (impresión 25/11/2025).
- `Fuentes-Gub.uy/Generales-Documentos de Interes/Servicios+Solicitudes+eFactura+1.0.pdf` (impresión 09/08/2024).
- PDF oficial enlazado desde `efactura.dgi.gub.uy` sobre ABITAB/ID-Digital (descargado y guardado en el workspace como `extracted_web/autoridad-certificadora-id-digital.html`, OCR a texto para citación).

---

## 1) Evidencia sobre ABITAB y certificados para Firma Electrónica Avanzada

### 1.1. ABITAB como prestador acreditado (Firma Electrónica Avanzada)

En una resolución de la **Unidad de Certificación Electrónica (UCE)** (AGESIC), consta:

- La solicitud de ABITAB “a los efectos de su acreditación” como prestador. (PDF “autoridad-certificadora-id-digital”, p.1, P2)
- Que la Ley 18.600 y el Decreto 436/011 “establecen los requisitos” para ser prestador acreditado. (p.1, P3)
- Que entre esos requisitos se incluye contar con procedimientos adecuados “en el ámbito de la firma electrónica avanzada”. (p.1, P5)
- La resolución “Autorizar la condición de Prestador de Servicios de Certificación Acreditado de ABITAB S.A.” e inscribirlo en el registro correspondiente. (p.2, P6)

**Implicancia para eFactura (solo con evidencia disponible):** las cartillas/formato de CFE requieren **Firma Electrónica Avanzada**; este documento acredita que ABITAB está habilitado (en el marco UCE/AGESIC) como prestador acreditado para certificación vinculada a FEA. No se encontró, en los PDFs locales, un párrafo que diga explícitamente “DGI acepta ABITAB para firmar CFE”, pero sí se documenta (ver sección 3) que todo CFE debe llevar FEA y que DGI valida la firma en Testing/Homologación/Producción.

---

## 2) Trámite en DGI para ser emisor reconocido: ambientes, usuarios y etapas

### 2.1. Ambientes del Portal eFactura: Testing, Homologación y Producción

El instructivo de ingreso describe los ambientes y su propósito:

- **Testing**: permite “validar los formatos y la firma electrónica” de CFE/reportes/mensajes mediante mecanismos automatizados; para ingreso tradicional exige cumplir la “Prueba de Testing” y requiere solicitar clave para acceder. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.3, P1)
- **Homologación**: opera para quienes cumplieron la prueba, quienes ingresan por mecanismo simplificado, y para solicitar autorización de “Nuevo CFE”; también se debe solicitar clave/rol específico. (p.3, P1)
- **Producción**: funcionalidades necesarias para la operativa (envío de CFE y reportes, consultas, actualización de datos), y solo pueden operar emisores autorizados desde la vigencia de su autorización; requiere solicitar clave/rol de Producción. (p.4, P1)

### 2.2. Solicitud de claves/usuarios (roles por ambiente)

Para ingresar al Portal eFactura se solicita usuario/clave por ambiente:

- Se ingresa en el Portal de Servicios en Línea, opción `eFactura-Solicitud Usuario`. (p.5, P1)
- Se debe completar “Solicitud de Creación de Usuario para eFactura” indicando CI/NIE y correo, el rol (Testing/Homologación/Homologación simplificada/Producción) y la clave. (p.5, P1)
- Si se solicita Homologación para ingreso tradicional, se debe indicar la fecha en que se cumplió la “Prueba de Testing” para verificación de DGI. (p.5, P1)

---

## 3) Acciones técnicas mínimas que DGI exige en el proceso (según instructivos + formatos)

### 3.1. En Testing: validación de formatos y firma, y “Prueba de Testing” (ingreso tradicional)

El instructivo detalla que, en Testing:

- Se validan “los formatos y la firma electrónica” de sobres, CFE y reportes enviados. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.6, P1)

Para la **Prueba de Testing** (solo ingreso tradicional):

- Debe enviarse a DGI un mínimo de **50 documentos distintos por cada tipo de CFE** del “combo mínimo” (incluye e-Factura y e-Ticket con sus notas), que cumplan validaciones y queden “Recibido”; los “Rechazado” no cuentan para el mínimo. (p.7, P1)
- Se debe “Generar y enviar el Reporte Diario correspondiente”; incluye recibidos y rechazados, y si el reporte es rechazado puede reenviarse; además se debe “Procesar Reporte Diario”. (p.7, P1)
- DGI verifica, para otorgar clave/rol de Homologación (ingreso tradicional), que exista un Reporte Diario con “Fecha de Resumen” igual a la indicada como “Fecha de prueba de testing” con estado “Reporte Procesado”, y que se cumpla el mínimo de 50 “Recibidos” por tipo del combo mínimo. (p.9, P1)

### 3.2. Postulación: datos técnicos del postulante (incluye “sitio web” y, si aplica, WebService)

En ingreso tradicional, el formulario de postulación exige (entre otros):

- “Dirección del sitio Web del postulante – URL.” (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.9, P1)
- “URL para Webservice” y “Mail de contacto técnico” como **obligatorios** si el proveedor de software es un “proveedor habilitado”. (p.10, P1)

### 3.3. Declaración de requisitos técnicos: publicación web de e-Tickets y obligaciones operativas

En la declaración de “requisitos técnicos” (que el postulante acepta), se listan funciones críticas (auditables por DGI), incluyendo:

- Almacenamiento/control de acceso del archivo CAE. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.10, P1)
- Respaldo de los CFE e información generada “incluye la **publicación de los e-tickets** … en la **Web del emisor electrónico**”. (p.10, P1)
- Envío de CFE y Reportes Diarios a DGI. (p.10, P1)
- Compromiso de cumplir cartillas de formatos publicadas por DGI y actualizar sistemas ante nuevas versiones. (p.10, P1)
- No permitir emisión de comprobantes que no cumplan con estándar de emisión/firma/envío definidos por DGI. (p.10, P1)

### 3.4. Autorización e inicio de emisión en Producción

Luego de cumplir requisitos, DGI comunica la inclusión y CFE autorizados; la inclusión se efectiviza al día siguiente de verificada la comunicación. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.11, P1)

Además, una vez autorizada la calidad de emisor electrónico:

- “la empresa dispone de un plazo de **1 mes** para documentar sus operaciones exclusivamente mediante los CFE” autorizados (con coexistencia temporal con papel). (p.11, P1)

---

## 4) Firma electrónica avanzada en el CFE y qué se firma / qué no se envía

El formato de CFE establece:

- “Todo CFE que se emita, debe contener una **firma electrónica avanzada** … garantiza la integridad del CFE.” (`Formato_CFE_v24-Publicado.pdf`, p.16, P1)
- En la zona de firma: “Se firma toda la información … (Zonas A, B, C, D, E, F, G, H y K). Esta firma **no incluye** la zona J - **Adenda**.” (p.16, P1)
- La Adenda “no debe ser enviada a la DGI.” (p.16, P1)

**Acción técnica derivada (con evidencia):**

- Implementar la firma FEA del XML del CFE sobre las zonas requeridas (excluyendo Adenda), y garantizar que la Adenda (si existe) no se envía a DGI.

---

## 5) “Sitio web” y verificación/publicación en la representación impresa (e-Ticket)

El formato de representación impresa indica, para el “pie del comprobante”:

- Se imprime un **QR-Code** y debajo “Código de seguridad” con “los 6 primeros caracteres del hash”. (`Formato_CFE_v24-Publicado.pdf`, p.80, P1)
- El QR contiene un “Link al Portal de e-factura” con parámetros (RUC, tipo CFE, serie/número, monto, fecha de firma, y “Código de seguridad … (hash SHA-2)”), y el link ejemplo es: `https://www.efactura.dgi.gub.uy/consultaQR/cfe?ruc,tipoCFE,serie,nroCFE,monto,fecha,hash`. (p.80, P1)
- En la frase de verificación, distingue:
  - “e-Tickets y sus notas de corrección: ‘Puede verificar comprobante en www…(**URL de la empresa**)’”
  - “Restantes comprobantes: ‘Puede verificar comprobante en **www.dgi.gub.uy**’” (p.80, P1)

**Implicancia para “sitio web” (según evidencia):**

- Para e-Ticket, la representación impresa requiere una **URL de la empresa** para “verificar comprobante”, y el proceso de postulación/declaración exige la **publicación de e-tickets en la web del emisor** (sección 3.3).

---

## 6) Envío a DGI: Sobres (CFE/CFC), reglas de envío, y certificado en el sobre

El formato del sobre establece:

- El emisor debe “emitir y enviar a la DGI … previo al envío del comprobante al receptor electrónico …” ciertos CFEs, incluyendo e-Facturas y e-Tickets (con condición de monto para e-Tickets). (`Formato_Sobre_v05-Publicado.pdf`, p.4, P1)
- Para e-Tickets: se listan “e-Tickets y sus notas de corrección con monto neto excluido el IVA mayor a **5.000 UI**”. (p.4, P1)
- “No se requiere esperar una autorización on line de la DGI” para enviar al receptor/transporte/entrega impresa (según corresponda). (p.4, P1)
- En la carátula del sobre se incluye “información pública del certificado electrónico con el cual se firmaron los CFE incorporados al sobre” y “Todos los CFE incluidos en el sobre deben ser firmados con el **mismo certificado electrónico**.” (p.4, P1)

**Acciones técnicas derivadas (con evidencia):**

- Implementar generación de sobres XML con carátula y contenido, asegurando consistencia de certificado (un solo certificado por sobre) y cumpliendo las reglas de envío previo.

---

## 7) Reporte Diario: formato y firma

El formato del Reporte Diario indica que una de sus zonas es:

- “C) Firma Electrónica Avanzada: firma electrónica avanzada del emisor sobre la totalidad de los datos del reporte.” (`Formato_Reporte_CFE_v13.2-Publicado.pdf`, p.8, P1)

Y el instructivo vincula su uso operativo y en Testing (procesar reporte, estado “Reporte Procesado”) para la Prueba de Testing. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.7–9, P1)

---

## 8) CAE: qué es, cómo se solicita y qué exige el proceso

El formato de CAE define:

- El CAE es un “archivo informático generado y firmado electrónicamente por DGI, en base a una solicitud de autorización enviada por un emisor electrónico”, y contiene rango de numeración autorizado. (`Formato_CAE_v05-Publicado.pdf`, p.4, P1)
- “Por cada tipo de CFE, se solicita un CAE.” (p.4, P1)
- “Se deja disponible en la Web al emisor electrónico.” (p.4, P1)
- “El plazo de validez es de 2 años.” (p.4, P1)

Y la declaración del instructivo exige “Almacenamiento y control de acceso del archivo … CAE”. (`Instructivo_Ingreso_Regimen_CFE_v18.pdf`, p.10, P1)

---

## 9) Mensajes de respuesta (acuse) y firma de DGI

En el formato de mensaje de respuesta:

- Para “Reporte Diario”: “DGI envía el mensaje al emisor del Reporte Diario” e “Incluye la firma electrónica avanzada sobre toda la información.” (`Formato_Mensaje_de_Respuesta_v19-Publicado.pdf`, p.11, P1)

---

## 10) Actualización obligatoria de datos de software (DGI 168/2021) y su trámite

El instructivo de actualización de datos indica:

- La Resolución DGI Nº 168/2021 estableció obligación de informar “todas las soluciones de software” que integran procesos de facturación y/o conservación de CFE. (`Instructivo_Actualizacion_Datos_SW_v03.pdf`, p.3, P1)
- Se presenta “exclusivamente” por emisores electrónicos en el portal e-Factura, en ambientes Homologación o Producción, mediante la aplicación “Actualización de datos”. (p.3, P1)
- La obligación se genera al adquirir calidad de emisor o al modificarse información; existe plazo “hasta el segundo mes siguiente” de producido el cambio. (p.3, P1)

---

## 11) Servicios Web Externos (eFactura): evidencia de WS-Security y de actualización de contactos

El documento `Servicios+Solicitudes+eFactura+1.0.pdf` establece:

- El servicio utiliza seguridad basada en “WS-Security” y depende del “uso de certificados y firmas digitales”, para lograr autenticación/confidencialidad/integridad/no repudio. (`Servicios+Solicitudes+eFactura+1.0.pdf`, p.3, P1)
- El WSDL “para ambiente de TEST” está publicado en una URL específica (ver p.6). (p.6, P1)
- En WS-Security: el certificado a utilizar “podrá ser” un certificado nominado o innominado de persona jurídica (y añade una nota “al día de hoy…” sobre emisores dentro de PKI Uruguay). (p.7, P1)
- Se incluye un método `EFACSOLACTUALIZARCONTACTO` que actualiza contactos del emisor, con “códigos habilitados… 19: URL Webservice y 20: Mail Contacto Técnico”. (p.3, P1)
- Hay un ejemplo de actualización del “ContactoCodigo 20 ( Mail Contacto Técnico )”. (p.5, P1)

> **Nota de consistencia**: este documento es de 2024 y describe certificados en el contexto de WS-Security/PKI; la evidencia de ABITAB como prestador acreditado para certificación/firma avanzada proviene del documento UCE/AGESIC 2014 (sección 1). No se halló en estas fuentes locales un texto que unifique explícitamente ambos mundos (“certificado para WS-Security” vs “certificado para firmar CFE”) bajo un mismo tipo.

---

## Checklist operativo (solo con base en evidencia de fuentes)

### A) Trámites (DGI + certificados)

- **Acreditar/obtener un certificado** para FEA con un prestador acreditado (ABITAB figura como prestador acreditado por UCE). (doc ABITAB p.1–2)
- **Solicitar usuario/clave/rol** en Portal eFactura por ambiente (Testing/Homologación/Producción). (`Instructivo_Ingreso...`, p.5)
- Si ingreso tradicional: **cumplir Prueba de Testing** (mínimo 50 por tipo del combo mínimo + Reporte Diario + procesar reporte). (`Instructivo_Ingreso...`, p.7–9)
- **Postularse en Homologación** completando, entre otros, **URL del sitio web** del postulante, y (si corresponde) URL WS y mail técnico. (`Instructivo_Ingreso...`, p.9–10)
- Tras autorización: operar en **Producción** desde la vigencia; considerar plazo de 1 mes para documentar operaciones solo con CFE autorizados. (`Instructivo_Ingreso...`, p.11)
- Cumplir con **Actualización de datos** (software) en Homologación/Producción cuando corresponda. (`Instructivo_Actualizacion...`, p.3)

### B) Acciones técnicas (core)

- **Generar XML de CFE** en el formato y zonas definidas, incluyendo FEA; **no** incluir Adenda en la firma y **no** enviar Adenda a DGI. (`Formato_CFE_v24`, p.16)
- **Construir y enviar sobres** cuando aplique, incluyendo certificado del sobre y usando el mismo certificado para todos los CFE del sobre. (`Formato_Sobre_v05`, p.4)
- **Generar y enviar Reporte Diario** con FEA del emisor sobre todo el reporte. (`Formato_Reporte_v13.2`, p.8)
- **Gestionar CAE**: solicitar por tipo de CFE; almacenar/controlar acceso al archivo CAE; respetar validez y rango. (`Formato_CAE_v05`, p.4; `Instructivo_Ingreso...`, p.10)
- **Procesar acuses/mensajes de respuesta** firmados por DGI (incluye firma avanzada en respuestas, p.ej. reporte diario). (`Formato_Mensaje_Respuesta_v19`, p.11)
- **“Sitio web” para e-Ticket**: contemplar que la representación impresa exige URL de la empresa para verificación en e-Tickets, y el proceso exige publicar e-Tickets en web del emisor; además el QR incluye un link al portal eFactura con parámetros, incluyendo hash SHA-2. (`Formato_CFE_v24`, p.80; `Instructivo_Ingreso...`, p.10)

---

## Apéndice: metodología de citación (párrafos)

Para los PDFs con texto embebido, se extrajo el contenido por página y se numeraron párrafos como bloques separados por líneas en blanco. En el PDF escaneado (ABITAB/UCE/AGESIC) se utilizó OCR; los “P#” corresponden a los bloques que devolvió el OCR por página.

