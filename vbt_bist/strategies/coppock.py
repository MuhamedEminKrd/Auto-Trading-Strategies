
import vectorbt as vbt
import os
import pandas as pd

def calistir(kapanis, baslik):
    strateji_adi = "coppock_curve"
    
    # Günlük grafikler için standart Coppock değerleri (14, 11, 10) kullanıyoruz
    roc1 = kapanis.pct_change(14) * 100 # 14 Günlük ROC
    roc2 = kapanis.pct_change(11) * 100 # 11 Günlük ROC
    
    # ROC'larin toplaminin WMA'si
    roc_sum = roc1 + roc2
    
    # Pandas ile manual 10 gunluk WMA hesaplama
    weights = pd.Series(range(1, 11))
    def calc_wma(x): return (x * weights).sum() / weights.sum()
    
    coppock = roc_sum.rolling(10).apply(calc_wma, raw=True)
    
    # Coppock 0'in altindan yukariya kivrildiginda (Dip donusu) AL
    al_sinyalleri = (coppock < 0) & (coppock > coppock.shift(1)) & (coppock.shift(1) <= coppock.shift(2))
    sat_sinyalleri = (coppock > 0) & (coppock < coppock.shift(1)) & (coppock.shift(1) >= coppock.shift(2))
    
    portfoy = vbt.Portfolio.from_signals(
        kapanis, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool),
        init_cash=10000, fees=0.001, slippage=0.002, freq='1d'
    )
    
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)
    portfoy.stats().to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv"))
    
    try:
        portfoy.trades.records_readable.to_csv(os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv"))
        fig = portfoy.plot(title=f"{baslik} - {strateji_adi}")
        fig.write_html(os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html"))
        fig.write_image(os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"), width=1400, height=900)
    except Exception as e:
        pass
        
    return portfoy.stats()
