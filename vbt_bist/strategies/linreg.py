
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=14):
    strateji_adi = f"linreg_slope_{periyot}"
    
    # VEKTÖREL OPTİMİZASYON (np.polyfit çok yavaştır, matematikle hızı 1000 kat artırıyoruz)
    x = np.arange(periyot)
    x_dev = x - x.mean()
    sum_x_dev_sq = np.sum(x_dev**2)
    
    def fast_slope(y):
        # OLS Eğim Formülü: cov(x,y) / var(x). Çok hızlı nokta çarpımı.
        return np.dot(x_dev, y) / sum_x_dev_sq
        
    slope_series = kapanis.rolling(window=periyot).apply(fast_slope, raw=True)
    
    # Eğim pozitife dönünce AL (yukselis trendi)
    al_sinyalleri = (slope_series > 0) & (slope_series.shift(1) <= 0)
    sat_sinyalleri = (slope_series < 0) & (slope_series.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
