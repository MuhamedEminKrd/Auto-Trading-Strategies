"""
Strateji : Ortalamaya Donus (Mean Reversion)
Mantik   : Fiyat ortalamanin cok altina duserse AL (ucuz)
           Fiyat ortalamanin cok ustune cikarsa SAT (pahali)
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis_fiyatlari, baslik, periyot=20, sapma_katsayisi=1.5):
    strateji_adi = f"mean_reversion_{periyot}_{sapma_katsayisi}"

    ortalama = kapanis_fiyatlari.rolling(periyot).mean()
    sapma    = kapanis_fiyatlari.rolling(periyot).std()

    alt_bant = ortalama - (sapma_katsayisi * sapma)
    ust_bant = ortalama + (sapma_katsayisi * sapma)

    al_sinyalleri  = kapanis_fiyatlari < alt_bant
    sat_sinyalleri = kapanis_fiyatlari > ust_bant

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
