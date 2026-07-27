
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"tema_{periyot}"
    
    ema1 = kapanis.ewm(span=periyot, adjust=False).mean()
    ema2 = ema1.ewm(span=periyot, adjust=False).mean()
    ema3 = ema2.ewm(span=periyot, adjust=False).mean()
    
    tema = 3 * ema1 - 3 * ema2 + ema3
    
    al_sinyalleri = (kapanis > tema) & (kapanis.shift(1) <= tema.shift(1))
    sat_sinyalleri = (kapanis < tema) & (kapanis.shift(1) >= tema.shift(1))
    
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
