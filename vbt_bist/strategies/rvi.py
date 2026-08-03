"""
Strateji : Relative Vigor Index (RVI)
Mantik   : Kapanis-Acilis farkini Yuksek-Dusuk farkina oranlar.
           RVI kendi sinyal hattini (SMA) yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, acilis, yuksek, dusuk, baslik, periyot=10, sinyal_periyot=4):
    strateji_adi = f"rvi_{periyot}_{sinyal_periyot}"

    co_diff = (kapanis - acilis).rolling(periyot).mean()
    hl_diff = (yuksek - dusuk).rolling(periyot).mean()
    
    rvi = co_diff / (hl_diff + 1e-10)
    sinyal = rvi.rolling(sinyal_periyot).mean()

    al_sinyalleri  = (rvi > sinyal) & (rvi.shift(1) <= sinyal.shift(1))
    sat_sinyalleri = (rvi < sinyal) & (rvi.shift(1) >= sinyal.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
