
import vectorbt as vbt
import os
import pandas as pd

def calistir(yuksek, dusuk, kapanis, baslik, periyot=25):
    strateji_adi = f"aroon_{periyot}"
    
    # Aroon Up: (Periyot - En yuksek tepeden gecen gun) / Periyot * 100
    aroon_up = yuksek.rolling(periyot + 1).apply(lambda x: x.argmax(), raw=True) / periyot * 100
    # Aroon Down: (Periyot - En dusuk dipten gecen gun) / Periyot * 100
    aroon_down = dusuk.rolling(periyot + 1).apply(lambda x: x.argmin(), raw=True) / periyot * 100
    
    aroon_osc = aroon_up - aroon_down
    
    al_sinyalleri = (aroon_osc > 0) & (aroon_osc.shift(1) <= 0)
    sat_sinyalleri = (aroon_osc < 0) & (aroon_osc.shift(1) >= 0)
    
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
