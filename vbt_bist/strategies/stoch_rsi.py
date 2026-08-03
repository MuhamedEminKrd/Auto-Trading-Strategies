"""
Strateji : Stochastic RSI (StochRSI)
Mantik   : RSI degerine Stochastic formulunu uygular. RSI'in RSI'i.
           0.2 altindan yukari kesince AL (asiri satim bitti)
           0.8 ustunden asagi kesince SAT (asiri alim bitti)
Kaynak   : Tushar Chande & Stanley Kroll (1994)
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, rsi_periyot=14, stoch_periyot=14, alt=0.2, ust=0.8):
    strateji_adi = f"stoch_rsi_{rsi_periyot}"

    # 1. RSI hesapla
    rsi = vbt.RSI.run(kapanis, window=rsi_periyot).rsi

    # 2. RSI degerlerine Stochastic formulunu uygula
    rsi_min = rsi.rolling(stoch_periyot).min()
    rsi_max = rsi.rolling(stoch_periyot).max()
    stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min + 1e-10)

    # 3. Crossover sinyalleri
    al_sinyalleri  = (stoch_rsi > alt) & (stoch_rsi.shift(1) <= alt)
    sat_sinyalleri = (stoch_rsi < ust) & (stoch_rsi.shift(1) >= ust)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
