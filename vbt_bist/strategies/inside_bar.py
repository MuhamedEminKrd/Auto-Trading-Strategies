
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, yuksek, dusuk, baslik):
    strateji_adi = "inside_bar"
    
    # Inside Bar sarti: Bugunun mumu tamamen dunku mumun icinde
    is_inside = (yuksek < yuksek.shift(1)) & (dusuk > dusuk.shift(1))
    
    # Ertesi gun dunku tepenin asilmasi (Breakout)
    onay = kapanis > yuksek.shift(2)
    
    al_sinyalleri = is_inside.shift(1) & onay
    sat_sinyalleri = al_sinyalleri.shift(4).fillna(False).infer_objects(copy=False)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
