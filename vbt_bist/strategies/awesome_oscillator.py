"""
Strateji : Awesome Oscillator (AO)
Mantik   : Bill Williams tarafindan tasarlanmistir. Kapanis degil Medyan fiyatlarinin (Y+D/2) hareketli ortalamalarina bakar.
           Sifir cizgisini yukari kirdiginda guclu bir momentum baslangicidir.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, hizli=5, yavas=34):
    strateji_adi = f"ao_{hizli}_{yavas}"
    
    median_price = (yuksek + dusuk) / 2
    
    sma_hizli = median_price.rolling(window=hizli).mean()
    sma_yavas = median_price.rolling(window=yavas).mean()
    
    ao = sma_hizli - sma_yavas
    
    # Sifiri yukari keserse AL, asagi keserse SAT
    al_sinyalleri = (ao > 0) & (ao.shift(1) <= 0)
    sat_sinyalleri = (ao < 0) & (ao.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool), exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool), init_cash=10000, fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d')
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    
    return portfoy.stats()
