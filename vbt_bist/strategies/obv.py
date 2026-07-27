
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"obv_{periyot}"
    
    # OBV Hesaplama: Kapanis yukselirse hacmi ekle, duserse cikar
    fiyat_farki = kapanis.diff()
    obv = pd.Series(0, index=kapanis.index)
    obv[fiyat_farki > 0] = hacim[fiyat_farki > 0]
    obv[fiyat_farki < 0] = -hacim[fiyat_farki < 0]
    obv = obv.cumsum()
    
    # OBV SMA'yi yukari kestiginde AL (Hacim artisi)
    obv_sma = obv.rolling(window=periyot).mean()
    al_sinyalleri = (obv > obv_sma) & (obv.shift(1) <= obv_sma.shift(1))
    sat_sinyalleri = (obv < obv_sma) & (obv.shift(1) >= obv_sma.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool),
        init_cash=10000, fees=0.001, slippage=0.002, freq='1d'
    )
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    
    try:
        fig = portfoy.plot(title=f"{baslik} - {strateji_adi}")
        fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
        fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)
    except: pass
    return portfoy.stats()
