import yfinance as yf
import vectorbt as vbt
import os

hisse_kodu = "GARAN.IS"
baslik = hisse_kodu.split(".")[0]

# -------------------------------------------------------------
# 1. VERİ ÇEKME
# -------------------------------------------------------------
print(f"1. {hisse_kodu} verileri çekiliyor...")
veri = yf.download(hisse_kodu, period="2y", interval="1d")
kapanis_fiyatlari = veri['Close'][hisse_kodu]

# -------------------------------------------------------------
# 2. ÜÇ ORTALAMA HESAPLAMA
# -------------------------------------------------------------
print("2. Üç Hareketli Ortalama hesaplanıyor...")
hizli_periyot = 5    # Kısa vadeli (anlık hareket)
orta_periyot  = 20   # Orta vadeli (kısa trend)
yavas_periyot = 50   # Uzun vadeli (ana trend onayı)

hizli_ma = vbt.MA.run(kapanis_fiyatlari, window=hizli_periyot)
orta_ma  = vbt.MA.run(kapanis_fiyatlari, window=orta_periyot)
yavas_ma = vbt.MA.run(kapanis_fiyatlari, window=yavas_periyot)

# -------------------------------------------------------------
# 3. SİNYAL ÜRETİMİ
# Kural: Hızlı ortayı keserken, fiyat YAVAŞın hangi tarafında?
# -------------------------------------------------------------
print("3. Al/Sat sinyalleri üretiliyor...")

# AL: Hızlı orta MA'yı yukarı kesti VE fiyat yavaş MA'nın üzerinde (trend yukarı)
al_sinyalleri  = hizli_ma.ma_crossed_above(orta_ma) & (kapanis_fiyatlari > yavas_ma.ma)

# SAT: Hızlı orta MA'yı aşağı kesti VE fiyat yavaş MA'nın altında (trend aşağı)
sat_sinyalleri = hizli_ma.ma_crossed_below(orta_ma) & (kapanis_fiyatlari < yavas_ma.ma)

# -------------------------------------------------------------
# 4. BACKTEST
# -------------------------------------------------------------
print("4. Portföy simülasyonu başlatılıyor...")
portfoy = vbt.Portfolio.from_signals(
    kapanis_fiyatlari,
    entries=al_sinyalleri,
    exits=sat_sinyalleri,
    init_cash=10000,
    fees=0.001,
    freq='1d'
)

# -------------------------------------------------------------
# 5. ÇIKTILARI KAYDET
# -------------------------------------------------------------
print("5. Sonuçlar ve grafik kaydediliyor...")
klasor_yolu = f"vbt_bist/output/{baslik}"
os.makedirs(klasor_yolu, exist_ok=True)

ozet = portfoy.stats()
ozet.to_csv(f"{klasor_yolu}/{baslik}_three_ma_ozet.csv")

islemler = portfoy.trades.records_readable
islemler.to_csv(f"{klasor_yolu}/{baslik}_three_ma_islemler.csv")

fig = portfoy.plot(title=f"{baslik} - Üçlü Hareketli Ortalama ({hizli_periyot}-{orta_periyot}-{yavas_periyot}) Stratejisi")
fig.write_html(f"{klasor_yolu}/{baslik}_three_ma_grafik.html")
fig.write_image(f"{klasor_yolu}/{baslik}_three_ma_vbt.png", width=1400, height=900)

print(f"\n*** İŞLEM TAMAMLANDI! ***")
print(f"Toplam Getiri (Net Kar): %{ozet['Total Return [%]']:.2f}")
print(f"Kazanma Oranı: %{ozet['Win Rate [%]']:.2f}")
