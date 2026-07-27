# pyrefly: ignore [missing-import]
import yfinance as yf
# pyrefly: ignore [missing-import]
import vectorbt as vbt
import os

hisse_kodu = "GARAN.IS"
# "GARAN.IS" yazısından sadece "GARAN" kısmını alıyoruz 
baslik = hisse_kodu.split(".")[0] 

# 1. VERİ ÇEKME AŞAMASI
print(f"1. {hisse_kodu} verileri yfinance'ten çekiliyor...")
# 2 yıllık 
veri = yf.download(hisse_kodu, period="2y", interval="1d")

# Kesişim stratejisini fiyatın Kapanış (Close) değerine göre kuracağız
kapanis_fiyatlari = veri['Close'][hisse_kodu]

# 2. STRATEJİ VE SİNYAL ÜRETİMİ (İkili Ortalama)

print("2. Hızlı ve Yavaş Hareketli Ortalamalar hesaplanıyor...")
hizli_periyot = 10  # Son 10 günün ortalaması (Kısa vadeli trend)
yavas_periyot = 50  # Son 50 günün ortalaması (Uzun vadeli trend)

# vectorbt (vbt) kütüphanesi ile ortalamaları tek satırda hesaplıyoruz
hizli_ma = vbt.MA.run(kapanis_fiyatlari, window=hizli_periyot)
yavas_ma = vbt.MA.run(kapanis_fiyatlari, window=yavas_periyot)

# Alış (Entry) ve Satış (Exit) sinyallerini kurala göre bağlıyoruz
al_sinyalleri = hizli_ma.ma_crossed_above(yavas_ma)  # Hızlı, yavaşı YUKARI kestiğinde AL (True döner)
sat_sinyalleri = hizli_ma.ma_crossed_below(yavas_ma) # Hızlı, yavaşı AŞAĞI kestiğinde SAT (True döner)

# 3. BACKTEST (GEÇMİŞE DÖNÜK SİMÜLASYON)
print("3. Geçmişe dönük portföy simülasyonu başlatılıyor...")
# Başlangıç bütçesi 10.000 TL, her işlemde binde 1 (%0.1) borsa/aracı kurum komisyonu kesilecek
portfoy = vbt.Portfolio.from_signals(
    kapanis_fiyatlari, 
    entries=al_sinyalleri, 
    exits=sat_sinyalleri, 
    init_cash=10000, 
    fees=0.001,
    freq='1d'  # Verinin GÜNLÜK (1 day) olduğunu belirttik
)

# 4. ÇIKTILARI VE GRAFİĞİ KAYDETME
print("4. Sonuçlar, işlemler ve grafik kaydediliyor...")
# Projenin içine output/GARAN adında bir klasör yoksa otomatik olarak oluşturuyoruz
klasor_yolu = f"vbt_bist/output/{baslik}"
os.makedirs(klasor_yolu, exist_ok=True)

# a) İstatistik Özetini (Sharpe oranı, kazanma oranı vb.) CSV olarak kaydet
ozet = portfoy.stats()
ozet.to_csv(f"{klasor_yolu}/{baslik}_two_ma_ozet.csv")

# b) Tüm Alım-Satım işlemlerini (Hangi tarihte, hangi fiyattan lot alındı/satıldı) CSV olarak kaydet
islemler = portfoy.trades.records_readable
islemler.to_csv(f"{klasor_yolu}/{baslik}_two_ma_islemler.csv")

# c) Hocanın gönderdiği görseldeki ok işaretli mükemmel grafiği PNG olarak çiz ve kaydet
fig = portfoy.plot(title=f"{baslik} - İkili Hareketli Ortalama ({hizli_periyot}-{yavas_periyot}) Stratejisi")
# 1) İnteraktif Web Grafiği (fareyle zoom yapılabilir)
fig.write_html(f"{klasor_yolu}/{baslik}_two_ma_grafik.html")

# 2) Statik Resim (hocaya göndermek için, raporlara koymak için)
fig.write_image(f"{klasor_yolu}/{baslik}_two_ma_vbt.png", width=1400, height=900)



print(f"\n*** İŞLEM TAMAMLANDI! ***")
print(f"Toplam Getiri (Net Kar): %{ozet['Total Return [%]']:.2f}")
print(f"Lütfen oluşturulan '{klasor_yolu}' klasörünün içindeki resme ve CSV dosyalarına göz at!")
