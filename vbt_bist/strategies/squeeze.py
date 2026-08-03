"""
Strateji : Squeeze Momentum (Bollinger + Keltner)
Mantik   : Bollinger Bantlari Keltner Kanali'nin icine girdiginde piyasa sikisir (Squeeze).
           Sikisiklik bitip (BB > KC) momentum pozitifse AL, negatifse SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, periyot=20):
    strateji_adi = f"squeeze_{periyot}"

    sma = kapanis.rolling(periyot).mean()
    std = kapanis.rolling(periyot).std()
    
    # Bollinger
    bb_ust = sma + 2 * std
    bb_alt = sma - 2 * std
    
    # Keltner
    tr = pd.concat([yuksek - dusuk, (yuksek - kapanis.shift(1)).abs(), (dusuk - kapanis.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(periyot).mean()
    kc_ust = sma + 1.5 * atr
    kc_alt = sma - 1.5 * atr
    
    # Squeeze: BB, Keltner icinde
    squeeze_on = (bb_ust < kc_ust) & (bb_alt > kc_alt)
    squeeze_off = ~squeeze_on
    
    momentum = kapanis - sma
    
    # Squeeze'den cikis aninda momentum yonune gore islem
    al_sinyalleri  = squeeze_off & squeeze_on.shift(1) & (momentum > 0)
    sat_sinyalleri = squeeze_off & squeeze_on.shift(1) & (momentum < 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
