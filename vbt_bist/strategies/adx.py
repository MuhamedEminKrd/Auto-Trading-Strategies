"""
Strateji : ADX (Average Directional Index)
Mantik   : ADX trendin GUCUNU gosterir, DI cizgileri YONUNU.
           +DI, -DI'yi yukari kestiginde ve ADX > 25 ise (Guclu Trend Baslangici) AL.
           -DI, +DI'yi yukari kestiginde SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, periyot=14, adx_sinir=25):
    strateji_adi = f"adx_{periyot}_{adx_sinir}"
    
    plus_dm = yuksek.diff()
    minus_dm = dusuk.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    minus_dm = minus_dm.abs()
    
    # Gercek DM (Buyuk olani al, kucuk olani sifirla)
    pdm_true = plus_dm.copy()
    mdm_true = minus_dm.copy()
    
    pdm_true[plus_dm < minus_dm] = 0
    mdm_true[minus_dm < plus_dm] = 0
    
    atr = vbt.ATR.run(yuksek, dusuk, kapanis, window=periyot).atr
    
    # Duzlestirilmis DI cizgileri (Wilder's Smoothing yaklasimi ile EWM)
    plus_di = 100 * (pdm_true.ewm(alpha=1/periyot, adjust=False).mean() / (atr + 1e-10))
    minus_di = 100 * (mdm_true.ewm(alpha=1/periyot, adjust=False).mean() / (atr + 1e-10))
    
    # DX ve ADX hesaplama
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10))
    adx = dx.ewm(alpha=1/periyot, adjust=False).mean()
    
    # Sinyaller
    # +DI, -DI'yi yukari kestiginde VE Trend cok gucluyse (ADX > 25)
    al_sarti_1 = (plus_di > minus_di) & (plus_di.shift(1) <= minus_di.shift(1))
    al_sarti_2 = (adx > adx_sinir)
    al_sinyalleri = al_sarti_1 & al_sarti_2
    
    # -DI, +DI'yi kestiginde (Yukselis trendi bittiginde)
    sat_sinyalleri = (minus_di > plus_di) & (minus_di.shift(1) <= plus_di.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

