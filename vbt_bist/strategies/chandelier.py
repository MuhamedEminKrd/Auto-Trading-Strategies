"""
Strateji : Chandelier Exit
Mantik   : ATR bazli takip eden stop (trailing stop) stratejisidir. 
           Fiyat Chandelier stop noktasini yukari kesince AL, asagi kesince SAT.
"""
import vectorbt as vbt
import pandas as pd
import os
from strategies.utils import sonuclari_kaydet

def calistir(kapanis, yuksek, dusuk, baslik, periyot=22, carpan=3.0):
    strateji_adi = f"chandelier_{periyot}_{carpan}"

    # ATR Hesaplama
    prev_close = kapanis.shift(1)
    tr1 = yuksek - dusuk
    tr2 = (yuksek - prev_close).abs()
    tr3 = (dusuk - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = true_range.rolling(window=periyot).mean()

    # Chandelier Long Stop (Trendin altindaki cizgi) = 22 gunun en yuksegi - 3 * ATR
    highest_high = yuksek.rolling(window=periyot).max()
    chandelier_long = highest_high - (atr * carpan)

    # Chandelier Short Stop (Trendin ustundeki cizgi) = 22 gunun en dusugu + 3 * ATR
    # lowest_low = dusuk.rolling(window=periyot).min()
    # chandelier_short = lowest_low + (atr * carpan)
    
    # Basit trend takibi icin Long Stop cizgisini kullanalim. Fiyat uzerindeyse AL, altindaysa SAT.
    al_sinyalleri  = (kapanis > chandelier_long) & (kapanis.shift(1) <= chandelier_long.shift(1))
    sat_sinyalleri = (kapanis < chandelier_long) & (kapanis.shift(1) >= chandelier_long.shift(1))

    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))

    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
