
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20, sinir=100):
    strateji_adi = f"cci_{periyot}"
    
    tipik_fiyat = (yuksek + dusuk + kapanis) / 3
    sma_tp = tipik_fiyat.rolling(window=periyot).mean()
    
    import numpy as np
    # Mean Deviation hesaplama (Pandas 2.0'da mad() kaldirildi) - Vektörel Hızlı Hesaplama
    mad = tipik_fiyat.rolling(window=periyot).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    
    cci = (tipik_fiyat - sma_tp) / (0.015 * (mad + 1e-10))
    
    # CCI 100'u yukari kestiginde Gucu Teyit Et (AL)
    al_sinyalleri = (cci > sinir) & (cci.shift(1) <= sinir)
    sat_sinyalleri = (cci < -sinir) & (cci.shift(1) >= -sinir)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
