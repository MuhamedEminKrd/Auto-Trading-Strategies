
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
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
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
