"""
Strateji : MFI (Money Flow Index - Hacim Bazlı RSI)
Mantik   : Fiyat artarken hacim de artiyorsa guc onayi alir. 
           Asiri satimdan cikista AL, asiri alimdan dususte SAT.
"""
import vectorbt as vbt
import pandas as pd
import os

def calistir(yuksek, dusuk, kapanis, hacim, baslik, periyot=14, alt_sinir=20, ust_sinir=80):
    strateji_adi = f"mfi_{periyot}_{alt_sinir}_{ust_sinir}"
    
    # Tipik fiyat (Typical Price)
    tp = (yuksek + dusuk + kapanis) / 3
    # Ham para akisi (Raw Money Flow)
    rmf = tp * hacim
    
    diff = tp.diff()
    
    # Pozitif ve negatif para akislarini ayir
    pos_mf = rmf.copy()
    pos_mf[diff <= 0] = 0.0
    
    neg_mf = rmf.copy()
    neg_mf[diff >= 0] = 0.0
    
    # Periyot bazli toplamlar
    pos_sum = pos_mf.rolling(window=periyot).sum()
    neg_sum = neg_mf.rolling(window=periyot).sum()
    
    # MFI Hesaplama (Sifira bolunme hatasini engellemek icin ufak bir kontrol eklenir)
    mfi = 100 - (100 / (1 + (pos_sum / (neg_sum + 1e-10))))
    
    # Sinyaller
    al_sinyalleri = (mfi > alt_sinir) & (mfi.shift(1) <= alt_sinir)
    sat_sinyalleri = (mfi < ust_sinir) & (mfi.shift(1) >= ust_sinir)
    
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

