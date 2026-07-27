
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "doji_reversal"
    acilis = kapanis.shift(1) # Acilis verimiz olmadigi icin 
    
    # Doji sarti: Acilis ile kapanis birbirine cok yakin, ama yuksek dusuk arasi genis
    govde_boyu = abs(kapanis - acilis)
    mum_boyu = yuksek - dusuk
    
    is_doji = (govde_boyu <= (mum_boyu * 0.1)) & (mum_boyu > 0)
    
    # Dusen trendde gelen Doji ve ertesi gun yukselis onayi
    dusus_trendi = kapanis.shift(2) < kapanis.shift(5)
    onay = kapanis > yuksek.shift(1) # Dojinin tepesini kirmak
    
    al_sinyalleri = is_doji.shift(1) & dusus_trendi & onay
    sat_sinyalleri = al_sinyalleri.shift(5).fillna(False).infer_objects(copy=False) # 5 gun tut
    
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
