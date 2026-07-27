"""
Strateji : Williams %R
Mantik   : Stokastik osilatorun daha agresif ve hizli halidir. Kapanis fiyatini son donemki range ile oranlar.
           -80 seviyesinden yukari zipladiginda AL, -20 seviyesinden asagi dustugunde SAT.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=14, alt_sinir=-80, ust_sinir=-20):
    strateji_adi = f"williams_r_{periyot}"
    
    highest_high = yuksek.rolling(window=periyot).max()
    lowest_low = dusuk.rolling(window=periyot).min()
    
    # Williams %R formulu
    wr = ((highest_high - kapanis) / (highest_high - lowest_low + 1e-10)) * -100
    
    al_sinyalleri = (wr > alt_sinir) & (wr.shift(1) <= alt_sinir)
    sat_sinyalleri = (wr < ust_sinir) & (wr.shift(1) >= ust_sinir)
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool), exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool), init_cash=10000, fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d')
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    
    return portfoy.stats()
