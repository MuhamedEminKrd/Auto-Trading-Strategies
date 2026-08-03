"""
Strateji : Triple Screen Trading System (Elder'in 3 Ekran Sistemi)
Mantik   : 1. Ekran: MACD Histogram ile trend yonunu belirle
           2. Ekran: Stochastic ile geri cekilmeleri yakala
           Ikisi ayni yone isaret ettiginde AL/SAT.
Kaynak   : Alexander Elder (1986) - "Trading for a Living"
           BIST ozelinde bu test yapan akademik makale yok -> Ozgun katki
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, macd_h=12, macd_y=26, macd_s=9, stoch_p=14, stoch_s=3):
    strateji_adi = f"triple_screen"

    # --- 1. Ekran: MACD Histogram trend yonu ---
    macd_ind = vbt.MACD.run(kapanis, fast_window=macd_h, slow_window=macd_y, signal_window=macd_s)
    histogram = macd_ind.hist

    # Histogram yukseliyor mu? (trend yonu)
    hist_yukseliyor = histogram > histogram.shift(1)
    hist_dusuyor = histogram < histogram.shift(1)

    # --- 2. Ekran: Stochastic geri cekilme ---
    stoch = vbt.STOCH.run(yuksek, dusuk, kapanis, k_window=stoch_p, d_window=stoch_s)

    # Stochastic asiri satim bolgesinden donus
    stoch_al = (stoch.percent_k > 20) & (stoch.percent_k.shift(1) <= 20)
    # Stochastic asiri alim bolgesinden donus
    stoch_sat = (stoch.percent_k < 80) & (stoch.percent_k.shift(1) >= 80)

    # --- Kombine Sinyal: Her iki ekran da ayni yonde ---
    al_sinyalleri  = hist_yukseliyor & stoch_al
    sat_sinyalleri = hist_dusuyor & stoch_sat

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
