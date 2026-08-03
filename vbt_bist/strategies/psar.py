"""
Strateji : Parabolic SAR (Stop and Reverse)
Mantik   : Fiyatin hizina (ivmesine) gore yaklasan parabolik noktalar kullanir.
           Fiyat noktalari kirarsa trend tersine donmustur (AL veya SAT).
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, accel_step=0.02, accel_max=0.2):
    strateji_adi = f"psar_{accel_step}_{accel_max}"
    
    high = yuksek.values
    low = dusuk.values
    length = len(high)
    
    sar_vals = np.zeros(length)
    ep = np.zeros(length)
    af = np.zeros(length)
    trend = np.ones(length)
    
    trend[0] = 1
    sar_vals[0] = low[0]
    ep[0] = high[0]
    af[0] = accel_step
    
    for i in range(1, length):
        prev_sar = sar_vals[i-1]
        prev_ep = ep[i-1]
        prev_af = af[i-1]
        prev_trend = trend[i-1]
        
        sar_vals[i] = prev_sar + prev_af * (prev_ep - prev_sar)
        
        if prev_trend == 1:
            if sar_vals[i] > low[i-1]: sar_vals[i] = low[i-1]
            if i > 1 and sar_vals[i] > low[i-2]: sar_vals[i] = low[i-2]
        else:
            if sar_vals[i] < high[i-1]: sar_vals[i] = high[i-1]
            if i > 1 and sar_vals[i] < high[i-2]: sar_vals[i] = high[i-2]
            
        if prev_trend == 1 and low[i] < sar_vals[i]:
            trend[i] = -1
            sar_vals[i] = prev_ep
            ep[i] = low[i]
            af[i] = accel_step
        elif prev_trend == -1 and high[i] > sar_vals[i]:
            trend[i] = 1
            sar_vals[i] = prev_ep
            ep[i] = high[i]
            af[i] = accel_step
        else:
            trend[i] = prev_trend
            ep[i] = prev_ep
            af[i] = prev_af
            if trend[i] == 1 and high[i] > prev_ep:
                ep[i] = high[i]
                af[i] = min(prev_af + accel_step, accel_max)
            elif trend[i] == -1 and low[i] < prev_ep:
                ep[i] = low[i]
                af[i] = min(prev_af + accel_step, accel_max)
                
    trend_series = pd.Series(trend, index=kapanis.index)
    
    # 1: Yukselis (Al), -1: Dusus (Sat)
    al_sinyalleri = (trend_series == 1) & (trend_series.shift(1) == -1)
    sat_sinyalleri = (trend_series == -1) & (trend_series.shift(1) == 1)
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

