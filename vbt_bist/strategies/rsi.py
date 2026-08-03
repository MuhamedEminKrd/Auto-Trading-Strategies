"""
Strateji : RSI (Göreceli Güç Endeksi)
Mantik   : RSI 30'un altina inerse hisse "Asiri Satilmistir", toparlar (AL)
           RSI 70'in ustune cikarsa hisse "Asiri Alinmistir", duser (SAT)
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis_fiyatlari, baslik, periyot=14, alt_sinir=30, ust_sinir=70):
    strateji_adi = f"rsi_{periyot}_{alt_sinir}_{ust_sinir}"

    # RSI Hesapla
    rsi = vbt.RSI.run(kapanis_fiyatlari, window=periyot)

    # Sinyaller (RSI belirlenen sinirlari kestiğinde)
    al_sinyalleri  = rsi.rsi < alt_sinir
    sat_sinyalleri = rsi.rsi > ust_sinir

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
