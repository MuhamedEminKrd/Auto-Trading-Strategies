"""
Strateji : RSI (Göreceli Güç Endeksi)
Mantik   : RSI 30'un altina inerse hisse "Asiri Satilmistir", toparlar (AL)
           RSI 70'in ustune cikarsa hisse "Asiri Alinmistir", duser (SAT)
"""
import vectorbt as vbt
import os

def calistir(kapanis_fiyatlari, baslik, periyot=14, alt_sinir=30, ust_sinir=70):
    strateji_adi = f"rsi_{periyot}_{alt_sinir}_{ust_sinir}"

    # RSI Hesapla
    rsi = vbt.RSI.run(kapanis_fiyatlari, window=periyot)

    # Sinyaller (RSI belirlenen sinirlari kestiğinde)
    al_sinyalleri  = rsi.rsi < alt_sinir
    sat_sinyalleri = rsi.rsi > ust_sinir

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

    fig = portfoy.plot(title=f"{baslik} - RSI Stratejisi ({periyot})")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
