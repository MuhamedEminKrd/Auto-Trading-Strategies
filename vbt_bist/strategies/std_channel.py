
import vectorbt as vbt
import os
import pandas as pd
import numpy as np

def calistir(kapanis, baslik, periyot=20, carpan=2.0):
    strateji_adi = f"std_channel_{periyot}_{carpan}"
    
    # Ortalama ve sapma hesapla (Bollinger'e benzer ama kanal mantigiyla regressif)
    sma = kapanis.rolling(periyot).mean()
    std = kapanis.rolling(periyot).std()
    
    ust_kanal = sma + (std * carpan)
    
    # Fiyat ust kanali sertce yukari kirarsa AL (Breakout)
    al_sinyalleri = (kapanis > ust_kanal) & (kapanis.shift(1) <= ust_kanal.shift(1))
    sat_sinyalleri = (kapanis < sma) # Ortalamaya donunce SAT
    
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
