
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"cmo_{periyot}"
    
    fark = kapanis.diff()
    yukselis = fark.where(fark > 0, 0)
    dusus = -fark.where(fark < 0, 0)
    
    sum_up = yukselis.rolling(periyot).sum()
    sum_down = dusus.rolling(periyot).sum()
    
    cmo = 100 * ((sum_up - sum_down) / (sum_up + sum_down + 1e-10))
    
    # Asiri satim bolgesinden (-50) yukari cikis
    al_sinyalleri = (cmo > -50) & (cmo.shift(1) <= -50)
    sat_sinyalleri = (cmo < 50) & (cmo.shift(1) >= 50)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
