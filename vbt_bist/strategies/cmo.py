
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, periyot=20):
    strateji_adi = f"cmo_{periyot}"
    
    fark = kapanis.diff()
    yukselis = fark.where(fark > 0, 0)
    dusus = -fark.where(fark < 0, 0)
    
    sum_up = yukselis.rolling(periyot).sum()
    sum_down = dusus.rolling(periyot).sum()
    
    cmo = 100 * ((sum_up - sum_down) / (sum_up + sum_down + 1e-10))
    
    # Asiri satim bolgesinden (-50) yukari cikis
    al_sinyalleri = (cmo > -50) & (cmo.shift(1) <= -50)
    sat_sinyalleri = (cmo < 50) & (cmo.shift(1) >= 50)
    
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
