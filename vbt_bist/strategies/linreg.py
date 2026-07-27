
import vectorbt as vbt
import os
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=14):
    strateji_adi = f"linreg_slope_{periyot}"
    
    # VEKTÖREL OPTİMİZASYON (np.polyfit çok yavaştır, matematikle hızı 1000 kat artırıyoruz)
    x = np.arange(periyot)
    x_dev = x - x.mean()
    sum_x_dev_sq = np.sum(x_dev**2)
    
    def fast_slope(y):
        # OLS Eğim Formülü: cov(x,y) / var(x). Çok hızlı nokta çarpımı.
        return np.dot(x_dev, y) / sum_x_dev_sq
        
    slope_series = kapanis.rolling(window=periyot).apply(fast_slope, raw=True)
    
    # Eğim pozitife dönünce AL (yukselis trendi)
    al_sinyalleri = (slope_series > 0) & (slope_series.shift(1) <= 0)
    sat_sinyalleri = (slope_series < 0) & (slope_series.shift(1) >= 0)
    
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
