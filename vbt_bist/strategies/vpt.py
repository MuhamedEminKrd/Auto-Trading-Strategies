
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, hacim, baslik, periyot=14):
    strateji_adi = f"vpt_{periyot}"
    
    # VPT Formulu: Onceki VPT + Hacim * ((Kapanis - Onceki Kapanis) / Onceki Kapanis)
    fiyat_degisimi = kapanis.pct_change()
    vpt = (hacim * fiyat_degisimi).cumsum()
    
    # VPT'nin kendi ortalamasini kesmesi
    vpt_sma = vpt.rolling(window=periyot).mean()
    
    al_sinyalleri = (vpt > vpt_sma) & (vpt.shift(1) <= vpt_sma.shift(1))
    sat_sinyalleri = (vpt < vpt_sma) & (vpt.shift(1) >= vpt_sma.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
