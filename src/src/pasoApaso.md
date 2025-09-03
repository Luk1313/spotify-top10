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
