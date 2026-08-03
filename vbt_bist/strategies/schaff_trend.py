"""
Strateji : Schaff Trend Cycle (STC)
Mantik   : MACD cizgisine Stochastic formulunu iki kez uygular. 
           Trend donuslerini MACD'den daha erken ve RSI'dan daha stabil tespit eder.
           25 altindan yukari kesince AL, 75 ustunden asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, macd_hizli=23, macd_yavas=50, stc_periyot=10, alt_sinir=25, ust_sinir=75):
    strateji_adi = f"schaff_trend"

    # 1. MACD
    ema_hizli = kapanis.ewm(span=macd_hizli, adjust=False).mean()
    ema_yavas = kapanis.ewm(span=macd_yavas, adjust=False).mean()
    macd = ema_hizli - ema_yavas

    # 2. Ilk Stochastic
    macd_min = macd.rolling(stc_periyot).min()
    macd_max = macd.rolling(stc_periyot).max()
    stoch_macd = (macd - macd_min) / (macd_max - macd_min + 1e-10) * 100
    
    # Ilk duzlestirme
    pf = stoch_macd.ewm(span=stc_periyot//2, adjust=False).mean()
    
    # 3. Ikinci Stochastic
    pf_min = pf.rolling(stc_periyot).min()
    pf_max = pf.rolling(stc_periyot).max()
    stoch_pf = (pf - pf_min) / (pf_max - pf_min + 1e-10) * 100
    
    # Ikinci duzlestirme -> Schaff Trend Cycle
    stc = stoch_pf.ewm(span=stc_periyot//2, adjust=False).mean()

    # Crossover Sinyalleri
    al_sinyalleri  = (stc > alt_sinir) & (stc.shift(1) <= alt_sinir)
    sat_sinyalleri = (stc < ust_sinir) & (stc.shift(1) >= ust_sinir)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
