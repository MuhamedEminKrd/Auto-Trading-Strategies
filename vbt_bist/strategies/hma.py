"""
Strateji : Hull Moving Average (HMA) Trend Kesismesi
Mantik   : Gecikmesi neredeyse sifir olan bu hareketli ortalama hizlica trend yonunu bulur.
           Hizli HMA Yavas HMA'yi yukari kestiginde AL, asagi kestiginde SAT.
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def wma_fast(series, window):
    if len(series) < window:
        return pd.Series(np.nan, index=series.index)
    weights = np.arange(1, window + 1)
    weights = weights / weights.sum()
    res = np.convolve(series.values, weights[::-1], mode='valid')
    return pd.Series(np.concatenate([np.full(window-1, np.nan), res]), index=series.index)

def hma(series, window):
    half_length = int(window / 2)
    sqrt_length = int(np.sqrt(window))
    
    wma_half = wma_fast(series, half_length)
    wma_full = wma_fast(series, window)
    
    raw_hma = (2 * wma_half) - wma_full
    return wma_fast(raw_hma, sqrt_length)

def calistir(yuksek, dusuk, kapanis, baslik, hizli=20, yavas=50):
    strateji_adi = f"hma_{hizli}_{yavas}"
    
    hizli_hma = hma(kapanis, hizli)
    yavas_hma = hma(kapanis, yavas)
    
    al_sinyalleri = (hizli_hma > yavas_hma) & (hizli_hma.shift(1) <= yavas_hma.shift(1))
    sat_sinyalleri = (hizli_hma < yavas_hma) & (hizli_hma.shift(1) >= yavas_hma.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

