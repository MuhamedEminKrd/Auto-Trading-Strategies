"""
Strateji : ATR Kanali Kirilimi (Turtle Trading Modernize)
Mantik   : Kapanis + N*ATR = Ust Kanal, Kapanis - N*ATR = Alt Kanal.
           Fiyat ust kanali kirinca AL, alt kanalin altina dusunce SAT.
           Volatiliteye gore kendini otomatik ayarlar.
Kaynak   : Richard Dennis - Turtle Traders (1983), Winton Group, Man AHL
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, atr_periyot=20, carpan=1.5):
    strateji_adi = f"atr_channel_{atr_periyot}"

    # True Range hesapla
    prev_close = kapanis.shift(1)
    tr1 = yuksek - dusuk
    tr2 = (yuksek - prev_close).abs()
    tr3 = (dusuk - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = true_range.rolling(atr_periyot).mean()

    # Kanal sinirlari
    ust_kanal = kapanis.rolling(atr_periyot).mean() + (carpan * atr)
    alt_kanal = kapanis.rolling(atr_periyot).mean() - (carpan * atr)

    # Kirilim sinyalleri (crossover)
    al_sinyalleri  = (kapanis > ust_kanal) & (kapanis.shift(1) <= ust_kanal.shift(1))
    sat_sinyalleri = (kapanis < alt_kanal) & (kapanis.shift(1) >= alt_kanal.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
