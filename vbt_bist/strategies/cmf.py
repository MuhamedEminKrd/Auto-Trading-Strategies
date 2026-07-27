
import vectorbt as vbt
import os
import pandas as pd

def calistir(yuksek, dusuk, kapanis, hacim, baslik, periyot=20):
    strateji_adi = f"cmf_{periyot}"
    
    # Money Flow Multiplier
    mfm = ((kapanis - dusuk) - (yuksek - kapanis)) / (yuksek - dusuk + 1e-10)
    mfv = mfm * hacim
    
    # CMF = 20 gunluk MFV Toplami / 20 gunluk Hacim Toplami
    cmf = mfv.rolling(window=periyot).sum() / (hacim.rolling(window=periyot).sum() + 1e-10)
    
    # CMF sifiri yukari keserse para girisi var (AL)
    al_sinyalleri = (cmf > 0) & (cmf.shift(1) <= 0)
    sat_sinyalleri = (cmf < 0) & (cmf.shift(1) >= 0)
    
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
