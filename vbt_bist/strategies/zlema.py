"""
Strateji : Zero Lag Exponential Moving Average (ZLEMA)
Mantik   : Hareketli ortalamalardaki gecikmeyi (lag) matematiksel olarak 
           sifira indirmeyi hedefler. Fiyat ZLEMA'yi yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"zlema_{periyot}"

    lag = int((periyot - 1) / 2)
    
    # Fiyati gecikme miktari kadar onceki fiyatla karsilastirip duzeltme yapalim
    zlema_data = kapanis + (kapanis - kapanis.shift(lag))
    zlema = zlema_data.ewm(span=periyot, adjust=False).mean()

    al_sinyalleri  = (kapanis > zlema) & (kapanis.shift(1) <= zlema.shift(1))
    sat_sinyalleri = (kapanis < zlema) & (kapanis.shift(1) >= zlema.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
