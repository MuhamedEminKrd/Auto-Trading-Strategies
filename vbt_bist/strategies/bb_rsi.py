"""
Strateji : Bollinger + RSI Filtre (Kombinasyon)
Mantik   : Fiyat Bollinger alt bandinda (veya degmis) VE RSI asiri satimdan 
           (30 altindan) donuyor. Ikisi ayni anda onayladiginda AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik):
    strateji_adi = "bb_rsi"

    rsi = vbt.RSI.run(kapanis, window=14).rsi
    sma = kapanis.rolling(20).mean()
    std = kapanis.rolling(20).std()
    bb_alt = sma - 2 * std
    bb_ust = sma + 2 * std
    
    rsi_al = (rsi > 30) & (rsi.shift(1) <= 30)
    rsi_sat = (rsi < 70) & (rsi.shift(1) >= 70)
    
    # RSI kesisimi aninda, fiyat son 3 gunde BB alt bandina degmisse
    al_sinyalleri = rsi_al & (kapanis.rolling(3).min() <= bb_alt.rolling(3).min())
    sat_sinyalleri = rsi_sat & (kapanis.rolling(3).max() >= bb_ust.rolling(3).max())

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
