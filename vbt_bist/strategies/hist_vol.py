
import vectorbt as vbt
import os
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"hist_vol_{periyot}"
    
    # Gunluk getirilerin standart sapmasi * kok(252)
    gunluk_getiri = kapanis.pct_change()
    hv = gunluk_getiri.rolling(window=periyot).std() * np.sqrt(252)
    
    hv_sma = hv.rolling(window=periyot).mean()
    
    # Volatilite asiri dusukken (HV < SMA) ve fiyat artiyorsa
    al_sinyalleri = (hv < hv_sma) & (kapanis > kapanis.rolling(20).mean()) & (kapanis.shift(1) <= kapanis.rolling(20).mean().shift(1))
    sat_sinyalleri = kapanis < kapanis.rolling(20).mean()
    
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
