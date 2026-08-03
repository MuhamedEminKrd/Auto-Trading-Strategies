"""
Strateji : ADX + MACD Trend Filtre
Mantik   : Sadece ADX 25'in uzerinde (guclu trend) oldugunda MACD kesisimlerini dinle.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "adx_macd"

    # Custom ADX Hesaplama
    periyot = 14
    plus_dm = yuksek.diff()
    minus_dm = dusuk.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    minus_dm = minus_dm.abs()
    
    pdm_true = plus_dm.copy()
    mdm_true = minus_dm.copy()
    
    pdm_true[plus_dm < minus_dm] = 0
    mdm_true[minus_dm < plus_dm] = 0
    
    atr = vbt.ATR.run(yuksek, dusuk, kapanis, window=periyot).atr
    
    plus_di = 100 * (pdm_true.ewm(alpha=1/periyot, adjust=False).mean() / (atr + 1e-10))
    minus_di = 100 * (mdm_true.ewm(alpha=1/periyot, adjust=False).mean() / (atr + 1e-10))
    
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10))
    adx = dx.ewm(alpha=1/periyot, adjust=False).mean()
    
    macd_ind = vbt.MACD.run(kapanis, fast_window=12, slow_window=26, signal_window=9)
    macd = macd_ind.macd
    signal = macd_ind.signal
    
    macd_al = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    macd_sat = (macd < signal) & (macd.shift(1) >= signal.shift(1))
    
    al_sinyalleri  = macd_al & (adx > 25)
    sat_sinyalleri = macd_sat & (adx > 25)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
