"""
Strateji : Ortalamaya Donus (Mean Reversion)
Mantik   : Fiyat ortalamanin cok altina duserse AL (ucuz)
           Fiyat ortalamanin cok ustune cikarsa SAT (pahali)
"""
import vectorbt as vbt
import os

def calistir(kapanis_fiyatlari, baslik, periyot=20, sapma_katsayisi=1.5):
    strateji_adi = f"mean_reversion_{periyot}_{sapma_katsayisi}"

    ortalama = kapanis_fiyatlari.rolling(periyot).mean()
    sapma    = kapanis_fiyatlari.rolling(periyot).std()

    alt_bant = ortalama - (sapma_katsayisi * sapma)
    ust_bant = ortalama + (sapma_katsayisi * sapma)

    al_sinyalleri  = kapanis_fiyatlari < alt_bant
    sat_sinyalleri = kapanis_fiyatlari > ust_bant

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d'
    )

    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))

    fig = portfoy.plot(title=f"{baslik} - Ortalamaya Donus ({periyot})")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
