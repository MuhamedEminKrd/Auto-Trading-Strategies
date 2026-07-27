"""
Strateji : Tekli Hareketli Ortalama (Single MA)
Mantık   : Fiyat, hareketli ortalamanın üzerine çıkarsa AL (trend başladı)
           Fiyat, hareketli ortalamanın altına inerse SAT (trend bitti)
Veri     : Sadece Kapanış (Close) fiyatı
"""
import vectorbt as vbt
import os


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
        exits=sat_sinyalleri.astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, freq='1d'
    )

    # --- Çıktıları Kaydet ---
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv")
    )
    portfoy.trades.records_readable.to_csv(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv")
    )

    fig = portfoy.plot(
        title=f"{baslik} — Tekli Ortalama ({periyot}) | vectorbt Backtest"
    )
    fig.write_html(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html")
    )
    fig.write_image(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"),
        width=1400, height=900
    )

    return portfoy.stats()
