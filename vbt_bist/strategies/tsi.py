
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, yavas=25, hizli=13, sinyal=7):
    strateji_adi = f"tsi_{yavas}_{hizli}"
    
    momentum = kapanis.diff()
    
    # TSI formulu (Cift düzlestirme)
    smooth1 = momentum.ewm(span=yavas, adjust=False).mean()
    smooth2 = smooth1.ewm(span=hizli, adjust=False).mean()
    
    abs_momentum = momentum.abs()
    abs_smooth1 = abs_momentum.ewm(span=yavas, adjust=False).mean()
    abs_smooth2 = abs_smooth1.ewm(span=hizli, adjust=False).mean()
    
    tsi = 100 * (smooth2 / (abs_smooth2 + 1e-10))
    tsi_sinyal = tsi.ewm(span=sinyal, adjust=False).mean()
    
    al_sinyalleri = (tsi > tsi_sinyal) & (tsi.shift(1) <= tsi_sinyal.shift(1))
    sat_sinyalleri = (tsi < tsi_sinyal) & (tsi.shift(1) >= tsi_sinyal.shift(1))
    
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
