"""
Strateji : PPO (Percentage Price Oscillator)
Mantik   : MACD'nin yuzdesel versiyonu. Farkli fiyat seviyelerindeki hisseleri
           karsilastirabilir kilar. PPO sinyal hattini yukari kesince AL, asagi kesince SAT.
Kaynak   : Gerald Appel (MACD mucidi) tarafindan onerilen normalize edilmis versiyon
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, hizli=12, yavas=26, sinyal=9):
    strateji_adi = f"ppo_{hizli}_{yavas}_{sinyal}"

    ema_hizli = kapanis.ewm(span=hizli, adjust=False).mean()
    ema_yavas = kapanis.ewm(span=yavas, adjust=False).mean()

    # PPO = (EMA_hizli - EMA_yavas) / EMA_yavas * 100
    ppo = (ema_hizli - ema_yavas) / ema_yavas * 100
    ppo_sinyal = ppo.ewm(span=sinyal, adjust=False).mean()

    # Sinyal hatti kesisimleri
    al_sinyalleri  = (ppo > ppo_sinyal) & (ppo.shift(1) <= ppo_sinyal.shift(1))
    sat_sinyalleri = (ppo < ppo_sinyal) & (ppo.shift(1) >= ppo_sinyal.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
