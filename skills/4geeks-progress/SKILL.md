---
name: 4geeks-progress
description: Analiza el progreso de Jheremy en 4Geeks y dice qué trabajo le falta completar, priorizado y accionable: tareas pendientes, empezadas sin terminar, en revisión, y próximo paso recomendado.
user-invocable: true
disable-model-invocation: false
---

# Progreso accionable en 4Geeks

En lugar de solo listar tareas con estado, genera una visión procesable de lo que realmente falta hacer, priorizado por urgencia.

## Pre-requisitos

`FOURGEEKS_TOKEN` debe estar en el vault de OpenClaw como `kind: env`.

## Ejecución

Usa el script `python3 {baseDir}/scripts/4geeks-progress.py` que ya contiene toda la lógica de análisis y formateo.

## Funcionalidad

1. Obtiene todas las tareas de `/v1/assignment/user/me/task` con `Authorization: Token $FOURGEEKS_TOKEN`.
2. Agrupa y prioriza:
   - 🔴 **Pendientes** (PENDING) — con urgencia por días desde creación (+14d = 🔥, +7d = ⚠️, menos = 🆕)
   - 🟡 **Iniciadas pero no entregadas** (opened_at sí, delivered_at no, task_status ≠ PENDING)
   - 🟢 **Entregadas en revisión** (DONE) — cuántas por cohorte y la más antigua
   - 📊 Resumen + próximo paso recomendado
3. Muestra enlaces directos a learn.4geeks.com para cada tarea pendiente.
4. Solo lectura. No modifica nada en la API.