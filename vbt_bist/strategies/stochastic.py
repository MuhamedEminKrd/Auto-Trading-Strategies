"""
Strateji : Stochastic Oscillator (Stokastik)
Mantik   : Fiyat, son N gunun araliginda nerede? 
           Asiri satimdan (%20 alti) yukari donerse AL, asiri alimdan (%80 ustu) asagi donerse SAT.
"""
import vectorbt as vbt
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=14, k_periyot=3, alt_sinir=20, ust_sinir=80):
    strateji_adi = f"stoch_{periyot}_{k_periyot}_{alt_sinir}_{ust_sinir}"
    
    # Son 14 gunun en dusugu ve en yuksegi
    low_min = dusuk.rolling(window=periyot).min()
    high_max = yuksek.rolling(window=periyot).max()
    
    # %K Cizgisi
    k_fast = 100 * (kapanis - low_min) / (high_max - low_min + 1e-10)
    # %D Cizgisi (K'nin 3 gunluk ortalamasi - sinyal icin kullanilir)
    k_slow = k_fast.rolling(window=k_periyot).mean()
    
    # Sinyaller
    al_sinyalleri = (k_slow > alt_sinir) & (k_slow.shift(1) <= alt_sinir)
    sat_sinyalleri = (k_slow < ust_sinir) & (k_slow.shift(1) >= ust_sinir)
    
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

