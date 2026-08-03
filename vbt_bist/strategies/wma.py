
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik, kisa=10, uzun=30):
    strateji_adi = f"wma_{kisa}_{uzun}"
    
    w_kisa = pd.Series(range(1, kisa + 1))
    w_uzun = pd.Series(range(1, uzun + 1))
    
    wma_kisa = kapanis.rolling(kisa).apply(lambda x: (x * w_kisa).sum() / w_kisa.sum(), raw=True)
    wma_uzun = kapanis.rolling(uzun).apply(lambda x: (x * w_uzun).sum() / w_uzun.sum(), raw=True)
    
    al_sinyalleri = (wma_kisa > wma_uzun) & (wma_kisa.shift(1) <= wma_uzun.shift(1))
    sat_sinyalleri = (wma_kisa < wma_uzun) & (wma_kisa.shift(1) >= wma_uzun.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
