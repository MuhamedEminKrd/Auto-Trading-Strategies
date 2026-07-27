"""
Strateji : Donchian Kanali (Fiyat Kirilimi / Breakout)
Mantik   : Fiyat, son N gunun (ornek: 20 gun) en yuksek seviyesini (direnci) yukari kirarsa AL.
           Fiyat, son N gunun en dusuk seviyesini (destegi) asagi kirarsa SAT.
"""
import vectorbt as vbt
import os

def calistir(yuksek, dusuk, kapanis, baslik, periyot=20):
    strateji_adi = f"donchian_{periyot}"

    # Üst Bant: Son 'periyot' (20) günün gördüğü en yüksek fiyat
    # shift(1) yapıyoruz çünkü bugünün fiyatı, "düne kadarki" rekoru kırıyor mu diye bakmalıyız.
    ust_bant = yuksek.rolling(window=periyot).max().shift(1)
    
    # Alt Bant: Son 'periyot' (20) günün gördüğü en düşük fiyat
    alt_bant = dusuk.rolling(window=periyot).min().shift(1)

    # Kirilim Sinyalleri
    # Kapanis fiyati, son 20 gunun zirvesinden BUYUKSE AL
    al_sinyalleri = kapanis > ust_bant
    # Kapanis fiyati, son 20 gunun dibinden KUCUKSE SAT
    sat_sinyalleri = kapanis < alt_bant

    portfoy = vbt.Portfolio.from_signals(
        kapanis,
        entries=al_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        exits=sat_sinyalleri.shift(1).fillna(False).astype(bool).astype(bool),
        init_cash=10000,
        fees=0.001, slippage=0.002, sl_stop=0.07, freq='1d'
    )

    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))

    fig = portfoy.plot(title=f"{baslik} - Donchian Kirilimi ({periyot})")
    fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
    fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)

    return portfoy.stats()
