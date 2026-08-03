"""
Strateji : Rainbow Moving Average
Mantik   : Birden fazla SMA'nin (2'den 20'ye) siralimina bakar.
           Kapanis > SMA2 > SMA4 ... > SMA20 (Kusursuz trend siralari) oldugunda AL,
           Kapanis SMA20'nin altina dustugunde (trend kirilinca) SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik):
    strateji_adi = "rainbow_ma"

    sma2 = kapanis.rolling(2).mean()
    sma4 = kapanis.rolling(4).mean()
    sma6 = kapanis.rolling(6).mean()
    sma8 = kapanis.rolling(8).mean()
    sma10 = kapanis.rolling(10).mean()
    sma12 = kapanis.rolling(12).mean()
    sma14 = kapanis.rolling(14).mean()
    sma16 = kapanis.rolling(16).mean()
    sma18 = kapanis.rolling(18).mean()
    sma20 = kapanis.rolling(20).mean()

    # Tam siralama (Kusursuz yukselis trendi)
    tam_siralama = (
        (kapanis > sma2) & (sma2 > sma4) & (sma4 > sma6) & (sma6 > sma8) &
        (sma8 > sma10) & (sma10 > sma12) & (sma12 > sma14) & (sma14 > sma16) &
        (sma16 > sma18) & (sma18 > sma20)
    )

    al_sinyalleri = tam_siralama & (~tam_siralama.shift(1).fillna(False))
    
    # En uzun ortalama asagi kirildiginda sat (Crossover)
    sat_sinyalleri = (kapanis < sma20) & (kapanis.shift(1) >= sma20.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
