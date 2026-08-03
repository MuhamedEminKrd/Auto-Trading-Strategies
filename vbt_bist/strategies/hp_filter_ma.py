"""
Strateji : HP Filter + Moving Average (Trend)
Mantik   : Fiyatlar Hodrick-Prescott (HP) filtresi ile gürültüden (noise) arındırılıp saf trend bulunur.
           Sonra bu saf trendin hareketli ortalama kesişimine bakılarak sahte sinyaller filtrelenir.
"""
import vectorbt as vbt
import pandas as pd
import os
import warnings
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, baslik, hizli=10, yavas=30):
    strateji_adi = "hp_filter_ma"
    
    # NaN degerleri dolduralim (Eger veride hata varsa filtre patlamasin diye)
    fiyat = kapanis.fillna(method='ffill').fillna(method='bfill')
    
    try:
        # HP Filter genelde statsmodels icinde hazir gelir.
        from statsmodels.tsa.filters.hp_filter import hpfilter
        # Günlük veri için lambda genelde 1600 (veya daha puruzsuz bir trend icin 14400) secilebilir.
        cycle, trend = hpfilter(fiyat, lamb=1600)
    except ImportError:
        # Eger ortamda statsmodels yüklü değilse, fallback olarak saf trendi çok yumuşatılmış EMA ile hesapla
        trend = fiyat.ewm(span=5, adjust=False).mean()

    # Pürüzsüzleştirilmiş "saf trend" üzerinden hareketli ortalamalar
    hizli_ma = trend.rolling(hizli).mean()
    yavas_ma = trend.rolling(yavas).mean()

    al_sinyalleri  = (hizli_ma > yavas_ma) & (hizli_ma.shift(1) <= yavas_ma.shift(1))
    sat_sinyalleri = (hizli_ma < yavas_ma) & (hizli_ma.shift(1) >= yavas_ma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
