# Spotify Top 10 (Spotipy)

Proyecto para obtener el **Top 10** desde las playlists editoriales de Spotify
(**Top 50 – Global** o **Top 50 – {País}**) usando `spotipy`. Incluye:
- Notebook Colab/Jupyter
- Script CLI de sólo lectura (Client Credentials)
- Script para **crear una playlist** en tu cuenta con el Top 10 (OAuth/PKCE)

## Requisitos
- Python 3.10+
- Cuenta de Spotify y una app en el [Dashboard de Spotify Developers](https://developer.spotify.com/dashboard/)
- **Client ID** (si usarás PKCE) y opcionalmente **Client Secret** (si prefieres Authorization Code con secreto)
- Registrar la Redirect URI si usas OAuth/PKCE: `http://localhost:8888/callback`

## Instalación
```bash
pip install -r requirements.txt
