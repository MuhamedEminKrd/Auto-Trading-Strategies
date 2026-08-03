"""
Strateji : TRIX (Triple EMA ROC)
Mantik   : Uclu ustel ortalamanin degisim orani. 
           Sifiri yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=15):
    strateji_adi = f"trix_{periyot}"

    ema1 = kapanis.ewm(span=periyot, adjust=False).mean()
    ema2 = ema1.ewm(span=periyot, adjust=False).mean()
    ema3 = ema2.ewm(span=periyot, adjust=False).mean()

    # 1 gunluk degisim orani (ROC)
    trix = (ema3 - ema3.shift(1)) / ema3.shift(1) * 100

    al_sinyalleri  = (trix > 0) & (trix.shift(1) <= 0)
    sat_sinyalleri = (trix < 0) & (trix.shift(1) >= 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
