#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea una playlist en TU cuenta con el Top 10 (Global o País).
Usa PKCE por defecto (sin secret). Si defines SPOTIPY_CLIENT_SECRET usará Authorization Code.

Uso:
  # PKCE (sin secret)
  export SPOTIPY_CLIENT_ID="tu_client_id"
  export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
  python -m src.playlist --pais Chile --nombre "Top 10 – Chile (API)" --privada

  # Authorization Code (con secret)
  export SPOTIPY_CLIENT_ID="tu_client_id"
  export SPOTIPY_CLIENT_SECRET="tu_secret"
  export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
  python -m src.playlist --pais Chile --nombre "Top 10 – Chile (API)" --privada
"""
import os
import argparse
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyPKCE, SpotifyOAuth

# ====== utilidades compartidas (copiadas de top10.py para hacerlo autónomo) ======
_VARIANTES_TOP50 = [
    "Top 50 - {pais}",
    "Top 50 – {pais}",
    "Top 50 — {pais}",
    "Top 50 – {pais} "
]

def buscar_playlist_top50(sp, pais=None):
    if pais:
        candidatos = [v.format(pais=pais) for v in _VARIANTES_TOP50]
    else:
        candidatos = ["Top 50 - Global", "Top 50 – Global", "Top 50 — Global"]
    for q in candidatos:
        res = sp.search(q=f'playlist:"{q}"', type="playlist", limit=5)
        items = (res.get("playlists") or {}).get("items", []) or []
        oficiales = [p for p in items if ((p.get("owner") or {}).get("display_name","").lower() in {"spotify","spotifycharts"})]
        if oficiales:
            return oficiales[0]
        if items:
            return items[0]
    return None

def top10_spotify(sp, pais=None):
    pl = buscar_playlist_top50(sp, pais=pais)
    if not pl:
        raise SystemExit(f"No se encontró playlist Top 50 para: {pais or 'Global'}")
    pl_id = pl["id"]
    tracks = sp.playlist_items(pl_id, limit=100).get("items", [])
    filas = []
    for i, it in enumerate(tracks[:10], start=1):
        t = it.get("track") or {}
        if not t:
            continue
        artistas = ", ".join(a["name"] for a in (t.get("artists") or []))
        filas.append({
            "posicion": i,
            "track": t.get("name"),
            "artista": artistas,
            "url": (t.get("external_urls") or {}).get("spotify"),
            "track_id": t.get("id"),
        })
    return pd.DataFrame(filas), pl
# ================================================================================

SCOPES = "playlist-modify-private playlist-read-private user-read-email"

def get_user_client():
    cid = os.getenv("SPOTIPY_CLIENT_ID")
    secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")
    if not cid:
        raise SystemExit("Falta SPOTIPY_CLIENT_ID")
    if secret:
        auth = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect, scope=SCOPES, open_browser=True, cache_path=".spotipyoauth")
    else:
        auth = SpotifyPKCE(client_id=cid, redirect_uri=redirect, scope=SCOPES)
    return spotipy.Spotify(auth_manager=auth)

def crear_playlist_top10(sp_user, df_top10, nombre, desc="", privada=True):
    me = sp_user.me()
    pl = sp_user.user_playlist_create(me["id"], nombre, public=not privada, description=desc)
    ids = [tid for tid in df_top10["track_id"].dropna().tolist()]
    if ids:
        sp_user.playlist_add_items(pl["id"], ids)
    return pl["external_urls"]["spotify"]

def main():
    ap = argparse.ArgumentParser(description="Crear playlist con el Top 10 (OAuth/PKCE)")
    ap.add_argument("--pais", default=None, help="Ej: Chile, Argentina, Mexico. Si no, Global.")
    ap.add_argument("--nombre", default=None, help="Nombre de la playlist (por defecto 'Top 10 – <País|Global> (API)')")
    ap.add_argument("--privada", action="store_true", help="Crea la playlist como privada (default).")
    args = ap.parse_args()

    sp_user = get_user_client()
    df, pl_ref = top10_spotify(sp_user, pais=args.pais)
    nombre = args.nombre or f"Top 10 – {args.pais or 'Global'} (API)"
    url = crear_playlist_top10(sp_user, df, nombre, desc=f"Playlist generada con Spotipy desde {pl_ref['name']}", privada=True)
    print("✅ Playlist creada:", url)

if __name__ == "__main__":
    main()
