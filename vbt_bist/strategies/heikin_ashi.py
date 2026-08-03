"""
Strateji : Heikin Ashi Trend
Mantik   : Trend yonunu bulmak icin HA mumlarini kullanir. Ardisik iki yesil mum -> AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik):
    strateji_adi = "heikin_ashi"

    ha_c = (acilis + yuksek + dusuk + kapanis) / 4
    ha_o = (acilis.shift(1) + kapanis.shift(1)) / 2
    
    yesil = ha_c > ha_o
    kirmizi = ha_c < ha_o

    # Ardisik 2 yesil muma donusum crossover efekti yaratir
    al_sinyalleri  = yesil & yesil.shift(1) & kirmizi.shift(2)
    sat_sinyalleri = kirmizi & kirmizi.shift(1) & yesil.shift(2)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
