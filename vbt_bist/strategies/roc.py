
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik, periyot=12):
    strateji_adi = f"roc_{periyot}"
    
    roc = kapanis.pct_change(periyot) * 100
    
    # ROC sifiri yukari kesti ise momentum artiyor (AL)
    al_sinyalleri = (roc > 0) & (roc.shift(1) <= 0)
    sat_sinyalleri = (roc < 0) & (roc.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
