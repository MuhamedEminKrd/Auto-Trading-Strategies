"""
Strateji : Tekli Hareketli Ortalama (Single MA)
Mantık   : Fiyat, hareketli ortalamanın üzerine çıkarsa AL (trend başladı)
           Fiyat, hareketli ortalamanın altına inerse SAT (trend bitti)
Veri     : Sadece Kapanış (Close) fiyatı
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet


def calistir(kapanis_fiyatlari, baslik, periyot=20):
    """
    Tekli Hareketli Ortalama stratejisini çalıştırır ve sonuçları kaydeder.

    Parametreler:
        kapanis_fiyatlari : yfinance'ten gelen Close fiyat serisi
        baslik            : Hisse sembolü (ör: "GARAN")
        periyot           : Ortalama gün sayısı (varsayılan: 20)

    Döndürür:
        portfoy istatistikleri (pandas Series)
    """
    strateji_adi = f"single_ma_{periyot}"

    # --- Sinyal Üretimi ---
    ma = vbt.MA.run(kapanis_fiyatlari, window=periyot)

    # Fiyat ortalamanın üzerine çıktığında AL, altına indiğinde SAT
    al_sinyalleri  = kapanis_fiyatlari > ma.ma
    sat_sinyalleri = kapanis_fiyatlari < ma.ma

    # --- Backtest ---
    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    # --- Çıktıları Kaydet ---
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
