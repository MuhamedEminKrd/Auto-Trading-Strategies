
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik, yavas=25, hizli=13, sinyal=7):
    strateji_adi = f"tsi_{yavas}_{hizli}"
    
    momentum = kapanis.diff()
    
    # TSI formulu (Cift düzlestirme)
    smooth1 = momentum.ewm(span=yavas, adjust=False).mean()
    smooth2 = smooth1.ewm(span=hizli, adjust=False).mean()
    
    abs_momentum = momentum.abs()
    abs_smooth1 = abs_momentum.ewm(span=yavas, adjust=False).mean()
    abs_smooth2 = abs_smooth1.ewm(span=hizli, adjust=False).mean()
    
    tsi = 100 * (smooth2 / (abs_smooth2 + 1e-10))
    tsi_sinyal = tsi.ewm(span=sinyal, adjust=False).mean()
    
    al_sinyalleri = (tsi > tsi_sinyal) & (tsi.shift(1) <= tsi_sinyal.shift(1))
    sat_sinyalleri = (tsi < tsi_sinyal) & (tsi.shift(1) >= tsi_sinyal.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
