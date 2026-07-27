"""
Strateji : Bollinger Bantları
Mantık   : Fiyat alt banda dokunursa AL (ucuz, toparlar)
           Fiyat üst banda dokunursa SAT (pahalı, düşer)
"""
import vectorbt as vbt
import os

def calistir(kapanis_fiyatlari, baslik, periyot=20, std_sapma=2.0):
    strateji_adi = f"bollinger_{periyot}_{std_sapma}"

    # Bollinger Bantlarını Hesapla
    bb = vbt.BBANDS.run(kapanis_fiyatlari, window=periyot, alpha=std_sapma)


    # Sinyaller: fiyat alt bandın altına inince AL, üst bandın üstüne çıkınca SAT
    al_sinyalleri  = kapanis_fiyatlari < bb.lower
    sat_sinyalleri = kapanis_fiyatlari > bb.upper

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, freq='1d'
    )

    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))

    fig = portfoy.plot(title=f"{baslik} — Bollinger Bantlari ({periyot}) | vectorbt")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
