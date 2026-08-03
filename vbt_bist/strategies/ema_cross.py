"""
Strateji : EMA Crossover (8/21)
Mantik   : Hizli EMA(8) yavasi EMA(21) yukari kesince AL, asagi kesince SAT.
           SMA'dan daha reaktiftir, son fiyatlara daha fazla agirlik verir.
Kaynak   : Swing trading klasigi, kurumsal kisa vadeli trend takibi
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, hizli=8, yavas=21):
    strateji_adi = f"ema_cross_{hizli}_{yavas}"

    ema_hizli = kapanis.ewm(span=hizli, adjust=False).mean()
    ema_yavas = kapanis.ewm(span=yavas, adjust=False).mean()

    al_sinyalleri  = (ema_hizli > ema_yavas) & (ema_hizli.shift(1) <= ema_yavas.shift(1))
    sat_sinyalleri = (ema_hizli < ema_yavas) & (ema_hizli.shift(1) >= ema_yavas.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
