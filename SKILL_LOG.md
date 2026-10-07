# SKILL_LOG.md

Registro de cada skill construida por conversación con Kai (OpenClaw) para integrar la cuenta de 4Geeks (BreatheCode API).

## Skill 1 — Verificar token (verify-4geeks-token)

**Prompt inicial:**
> "Ahora sí, construyamos la primera skill: quiero que puedas verificar que el token es válido y que la sesión esté activa, llamando a la API de BreatheCode."

**Qué hace / endpoint:**
Verifica que `FOURGEEKS_TOKEN` (guardado en el vault de OpenClaw como `kind: env`, nunca escrito en archivos) sea válido y la sesión esté activa. Llama a `GET https://breathecode.herokuapp.com/v1/auth/user/me` con cabecera `Authorization: Token $FOURGEEKS_TOKEN`. Interpreta 200 como válido, 401/403 como expirado/inválido.
Archivo: `workspace/skills/verify-4geeks-token/SKILL.md`

**Prueba de que funciona:**
Con un token fresco, Kai devolvió el perfil real del estudiante: nombre (Jheremy Pinto Crespo), email, usuario de GitHub vinculado, rol (student @ 4Geeks Madrid) y fecha de alta (2026-07-07). Confirmó "TOKEN VÁLIDO — Sesión activa".

## Skill 2 — Obtener mis proyectos (4geeks-tasks)

**Prompt inicial:**
> "Ahora quiero la segunda skill: que puedas recuperar la lista de mis proyectos/tareas asignados con su estado actual (pendiente, entregado, calificado)."

**Qué hace / endpoint:**
Lista las tareas/proyectos asignados al estudiante vía `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`, con cabecera `Authorization: Token $FOURGEEKS_TOKEN`. Agrupa el resultado por `task_status` (PENDING, DONE, APPROVED, REJECTED).
Archivo: `workspace/skills/4geeks-tasks/SKILL.md`

**Prueba de que funciona:**
Devolvió 43 tareas reales agrupadas por estado: 2 pendientes ("Optimize Ubuntu on a VPS...", "My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress"), 41 en revisión, 0 aprobadas, 0 rechazadas — con nombres de tarea, tipo y cohorte reales en cada grupo.

## Skill 3 — Obtener trabajo pendiente (4geeks-progress)

**Prompt inicial:**
> "Ahora la tercera skill: dime específicamente qué trabajo me falta por completar — no solo la lista con estado, sino algo accionable: qué tareas están pendientes y, si la API lo da, para cuándo."

**Qué hace / endpoint:**
Analiza las tareas obtenidas de `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task` (mismo endpoint que la skill 2, filtrando por estado) y las convierte en una lista accionable: prioriza las pendientes por antigüedad, detecta tareas iniciadas pero nunca entregadas, y sugiere el próximo paso concreto.
Archivo: `workspace/skills/4geeks-progress/SKILL.md`

**Prueba de que funciona:**
Devolvió, con datos reales: 2 tareas pendientes priorizadas (una lección abierta hace 9 días, un proyecto creado hace 2 días), 1 tarea iniciada pero nunca entregada (42 días abierta), y 41 entregadas esperando revisión agrupadas por cohorte. Terminó con un "próximo paso" concreto: completar la lección que lleva más tiempo pendiente.

## Skill 4 — Resumen general de progreso (4geeks-dashboard)

**Prompt inicial:**
> "Última skill principal: quiero un resumen general de mi progreso en el curso — algo como un porcentaje o conteo de avance (cuántas tareas completadas vs totales, por cohorte si aplica), no la lista de tareas pendientes, sino la foto general de cómo voy."

**Qué hace / endpoint:**
Calcula un resumen cuantitativo del progreso a partir de `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`: porcentaje global de avance, conteo por `task_status`, desglose por cohorte y por `task_type`. A diferencia de la skill 3 (que da acciones concretas sobre tareas puntuales), esta da la foto general del curso.
Archivo: `workspace/skills/4geeks-dashboard/SKILL.md`

**Prueba de que funciona:**
Devolvió, con datos reales: progreso global 95% (41/43), desglose por 5 cohortes con porcentajes individuales (100%, 92%, 86%, 100%, 100%), desglose por tipo (ejercicios 100%, proyectos 89%, lecciones 50%), y una síntesis correcta señalando las 2 tareas que frenan el 100%.


## Conversación de descubrimiento

**Prompt inicial enviado a Kai:**
> "Quiero darte la habilidad de conectarte a mi cuenta de 4Geeks usando mi token de estudiante, sin que tenga que desarrollar código de mi parte. ¿Qué debemos hacer?"

**Qué sugirió / qué pidió Kai:**
Kai propuso varias opciones para obtener acceso a la cuenta de 4Geeks: una opción basada en credenciales (email/contraseña) que fue descartada por insegura, y una opción de pasar el token directamente por chat, también descartada porque quedaría persistido en el historial de Telegram y en la memoria del propio agente. Se optó en su lugar por el mecanismo seguro de OpenClaw: guardar el token (`4g_tok`, obtenido desde las cookies del navegador en learn.4geeks.com) en el vault de secretos (`openclaw secrets store set FOURGEEKS_TOKEN --kind env --value-file -`), inyectado como variable de entorno accesible solo por las llamadas `exec` del agente, sin pasar nunca por el chat ni quedar escrito en ningún archivo del repositorio.

## Skill 5 (extendida) — 4geeks-certificates

**Prompt inicial:**
> "Quiero una skill extra: que puedas consultar mis certificados obtenidos en 4Geeks."

**Qué hace / endpoint:**
Consulta los certificados obtenidos por el estudiante en BreatheCode, llamando a `GET /v1/certificate/me` con cabecera `Authorization: Token $FOURGEEKS_TOKEN`.
Nota: la documentación de referencia (`docs-4geeks-api-reference.md`) describe el endpoint genérico `GET /v1/certificate/` (con filtro opcional `cohort`), pero este exige un parámetro `academy_id` no resuelto en este flujo — probado directamente, devuelve `403: Missing academy_id parameter`. `/v1/certificate/me` es el endpoint correcto para consultar los certificados de un estudiante individual sin ese parámetro adicional; confirmado mediante prueba comparativa de ambos endpoints.
Archivo: `workspace/skills/4geeks-certificates/SKILL.md`

**Prueba de que funciona:**
Devolvió 1 certificado real: "Basic personal assistants with Opencraw", cohorte "Personal assistants with Opencraw" (4Geeks Madrid), firmado por Marco Gomez (Main Instructor), expedido 2026-10-05, estado PERSISTED (en cola para generación de PDF), con enlace de vista previa y enlace al PDF.

## Auditoría de endpoints contra la referencia oficial

**Prompt enviado a Kai:**
> "Ahora quiero que revises algo importante: en workspace/docs-4geeks-api-reference.md guardé la documentación oficial de los endpoints de la API de BreatheCode que debemos usar. Quiero que leas ese archivo y compares cada una de tus skills actuales (verify-4geeks-token, 4geeks-tasks, 4geeks-progress, 4geeks-dashboard, 4geeks-certificates) contra esa referencia: ¿cada una está llamando al endpoint correcto y con los parámetros correctos según el documento? [...] También confírmame que cada skill sigue manejando una sola responsabilidad de la API."

**Resultado:**
- `verify-4geeks-token` y `4geeks-dashboard` usaban `/v1/auth/user/me` en vez del endpoint recomendado por la referencia, `/v1/admissions/user/me`. Corregidas para usar `/v1/admissions/user/me`, manteniendo el resto de la lógica igual.
- `4geeks-tasks` y `4geeks-progress` ya coincidían exactamente con la referencia (sin cambios).
- `4geeks-certificates` mantiene `/v1/certificate/me` en vez del genérico `/v1/certificate/` de la referencia, por la razón justificada arriba (falta `academy_id`).
- Las 5 skills siguen manejando una sola responsabilidad de API cada una.

**Prueba de que funciona (post-corrección):**
`verify-4geeks-token` vía `/v1/admissions/user/me`: HTTP 200, perfil completo (Jheremy Pinto Crespo, GitHub jheremydev), cohorte activo detectado correctamente.
`4geeks-dashboard` vía `/v1/admissions/user/me`: dashboard completo generado (71 líneas), mismo output y nombre correcto que antes de la corrección.

## Skill 6 (extendida) — 4geeks-events

**Prompt inicial:**
> "Última skill extendida: quiero poder consultar los próximos eventos de la academia — charlas, workshops, demo days, lo que haya programado. Llama a GET /v1/events/all (puedes filtrar por upcoming=true para quedarte solo con los que vienen, y por academy si hace falta el id de mi academia). Que la skill se encargue únicamente de esto — eventos — sin mezclar nada de tareas, certificados o perfil."

**Qué hace / endpoint:**
Consulta los próximos eventos programados por la academia, llamando a `GET /v1/events/all` con `Authorization: Token $FOURGEEKS_TOKEN`, filtrando por `upcoming=true` para mostrar solo los que vienen.
Archivo: `workspace/skills/4geeks-events/SKILL.md`

**Prueba de que funciona:**
Devolvió 2 eventos próximos reales: "Miedos, Mitos y Realidades | ESPAÑA" (14/10/2026, 17:30–18:30, charla "¿La inteligencia artificial es una amenaza o una oportunidad?", online, 150 plazas) y la misma charla en horario LATAM (14/10/2026, 23:00–00:00).
