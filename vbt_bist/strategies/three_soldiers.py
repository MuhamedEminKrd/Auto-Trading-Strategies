"""
Strateji : Three White Soldiers / Three Black Crows
Mantik   : 3 ardisik yesil mum (White Soldiers) AL sinyali,
           3 ardisik kirmizi mum (Black Crows) SAT sinyalidir.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(acilis, yuksek, dusuk, kapanis, baslik):
    strateji_adi = "three_soldiers"

    yesil = kapanis > acilis
    kirmizi = kapanis < acilis
    
    # Three White Soldiers
    al_sinyalleri = (
        yesil & yesil.shift(1) & yesil.shift(2) & 
        (kapanis > kapanis.shift(1)) & 
        (kapanis.shift(1) > kapanis.shift(2))
    )
    
    # Three Black Crows
    sat_sinyalleri = (
        kirmizi & kirmizi.shift(1) & kirmizi.shift(2) & 
        (kapanis < kapanis.shift(1)) & 
        (kapanis.shift(1) < kapanis.shift(2))
    )
    
    # Tekrarlari filtrele
    al_sinyalleri = al_sinyalleri & (~al_sinyalleri.shift(1).fillna(False))
    sat_sinyalleri = sat_sinyalleri & (~sat_sinyalleri.shift(1).fillna(False))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
