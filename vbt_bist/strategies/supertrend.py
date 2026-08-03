"""
Strateji : SuperTrend (ATR Bazlı İzleyen Trend)
Mantik   : Fiyat Supertrend cizgisinin ustune cikarsa AL (Yukselis Trendi)
           Fiyat Supertrend cizgisinin altina inerse SAT (Dusus Trendi)
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, periyot=10, carpan=3.0):
    strateji_adi = f"supertrend_{periyot}_{carpan}"

    # ATR (Oynaklik) Hesaplama
    atr = vbt.ATR.run(yuksek, dusuk, kapanis, window=periyot).atr

    # Hizi artirmak icin verileri numpy dizilerine ceviriyoruz
    high_arr = yuksek.values
    low_arr = dusuk.values
    close_arr = kapanis.values
    atr_arr = atr.values

    hl2 = (high_arr + low_arr) / 2
    final_upperband = hl2 + (carpan * atr_arr)
    final_lowerband = hl2 - (carpan * atr_arr)
    
    # 1 = Yukselis Trendi, -1 = Dusus Trendi
    dir_ = np.ones(len(close_arr))
    
    for i in range(1, len(close_arr)):
        if np.isnan(atr_arr[i]):
            continue
            
        if close_arr[i] > final_upperband[i-1]:
            dir_[i] = 1
        elif close_arr[i] < final_lowerband[i-1]:
            dir_[i] = -1
        else:
            dir_[i] = dir_[i-1]
            if dir_[i] == 1 and final_lowerband[i] < final_lowerband[i-1]:
                final_lowerband[i] = final_lowerband[i-1]
            if dir_[i] == -1 and final_upperband[i] > final_upperband[i-1]:
                final_upperband[i] = final_upperband[i-1]

    # AL (1) ve SAT (-1) Kesisim Sinyallerini Uret
    dir_series = pd.Series(dir_, index=kapanis.index)
    al_sinyalleri = (dir_series == 1) & (dir_series.shift(1) == -1)
    sat_sinyalleri = (dir_series == -1) & (dir_series.shift(1) == 1)

    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
