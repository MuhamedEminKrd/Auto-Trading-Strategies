# 🚀 Uygulama Planı: Strateji Cephaneliği (Faz 2.5 - İleri Düzey Quant Algoritmaları)

Araştırmalarımı derinleştirdim. Wall Street'teki kurumsal fonların (Quant Funds) sadece basit RSI veya MACD kullanmadığını, **istatistiksel anormalliklere (Z-Score)**, **gecikmesiz ortalamalara (HMA)** ve **sentetik volatiliteye (VIX Fix)** odaklandığını saptadım. 

Sistemimizi bir "Hobi" projesinden, "Kurumsal" bir algoritmik trade motoruna dönüştürecek 6 yeni elit strateji belirledim.

## User Review Required
> [!CAUTION]
> Bu eklemelerle sistemdeki toplam strateji sayımız 20'ye ulaşacak. Arayüzlü nihai backend mimarimizi kurduğumuzda, sistem her hisse için bu 20 stratejiyi saniyeler içinde kapıştırıp "En iyisini" seçecek. Strateji havuzumuz ne kadar kaliteliyse, yapay zekanın seçeceği algoritma o kadar kârlı olur.

## Open Questions
> [!WARNING]
> 1. Bu 6 yeni stratejiyi de sisteme entegre ettikten sonra, nihayet o ünlü **"Kâr/Zararı Excel'e Yazdırma"** özelliğini ekleyelim mi? Terminalde 20 satırı okumak artık çok zorlaşacak.
> 2. Onay verdiğin an kodları yazmaya başlayacağım. Hazır mısın?

---

## Önerilen Yeni İleri Düzey Stratejiler

### 1. Z-Score İstatistiksel Mean Reversion
- **Mantık:** Fiyatın kendi 20 günlük ortalamasından "Standart Sapma" olarak ne kadar uzaklaştığını ölçer. Kurumsal fonların en çok kullandığı "İstatistiksel Arbitraj" yöntemidir. Fiyat 2 standart sapma aşağı düştüğünde (aşırı panik) AL, +2'ye çıktığında SAT.
- **Kategori:** Kurumsal Mean Reversion

### 2. Williams VIX Fix (Sentetik Korku Endeksi)
- **Mantık:** Efsanevi trader Larry Williams'ın icadıdır. VIX (Korku) endeksi sadece piyasa geneli için vardır, ancak VIX Fix **tekil hisselerdeki (Örn: THYAO) korkuyu** hesaplar. Endeks tepe yaptığında piyasada kan gövdeyi götürüyordur ve tam orası **DİP** noktasıdır. Düşen bıçağı tutmanın en güvenli yoludur.
- **Kategori:** Dip Avcısı (Bottom Fishing)

### 3. HMA (Hull Moving Average)
- **Mantık:** Klasik hareketli ortalamaların (SMA, EMA) en büyük sorunu **gecikmedir (lag)**. Alan Hull tarafından bulunan HMA, karmaşık bir karekök ve ağırlıklandırma formülüyle gecikmeyi neredeyse sıfıra indirir. Trend dönüşlerini SMA'dan günlerce önce yakalar.
- **Kategori:** Gecikmesiz Trend Takibi

### 4. Williams %R
- **Mantık:** Stokastik osilatörün daha hızlı ve agresif kuzenidir. Trend içindeki çok kısa süreli geri çekilmelerde (pullback) "Fırsat" sinyali üretir.
- **Kategori:** Hızlı Momentum

### 5. Awesome Oscillator (AO)
- **Mantık:** Bill Williams'ın tasarladığı bu osilatör, piyasanın "Sürüş Gücünü" (Driving Force) ölçer. Kapanış fiyatları yerine **Medyan fiyatları (Yüksek+Düşük / 2)** kullanır. Histogram yeşile dönüp sıfır çizgisini kestiğinde muazzam bir trend başlangıcıdır.
- **Kategori:** Fiyat Hareketi (Price Action) Momentum

### 6. Parabolic SAR (Stop and Reverse)
- **Mantık:** Fiyatın altına "noktalar" koyarak trendi takip eder. Özelliği şudur: Trend uzadıkça noktalar fiyata daha da yaklaşır (İzleyen stop mantığı). Fiyat noktaya değdiği an "SAT ve SHORTLA" der. (Biz sadece AL ve NAKDE GEÇ için kullanacağız).
- **Kategori:** İzleyen Trend ve Çıkış

---

## Doğrulama Planı (Verification)
1. Bu 6 stratejinin formülleri tamamen `numpy` ve `pandas` vektörizasyonu ile sıfırdan yazılarak yeni dosyalara eklenecek.
2. `main.py` güncellenecek (Toplam 20 strateji).
3. Testler çalıştırılıp loglar incelenecek.
