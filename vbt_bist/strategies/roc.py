
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, periyot=12):
    strateji_adi = f"roc_{periyot}"
    
    roc = kapanis.pct_change(periyot) * 100
    
    # ROC sifiri yukari kesti ise momentum artiyor (AL)
    al_sinyalleri = (roc > 0) & (roc.shift(1) <= 0)
    sat_sinyalleri = (roc < 0) & (roc.shift(1) >= 0)
    
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
