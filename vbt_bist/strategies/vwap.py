"""
Strateji : VWAP Sapma (Volume Weighted Average Price)
Mantik   : 20 gunluk VWAP hesapla. Fiyat VWAP altindan ustune gecince AL,
           ustunden altina gecince SAT.
           Kurumsal alicilarin benchmark fiyati.
Kaynak   : Goldman Sachs, Morgan Stanley execution algoritmalari
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, hacim, baslik, periyot=20):
    strateji_adi = f"vwap_{periyot}"

    # Tipik fiyat = (Yuksek + Dusuk + Kapanis) / 3
    tipik_fiyat = (yuksek + dusuk + kapanis) / 3

    # Rolling VWAP = sum(Tipik * Hacim) / sum(Hacim)
    tp_hacim = (tipik_fiyat * hacim).rolling(periyot).sum()
    hacim_toplam = hacim.rolling(periyot).sum()
    vwap = tp_hacim / (hacim_toplam + 1e-10)

    # Crossover sinyalleri
    al_sinyalleri  = (kapanis > vwap) & (kapanis.shift(1) <= vwap.shift(1))
    sat_sinyalleri = (kapanis < vwap) & (kapanis.shift(1) >= vwap.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
