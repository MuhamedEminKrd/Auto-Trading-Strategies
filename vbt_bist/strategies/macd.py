"""
Strateji : MACD (Hareketli Ortalama Yakınsaması ve Iraksaması)
Mantik   : MACD çizgisi Sinyal çizgisini yukari keserse AL (Yukselis trendi)
           MACD çizgisi Sinyal çizgisini asagi keserse SAT (Dusus trendi)
"""
import vectorbt as vbt
import os

def calistir(kapanis_fiyatlari, baslik, hizli=12, yavas=26, sinyal=9):
    strateji_adi = f"macd_{hizli}_{yavas}_{sinyal}"

    # MACD Hesapla
    macd = vbt.MACD.run(kapanis_fiyatlari, fast_window=hizli, slow_window=yavas, signal_window=sinyal)

    # Sinyaller (MACD cizgisi, Sinyal cizgisini kestiginde)
    al_sinyalleri  = macd.macd_crossed_above(macd.signal)
    sat_sinyalleri = macd.macd_crossed_below(macd.signal)

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

    fig = portfoy.plot(title=f"{baslik} - MACD Stratejisi ({hizli}-{yavas}-{sinyal})")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
