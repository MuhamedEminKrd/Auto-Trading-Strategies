"""
Strateji : Elder Ray Index (Boga / Ayi Gucu)
Mantik   : Bull Power = Yuksek - EMA13, Bear Power = Dusuk - EMA13
           EMA yukselirken Bear Power negatiften pozitife donerse AL
           EMA dusuyorken Bull Power pozitiften negatife donerse SAT
Kaynak   : Alexander Elder - "Trading for a Living" (1993)
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, ema_periyot=13):
    strateji_adi = f"elder_ray_{ema_periyot}"

    ema = kapanis.ewm(span=ema_periyot, adjust=False).mean()
    bull_power = yuksek - ema
    bear_power = dusuk - ema

    # Trend yonu: EMA yukseliyor mu?
    ema_yukseliyor = ema > ema.shift(1)
    ema_dusuyor = ema < ema.shift(1)

    # AL: EMA yukselirken Bear Power negatiften pozitife donerse
    al_sinyalleri = ema_yukseliyor & (bear_power > 0) & (bear_power.shift(1) <= 0)

    # SAT: EMA dusuyorken Bull Power pozitiften negatife donerse
    sat_sinyalleri = ema_dusuyor & (bull_power < 0) & (bull_power.shift(1) >= 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
