"""
Strateji : Klinger Volume Oscillator
Mantik   : Hacim akisinin 34 ve 55 gunluk ustel ortalamalari arasindaki fark.
           Sinyal hattini (13) yukari kesince AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, hacim, baslik, kisa=34, uzun=55, sinyal=13):
    strateji_adi = f"klinger"

    tp = (yuksek + dusuk + kapanis) / 3
    trend = (tp > tp.shift(1)).astype(int) - (tp < tp.shift(1)).astype(int)
    
    v_force = hacim * trend
    ema_kisa = v_force.ewm(span=kisa, adjust=False).mean()
    ema_uzun = v_force.ewm(span=uzun, adjust=False).mean()
    
    kvo = ema_kisa - ema_uzun
    sig = kvo.ewm(span=sinyal, adjust=False).mean()

    al_sinyalleri  = (kvo > sig) & (kvo.shift(1) <= sig.shift(1))
    sat_sinyalleri = (kvo < sig) & (kvo.shift(1) >= sig.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
