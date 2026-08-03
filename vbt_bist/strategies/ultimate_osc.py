"""
Strateji : Ultimate Oscillator (Larry Williams)
Mantik   : 3 farkli periyodun (7, 14, 28) agirlikli ortalamasi.
           30 altindan yukari kesince AL, 70 ustunden asagi kesince SAT.
           Tek periyotlu oscilatörlerin zayifligini giderir.
Kaynak   : Larry Williams (1985) - Technical Analysis of Stocks & Commodities
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, p1=7, p2=14, p3=28, alt=30, ust=70):
    strateji_adi = f"ultimate_osc_{p1}_{p2}_{p3}"

    # Buying Pressure = Kapanis - min(Dusuk, Onceki Kapanis)
    prev_close = kapanis.shift(1)
    true_low = pd.concat([dusuk, prev_close], axis=1).min(axis=1)
    true_high = pd.concat([yuksek, prev_close], axis=1).max(axis=1)
    bp = kapanis - true_low
    tr = true_high - true_low

    # 3 periyot icin ortalamalar
    avg1 = bp.rolling(p1).sum() / tr.rolling(p1).sum()
    avg2 = bp.rolling(p2).sum() / tr.rolling(p2).sum()
    avg3 = bp.rolling(p3).sum() / tr.rolling(p3).sum()

    # Ultimate Oscillator = agirlikli ortalama * 100
    uo = 100 * (4 * avg1 + 2 * avg2 + avg3) / 7

    # Crossover sinyalleri
    al_sinyalleri  = (uo > alt) & (uo.shift(1) <= alt)
    sat_sinyalleri = (uo < ust) & (uo.shift(1) >= ust)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
