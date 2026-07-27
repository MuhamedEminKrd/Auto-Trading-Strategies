"""
Strateji : Z-Score Mean Reversion
Mantik   : Fiyatin kendi ortalamasindan standart sapma bazinda ne kadar uzaklastigini olcer.
           Z-Score < -2 (Fiyat ortalamadan asagi koptu, asiri satis) -> AL
           Z-Score > 0 (Fiyat ortalamaya dondu) -> SAT
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20, alt_sapma=-2.0, ust_sapma=0.0):
    strateji_adi = f"zscore_{periyot}"
    
    # Ortalama ve Standart Sapma
    sma = kapanis.rolling(window=periyot).mean()
    std = kapanis.rolling(window=periyot).std()
    
    # Z-Score formulu: (X - Mean) / Std
    z_score = (kapanis - sma) / (std + 1e-10)
    
    # Sinyaller: -2'nin altina dusunce panik alisi yap
    al_sinyalleri = (z_score < alt_sapma) & (z_score.shift(1) >= alt_sapma)
    # Ortalamaya donunce (0 veya ustu) sat
    sat_sinyalleri = (z_score > ust_sapma) & (z_score.shift(1) <= ust_sapma)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d'
    )
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    
    return portfoy.stats()
