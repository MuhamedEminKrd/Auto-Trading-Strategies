
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet
import pandas as pd

def calistir(yuksek, dusuk, kapanis, baslik, periyot=25):
    strateji_adi = f"aroon_{periyot}"
    
    # Aroon Up: (Periyot - En yuksek tepeden gecen gun) / Periyot * 100
    aroon_up = yuksek.rolling(periyot + 1).apply(lambda x: x.argmax(), raw=True) / periyot * 100
    # Aroon Down: (Periyot - En dusuk dipten gecen gun) / Periyot * 100
    aroon_down = dusuk.rolling(periyot + 1).apply(lambda x: x.argmin(), raw=True) / periyot * 100
    
    aroon_osc = aroon_up - aroon_down
    
    al_sinyalleri = (aroon_osc > 0) & (aroon_osc.shift(1) <= 0)
    sat_sinyalleri = (aroon_osc < 0) & (aroon_osc.shift(1) >= 0)
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
