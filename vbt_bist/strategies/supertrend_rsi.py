"""
Strateji : Trend + RSI Filtresi (Basitlestirilmis Supertrend)
Mantik   : Fiyat SMA50'nin uzerinde (Trend Boğa) VE RSI 50'yi yukari kesti ise AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik):
    strateji_adi = "supertrend_rsi"

    sma = kapanis.rolling(50).mean()
    rsi = vbt.RSI.run(kapanis, window=14).rsi
    
    rsi_al = (rsi > 50) & (rsi.shift(1) <= 50)
    rsi_sat = (rsi < 50) & (rsi.shift(1) >= 50)
    
    al_sinyalleri  = rsi_al & (kapanis > sma)
    sat_sinyalleri = rsi_sat & (kapanis < sma)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
