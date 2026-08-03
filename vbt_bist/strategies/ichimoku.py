"""
Strateji : Ichimoku Cloud (Kinko Hyo)
Mantik   : Japon teknigi. Fiyat bulutun (Senkou Span A ve B) ustune cikarsa AL.
           Fiyat bulutun altina inerse SAT. Bulut icindeyken islem yapma.
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, t_periyot=9, k_periyot=26, s_periyot=52):
    strateji_adi = f"ichimoku_{t_periyot}_{k_periyot}_{s_periyot}"
    
    # Tenkan-sen (Donusum Cizgisi)
    t_high = yuksek.rolling(window=t_periyot).max()
    t_low = dusuk.rolling(window=t_periyot).min()
    tenkan_sen = (t_high + t_low) / 2
    
    # Kijun-sen (Temel Cizgi)
    k_high = yuksek.rolling(window=k_periyot).max()
    k_low = dusuk.rolling(window=k_periyot).min()
    kijun_sen = (k_high + k_low) / 2
    
    # Senkou Span B (Öncü Çizgi B)
    s_high = yuksek.rolling(window=s_periyot).max()
    s_low = dusuk.rolling(window=s_periyot).min()
    senkou_span_b = (s_high + s_low) / 2
    
    # Senkou Span A (Öncü Çizgi A)
    senkou_span_a = (tenkan_sen + kijun_sen) / 2
    
    # Kumo Bulutunu ileriye kaydir (k_periyot kadar, genelde 26 gun)
    senkou_span_a = senkou_span_a.shift(k_periyot)
    senkou_span_b = senkou_span_b.shift(k_periyot)
    
    # Fiyat bulutun neresinde?
    bulut_ustu = np.maximum(senkou_span_a, senkou_span_b)
    bulut_alti = np.minimum(senkou_span_a, senkou_span_b)
    
    # Sinyaller
    # Fiyat bulutun (direncin) ustune kirarsa AL
    al_sinyalleri = (kapanis > bulut_ustu) & (kapanis.shift(1) <= bulut_ustu.shift(1))
    
    # Fiyat bulutun (destegin) altina duserse SAT
    sat_sinyalleri = (kapanis < bulut_alti) & (kapanis.shift(1) >= bulut_alti.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

