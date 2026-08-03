
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, window=20, offset=0.85, sigma=6):
    strateji_adi = f"alma_{window}"
    
    m = int(offset * (window - 1))
    s = window / sigma
    
    weights = np.exp(-((np.arange(window) - m) ** 2) / (2 * s * s))
    weights /= weights.sum()
    
    def calc_alma(x):
        return (x * weights).sum()
        
    alma = kapanis.rolling(window).apply(calc_alma, raw=True)
    
    al_sinyalleri = (kapanis > alma) & (kapanis.shift(1) <= alma.shift(1))
    sat_sinyalleri = (kapanis < alma) & (kapanis.shift(1) >= alma.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
