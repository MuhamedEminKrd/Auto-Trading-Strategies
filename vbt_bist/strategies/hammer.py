"""
Strateji : Hammer / Hanging Man (Çekiç)
Mantik   : Alt fitil govdenin 2 katindan buyukse ve dusus trendindeyse AL sinyali uretir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik):
    strateji_adi = "hammer"

    govde = (kapanis - acilis).abs()
    alt_fitil = pd.concat([acilis, kapanis], axis=1).min(axis=1) - dusuk
    ust_fitil = yuksek - pd.concat([acilis, kapanis], axis=1).max(axis=1)
    tr = yuksek - dusuk
    
    sma20 = kapanis.rolling(20).mean()
    
    # Cekic kosullari: Alt fitil uzun, ust fitil yok denecek kadar kucuk ve SMA altinda 
    hammer = (alt_fitil > 2 * govde) & (ust_fitil < 0.1 * tr) & (kapanis < sma20)
    
    al_sinyalleri  = hammer & (~hammer.shift(1).fillna(False))
    sat_sinyalleri = (kapanis > sma20) & (kapanis.shift(1) <= sma20.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
