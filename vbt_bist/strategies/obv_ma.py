"""
Strateji : OBV + MA Trend (Kombinasyon)
Mantik   : On-Balance Volume (OBV) kendi 20 gunluk hareketli ortalamasini yukari kestiginde
           VE fiyat SMA20 uzerinde ise guclu bir yukselis AL sinyali uretilir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"obv_ma_{periyot}"

    trend = (kapanis > kapanis.shift(1)).astype(int) - (kapanis < kapanis.shift(1)).astype(int)
    obv = (hacim * trend).cumsum()
    
    obv_sma = obv.rolling(periyot).mean()
    kapanis_sma = kapanis.rolling(periyot).mean()
    
    obv_al = (obv > obv_sma) & (obv.shift(1) <= obv_sma.shift(1))
    obv_sat = (obv < obv_sma) & (obv.shift(1) >= obv_sma.shift(1))
    
    al_sinyalleri  = obv_al & (kapanis > kapanis_sma)
    sat_sinyalleri = obv_sat & (kapanis < kapanis_sma)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
