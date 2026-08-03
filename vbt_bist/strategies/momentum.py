"""
Strateji : Momentum (Basit)
Mantik   : Bugunku fiyat / N gun onceki fiyat. (veya Bugunku fiyat - N gun onceki fiyat)
           Oran 1.0 (veya 100) uzerine cikinca AL, asagi inince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=14):
    strateji_adi = f"momentum_{periyot}"

    # Fiyat / N gun onceki fiyat oranina bakalim
    momentum = kapanis / kapanis.shift(periyot)

    al_sinyalleri  = (momentum > 1.0) & (momentum.shift(1) <= 1.0)
    sat_sinyalleri = (momentum < 1.0) & (momentum.shift(1) >= 1.0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
