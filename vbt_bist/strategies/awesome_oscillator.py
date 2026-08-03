"""
Strateji : Awesome Oscillator (AO)
Mantik   : Bill Williams tarafindan tasarlanmistir. Kapanis degil Medyan fiyatlarinin (Y+D/2) hareketli ortalamalarina bakar.
           Sifir cizgisini yukari kirdiginda guclu bir momentum baslangicidir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, hizli=5, yavas=34):
    strateji_adi = f"ao_{hizli}_{yavas}"
    
    median_price = (yuksek + dusuk) / 2
    
    sma_hizli = median_price.rolling(window=hizli).mean()
    sma_yavas = median_price.rolling(window=yavas).mean()
    
    ao = sma_hizli - sma_yavas
    
    # Sifiri yukari keserse AL, asagi keserse SAT
    al_sinyalleri = (ao > 0) & (ao.shift(1) <= 0)
    sat_sinyalleri = (ao < 0) & (ao.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)

