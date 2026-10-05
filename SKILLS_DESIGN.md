# SKILLS_DESIGN.md

Diseño de las skills personalizadas antes de implementarlas.

## 1. Diario de aprendizaje diario

**¿Qué hace esta skill?**
Convierte unos apuntes sueltos sobre lo aprendido en el día en una entrada formateada de un diario de aprendizaje en Google Docs, usado para llevar registro del curso de AI Engineering.

**¿Qué input necesita el agente?**
Jheremy le dice en lenguaje natural, en cualquier formato, qué aprendió hoy (puede ser una lista de bullets sueltos o un párrafo). El agente ya sabe por `USER.md` que está haciendo el programa de 4GeeksAcademy AI Engineering, y por `TOOLS.md` que el documento se busca por nombre exacto antes de crear uno nuevo (para no duplicar diarios).

**¿Cómo es un buen output?**
Una entrada nueva al final del Google Doc "Diario de Aprendizaje - AI Engineering" (se crea si no existe), con fecha como encabezado (`## YYYY-MM-DD`) y los puntos aprendidos como lista, reescritos de forma clara pero sin inventar contenido que Jheremy no mencionó. El agente confirma por el canal donde se le pidió (normalmente Telegram) con un enlace directo al documento. Se sabe que funcionó si el Doc tiene una nueva sección con la fecha de hoy y el contenido correcto, sin duplicar entradas de días anteriores.

## 2. Resumen diario de GitHub

**¿Qué hace esta skill?**
Lee el estado de los repos relevantes de Jheremy en GitHub y manda un briefing corto por Telegram con lo que necesita su atención.

**¿Qué input necesita el agente?**
Ninguno obligatorio — se activa con un mensaje tipo "resúmeme GitHub" o por una automatización programada. El agente ya sabe por `TOOLS.md` qué repos mirar (`ai-engineering-company-project-monorepo-jheremydev`, `openclaw-jheremydev`) y el orden de prioridad (PRs abiertos esperando review > issues asignados a Jheremy > actividad reciente), y por `AGENTS.md` que nunca debe hacer push/merge a main sin confirmación — esta skill es solo de lectura, no toca nada.

**¿Cómo es un buen output?**
Un mensaje de Telegram corto (no más de ~10 líneas), agrupado por repo, con como mucho 3-5 ítems por categoría y enlaces directos a cada PR/issue. Si no hay nada pendiente en un repo, lo omite en vez de decir "no hay nada". Se sabe que funcionó si el mensaje llega con datos reales (no inventados) que coinciden con lo que se ve en github.com en ese momento.
