
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"hist_vol_{periyot}"
    
    # Gunluk getirilerin standart sapmasi * kok(252)
    gunluk_getiri = kapanis.pct_change()
    hv = gunluk_getiri.rolling(window=periyot).std() * np.sqrt(252)
    
    hv_sma = hv.rolling(window=periyot).mean()
    
    # Volatilite asiri dusukken (HV < SMA) ve fiyat artiyorsa
    al_sinyalleri = (hv < hv_sma) & (kapanis > kapanis.rolling(20).mean()) & (kapanis.shift(1) <= kapanis.rolling(20).mean().shift(1))
    sat_sinyalleri = kapanis < kapanis.rolling(20).mean()
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
