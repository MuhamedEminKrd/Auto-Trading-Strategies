"""
Strateji : İkili Hareketli Ortalama Kesişimi (Two MA)
Mantık   : Hızlı ortalama, yavaş ortalamanın üzerine çıkarsa AL
           Hızlı ortalama, yavaş ortalamanın altına inerse SAT
Veri     : Sadece Kapanış (Close) fiyatı
"""
import vectorbt as vbt
import os


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
        entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d'
    )

    # --- Çıktıları Kaydet ---
    # Yapı: output / HISSE_ADI / STRATEJI_ADI /
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv")
    )
    portfoy.trades.records_readable.to_csv(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv")
    )

    fig = portfoy.plot(
        title=f"{baslik} — İkili Ortalama ({hizli_periyot}/{yavas_periyot}) | vectorbt Backtest"
    )
    fig.write_html(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html")
    )
    fig.write_image(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"),
        width=1400, height=900
    )

    return portfoy.stats()
