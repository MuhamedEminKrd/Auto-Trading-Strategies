"""
Strateji : Trend Intensity Index
Mantik   : Kapanisin N gunluk SMA uzerinde oldugu gunlerin yuzdesini olcer.
           Son M gunde (ornek: 30 gun), bu yuzde 80'i yukari kesince AL, 20'yi asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, sma_periyot=30, ti_periyot=30, al_sinir=80, sat_sinir=20):
    strateji_adi = f"trend_intensity_{ti_periyot}"

    sma = kapanis.rolling(window=sma_periyot).mean()
    ustunde_mi = (kapanis > sma).astype(int)
    
    # Son ti_periyot icinde yuzde kac kez SMA'nin ustundeydi?
    ti_index = ustunde_mi.rolling(window=ti_periyot).sum() / ti_periyot * 100

    al_sinyalleri  = (ti_index > al_sinir) & (ti_index.shift(1) <= al_sinir)
    sat_sinyalleri = (ti_index < sat_sinir) & (ti_index.shift(1) >= sat_sinir)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
