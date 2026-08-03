"""
Strateji : Volatilite Siralama (Historical Volatility Rank)
Mantik   : Son 252 gunluk volatiliteye kiyasla su anki volatilitenin yuzdelik sirasi.
           Volatilite dip yapip dondugunde (10. yuzdelik dilimden yukari kirinca) AL.
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, periyot=20, rank_periyot=252):
    strateji_adi = f"historical_vol_rank_{periyot}"

    log_return = np.log(kapanis / kapanis.shift(1))
    hv = log_return.rolling(periyot).std() * np.sqrt(252)
    
    # 252 gunluk yuzdelik sira
    hv_rank = hv.rolling(rank_periyot).apply(lambda x: (x.iloc[-1] > x).sum() / len(x) * 100, raw=False)
    
    al_sinyalleri  = (hv_rank > 10) & (hv_rank.shift(1) <= 10)
    sat_sinyalleri = (hv_rank < 90) & (hv_rank.shift(1) >= 90)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
