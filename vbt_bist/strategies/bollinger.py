"""
Strateji : Bollinger Bantları
Mantık   : Fiyat alt banda dokunursa AL (ucuz, toparlar)
           Fiyat üst banda dokunursa SAT (pahalı, düşer)
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis_fiyatlari, baslik, periyot=20, std_sapma=2.0):
    strateji_adi = f"bollinger_{periyot}_{std_sapma}"

    # Bollinger Bantlarını Hesapla
    bb = vbt.BBANDS.run(kapanis_fiyatlari, window=periyot, alpha=std_sapma)


    # Sinyaller: fiyat alt bandın altına inince AL, üst bandın üstüne çıkınca SAT
    al_sinyalleri  = kapanis_fiyatlari < bb.lower
    sat_sinyalleri = kapanis_fiyatlari > bb.upper

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
