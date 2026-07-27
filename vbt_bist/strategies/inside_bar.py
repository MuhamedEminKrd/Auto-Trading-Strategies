
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "inside_bar"
    
    # Inside Bar sarti: Bugunun mumu tamamen dunku mumun icinde
    is_inside = (yuksek < yuksek.shift(1)) & (dusuk > dusuk.shift(1))
    
    # Ertesi gun dunku tepenin asilmasi (Breakout)
    onay = kapanis > yuksek.shift(2)
    
    al_sinyalleri = is_inside.shift(1) & onay
    sat_sinyalleri = al_sinyalleri.shift(4).fillna(False).infer_objects(copy=False)
    
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
