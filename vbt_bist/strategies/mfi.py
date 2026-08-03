"""
Strateji : MFI (Money Flow Index - Hacim Bazlı RSI)
Mantik   : Fiyat artarken hacim de artiyorsa guc onayi alir. 
           Asiri satimdan cikista AL, asiri alimdan dususte SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, hacim, baslik, periyot=14, alt_sinir=20, ust_sinir=80):
    strateji_adi = f"mfi_{periyot}_{alt_sinir}_{ust_sinir}"
    
    # Tipik fiyat (Typical Price)
    tp = (yuksek + dusuk + kapanis) / 3
    # Ham para akisi (Raw Money Flow)
    rmf = tp * hacim
    
    diff = tp.diff()
    
    # Pozitif ve negatif para akislarini ayir
    pos_mf = rmf.copy()
    pos_mf[diff <= 0] = 0.0
    
    neg_mf = rmf.copy()
    neg_mf[diff >= 0] = 0.0
    
    # Periyot bazli toplamlar
    pos_sum = pos_mf.rolling(window=periyot).sum()
    neg_sum = neg_mf.rolling(window=periyot).sum()
    
    # MFI Hesaplama (Sifira bolunme hatasini engellemek icin ufak bir kontrol eklenir)
    mfi = 100 - (100 / (1 + (pos_sum / (neg_sum + 1e-10))))
    
    # Sinyaller
    al_sinyalleri = (mfi > alt_sinir) & (mfi.shift(1) <= alt_sinir)
    sat_sinyalleri = (mfi < ust_sinir) & (mfi.shift(1) >= ust_sinir)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

