"""
Strateji : Awesome Oscillator (AO)
Mantik   : Bill Williams tarafindan tasarlanmistir. Kapanis degil Medyan fiyatlarinin (Y+D/2) hareketli ortalamalarina bakar.
           Sifir cizgisini yukari kirdiginda guclu bir momentum baslangicidir.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, hizli=5, yavas=34):
    strateji_adi = f"ao_{hizli}_{yavas}"
    
    median_price = (yuksek + dusuk) / 2
    
    sma_hizli = median_price.rolling(window=hizli).mean()
    sma_yavas = median_price.rolling(window=yavas).mean()
    
    ao = sma_hizli - sma_yavas
    
    # Sifiri yukari keserse AL, asagi keserse SAT
    al_sinyalleri = (ao > 0) & (ao.shift(1) <= 0)
    sat_sinyalleri = (ao < 0) & (ao.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool), init_cash=10000, fees=0.001, slippage=0.002, freq='1d')
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    

    # --- Grafik Ciktilari ---
    try:
        portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))
        fig = portfoy.plot(title=f"{baslik} - {strateji_adi}")
        fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
        fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)
    except Exception as e:
        pass
        
    return portfoy.stats()

