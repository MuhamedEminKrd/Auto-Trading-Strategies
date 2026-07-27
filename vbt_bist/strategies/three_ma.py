"""
Strateji : Üçlü Hareketli Ortalama Kesişimi (Three MA)
Mantık   : Hızlı ortalama ortayı yukarı kestiğinde VE fiyat yavaş MA üzerindeyse AL
           Hızlı ortalama ortayı aşağı kestiğinde VE fiyat yavaş MA altındaysa SAT
           (Üçüncü ortalama, "ana trend" onay filtresi görevi görür)
Veri     : Sadece Kapanış (Close) fiyatı
"""
import vectorbt as vbt
import os


def calistir(kapanis_fiyatlari, baslik, hizli_periyot=5, orta_periyot=20, yavas_periyot=50):
    """
    Üçlü Hareketli Ortalama stratejisini çalıştırır ve sonuçları kaydeder.

    Parametreler:
        kapanis_fiyatlari : yfinance'ten gelen Close fiyat serisi
        baslik            : Hisse sembolü (ör: "GARAN")
        hizli_periyot     : Hızlı ortalama gün sayısı (varsayılan: 5)
        orta_periyot      : Orta ortalama gün sayısı  (varsayılan: 20)
        yavas_periyot     : Yavaş ortalama gün sayısı (varsayılan: 50)

    Döndürür:
        portfoy istatistikleri (pandas Series)
    """
    strateji_adi = f"three_ma_{hizli_periyot}_{orta_periyot}_{yavas_periyot}"

    # --- Sinyal Üretimi ---
    hizli_ma = vbt.MA.run(kapanis_fiyatlari, window=hizli_periyot)
    orta_ma  = vbt.MA.run(kapanis_fiyatlari, window=orta_periyot)
    yavas_ma = vbt.MA.run(kapanis_fiyatlari, window=yavas_periyot)

    al_sinyalleri  = hizli_ma.ma_crossed_above(orta_ma) & (kapanis_fiyatlari > yavas_ma.ma)
    sat_sinyalleri = hizli_ma.ma_crossed_below(orta_ma) & (kapanis_fiyatlari < yavas_ma.ma)

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
        title=f"{baslik} — Üçlü Ortalama ({hizli_periyot}/{orta_periyot}/{yavas_periyot}) | vectorbt Backtest"
    )
    fig.write_html(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html")
    )
    fig.write_image(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"),
        width=1400, height=900
    )

    return portfoy.stats()
