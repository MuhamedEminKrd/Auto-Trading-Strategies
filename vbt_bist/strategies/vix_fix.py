"""
Strateji : Williams VIX Fix (Sentetik Korku Endeksi)
Mantik   : Hisseye ozel bir VIX hesaplar. Fiyat en yuksekten cok dustuyse korku tepe yapmistir.
           Korku cok arttiginda (Bollinger ust bandini kirdiginda) AL -> Dip avciligi.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=22, bb_periyot=20, bb_sapma=2.0):
    strateji_adi = f"vixfix_{periyot}"
    
    # Highest Close
    highest_close = kapanis.rolling(window=periyot).max()
    
    # VIX Fix Formulu
    wvf = ((highest_close - dusuk) / (highest_close + 1e-10)) * 100
    
    # VIX Fix icin Bollinger Bandi (Korkunun asiriligi)
    wvf_sma = wvf.rolling(window=bb_periyot).mean()
    wvf_std = wvf.rolling(window=bb_periyot).std()
    wvf_upper = wvf_sma + (bb_sapma * wvf_std)
    
    # Sinyaller: Korku bandin ustune ciktiginda (Piyasada inanilmaz bir kriz/panik var = DİP)
    al_sinyalleri = (wvf > wvf_upper) & (wvf.shift(1) <= wvf_upper.shift(1))
    # Korku ortalamaya dondugunde SAT
    sat_sinyalleri = (wvf < wvf_sma) & (wvf.shift(1) >= wvf_sma.shift(1))
    
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

