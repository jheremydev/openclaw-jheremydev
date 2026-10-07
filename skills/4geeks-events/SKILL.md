---
name: 4geeks-events
description: Consulta los próximos eventos de 4Geeks Academy: workshops, charlas, demo days y actividades programadas, con fecha, descripción, tipo e idioma.
user-invocable: true
disable-model-invocation: false
---

# Eventos próximos de 4Geeks Academy

Usa esta skill cuando Jheremy quiera saber qué eventos hay programados en la academia — workshops, charlas, demo days, mentorías grupales, lo que esté por venir. No mezcla nada de tareas, certificados ni perfil.

## Pre-requisitos

`FOURGEEKS_TOKEN` en el vault de OpenClaw como `kind: env`.

## Ejecución

```bash
python3 {baseDir}/scripts/4geeks-events.py
```

## Qué hace

1. Llama a `GET /v1/events/all?upcoming=true` en breathecode.herokuapp.com.
2. Ordena los eventos por fecha de inicio.
3. Para cada evento, muestra:
   - 📅 Cuándo es (fecha legible + "Hoy", "Mañana", "En X días", etc.)
   - Título del evento
   - Descripción o excerpt
   - Tipo de evento (workshop, charla, etc.)
   - Idioma
   - Modalidad (online o presencial + lugar)
   - Capacidad (si aplica)
   - URL de inscripción / banner
4. Resumen final agrupado por tipo.

## Notas

- Solamente eventos con `upcoming=true` — no muestra eventos pasados.
- Autenticación: `Authorization: Token $FOURGEEKS_TOKEN`.
- No modifica nada en la API — solo lectura.