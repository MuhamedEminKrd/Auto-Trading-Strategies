"""
Strateji : Ichimoku Cloud (Kinko Hyo)
Mantik   : Japon teknigi. Fiyat bulutun (Senkou Span A ve B) ustune cikarsa AL.
           Fiyat bulutun altina inerse SAT. Bulut icindeyken islem yapma.
"""
import vectorbt as vbt
import pandas as pd
import numpy as np
import os

def calistir(yuksek, dusuk, kapanis, baslik, t_periyot=9, k_periyot=26, s_periyot=52):
    strateji_adi = f"ichimoku_{t_periyot}_{k_periyot}_{s_periyot}"
    
    # Tenkan-sen (Donusum Cizgisi)
    t_high = yuksek.rolling(window=t_periyot).max()
    t_low = dusuk.rolling(window=t_periyot).min()
    tenkan_sen = (t_high + t_low) / 2
    
    # Kijun-sen (Temel Cizgi)
    k_high = yuksek.rolling(window=k_periyot).max()
    k_low = dusuk.rolling(window=k_periyot).min()
    kijun_sen = (k_high + k_low) / 2
    
    # Senkou Span B (Öncü Çizgi B)
    s_high = yuksek.rolling(window=s_periyot).max()
    s_low = dusuk.rolling(window=s_periyot).min()
    senkou_span_b = (s_high + s_low) / 2
    
    # Senkou Span A (Öncü Çizgi A)
    senkou_span_a = (tenkan_sen + kijun_sen) / 2
    
    # Kumo Bulutunu ileriye kaydir (k_periyot kadar, genelde 26 gun)
    senkou_span_a = senkou_span_a.shift(k_periyot)
    senkou_span_b = senkou_span_b.shift(k_periyot)
    
    # Fiyat bulutun neresinde?
    bulut_ustu = np.maximum(senkou_span_a, senkou_span_b)
    bulut_alti = np.minimum(senkou_span_a, senkou_span_b)
    
    # Sinyaller
    # Fiyat bulutun (direncin) ustune kirarsa AL
    al_sinyalleri = (kapanis > bulut_ustu) & (kapanis.shift(1) <= bulut_ustu.shift(1))
    
    # Fiyat bulutun (destegin) altina duserse SAT
    sat_sinyalleri = (kapanis < bulut_alti) & (kapanis.shift(1) >= bulut_alti.shift(1))
    
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

