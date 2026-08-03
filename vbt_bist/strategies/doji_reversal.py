
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(kapanis, yuksek, dusuk, acilis, baslik):
    strateji_adi = "doji_reversal"
    
    # Doji sarti: Acilis ile kapanis birbirine cok yakin, ama yuksek dusuk arasi genis
    govde_boyu = abs(kapanis - acilis)
    mum_boyu = yuksek - dusuk
    
    is_doji = (govde_boyu <= (mum_boyu * 0.1)) & (mum_boyu > 0)
    
    # Dusen trendde gelen Doji ve ertesi gun yukselis onayi
    dusus_trendi = kapanis.shift(2) < kapanis.shift(5)
    onay = kapanis > yuksek.shift(1) # Dojinin tepesini kirmak
    
    al_sinyalleri = is_doji.shift(1) & dusus_trendi & onay
    sat_sinyalleri = al_sinyalleri.shift(5).fillna(False).infer_objects(copy=False) # 5 gun tut
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
