"""
Strateji : True Range EMA Filtresi
Mantik   : Gercek Aralik (TR) uzerinden hareketli ortalama kesismeleri.
           Volatilitenin genislemesini hizli/yavas EMA kesisimiyle yakalar.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, hizli=10, yavas=30):
    strateji_adi = f"true_range_ema"

    tr = pd.concat([yuksek - dusuk, (yuksek - kapanis.shift(1)).abs(), (dusuk - kapanis.shift(1)).abs()], axis=1).max(axis=1)
    
    ema_hizli = tr.ewm(span=hizli, adjust=False).mean()
    ema_yavas = tr.ewm(span=yavas, adjust=False).mean()

    al_sinyalleri  = (ema_hizli > ema_yavas) & (ema_hizli.shift(1) <= ema_yavas.shift(1))
    sat_sinyalleri = (ema_hizli < ema_yavas) & (ema_hizli.shift(1) >= ema_yavas.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
