"""
Strateji : Detrended Price Oscillator (DPO)
Mantik   : Fiyattan n/2+1 gun onceki SMA'yi cikarir, trendi kaldirir.
           Sifiri yukari kesince AL, asagi kesince SAT.
           Sadece dongusel (cyclical) hareketleri olcer.
Kaynak   : William Blau - teknik analiz klasikleri
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"dpo_{periyot}"

    # DPO = Kapanis - SMA(n/2 + 1 gun once)
    shift_amount = periyot // 2 + 1
    sma = kapanis.rolling(periyot).mean()
    dpo = kapanis - sma.shift(shift_amount)

    # Sifiri kesme sinyalleri
    al_sinyalleri  = (dpo > 0) & (dpo.shift(1) <= 0)
    sat_sinyalleri = (dpo < 0) & (dpo.shift(1) >= 0)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
