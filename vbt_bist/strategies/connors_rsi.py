"""
Strateji : ConnorsRSI
Mantik   : 3 bilesenin ortalamasi:
           1. RSI(3)
           2. Up/Down Streak RSI(2) 
           3. 1 Gunluk Getirinin Percentile Rank'i (100)
           ConnorsRSI 10'u yukari kesince AL, 90'i asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, rsi_p=3, streak_p=2, rank_p=100, alt_sinir=10, ust_sinir=90):
    strateji_adi = f"connors_rsi"

    # 1. Bilesen: RSI(3)
    rsi = vbt.RSI.run(kapanis, window=rsi_p).rsi

    # 2. Bilesen: Up/Down Streak RSI(2)
    # Streak hesaplama
    diff = kapanis.diff()
    streak = pd.Series(0, index=kapanis.index)
    
    current_streak = 0
    for i in range(1, len(diff)):
        if diff.iloc[i] > 0:
            current_streak = current_streak + 1 if current_streak > 0 else 1
        elif diff.iloc[i] < 0:
            current_streak = current_streak - 1 if current_streak < 0 else -1
        else:
            current_streak = 0
        streak.iloc[i] = current_streak
        
    streak_rsi = vbt.RSI.run(streak, window=streak_p).rsi

    # 3. Bilesen: Rate of Change Percentile Rank
    roc = (kapanis - kapanis.shift(1)) / kapanis.shift(1)
    
    # 100 gunluk periyotta bugunku ROC'nin yuzdelik sirasi
    rank = roc.rolling(window=rank_p).apply(lambda x: (x < x.iloc[-1]).sum() / len(x) * 100, raw=False)
    
    # ConnorsRSI = (RSI + StreakRSI + Rank) / 3
    crsi = (rsi + streak_rsi + rank) / 3
    
    # Sinyaller (Crossover)
    al_sinyalleri  = (crsi > alt_sinir) & (crsi.shift(1) <= alt_sinir)
    sat_sinyalleri = (crsi < ust_sinir) & (crsi.shift(1) >= ust_sinir)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
