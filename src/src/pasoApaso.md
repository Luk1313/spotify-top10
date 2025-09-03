# Create a step-by-step guide (without code) for configuring a Spotify Developer app
from pathlib import Path

contenido = """
# Guía paso a paso (sin código) para configurar tu aplicación en Spotify for Developers

> Objetivo: dejar tu app lista en el **Dashboard** para que tus proyectos puedan usar la Web API de Spotify.


## 1) Entra al Dashboard
- Abre: https://developer.spotify.com/dashboard/
- Inicia sesión con tu cuenta de Spotify.


## 2) Crea una nueva aplicación
- Haz clic en **“Crear aplicación”**.
- Completa los campos visibles en el formulario:

### a) Nombre de la aplicación
- Escribe un nombre claro y corto. Ejemplos: “MiPlayer IA (educativo)” o “Spotify Top 10 – Lucas”.

### b) Descripción de la aplicación
- Explica el propósito, el tipo de uso (educativo/no comercial) y las principales funcionalidades.
- Ejemplo orientativo: “Aplicación educativa para consumir la Web API de Spotify desde Colab/VS Code. Funciones: búsquedas, lectura de playlists y análisis básico. Uso no comercial.”

### c) Sitio web (opcional)
- Puedes dejarlo vacío o poner un enlace a tu GitHub/LinkedIn/portafolio personal.

### d) URI de redireccionamiento (obligatorio si vas a iniciar sesión de usuario)
- Añade la siguiente dirección de desarrollo: **http://localhost:8888/callback**
- Si luego usas otra app o puerto, podrás agregar URIs adicionales.

### e) ¿Qué API/SDK planeas utilizar?
- Marca **API web**.

- Acepta los términos si aparecen y presiona **“Crear”**.


## 3) Ver credenciales y estado de la app
Tras crearla, entrarás a la ficha de tu app.

### a) Identificador de cliente (Client ID)
- Lo verás en la parte superior de **Información básica**.
- Guárdalo en un lugar seguro (lo vas a necesitar en tus proyectos).

### b) Secreto del cliente (Client Secret)
- Haz clic en **“Ver el secreto del cliente”** para mostrarlo.
- Guárdalo con cuidado. No lo compartas públicamente ni lo subas a repositorios.

### c) Estado de la aplicación
- Por defecto estará en **Modo de desarrollo**. En este modo, sólo las cuentas que agregues como usuarias de prueba podrán autorizar la app.


## 4) Registrar/editar URIs de redireccionamiento
- En “Información básica”, ubica la sección **URI de redireccionamiento**.
- Verifica que esté **http://localhost:8888/callback**.
- Puedes agregar otras URIs más adelante si cambias de entorno (por ejemplo, un dominio propio).


## 5) (Opcional) Añadir usuarios de prueba
- Ve a **Gestión de usuarios** (Users and Access).
- Pulsa **“Agregar usuarios”** y escribe los correos de las cuentas de Spotify que necesiten probar la app.
- Límite típico en modo desarrollo: hasta 25 cuentas.


## 6) Comprobación final (checklist)
- [ ] El nombre y la descripción describen claramente la app.
- [ ] **API web** seleccionada.
- [ ] URI de redireccionamiento registrada (al menos **http://localhost:8888/callback**).
- [ ] Tomaste nota de **Client ID** y, si corresponde, de **Client Secret**.
- [ ] (Opcional) Agregaste usuarios de prueba en **Gestión de usuarios**.
- [ ] Guardaste los cambios.


## 7) Errores comunes y cómo resolverlos
- **“Invalid redirect URI”**: la dirección que usa tu app no coincide exactamente con la registrada en el Dashboard. Revísala y corrígela (respeta mayúsculas/minúsculas y el puerto).
- **“User not authorized” en modo desarrollo**: la cuenta que intenta autorizar no está en la lista de **Usuarios de prueba**.
- **“Insufficient scope”**: tu app solicita permisos que no fueron aceptados durante la autorización. Repite la autorización aceptando los permisos solicitados.
- **Credenciales expuestas**: nunca publiques el *Client Secret*. Si lo compartiste accidentalmente, genera uno nuevo desde el Dashboard.


## 8) Pasos siguientes (cuando quieras avanzar)
- Mantener una **política de privacidad** y **términos** si planeas publicar la app.
- Solicitar revisión si necesitas pasar a **producción** (acceso para más usuarios).
- Documentar tus URIs de redireccionamiento y flujos de inicio de sesión para tu equipo.


---

¡Listo! Con estos pasos tu aplicación queda creada y configurada en Spotify for Developers, sin necesidad de escribir código en esta guía.
"""

ruta = Path("/mnt/data/Guia_Spotify_Sin_Codigo.md")
ruta.write_text(contenido, encoding="utf-8")
str(ruta)

from pathlib import Path

content = """# Guía paso a paso · Spotify for Developers (crear y configurar tu aplicación)

> Objetivo: dejar tu app lista para usar la **Web API** con tus proyectos (Colab/VS Code), obtener `CLIENT_ID`/`CLIENT_SECRET` y registrar la **Redirect URI** correcta.

---

## 0) Requisitos previos
- Cuenta de Spotify (gratuita o premium).
- Iniciar sesión en el **Dashboard de Spotify for Developers**: <https://developer.spotify.com/dashboard/>
- Tener a mano un nombre y una descripción para tu app.

---

## 1) Crear la aplicación
1. Entra al dashboard y haz clic en **Create app** (Crear aplicación).
2. Completa los campos:
   - **App name**: un nombre claro, por ejemplo: `Spotify Top 10 – Lucas`.
   - **App description**: propósito y alcance. Ejemplo:  
     `Aplicación educativa para consultar la Web API de Spotify (búsqueda, audio-features y playlists) desde Google Colab. Sin fines comerciales.`
   - **Website** *(opcional)*: puede ser tu LinkedIn, GitHub o dejarlo vacío.
   - **Redirect URIs** *(obligatorio para OAuth/PKCE)*: **agrega**  
     ```
     http://localhost:8888/callback
     ```
     > Puedes agregar más luego (p. ej. `http://localhost:3000/callback`).
   - **Which API/SDKs are you planning to use?**: marca **Web API**.
3. Acepta los términos (si aplica) y **Create**.

---

## 2) Guardar tus credenciales
1. En la ficha de tu app verás:
   - **Client ID**
   - **Client Secret** (clic en *View client secret* para mostrarlo).
2. Guarda estos valores **de forma segura** (no los publiques).
3. Sugerencia: crea un archivo `.env` (no lo subas a GitHub) con:
   ```env
   SPOTIPY_CLIENT_ID=<TU_CLIENT_ID>
   SPOTIPY_CLIENT_SECRET=<TU_CLIENT_SECRET>
   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

