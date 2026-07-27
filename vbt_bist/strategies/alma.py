
import vectorbt as vbt
import os
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, window=20, offset=0.85, sigma=6):
    strateji_adi = f"alma_{window}"
    
    m = int(offset * (window - 1))
    s = window / sigma
    
    weights = np.exp(-((np.arange(window) - m) ** 2) / (2 * s * s))
    weights /= weights.sum()
    
    def calc_alma(x):
        return (x * weights).sum()
        
    alma = kapanis.rolling(window).apply(calc_alma, raw=True)
    
    al_sinyalleri = (kapanis > alma) & (kapanis.shift(1) <= alma.shift(1))
    sat_sinyalleri = (kapanis < alma) & (kapanis.shift(1) >= alma.shift(1))
    
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
