"""
Strateji : Internal Bar Strength (IBS)
Mantik   : IBS = (Kapanis - Dusuk) / (Yuksek - Dusuk).
           Fiyatın günlük bandının neresinde kapandığına bakar.
           IBS < 0.2 ise aşırı satımdır (Ertesi gün için AL üretir).
           IBS > 0.8 ise aşırı alımdır (SAT üretir).
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik):
    strateji_adi = "ibs"

    # IBS Formülü: 1e-10 sıfıra bölme hatasını engellemek için
    ibs = (kapanis - dusuk) / (yuksek - dusuk + 1e-10)
    
    # 0.2'yi aşağı kestikten sonra toparlanırken (aşırı satımdan çıkış)
    al_sinyalleri  = (ibs < 0.2) & (ibs.shift(1) >= 0.2)
    # 0.8'i yukarı kestikten sonra aşağı dönerken (aşırı alımdan çıkış)
    sat_sinyalleri = (ibs > 0.8) & (ibs.shift(1) <= 0.8)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
