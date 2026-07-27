
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik):
    strateji_adi = "kst"
    
    # 4 farkli ROC hesaplanir ve agirlikli olarak toplanir
    roc1 = kapanis.pct_change(10).rolling(10).mean() * 1
    roc2 = kapanis.pct_change(15).rolling(10).mean() * 2
    roc3 = kapanis.pct_change(20).rolling(10).mean() * 3
    roc4 = kapanis.pct_change(30).rolling(15).mean() * 4
    
    kst = (roc1 + roc2 + roc3 + roc4) * 100
    kst_sinyal = kst.rolling(9).mean()
    
    al_sinyalleri = (kst > kst_sinyal) & (kst.shift(1) <= kst_sinyal.shift(1))
    sat_sinyalleri = (kst < kst_sinyal) & (kst.shift(1) >= kst_sinyal.shift(1))
    
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
