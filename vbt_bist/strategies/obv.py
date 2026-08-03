
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"obv_{periyot}"
    
    # OBV Hesaplama: Kapanis yukselirse hacmi ekle, duserse cikar
    fiyat_farki = kapanis.diff()
    obv = pd.Series(0, index=kapanis.index)
    obv[fiyat_farki > 0] = hacim[fiyat_farki > 0]
    obv[fiyat_farki < 0] = -hacim[fiyat_farki < 0]
    obv = obv.cumsum()
    
    # OBV SMA'yi yukari kestiginde AL (Hacim artisi)
    obv_sma = obv.rolling(window=periyot).mean()
    al_sinyalleri = (obv > obv_sma) & (obv.shift(1) <= obv_sma.shift(1))
    sat_sinyalleri = (obv < obv_sma) & (obv.shift(1) >= obv_sma.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
