
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "fractal_breakout"
    
    # Williams Up Fractal (Ortadaki mumun sagi solu daha dusuk tepelere sahip)
    up_fractal = (yuksek.shift(2) > yuksek.shift(4)) & (yuksek.shift(2) > yuksek.shift(3)) & \
                 (yuksek.shift(2) > yuksek.shift(1)) & (yuksek.shift(2) > yuksek)
                 
    # Fraktal noktasini kaydet (ileri tasi)
    fractal_seviyesi = yuksek.shift(2).where(up_fractal).ffill()
    
    # Fiyat yakin zamanda (son 10 gun icinde) bu fraktal direncini kirarsa AL
    al_sinyalleri = (kapanis > fractal_seviyesi) & (kapanis.shift(1) <= fractal_seviyesi.shift(1))
    
    # Basit Exit: Kapanis 10 gunluk dusugun altina inince SAT
    stop_loss = dusuk.rolling(10).min()
    sat_sinyalleri = kapanis < stop_loss
    
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
