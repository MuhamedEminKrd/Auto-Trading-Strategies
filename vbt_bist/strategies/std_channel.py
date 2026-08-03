
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=20, carpan=2.0):
    strateji_adi = f"std_channel_{periyot}_{carpan}"
    
    # Ortalama ve sapma hesapla (Bollinger'e benzer ama kanal mantigiyla regressif)
    sma = kapanis.rolling(periyot).mean()
    std = kapanis.rolling(periyot).std()
    
    ust_kanal = sma + (std * carpan)
    
    # Fiyat ust kanali sertce yukari kirarsa AL (Breakout)
    al_sinyalleri = (kapanis > ust_kanal) & (kapanis.shift(1) <= ust_kanal.shift(1))
    sat_sinyalleri = (kapanis < sma) # Ortalamaya donunce SAT
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
