"""
Strateji : Ichimoku + RSI Filtre (Kombinasyon)
Mantik   : Fiyat Kumo (Bulut) uzerindeyse trend Boğa kabul edilir.
           Bu sart altinda RSI 50'yi yukari kestiginde isleme girilir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "ichimoku_rsi"

    # Ichimoku Bilesenleri (Senkou Span A & B ile Bulut hesabi)
    tenkan = (yuksek.rolling(9).max() + dusuk.rolling(9).min()) / 2
    kijun = (yuksek.rolling(26).max() + dusuk.rolling(26).min()) / 2
    senkou_a = ((tenkan + kijun) / 2).shift(26)
    senkou_b = ((yuksek.rolling(52).max() + dusuk.rolling(52).min()) / 2).shift(26)
    
    bulut_ust = pd.concat([senkou_a, senkou_b], axis=1).max(axis=1)
    bulut_alt = pd.concat([senkou_a, senkou_b], axis=1).min(axis=1)
    
    # RSI Sinyalleri
    rsi = vbt.RSI.run(kapanis, window=14).rsi
    rsi_al = (rsi > 50) & (rsi.shift(1) <= 50)
    rsi_sat = (rsi < 50) & (rsi.shift(1) >= 50)
    
    # Kombinasyon: Bulut uzerinde (Trend yonu) + RSI 50 kesisimi
    al_sinyalleri  = rsi_al & (kapanis > bulut_ust)
    sat_sinyalleri = rsi_sat & (kapanis < bulut_alt)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
