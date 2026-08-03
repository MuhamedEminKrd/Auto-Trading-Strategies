"""
Strateji : Ease of Movement (EOM)
Mantik   : Hacimli ve dusuk direncli yukselisleri yakalar. EOM kendi ortalamasini 
           yukari kestiginde AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, hacim, kapanis, baslik, periyot=14):
    strateji_adi = f"eom_{periyot}"

    dm = ((yuksek + dusuk) / 2) - ((yuksek.shift(1) + dusuk.shift(1)) / 2)
    br = (hacim / 100000000) / (yuksek - dusuk + 1e-10) # Buyuk sayilari onle
    eom = dm / br
    
    eom_sma = eom.rolling(periyot).mean()

    al_sinyalleri  = (eom_sma > 0) & (eom_sma.shift(1) <= 0)
    sat_sinyalleri = (eom_sma < 0) & (eom_sma.shift(1) >= 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
