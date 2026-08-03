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
    fiyat = kapanis.ffill().bfill()
    
    # HP Filter (Hodrick-Prescott) tüm zaman serisini hesaplamaya kattığı için Lookahead Bias (Geleceği Görme) yaratır.
    # Bu nedenle kaldırıldı. Yerine saf trendi çok yumuşatılmış EMA ile hesaplıyoruz.
    trend = fiyat.ewm(span=5, adjust=False).mean()

    # Pürüzsüzleştirilmiş "saf trend" üzerinden hareketli ortalamalar
    hizli_ma = trend.rolling(hizli).mean()
    yavas_ma = trend.rolling(yavas).mean()

    al_sinyalleri  = (hizli_ma > yavas_ma) & (hizli_ma.shift(1) <= yavas_ma.shift(1))
    sat_sinyalleri = (hizli_ma < yavas_ma) & (hizli_ma.shift(1) >= yavas_ma.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
