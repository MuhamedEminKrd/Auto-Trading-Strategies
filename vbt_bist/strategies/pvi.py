"""
Strateji : Positive Volume Index (PVI)
Mantik   : Sadece hacim arttigi gunlerde fiyat degisimini izler. (Trendin gucu)
           PVI kendi EMA'sini yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, hacim, baslik, periyot=255):
    strateji_adi = f"pvi_{periyot}"

    roc = kapanis.pct_change()
    vol_up = hacim > hacim.shift(1)
    
    roc_filtered = roc.where(vol_up, 0.0)
    pvi = 1000 * (1 + roc_filtered).cumprod()
    pvi_sma = pvi.rolling(periyot).mean()

    al_sinyalleri  = (pvi > pvi_sma) & (pvi.shift(1) <= pvi_sma.shift(1))
    sat_sinyalleri = (pvi < pvi_sma) & (pvi.shift(1) >= pvi_sma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
