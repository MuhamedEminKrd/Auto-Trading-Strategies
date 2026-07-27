
import vectorbt as vbt
import os
import pandas as pd

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20, sinir=100):
    strateji_adi = f"cci_{periyot}"
    
    tipik_fiyat = (yuksek + dusuk + kapanis) / 3
    sma_tp = tipik_fiyat.rolling(window=periyot).mean()
    
    import numpy as np
    # Mean Deviation hesaplama (Pandas 2.0'da mad() kaldirildi) - Vektörel Hızlı Hesaplama
    mad = tipik_fiyat.rolling(window=periyot).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    
    cci = (tipik_fiyat - sma_tp) / (0.015 * (mad + 1e-10))
    
    # CCI 100'u yukari kestiginde Gucu Teyit Et (AL)
    al_sinyalleri = (cci > sinir) & (cci.shift(1) <= sinir)
    sat_sinyalleri = (cci < -sinir) & (cci.shift(1) >= -sinir)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool),
        init_cash=10000, fees=0.001, slippage=0.002, freq='1d'
    )
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    try:
        portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))
        fig = portfoy.plot(title=f"{baslik} - {strateji_adi}")
        fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
        fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)
    except Exception as e:
        pass
    return portfoy.stats()
