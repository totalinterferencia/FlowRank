#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################################
#            FlowRank                 #
#  www.totalinterferencia.com         #
#  t.me/totalinterferencia_comunidad  #
######################################

"""
FlowRank — Screener de criptomonedas basado en volumen relativo (rel_volume = volumen/marketcap).
- Filtra solo pares USDT en Binance.
- Excluye stablecoins.
- Muestra en pantalla el TOP 20 tokens con mayor rotación de capital.

Proyecto de: https://totalinterferencia.com
Comunidad en Telegram: https://t.me/totalinterferencia_comunidad
"""

import requests
import pandas as pd
import numpy as np

URL_BUBBLES = "https://cryptobubbles.net/backend/data/bubbles1000.usd.json"

STABLE_NAMES = {"USDT","USDC","BUSD","DAI","TUSD","FDUSD","PYUSD","USDD","USDE","USDL"}

def fetch_json(url, timeout=25):
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "FlowRank/1.0"})
    r.raise_for_status()
    return r.json()

def is_stable_like(row) -> bool:
    # Usa el booleano 'stable' del feed + heurística por precio ≈ 1 y nombres típicos
    if bool(row.get("stable", False)):
        return True
    symbol = str(row.get("symbol","")).upper()
    name = str(row.get("name","")).upper()
    if symbol in STABLE_NAMES or any(s in name for s in STABLE_NAMES):
        return True
    try:
        p = float(row.get("price", np.nan))
        if np.isfinite(p) and 0.97 <= p <= 1.03:
            return True
    except Exception:
        pass
    return False

def has_binance_usdt(row) -> bool:
    sym = row.get("symbols") or {}
    b = str(sym.get("binance","") or "")
    return "USDT" in b.upper()

def main():
    try:
        data = fetch_json(URL_BUBBLES)
    except Exception as e:
        print(f"[ERROR] No se pudo descargar el JSON: {e}")
        return

    rows = []
    for it in data if isinstance(data, list) else []:
        perf = it.get("performance") or {}
        symbols = it.get("symbols") or {}
        rows.append({
            "id": it.get("id"),
            "name": it.get("name"),
            "slug": it.get("slug"),
            "symbol": it.get("symbol"),
            "price": pd.to_numeric(it.get("price"), errors="coerce"),
            "market_cap": pd.to_numeric(it.get("marketcap"), errors="coerce"),
            "volume_24h": pd.to_numeric(it.get("volume"), errors="coerce"),
            "change_24h": pd.to_numeric(perf.get("day"), errors="coerce"),
            "stable_flag": bool(it.get("stable", False)),
            "symbols": symbols,
        })

    df = pd.DataFrame(rows)

    if df.empty:
        print("El dataset vino vacío o con formato inesperado.")
        return

    # Solo pares USDT de Binance
    df = df[df.apply(has_binance_usdt, axis=1)].copy()

    # Excluir stablecoins
    df["is_stable"] = df.apply(is_stable_like, axis=1)
    df = df[~df["is_stable"]].copy()

    # Filtros mínimos (ajustables)
    df = df.dropna(subset=["market_cap", "volume_24h"])
    df = df[(df["market_cap"] > 1e8) & (df["volume_24h"] > 5e6)]

    if df.empty:
        print("No hay resultados con los filtros actuales (bajá umbrales o revisá el feed).")
        return

    # Métrica principal
    df["rel_volume"] = df["volume_24h"] / df["market_cap"]

    # Orden y TOP 20
    df = df.sort_values("rel_volume", ascending=False)
    top = df[["symbol","name","price","change_24h","volume_24h","market_cap","rel_volume"]].head(20)

    # Salida legible
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)
    print("\n=== FlowRank — Binance (USDT) — TOP 20 por rel_volume (excluyendo stablecoins) ===\n")
    print(top.to_string(index=False))

if __name__ == "__main__":
    main()
