"""
Strateji : Marubozu (Gövde Mum)
Mantik   : Mumun govdesi (Kapanis-Acilis arasi) toplam mum boyunun %95'inden buyukse 
           Marubozu kabul edilir. Yesil Marubozu guclu alim sinyalidir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik):
    strateji_adi = "marubozu"

    govde = (kapanis - acilis).abs()
    tr = yuksek - dusuk
    
    marubozu = (govde / (tr + 1e-10)) > 0.95
    yesil = kapanis > acilis
    kirmizi = kapanis < acilis

    al_sinyalleri  = marubozu & yesil & (~marubozu.shift(1).fillna(False))
    sat_sinyalleri = marubozu & kirmizi & (~marubozu.shift(1).fillna(False))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
