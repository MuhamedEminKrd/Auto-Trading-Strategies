"""
Strateji : RSI Sapma (Divergence)
Mantik   : Fiyat yeni dip yaparken RSI yeni dip yapmiyorsa pozitif sapma (AL).
           Fiyat yeni zirve yaparken RSI yeni zirve yapmiyorsa negatif sapma (SAT).
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=14, div_periyot=20):
    strateji_adi = f"rsi_divergence_{periyot}_{div_periyot}"

    rsi = vbt.RSI.run(kapanis, window=periyot).rsi

    # Fiyat yeni dip yapiyor mu?
    fiyat_yeni_dip = kapanis == kapanis.rolling(div_periyot).min()
    # RSI yeni dip yapmiyor mu?
    rsi_yeni_dip_degil = rsi > rsi.rolling(div_periyot).min()

    # Fiyat yeni zirve yapiyor mu?
    fiyat_yeni_zirve = kapanis == kapanis.rolling(div_periyot).max()
    # RSI yeni zirve yapmiyor mu?
    rsi_yeni_zirve_degil = rsi < rsi.rolling(div_periyot).max()

    al_sinyalleri  = fiyat_yeni_dip & rsi_yeni_dip_degil
    sat_sinyalleri = fiyat_yeni_zirve & rsi_yeni_zirve_degil

    # Crossover benzeri sinyal uretmek icin sadece kosulun saglandigi ilk ani alalim
    al_sinyalleri = al_sinyalleri & (~al_sinyalleri.shift(1).fillna(False))
    sat_sinyalleri = sat_sinyalleri & (~sat_sinyalleri.shift(1).fillna(False))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
