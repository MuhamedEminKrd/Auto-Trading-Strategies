"""
Strateji : Chaikin Volatility
Mantik   : Yuksek-Dusuk bandinin EMA'sinin degisim orani (ROC). 
           Volatilite dustukten sonra yeniden yukselise gectiginde AL sinyali uretir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(yuksek, dusuk, kapanis, baslik, ema_periyot=10, roc_periyot=10):
    strateji_adi = f"chaikin_vol_{ema_periyot}"

    hl_ema = (yuksek - dusuk).ewm(span=ema_periyot, adjust=False).mean()
    cv = (hl_ema - hl_ema.shift(roc_periyot)) / (hl_ema.shift(roc_periyot) + 1e-10) * 100

    al_sinyalleri  = (cv > 0) & (cv.shift(1) <= 0)
    sat_sinyalleri = (cv < 0) & (cv.shift(1) >= 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
