"""
Strateji : Double EMA (DEMA)
Mantik   : DEMA = 2 * EMA - EMA(EMA). 
           Tekli EMA'ya gore fiyata daha hizli tepki verir ve gecikmeyi azaltir.
           Fiyat DEMA'yi yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=21):
    strateji_adi = f"dema_{periyot}"

    ema1 = kapanis.ewm(span=periyot, adjust=False).mean()
    ema2 = ema1.ewm(span=periyot, adjust=False).mean()
    
    dema = 2 * ema1 - ema2

    al_sinyalleri  = (kapanis > dema) & (kapanis.shift(1) <= dema.shift(1))
    sat_sinyalleri = (kapanis < dema) & (kapanis.shift(1) >= dema.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
