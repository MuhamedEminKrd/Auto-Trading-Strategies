"""
Strateji : İkili Hareketli Ortalama Kesişimi (Two MA)
Mantık   : Hızlı ortalama, yavaş ortalamanın üzerine çıkarsa AL
           Hızlı ortalama, yavaş ortalamanın altına inerse SAT
Veri     : Sadece Kapanış (Close) fiyatı
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet


def calistir(kapanis_fiyatlari, baslik, hizli_periyot=10, yavas_periyot=50):
    """
    İkili Hareketli Ortalama stratejisini çalıştırır ve sonuçları kaydeder.

    Parametreler:
        kapanis_fiyatlari : yfinance'ten gelen Close fiyat serisi
        baslik            : Hisse sembolü (ör: "GARAN")
        hizli_periyot     : Kısa vadeli ortalama gün sayısı (varsayılan: 10)
        yavas_periyot     : Uzun vadeli ortalama gün sayısı (varsayılan: 50)

    Döndürür:
        portfoy istatistikleri (pandas Series)
    """
    strateji_adi = f"two_ma_{hizli_periyot}_{yavas_periyot}"

    # --- Sinyal Üretimi ---
    hizli_ma = vbt.MA.run(kapanis_fiyatlari, window=hizli_periyot)
    yavas_ma = vbt.MA.run(kapanis_fiyatlari, window=yavas_periyot)

    al_sinyalleri  = hizli_ma.ma_crossed_above(yavas_ma)
    sat_sinyalleri = hizli_ma.ma_crossed_below(yavas_ma)

    # --- Backtest ---
    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    # --- Çıktıları Kaydet ---
    # Yapı: output / HISSE_ADI / STRATEJI_ADI /
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
