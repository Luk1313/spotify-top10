#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spotify Top 10 – CLI (Client Credentials)
Uso:
  python -m src.top10 --pais Chile --csv
Requiere variables de entorno:
  SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
"""
import os
import argparse
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

_VARIANTES_TOP50 = [
    "Top 50 - {pais}",
    "Top 50 – {pais}",
    "Top 50 — {pais}",
    "Top 50 – {pais} "
]

def get_client():
    cid = os.getenv("SPOTIPY_CLIENT_ID")
    csec = os.getenv("SPOTIPY_CLIENT_SECRET")
    if not cid or not csec:
        raise SystemExit("Faltan SPOTIPY_CLIENT_ID / SPOTIPY_CLIENT_SECRET en variables de entorno.")
    auth = SpotifyClientCredentials(client_id=cid, client_secret=csec)
    return spotipy.Spotify(auth_manager=auth)

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
    tracks, offset, limit = [], 0, 100
    while True:
        chunk = sp.playlist_items(pl_id, offset=offset, limit=limit, additional_types=("track",))
        items = chunk.get("items", [])
        if not items:
            break
        tracks.extend(items)
        if chunk.get("next") is None:
            break
        offset += limit

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
            "album": (t.get("album") or {}).get("name"),
            "popularidad": t.get("popularity"),
            "url": (t.get("external_urls") or {}).get("spotify"),
            "track_id": t.get("id"),
        })
    return pd.DataFrame(filas), pl

def main():
    ap = argparse.ArgumentParser(description="Spotify Top 10 (Client Credentials)")
    ap.add_argument("--pais", default=None, help="Ej: Chile, Argentina, Mexico. Si no, Global.")
    ap.add_argument("--csv", action="store_true", help="Guardar CSV en disco.")
    args = ap.parse_args()

    sp = get_client()
    df, pl = top10_spotify(sp, pais=args.pais)
    print(f"Usando playlist: {pl['name']} — Owner: {pl['owner']['display_name']} — ID: {pl['id']}")
    print(df)

    if args.csv:
        name = f"spotify_top10_{(args.pais or 'Global').lower()}.csv".replace(" ", "_")
        df.to_csv(name, index=False)
        print("CSV guardado:", name)

if __name__ == "__main__":
    main()
