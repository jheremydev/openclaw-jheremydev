---
name: verify-4geeks-token
description: Verifica que el token de 4Geeks (FOURGEEKS_TOKEN) sea válido y la sesión en BreatheCode esté activa. Consulta el perfil del estudiante, su estado en la academia y su información de GitHub vinculada.
user-invocable: true
disable-model-invocation: false
---

# Verificar token de 4Geeks (BreatheCode)

Usa esta skill cuando Jheremy pida verificar que su token de estudiante de 4Geeks siga activo, comprobar su sesión en la plataforma, o consultar sus datos de perfil en BreatheCode API.

## Pre-requisitos

El token debe estar guardado en OpenClaw como variable de entorno con el nombre `FOURGEEKS_TOKEN` y `kind: env`. La inyección la gestiona OpenClaw automáticamente; el skill no expone el valor del token.

## Pasos

1. **Llamar a la API de BreatheCode** para obtener los datos del usuario autenticado:

   ```bash
   curl -s -w "\nHTTP:%{http_code}" "https://breathecode.herokuapp.com/v1/admissions/user/me" \
     -H "Authorization: Token $FOURGEEKS_TOKEN" \
     -H "Content-Type: application/json"
   ```

2. **Interpretar la respuesta:**
   - Si el código HTTP es **200** y devuelve un JSON con `id`, `email` y `roles`, el token es **válido** y la sesión está **activa**.
   - Si el código HTTP es **401** con `"detail": "Authentication credentials were not provided."`, el token **no se está enviando** — el problema es de inyección del secreto.
   - Si el código HTTP es **401** con `"error": "Invalid or Inactive Token"`, el token **ha expirado o es inválido** — Jheremy necesita renovarlo desde learn.4geeks.com (cookie `4g_tok`) y actualizarlo con:
     ```bash
     openclaw secrets store set FOURGEEKS_TOKEN --kind env
     ```
   - Si el código HTTP es **403** con `"detail": "Expired or invalid token"`, el token también **ha expirado**.
   - Cualquier otro código o error de red indica que la API de BreatheCode no está accesible temporalmente.

3. **Mostrar resumen al usuario:** Si el token es válido, mostrar:
   - **Nombre:** `first_name last_name`
   - **Email:** `email`
   - **GitHub:** `github.username`
   - **Rol:** `roles[].role` en `roles[].academy.name`
   - **Academia:** `roles[].academy.slug`, huso `roles[].academy.timezone`
   - **Miembro desde:** `date_joined`
   - **Sesión:** Activa

   Si el token no es válido, indicar claramente que el token ha expirado y pedir a Jheremy que lo renueve.

## Notas

- El token `FOURGEEKS_TOKEN` se guarda en el vault de OpenClaw como `kind: env` — se inyecta en los comandos `exec` como variable de entorno, pero nunca se escribe en ningún archivo del workspace, skill, ni repo.
- La API base es `breathecode.herokuapp.com` (backend de learn.4geeks.com, construido sobre Django REST Framework).
- El endpoint oficial para datos del estudiante es `/v1/admissions/user/me`, que devuelve: id, email, first_name, last_name, date_joined, github, profile_academy (con academias vinculadas), cohorts, roles (con academy info), permissions y settings.
- El endpoint usa autenticación por header `Authorization: Token <valor>`, no `Bearer`.
- El token `4g_tok` de la cookie en learn.4geeks.com NO es un JWT — tiene una sola parte y se usa directamente como `Token` de Django REST Framework.