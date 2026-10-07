---
name: 4geeks-tasks
description: Recupera la lista de proyectos/tareas asignados a Jheremy en 4Geeks con su estado actual (PENDING, DONE, APPROVED, REJECTED). Soporta filtros por estado, tipo y cohorte.
user-invocable: true
disable-model-invocation: false
---

# Listar tareas/proyectos de 4Geeks (BreatheCode)

Usa esta skill cuando Jheremy pida ver sus tareas, proyectos, ejercicios o assignments pendientes en 4Geeks, consultar el estado de sus entregas, o revisar qué tiene calificado y qué le falta.

## Pre-requisitos

El token debe estar guardado en OpenClaw como `FOURGEEKS_TOKEN` con `kind: env`.

## Pasos

1. **Llamar a la API de BreatheCode** para obtener las tareas del estudiante:

   ```bash
   curl -s -w "\nHTTP:%{http_code}" "https://breathecode.herokuapp.com/v1/assignment/user/me/task" \
     -H "Authorization: Token ***" \
     -H "Content-Type: application/json"
   ```

2. **Interpretar la respuesta:**
   - HTTP **200** con un array → tareas obtenidas correctamente.
   - HTTP **401** con `"error": "Invalid or Inactive Token"` → el token ha expirado. Pedir a Jheremy que renueve el `4g_tok` desde learn.4geeks.com y lo actualice con:
     ```bash
     openclaw secrets store set FOURGEEKS_TOKEN --kind env
     ```

3. **Agrupar y mostrar las tareas** por estado, en este orden:
   - **PENDING** (pendientes)
   - **DONE** (entregadas, esperando revisión)
   - **APPROVED** (aprobadas/calificadas)
   - **REJECTED** (rechazadas, requieren corrección)

   Para cada tarea mostrar:
   - Título/descripción del proyecto
   - Tipo (`assignment`, `project`, `exercise`, `quiz`, etc.)
   - Cohorte (si aplica) y fecha de creación/entrega
   - Enlace al repo o URL de entrega (si existe)

4. **Resumen rápido** al final si hay muchas tareas — ej. "Tienes 3 pendientes, 2 en revisión, 15 aprobadas y 1 rechazada."

## Filtros opcionales

Si el usuario pide filtrar, se pueden pasar como query params:

| Parámetro | Valores |
|-----------|---------|
| `task_status` | `PENDING`, `DONE`, `APPROVED`, `REJECTED` |
| `task_type` | `assignment`, `project`, `exercise`, `quiz`, etc. |
| `cohort` | Slug del cohorte (ej. `madrid-spain`) |

Ejemplo:

```bash
curl -s "https://breathecode.herokuapp.com/v1/assignment/user/me/task?task_status=PENDING"
```

## Notas

- El token se inyecta automáticamente por OpenClaw desde el vault (`kind: env`), nunca se escribe en el skill ni en el repo.
- API base: `breathecode.herokuapp.com` (backend Django REST de learn.4geeks.com).
- Autenticación: header `Authorization: Token ***`.
- El token (`4g_tok`) tiene vida limitada — si expira durante el uso, pedir renovación.
- El endpoint devuelve un array plano de objetos, no paginación anidada.