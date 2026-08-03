
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik):
    strateji_adi = "kst"
    
    # 4 farkli ROC hesaplanir ve agirlikli olarak toplanir
    roc1 = kapanis.pct_change(10).rolling(10).mean() * 1
    roc2 = kapanis.pct_change(15).rolling(10).mean() * 2
    roc3 = kapanis.pct_change(20).rolling(10).mean() * 3
    roc4 = kapanis.pct_change(30).rolling(15).mean() * 4
    
    kst = (roc1 + roc2 + roc3 + roc4) * 100
    kst_sinyal = kst.rolling(9).mean()
    
    al_sinyalleri = (kst > kst_sinyal) & (kst.shift(1) <= kst_sinyal.shift(1))
    sat_sinyalleri = (kst < kst_sinyal) & (kst.shift(1) >= kst_sinyal.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
