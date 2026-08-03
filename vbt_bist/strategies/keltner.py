"""
Strateji : Keltner Channels (Keltner Kanallari Breakout)
Mantik   : Bollinger'a benzer ama volatilitesi ATR'ye baglidir. 
           Fiyat Keltner Ust Bandini kirarsa AL (Squeeze patlamasi). Alt banti kirarsa SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20, carpan=2.0):
    strateji_adi = f"keltner_{periyot}_{carpan}"
    
    # Keltner Orta Bant (Genelde EMA 20 kullanilir)
    orta_bant = kapanis.ewm(span=periyot, adjust=False).mean()
    
    # ATR hesapla (Volatilite)
    atr = vbt.ATR.run(yuksek, dusuk, kapanis, window=periyot).atr
    
    # Ust ve Alt Bant
    ust_bant = orta_bant + (carpan * atr)
    alt_bant = orta_bant - (carpan * atr)
    
    # Keltner Kirilimi (Breakout)
    al_sinyalleri = (kapanis > ust_bant) & (kapanis.shift(1) <= ust_bant.shift(1))
    sat_sinyalleri = (kapanis < alt_bant) & (kapanis.shift(1) >= alt_bant.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

