
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(acilis, kapanis, baslik):
    strateji_adi = "bullish_engulfing"
    
    # Gun 1 Dusus Mumu (Dünkü kapanış, dünkü açılıştan küçük)
    gun1_dusus = kapanis.shift(1) < acilis.shift(1)
    
    # Gun 2 Yukselis Mumu (Bugünkü kapanış, bugünkü açılıştan büyük)
    gun2_yukselis = kapanis > acilis
    
    # Yutma Sarti (Bugünkü gövde, dünkü gövdeyi tamamen kapsar)
    # Yani: Bugünün kapanışı > Dünün açılışı VE Bugünün açılışı < Dünün kapanışı
    yutma = (kapanis > acilis.shift(1)) & (acilis < kapanis.shift(1))
    
    al_sinyalleri = gun1_dusus & gun2_yukselis & yutma
    # Sabit sureli (5 gunluk) elde tutma
    sat_sinyalleri = al_sinyalleri.shift(5).fillna(False).infer_objects(copy=False)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
