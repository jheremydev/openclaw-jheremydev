---
name: github-daily-digest
description: Resume PRs e issues pendientes de los repos de Jheremy en GitHub y lo manda por Telegram. Solo lectura, no modifica nada.
user-invocable: true
disable-model-invocation: false
---

# Resumen diario de GitHub

Usa esta skill cuando Jheremy pida un resumen/briefing de GitHub, o cuando una automatización programada la dispare.

## Alcance

Repos a mirar (ver `TOOLS.md`): `jheremydev/ai-engineering-company-project-monorepo-jheremydev` y `jheremydev/openclaw-jheremydev`. Si Jheremy menciona otro repo explícitamente, úsalo también.

Esta skill es de solo lectura: nunca hagas push, merge, commit, ni cierres o edites issues/PRs al ejecutarla. Si GitHub no está autenticado (ver `doctor` — search público), dilo explícitamente en vez de dar un resumen incompleto como si fuera completo.

## Pasos

1. Para cada repo, obtén: PRs abiertos esperando review, issues abiertos asignados a Jheremy, y si no hay nada de lo anterior, la actividad reciente relevante (últimos commits/PRs mergeados en las últimas 24-48h).
2. Prioriza en este orden: PRs abiertos esperando review > issues asignados a Jheremy > actividad reciente general.
3. Si un repo no tiene nada pendiente, omítelo del mensaje — no escribas "no hay nada en X".
4. Construye un mensaje de Telegram corto (máximo ~10 líneas), agrupado por repo, con 3-5 ítems como mucho por categoría, cada uno con un enlace directo.
5. Envía el mensaje por Telegram. No ejecutes ninguna acción adicional sobre lo que encuentres sin que Jheremy lo pida explícitamente.

## Formato de ejemplo

Repo: N PRs esperando review, M issues asignados — seguido de la lista con enlaces. Si ambos repos están sin nada pendiente, dilo en una sola línea en vez de mandar un mensaje vacío.
