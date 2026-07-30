"""
Strateji : Golden Cross / Death Cross (SMA 50 / SMA 200)
Mantik   : 50 gunluk hareketli ortalama, 200 gunluk hareketli ortalamani
           yukari kestiginde "Altin Kesisim" olusur -> AL
           Asagi kestiginde "Olum Kesisimi" olusur  -> SAT

Akademik : En cok referans verilen uzun vadeli trend teyit stratejisi.
           Goldman Sachs, JPMorgan analist raporlarinin temel filtresi.
           2 yillik veri: ~500 gun. Isinma: 200 gun. Sinyal penceresi: ~300 gun.
"""
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, kisa_periyot=50, uzun_periyot=200):
    strateji_adi = f"golden_cross_{kisa_periyot}_{uzun_periyot}"

    # Hareketli Ortalamalar
    sma_kisa = kapanis.rolling(kisa_periyot).mean()
    sma_uzun = kapanis.rolling(uzun_periyot).mean()

    # Altin Kesisim: SMA50 bugün SMA200'ün üstünde, dün değildi -> AL
    al_sinyalleri  = (sma_kisa > sma_uzun) & (sma_kisa.shift(1) <= sma_uzun.shift(1))

    # Olum Kesisimi: SMA50 bugün SMA200'ün altında, dün değildi -> SAT
    sat_sinyalleri = (sma_kisa < sma_uzun) & (sma_kisa.shift(1) >= sma_uzun.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, freq='1d'
    )

    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))

    fig = portfoy.plot(title=f"{baslik} - Golden Cross ({kisa_periyot}/{uzun_periyot})")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
