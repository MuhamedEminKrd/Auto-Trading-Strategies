"""
Strateji : RSI + MACD Filtre (Multi-Indicator)
Mantik   : MACD yukari kesistiginde, RSI da 50'nin uzerindeyse isleme gir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik):
    strateji_adi = "rsi_macd_filtre"

    rsi = vbt.RSI.run(kapanis, window=14).rsi
    macd_ind = vbt.MACD.run(kapanis, fast_window=12, slow_window=26, signal_window=9)
    macd = macd_ind.macd
    signal = macd_ind.signal

    macd_al = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    macd_sat = (macd < signal) & (macd.shift(1) >= signal.shift(1))

    al_sinyalleri  = macd_al & (rsi > 50)
    sat_sinyalleri = macd_sat & (rsi < 50)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
