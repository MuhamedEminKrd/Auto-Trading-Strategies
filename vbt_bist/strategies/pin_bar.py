"""
Strateji : Pin Bar (Igne Mum)
Mantik   : Alt fitili gövdenin en az 2 kati olan mum = Bullish Pin Bar -> AL
           Ust fitili gövdenin en az 2 kati olan mum = Bearish Pin Bar -> SAT
           Guclu bir fiyat ret (rejection) sinyalidir.
Kaynak   : Nial Fuller, Steve Nison - Japanese Candlestick Charting
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, acilis, yuksek, dusuk, baslik, fitil_orani=2.0):
    strateji_adi = f"pin_bar"

    govde = (kapanis - acilis).abs()
    alt_fitil = pd.concat([acilis, kapanis], axis=1).min(axis=1) - dusuk
    ust_fitil = yuksek - pd.concat([acilis, kapanis], axis=1).max(axis=1)

    # Minimum govde buyuklugu (cok kucuk mumlar filtre)
    min_govde = govde.rolling(20).mean() * 0.1

    # Bullish Pin Bar: alt fitil gövdenin 2+ kati VE ust fitil kucuk
    al_sinyalleri = (
        (alt_fitil > govde * fitil_orani) &
        (ust_fitil < govde * 0.5) &
        (govde > min_govde)
    )

    # Bearish Pin Bar: ust fitil gövdenin 2+ kati VE alt fitil kucuk
    sat_sinyalleri = (
        (ust_fitil > govde * fitil_orani) &
        (alt_fitil < govde * 0.5) &
        (govde > min_govde)
    )

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
