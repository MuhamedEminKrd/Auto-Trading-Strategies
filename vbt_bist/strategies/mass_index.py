"""
Strateji : Mass Index
Mantik   : Yuksek-Dusuk bandinin genislemesini olcer. 
           "Reversal Bulge" (Mass Index once 27 uzerine cikar, sonra 26.5 altina duserse)
           trend donusumu sinyali uretir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, ema_periyot=9, mi_periyot=25, ust_sinir=27.0, alt_sinir=26.5):
    strateji_adi = f"mass_index_{mi_periyot}"

    hl = yuksek - dusuk
    ema1 = hl.ewm(span=ema_periyot, adjust=False).mean()
    ema2 = ema1.ewm(span=ema_periyot, adjust=False).mean()
    
    # EMA Ratio
    ema_ratio = ema1 / (ema2 + 1e-10)
    
    # Mass Index
    mass_index = ema_ratio.rolling(mi_periyot).sum()

    # Reversal Bulge Sinyali
    # Once 27'yi gordu mu (son 10 gun icinde) ve simdi 26.5'u asagi kesti mi?
    gordu = (mass_index > ust_sinir).rolling(10).max().astype(bool)
    kesti = (mass_index < alt_sinir) & (mass_index.shift(1) >= alt_sinir)
    
    # Donus sinyali (Burada fiyat da 9 gunluk EMA'nin altindaysa AL, ustundeyse SAT gibi bir eklenti
    # yaygindir ama basite indirgeyip kesisimde direk sinyal uretelim - genelde trend yonunde)
    fiyat_ema = kapanis.ewm(span=ema_periyot, adjust=False).mean()
    
    al_sinyalleri  = gordu & kesti & (kapanis < fiyat_ema)
    sat_sinyalleri = gordu & kesti & (kapanis > fiyat_ema)

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
