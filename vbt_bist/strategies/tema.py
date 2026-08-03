
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"tema_{periyot}"
    
    ema1 = kapanis.ewm(span=periyot, adjust=False).mean()
    ema2 = ema1.ewm(span=periyot, adjust=False).mean()
    ema3 = ema2.ewm(span=periyot, adjust=False).mean()
    
    tema = 3 * ema1 - 3 * ema2 + ema3
    
    al_sinyalleri = (kapanis > tema) & (kapanis.shift(1) <= tema.shift(1))
    sat_sinyalleri = (kapanis < tema) & (kapanis.shift(1) >= tema.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
