---
name: 4geeks-certificates
description: Consulta los certificados obtenidos por Jheremy en 4Geeks Academy: especialidad, academia, cohorte, fecha de expedición, firmante, estado y enlaces a vista previa y PDF.
user-invocable: true
disable-model-invocation: false
---

# Certificados de 4Geeks

Usa esta skill cuando Jheremy pida ver sus certificados del curso, comprobar si ya le emitieron alguno, o acceder al PDF/enlace de un certificado existente.

## Pre-requisitos

`FOURGEEKS_TOKEN` en el vault de OpenClaw como `kind: env`.

## Ejecución

```bash
python3 {baseDir}/scripts/4geeks-certificates.py
```

## Qué muestra

Lista todos los certificados del usuario con:
- Especialidad / nombre del certificado
- Academia y cohorte asociados
- Firmante y su rol
- Fecha de expedición
- Estado del certificado (PERSISTED = listo, PENDING = en cola)
- Enlace a vista previa (Google Storage)
- Enlace al PDF

## Notas

- Endpoint: `GET /v1/certificate/me` en breathecode.herokuapp.com
- Autenticación: `Authorization: Token ***
- Si el token expira, pide renovar con `openclaw secrets store set FOURGEEKS_TOKEN --kind env`