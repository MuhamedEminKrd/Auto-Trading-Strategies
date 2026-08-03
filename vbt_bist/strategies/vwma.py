"""
Strateji : Volume Weighted Moving Average (VWMA)
Mantik   : Hacim agirlikli hareketli ortalama. Hacmin yuksek oldugu gunlerdeki 
           fiyatlara daha fazla agirlik verir. 
           Fiyat VWMA'yi yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"vwma_{periyot}"

    vwma = (kapanis * hacim).rolling(window=periyot).sum() / hacim.rolling(window=periyot).sum()

    al_sinyalleri  = (kapanis > vwma) & (kapanis.shift(1) <= vwma.shift(1))
    sat_sinyalleri = (kapanis < vwma) & (kapanis.shift(1) >= vwma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
