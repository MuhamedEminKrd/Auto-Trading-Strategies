"""
Strateji : Accumulation/Distribution Line (AD Line)
Mantik   : Kapanisin gun ici araliktaki konumu * Hacim. A/D kendi ortalamasini 
           yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"ad_line_{periyot}"

    mfm = ((kapanis - dusuk) - (yuksek - kapanis)) / (yuksek - dusuk + 1e-10)
    mfv = mfm * hacim
    adl = mfv.cumsum()
    
    adl_sma = adl.rolling(periyot).mean()

    al_sinyalleri  = (adl > adl_sma) & (adl.shift(1) <= adl_sma.shift(1))
    sat_sinyalleri = (adl < adl_sma) & (adl.shift(1) >= adl_sma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
