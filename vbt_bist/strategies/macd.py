"""
Strateji : MACD (Hareketli Ortalama Yakınsaması ve Iraksaması)
Mantik   : MACD çizgisi Sinyal çizgisini yukari keserse AL (Yukselis trendi)
           MACD çizgisi Sinyal çizgisini asagi keserse SAT (Dusus trendi)
"""
import vectorbt as vbt
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis_fiyatlari, baslik, hizli=12, yavas=26, sinyal=9):
    strateji_adi = f"macd_{hizli}_{yavas}_{sinyal}"

    # MACD Hesapla
    macd = vbt.MACD.run(kapanis_fiyatlari, fast_window=hizli, slow_window=yavas, signal_window=sinyal)

    # Sinyaller (MACD cizgisi, Sinyal cizgisini kestiginde)
    al_sinyalleri  = macd.macd_crossed_above(macd.signal)
    sat_sinyalleri = macd.macd_crossed_below(macd.signal)

    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri.astype(bool),
        exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
