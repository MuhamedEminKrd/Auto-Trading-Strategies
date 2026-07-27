"""
Strateji : Keltner Channels (Keltner Kanallari Breakout)
Mantik   : Bollinger'a benzer ama volatilitesi ATR'ye baglidir. 
           Fiyat Keltner Ust Bandini kirarsa AL (Squeeze patlamasi). Alt banti kirarsa SAT.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20, carpan=2.0):
    strateji_adi = f"keltner_{periyot}_{carpan}"
    
    # Keltner Orta Bant (Genelde EMA 20 kullanilir)
    orta_bant = kapanis.ewm(span=periyot, adjust=False).mean()
    
    # ATR hesapla (Volatilite)
    atr = vbt.ATR.run(yuksek, dusuk, kapanis, window=periyot).atr
    
    # Ust ve Alt Bant
    ust_bant = orta_bant + (carpan * atr)
    alt_bant = orta_bant - (carpan * atr)
    
    # Keltner Kirilimi (Breakout)
    al_sinyalleri = (kapanis > ust_bant) & (kapanis.shift(1) <= ust_bant.shift(1))
    sat_sinyalleri = (kapanis < alt_bant) & (kapanis.shift(1) >= alt_bant.shift(1))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, freq='1d'
    )
    
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

