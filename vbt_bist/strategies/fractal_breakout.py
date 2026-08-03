
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "fractal_breakout"
    
    # Williams Up Fractal (Ortadaki mumun sagi solu daha dusuk tepelere sahip)
    up_fractal = (yuksek.shift(2) > yuksek.shift(4)) & (yuksek.shift(2) > yuksek.shift(3)) & \
                 (yuksek.shift(2) > yuksek.shift(1)) & (yuksek.shift(2) > yuksek)
                 
    # Fraktal noktasini kaydet (ileri tasi)
    fractal_seviyesi = yuksek.shift(2).where(up_fractal).ffill()
    
    # Fiyat yakin zamanda (son 10 gun icinde) bu fraktal direncini kirarsa AL
    al_sinyalleri = (kapanis > fractal_seviyesi) & (kapanis.shift(1) <= fractal_seviyesi.shift(1))
    
    # Basit Exit: Kapanis 10 gunluk dusugun altina inince SAT
    stop_loss = dusuk.rolling(10).min()
    sat_sinyalleri = kapanis < stop_loss
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
