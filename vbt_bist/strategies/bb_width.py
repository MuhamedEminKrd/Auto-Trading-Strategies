"""
Strateji : Bollinger Band Width (BBW)
Mantik   : BB Bant genisligi. Daraldiginda sikisma, genislediginde kirilim yasanir.
           Bant genisligi SMA'sini yukari kirarken fiyat da yukseliyorsa AL.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"bb_width_{periyot}"

    sma = kapanis.rolling(periyot).mean()
    std = kapanis.rolling(periyot).std()
    
    bbw = (4 * std) / sma
    bbw_sma = bbw.rolling(periyot).mean()

    # Bant genisliyor ve fiyat ortalamanin ustunde
    al_sinyalleri  = (bbw > bbw_sma) & (bbw.shift(1) <= bbw_sma.shift(1)) & (kapanis > sma)
    # Bant genisliyor ve fiyat ortalamanin altinda
    sat_sinyalleri = (bbw > bbw_sma) & (bbw.shift(1) <= bbw_sma.shift(1)) & (kapanis < sma)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
