"""
Strateji : ATR Breakout
Mantik   : Fiyat, dunku kapanis + 1.5 * ATR'yi asarsa volatilite kirilimi ile AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, periyot=14, carpan=1.5):
    strateji_adi = f"atr_breakout_{periyot}"

    tr = pd.concat([yuksek - dusuk, (yuksek - kapanis.shift(1)).abs(), (dusuk - kapanis.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(periyot).mean()
    
    ust_sinir = kapanis.shift(1) + (carpan * atr.shift(1))
    alt_sinir = kapanis.shift(1) - (carpan * atr.shift(1))

    al_sinyalleri  = (kapanis > ust_sinir) & (kapanis.shift(1) <= ust_sinir.shift(1))
    sat_sinyalleri = (kapanis < alt_sinir) & (kapanis.shift(1) >= alt_sinir.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
