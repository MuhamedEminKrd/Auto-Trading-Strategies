"""
Strateji : Normalized ATR (NATR)
Mantik   : NATR = ATR / Kapanis * 100. 
           Volatilitenin kendi hareketli ortalamasini kesmesini momentum gostergesi kabul eder.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, periyot=14):
    strateji_adi = f"natr_{periyot}"

    tr = pd.concat([yuksek - dusuk, (yuksek - kapanis.shift(1)).abs(), (dusuk - kapanis.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(periyot).mean()
    natr = (atr / kapanis) * 100
    
    sma = natr.rolling(periyot).mean()

    al_sinyalleri  = (natr > sma) & (natr.shift(1) <= sma.shift(1))
    sat_sinyalleri = (natr < sma) & (natr.shift(1) >= sma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
