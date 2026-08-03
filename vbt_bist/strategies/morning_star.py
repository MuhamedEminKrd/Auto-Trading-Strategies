"""
Strateji : Morning Star / Evening Star (Mum Formasyonu)
Mantik   : 3 mumluk formasyonlar. Dipte olusursa (Morning Star) AL,
           Tepede olusursa (Evening Star) SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik):
    strateji_adi = "morning_star"

    govde = (kapanis - acilis).abs()
    yesil = kapanis > acilis
    kirmizi = kapanis < acilis
    
    # Morning Star:
    # 2 gun once kirmizi buyuk, 1 gun once kucuk govde, bugun yesil (buyuk, 2 gun oncekinin yarisini gecmeli)
    orta = (acilis.shift(2) + kapanis.shift(2)) / 2
    al_sinyalleri = (
        kirmizi.shift(2) & 
        (govde.shift(1) < govde.shift(2) * 0.3) & 
        yesil & (kapanis > orta)
    )
    
    # Evening Star:
    # 2 gun once yesil buyuk, 1 gun once kucuk govde, bugun kirmizi
    sat_sinyalleri = (
        yesil.shift(2) & 
        (govde.shift(1) < govde.shift(2) * 0.3) & 
        kirmizi & (kapanis < orta)
    )
    
    # Tekrarlari filtrele
    al_sinyalleri = al_sinyalleri & (~al_sinyalleri.shift(1).fillna(False))
    sat_sinyalleri = sat_sinyalleri & (~sat_sinyalleri.shift(1).fillna(False))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
