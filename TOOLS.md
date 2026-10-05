# TOOLS.md - Connected Services

Qué conector de Zapier usar para cada tarea, cuándo usarlo y las convenciones a seguir. Lee la sección relevante antes de tocar un servicio por primera vez en una sesión.

## Google Calendar

- Úsalo para: crear eventos, consultar huecos libres, recordatorios con hora fija.
- Antes de crear un evento, consulta el calendario para evitar solapes.
- Formato de título: corto y descriptivo ("Entrevista - Empresa X", no "Reunión").
- Si el usuario no da duración, asume 30 min para llamadas/reuniones y 1h para bloques de trabajo/estudio.
- Añade una descripción con contexto (link, agenda, quién convoca) cuando se tenga.
- No borres ni muevas eventos que no hayas creado tú en la misma conversación sin confirmar.

## Gmail

- Úsalo para: leer bandeja de entrada, redactar borradores, enviar correos.
- **Nunca envíes un correo sin que Jheremy confirme el contenido final** (ver AGENTS.md). Redactar el borrador y mostrarlo sí es libre.
- Al triar la bandeja de entrada, distingue "requiere acción" de "solo informativo" — no crees tareas para newsletters o notificaciones automáticas.
- Firma por defecto: nombre completo, sin cargo salvo que el contexto sea claramente profesional/Projectum.

## Google Docs

- Úsalo para: crear documentos nuevos (planes, notas, resúmenes, diario de aprendizaje), o actualizar uno existente si el usuario lo referencia.
- Nombra los documentos con fecha + tema: "2026-10-05 - Plan de la semana".
- Si una skill reutiliza siempre el mismo documento (p. ej. el diario de aprendizaje), añade al final en vez de crear uno nuevo cada vez — busca el documento por nombre exacto primero.

## Google Drive

- Úsalo para: buscar, listar y organizar archivos; guardar el resultado de una skill cuando no encaja en un Doc (ej. notas de reunión).
- Carpeta por defecto para archivos generados por el agente: `OpenClaw/` en la raíz de Drive (créala la primera vez que haga falta).
- No borres ni muevas archivos que no hayas creado tú sin confirmar primero.

## Google Tasks

- Úsalo para: crear tareas puntuales (ej. triaje de bandeja de entrada, seguimiento de un correo).
- Lista por defecto: la lista principal ("My Tasks") salvo que el usuario pida una lista concreta.
- Cada tarea creada automáticamente debe llevar una descripción de una línea con el porqué (de dónde salió).

## GitHub

- Úsalo para: leer issues, PRs, commits; resumir actividad; abrir borradores de PR o issue.
- Repos relevantes: `jheremydev/ai-engineering-company-project-monorepo-jheremydev` (proyecto del curso), `jheremydev/openclaw-jheremydev` (este propio agente).
- **Nunca** push/merge directo a `main` sin confirmación (ver AGENTS.md). Commits en rama propia y PRs abiertos sí son libres.
- Al resumir, prioriza: PRs abiertos esperando review > issues asignados a Jheremy > actividad reciente general.

## Telegram

- Es el canal principal de contacto con Jheremy — úsalo para briefings, avisos proactivos y confirmaciones.
- Mensajes cortos y directos; si el contenido es largo (un resumen, un plan), manda 2-3 líneas + enlace al Doc/evento creado, no el contenido entero pegado.
- Solo la cuenta de Telegram emparejada (`dmPolicy: pairing`) puede hablar con el agente; no asumas que un mensaje de otro chat es de Jheremy.

## Convención general

Cuando una skill combine varios servicios (ej. Tareas → Calendar), deja claro en la respuesta qué se creó en cada uno, con enlaces directos. Si un conector falla o da error de permisos, dilo explícitamente en vez de reintentar en bucle o fingir que funcionó.
