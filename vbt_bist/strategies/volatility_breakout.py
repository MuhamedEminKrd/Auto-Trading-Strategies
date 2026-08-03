"""
Strateji : Volatilite Kirilimi (Larry Williams Volatility Breakout)
Mantik   : Bugunku acilis fiyati, dunku araligin (Yuksek-Dusuk) bir yuzdesi (K carpan) 
           kadar asilirsa hizli bir volatilite patlamasi baslamistir (AL).
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik, k=0.5):
    strateji_adi = f"volatility_breakout_{k}"

    range_dun = yuksek.shift(1) - dusuk.shift(1)
    
    al_seviye = acilis + (k * range_dun)
    sat_seviye = acilis - (k * range_dun)
    
    al_sinyalleri  = (kapanis > al_seviye) & (kapanis.shift(1) <= al_seviye.shift(1))
    sat_sinyalleri = (kapanis < sat_seviye) & (kapanis.shift(1) >= sat_seviye.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
