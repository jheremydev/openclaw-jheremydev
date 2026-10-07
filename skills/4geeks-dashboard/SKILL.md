---
name: 4geeks-dashboard
description: Muestra el panel de progreso general de Jheremy en 4Geeks: porcentaje de avance, métricas por cohorte, por tipo de tarea, últimas entregas y foto general del curso. No lista pendientes uno por uno.
user-invocable: true
disable-model-invocation: false
---

# Panel de Progreso General — 4Geeks Academy

Foto general del curso: porcentaje completado, desglose por cohorte, por tipo de tarea, timeline de últimas entregas. No es una lista de pendientes — es el "cómo voy" global.

## Pre-requisitos

`FOURGEEKS_TOKEN` en el vault de OpenClaw como `kind: env`.

## Ejecución

```bash
python3 {baseDir}/scripts/4geeks-dashboard.py
```

## Qué muestra

- **Barra de progreso general** con porcentaje (completadas = DONE + APPROVED / total)
- **Métricas clave:** total tareas, entregadas, aprobadas, rechazadas, pendientes
- **Progreso por cohorte:** mini barra, porcentaje, desglose por estado y tipos de tarea
- **Progreso por tipo:** lecciones, proyectos, ejercicios — con su % individual
- **Últimas 5 entregas:** timeline con fecha y cohorte
- **Resumen final** con eficiencia global (% completado vs % aprobado oficialmente)