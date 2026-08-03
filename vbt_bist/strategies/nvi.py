"""
Strateji : Negative Volume Index (NVI)
Mantik   : Sadece hacim dustugu gunlerde fiyat degisimini izler. (Akilli para algisi)
           NVI kendi EMA'sini yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, hacim, baslik, periyot=255):
    strateji_adi = f"nvi_{periyot}"

    roc = kapanis.pct_change()
    vol_down = hacim < hacim.shift(1)
    
    # Sadece hacim dustugunde ROC hesapla, diger gunlerde 0 al.
    roc_filtered = roc.where(vol_down, 0.0)
    
    # Cumulative Product ile NVI 1000 baz degerinden hesaplanir
    nvi = 1000 * (1 + roc_filtered).cumprod()
    nvi_sma = nvi.rolling(periyot).mean()

    al_sinyalleri  = (nvi > nvi_sma) & (nvi.shift(1) <= nvi_sma.shift(1))
    sat_sinyalleri = (nvi < nvi_sma) & (nvi.shift(1) >= nvi_sma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
