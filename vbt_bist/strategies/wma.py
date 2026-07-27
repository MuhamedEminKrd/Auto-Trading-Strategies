
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik, kisa=10, uzun=30):
    strateji_adi = f"wma_{kisa}_{uzun}"
    
    w_kisa = pd.Series(range(1, kisa + 1))
    w_uzun = pd.Series(range(1, uzun + 1))
    
    wma_kisa = kapanis.rolling(kisa).apply(lambda x: (x * w_kisa).sum() / w_kisa.sum(), raw=True)
    wma_uzun = kapanis.rolling(uzun).apply(lambda x: (x * w_uzun).sum() / w_uzun.sum(), raw=True)
    
    al_sinyalleri = (wma_kisa > wma_uzun) & (wma_kisa.shift(1) <= wma_uzun.shift(1))
    sat_sinyalleri = (wma_kisa < wma_uzun) & (wma_kisa.shift(1) >= wma_uzun.shift(1))
    
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
