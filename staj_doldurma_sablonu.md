# STAJ DEFTERI DOLDURMA SABLONU
## BIST Algoritmik Backtest Projesi — 20 Is Gunu

> Bu dosya: her gun ne yazilacak, hangi gorsel eklenecek, haftalik tablolara ne girilecek.
> Word'e aktarirken: Times New Roman 11pt, iki yana yasli, her gun ayri sayfa.
> Her sayfanin USTUNDE Sayfa No, ALTINDA tarih, sorumlu muhendis islak imzasi olmali.
> Tum gorseller 6cm yuksekliginde. Sekil adi gorselin ALTINDA. Tablo adi tablonun USTUNDE.

---

## BOLUM A — ON SAYFALAR (Bir Kere Doldurulur)

### A.1 — Kapak / Ogrenci Bilgileri Tablosu

- AD SOYAD: Muhammed Emin Kardas
- OGRENCI NO: [kendi numarani yaz]
- BOLUM: Bilgisayar Muhendisligi
- STAJ TURU: [1. veya 2. Donem Staji]
- STAJ YERI ADI: [Sirket adi]
- STAJ YERI ADRESI: [Adres]
- SORUMLU MUHENDIS: [Huseyin Hoca veya Yunus Hoca — hangisi resmi ise]
- AMIR: [ekip lideri varsa]
- BASLANGIC TARIHI: [tarih]
- BITIS TARIHI: [tarih]

---

### A.2 — ICERIKLER Sayfasi

Her gunu ayri satir halinde ekle. Sayfa numaralarini en son doldur.

Ornek format:
```
Sekil, Cizelge ve Ekler Listesi ....... 1
Gun 1 — Proje Tanitimi ve Ortam Kurulumu ....... 2
Gun 2 — BIST Veri Mimarisi ve Ilk Backtest ....... 3
Gun 3 — Moduler Mimari: main.py + strategies/ ....... 4
... (20. gune kadar devam eder)
```

---

### A.3 — SEKIL, CIZELGE VE EKLER LISTESI

| No | Aciklama | Sayfa (Gun) |
|---|---|---|
| Sekil 1 | pip list veya requirements_vbt.txt terminal ciktisi | Gun 1 |
| Sekil 2 | GARAN.IS single_ma backtest grafigi | Gun 2 |
| Sekil 3 | strategies/ klasoru icerik listesi | Gun 3 |
| Sekil 4 | main.py importlib dinamik cagirma kodu | Gun 4 |
| Sekil 5 | 40 hisse terminal backtest ciktisi | Gun 5 |
| Sekil 6 | RSI veya MACD stratejisi grafik ciktisi | Gun 6 |
| Sekil 7 | Engulfing formasyonu semasi veya kodu | Gun 7 |
| Sekil 8 | OBV veya CMF grafik ciktisi | Gun 8 |
| Sekil 9 | strategies/ klasoru 90 dosya tam listesi | Gun 9 |
| Sekil 10 | 5 yillik veri indirme terminal ciktisi | Gun 10 |
| Sekil 11 | Master Excel 8.370 satir ekran goruntusu | Gun 11 |
| Sekil 12 | Overfitting Suphesi etiketli satir ornegi | Gun 12 |
| Sekil 13 | Dashboard mimari akis diyagrami | Gun 13 |
| Sekil 14 | run_strategy_and_get_portfoy kodu (monkey-patching) | Gun 14 |
| Sekil 15 | FastAPI api/metrics endpoint ciktisi | Gun 15 |
| Sekil 16 | Ilk React frontend prototip ekran goruntusu | Gun 16 |
| Sekil 17 | CSS Grid ile hizalanmis virtual scroll tablosu | Gun 17 |
| Sekil 18 | Dashboard sol sidebar filtre paneli | Gun 18 |
| Sekil 19 | Dashboard tam ekran — tum paneller acik | Gun 19 |
| Sekil 20 | Kategori bazli Alfa/getiri dagilimi tablosu | Gun 20 |

NOT: Gorseller 6cm yuksekliginde. Sekil adi ALTINDA. Tablo adi USTUNDE.

---

### A.4 — STAJIN YAPILDIGI KURUM TANITIMI

Format: Paragraf, Times New Roman 11pt, iki yana yasli, ~1 sayfa.

Kapsanmasi gerekenler (paragraf olarak yazilacak):
1. Sirketin adi, adresi, kurulus yili, faaliyet alani
2. Organizasyon yapisi: departmanlar, yonetim, calisma profili
3. Sunulan urun ve hizmetler: algoritmik trading, veri analizi
4. Calisma ortami: uzaktan/hibrit, gunluk is akisi
5. Staj yapilan bolum: Ar-Ge — kullanilan araclar (Python, vectorbt, React, FastAPI)
6. Yurutulen projeler: BIST Algoritmik Backtest Sistemi

Taslak paragraf:
[Sirket adi], [kurulus yili] yilinda kurulmus, finans teknolojileri alaninda faaliyet
gosteren bir yazilim sirketidir. Algoritmik trading sistemleri ve veri analizi konularinda
urun gelistiren sirketin [adres]te bulunan ofisinde stajimi tamamladim. Arastirma-Gelistirme
bolumunde gorev aldim; bolumde Python, vectorbt, FastAPI ve React teknolojileri
kullanilmaktadir. Staj surecinde BIST Algoritmik Backtest Sistemi projesine katki saglayarak
90 teknik analiz stratejisinin kodlanmasini, analiz edilmesini ve web dashboard uzerinden
gorsellestirilmesini gerceklestirdim.

---

### A.5 — GIRIS BOLUMU

Format: Paragraf, Times New Roman 11pt, iki yana yasli, ~1 sayfa.

Kapsanmasi gerekenler:
1. Stajin amaci: Finansal algoritmalarin BIST'e uygulanmasi, backtesting yontemiyle analiz
2. Kapsam: 90 strateji gelistirme, 63 hisse, 5 yillik veri, dashboard
3. Kurum tanitimi (kisaca)
4. Yapilan calismalarin ozeti: mimari → strateji → raporlama → dashboard
5. Mesleki katki: finans muhendisligi, yazilim mimarisi, veri analizi

Taslak:
Bu staj, Borsa Istanbul (BIST) hisse senetleri uzerinde algoritmik ticaret stratejilerinin
backtesting yontemiyle karsilastirilmasina yonelik kapsamli bir yazilim sistemi gelistirmek
amaciyla yurutulmustur. Python programlama dili ve vectorbt kutuphanesi kullanilarak 90 farkli
teknik analiz stratejisi kodlanmis; bu stratejilerin 63 BIST hissesi uzerindeki 5 yillik
(2020-2025) performanslari analiz edilmistir. Calisma sonucunda modüler bir backtest motoru,
otomatik master raporlama sistemi ve web tabanli interaktif analiz dashboard'u gelistirilmistir.
Bu proje; finansal algoritmalar, yazilim mimarisi tasarimi ve buyuk olcekli veri analizi
alanlarinda derinlemesine pratik bilgi kazandirmistir.

---

## BOLUM B — HAFTALIK OZET TABLOLAR

Sablondaki her haftalik tablo: Gun | Yapilan Isler | Sayfa No | Saat

### Hafta 1

| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Proje Tanitimi, Ortam Kurulumu, Ilk Veri Analizi | 2 | 8 |
| Sali | BIST Veri Mimarisi ve Ilk Backtest Denemeleri | 3 | 8 |
| Carsamba | Moduler Mimari: main.py ve strategies/ Klasoru | 4 | 8 |
| Persembe | Dinamik importlib Sistemi ve ATR Stratejileri | 5 | 8 |
| Cuma | Buyuk Olcek Backtest ve Smart Skip Sistemi | 6 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 2

| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | RSI MACD Momentum ve Mum Formasyonu Stratejileri | 7 | 8 |
| Sali | Hacim Analizi Stratejileri: OBV CMF VPT | 8 | 8 |
| Carsamba | Istatistiksel ve Ileri Momentum Stratejileri | 9 | 8 |
| Persembe | 90 Strateji Kutuphanesi ve 5 Yillik Veri Gecisi | 10 | 8 |
| Cuma | CCI mad() Hatasi ve Coppock Isinma Sorunu Cozumu | 11 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 3

| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Master Rapor Olusturma ve Yeni Metrikler | 12 | 8 |
| Sali | Anomali Analizi: Overfitting Etiketi ve Alfa Metrigi | 13 | 8 |
| Carsamba | Dashboard Mimari Tasarimi ve FastAPI Backend | 14 | 8 |
| Persembe | Monkey-Patching ile RAM Portfoy Yakalama | 15 | 8 |
| Cuma | React Frontend Kurulumu ve Veri Entegrasyonu | 16 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 4

| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Virtual Scroll ve HTML Table Hizalama Krizinin Cozumu | 17 | 8 |
| Sali | Excel-Like Filtre Sidebar Gelistirmesi | 18 | 8 |
| Carsamba | Canli Grafik Paneli iframe Entegrasyonu ve Excel Export | 19 | 8 |
| Persembe | Sistem Testleri Dashboard Polisleme ve Hata Duzeltme | 20 | 8 |
| Cuma | Genel Bulgular Alfa Analizi ve Staj Sonu Degerlendirme | 21 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

---

## BOLUM C — HER SAYFA KURALLARI

Sablonun her gun sayfasi icin zorunlular:
- En az 1 tam sayfa (sayfanin en az yarisi dolu)
- En az 1 gorsel/grafik/kod ekran goruntusu (Sekil No ile)
- Sayfanin ALTINDA tarih
- Her sayfada sorumlu muhendis islak imzasi
- Sayfanin USTUNDE 'Sayfa No: ___'
- Times New Roman 11pt, iki yana yasli paragraf
- Sayfalar tek yuz (arkali onlu degil)

Her paragraf mutlaka kapsayacaklar:
- O gun hangi gorevleri yerine getirdin?
- Hangi yazilim, arac veya metodolojileri kullandin?
- O gun ne ogrendi?
- Karsilasilan hata/sorun olduysa nasil cozuldu?
- Gunun genel ozeti ve degerlendirme

---

## BOLUM D — 20 GUNLUK PLAN

---

### GUN 1 — Proje Tanitimi, Ortam Kurulumu ve Ilk Analiz
**HAFTALIK TABLO GIRISI:** Proje Tanitimi, Ortam Kurulumu, Ilk Veri Analizi | 8 saat

**YAZILACAKLAR:**
Staj projesinin amaci: 151 stratejili GitHub reposundan BIST'e ozgu sistem gelistirme
Python sanal ortami (venv) olusturulmasi
Temel kutuphanelerin kurulumu: vectorbt, yfinance, pandas, plotly, kaleido
151 stratejili reponun incelenmesi ve BIST icin kullanilabilir strateji tespiti
Kritik bulgu: 151 stratejiden YALNIZCA 5 TANESI BIST verisiyle dogrudan calisiyor
Sebebi: cogu strateji coklu varlik karsilastirmasi veya BIST'te olmayan veri istiyor
Karar: Sifirdan BIST'e ozel moduler bir sistem kurulacak

**Kullanilan Araclar:** Python 3.12, pip, venv, VS Code, GitHub

**GORSEL:** Sekil 1: requirements_vbt.txt icerigi veya terminal pip list ciktisi

**Ogrenilen:** vectorbt kutuphanesinin temelleri. BIST ticker formati: .IS eki (GARAN.IS gibi). yfinance API kullanimi.

**Sorun / Cozum:** numpy/tensorflow surum uyumsuzlugu → requirements_vbt.txt ile surum sabitleme cozumu.

---

### GUN 2 — BIST Veri Mimarisi ve Ilk Backtest Denemeleri
**HAFTALIK TABLO GIRISI:** BIST Veri Mimarisi ve Ilk Backtest Denemeleri | 8 saat

**YAZILACAKLAR:**
yfinance ile GARAN.IS verisi cekilmesi ve OHLCV yapisinin incelenmesi
auto_adjust=True parametresinin onemi: temttu ve hisse bolunmesi duzeltmesi
MultiIndex vs duz DataFrame sorunu tespiti ve cozumu
single_ma.py ve two_ma.py ilk strateji dosyalarinin yazilmasi
vectorbt ile portfoy simulasyonu: vbt.Portfolio.from_signals()
Ilk sonuclar: GARAN single_ma → yaklasik yuzde 44 getiri
HTML interaktif grafik uretimi (plotly) + kaleido ile PNG export
KRITIK FARK: Lookahead bias sorunu — sinyal kapanista uretilip ayni gun alisim yapiliyor
Bu gercekte IMKANSIZ: kapanisi ancak gunun sonunda ogreniriz
Cozum: .shift(1) ile sinyaller bir gun otele alinir — 'bugun sinyal, yarin islem'

**Kullanilan Araclar:** Python, yfinance, pandas, vectorbt, plotly, kaleido

**GORSEL:** Sekil 2: GARAN.IS single_ma backtest grafigi (HTML'den ekran goruntusu)

**Ogrenilen:** Adjusted vs unadjusted fiyat farki. Backtest nedir ve nasil calisir. Lookahead bias neden tehlikeli ve sonuclari nasil bozar.

**Sorun / Cozum:** TypeError Only one column allowed → tek sutunlu portfoy secimi. kaleido eksikligi → pip install kaleido. Lookahead bias → .shift(1).

---

### GUN 3 — Moduler Mimari: main.py ve strategies/ Klasoru
**HAFTALIK TABLO GIRISI:** Moduler Mimari: main.py ve strategies/ Klasoru | 8 saat

**YAZILACAKLAR:**
Tek dosyali spaghetti mimarinin sorunlari: hardcoded hisse kodu, kod tekrari, bakimi zor
Yeni moduler mimari tasarimi:
  main.py: merkezi orkestrator — hisse listesi ve strateji listesi burada
  strategies/: her strateji ayri .py dosyasi, standart calistir() arayuzu
  output/HISSE/strateji_adi/: organize cikti klasor yapisi
strategies/utils.py olusturulmasi: merkezi konfigurasyon
  init_cash=10000 TL, fees=0.001 (yuzde 0.1 komisyon), slippage=0.002 (yuzde 0.2 slipaj)
three_ma.py, bollinger.py, mean_reversion.py eklenmesi
Komisyon ve slipaj kavramlarinin anlasılmasi: gercekci backtest icin neden gerekli

**Kullanilan Araclar:** Python, os, pathlib, VS Code

**GORSEL:** Sekil 3: strategies/ klasoru icerik listesi (ilk 5 strateji dosyasi gorunur)

**Ogrenilen:** Separation of Concerns yazilim prensibi. DRY (Don't Repeat Yourself). Moduler tasarimin bakım ve genisletme avantajlari. Komisyon ve slipaj backtest ekonomisi.

**Sorun / Cozum:** Ayni isimde klasor olusturma → os.makedirs(exist_ok=True) cozumu.

---

### GUN 4 — Dinamik importlib Sistemi ve ATR Tabanli Stratejiler
**HAFTALIK TABLO GIRISI:** Dinamik importlib Sistemi ve ATR Stratejileri | 8 saat

**YAZILACAKLAR:**
Strateji sayisi arttikca main.py'ye tek tek import yazmak sorun olmaya basladi
Cozum: importlib.import_module + inspect.signature ile dinamik strateji sistemi
  → Her strateji dosyasi yalnizca kendi ihtiyaci olan veriyi talep eder
  → main.py strateji detaylarini bilmek zorunda degil
  → Yeni strateji = yalnizca yeni .py dosyasi, main.py'ye dokunmak gerekmiyor
SuperTrend stratejisi: ATR (Average True Range) ile dinamik destek/direnc
Donchian Kanali: n gunluk yuksek/dusuk kirilim stratejisi
Bu stratejiler HLC (High/Low/Close) verisi gerektiriyor — veri enjeksiyonu otomatik
ADX, Keltner Kanali, Ichimoku stratejilerinin eklenmesi

**Kullanilan Araclar:** Python, importlib, inspect, vectorbt, pandas

**GORSEL:** Sekil 4: main.py importlib + inspect.signature dinamik cagirma kodu ekran goruntusu

**Ogrenilen:** Python reflection mekanizmasi. inspect.signature() ile parametre tespiti. Bagimlilik enjeksiyonu tasarim deseni. ATR ile volatilite olcumu.

**Sorun / Cozum:** AttributeError module has no attribute calistir → her dosyada standart arayuz zorunlulugu.

---

### GUN 5 — Buyuk Olcek Backtest ve Smart Skip Sistemi
**HAFTALIK TABLO GIRISI:** Buyuk Olcek Backtest ve Smart Skip Sistemi | 8 saat

**YAZILACAKLAR:**
BIST100'den 40 likit hissenin secilmesi: hacim, piyasa degeri kriterleri
40 hisse x 9 strateji = 360 kombinasyon ilk tam calisma
Calisma suresi sorunu: ~45 dakika, her yeni strateji eklendiginde tekrar calistiriliyor
Smart Skip sistemi tasarimi ve uygulamasi:
  Cikti klasoru zaten var ve dosya iceriyorsa → o kombinasyonu atla
  Yalnizca yeni strateji veya yeni hisse hesaplaniyor
Smart Skip'in etkisi: 360 kombinasyon yerine yalnizca 40 yeni kombinasyon hesaplaniyor
ASELS'te fractal_breakout stratejisinde yuzde 5000+ getiri → overfitting tartismasi
Multiple Comparisons problemi: 360 testten en iyiyi secmek istatistiksel anlamsiz

**Kullanilan Araclar:** Python, for dongusu, os.path, glob

**GORSEL:** Sekil 5: Terminal 40 hisse backtest ciktisi — [SKIP] mesajlari ve [1/9]...[9/9] siralama

**Ogrenilen:** Idempotency yazilim prensibi. Hesaplama maliyeti ve optimizasyon. Overfitting kavrami: gecmis veriye asiri uyum. Multiple comparisons / data snooping problemi.

**Sorun / Cozum:** PermissionError output klasoru → exist_ok=True parametresi cozumu.

---

### GUN 6 — RSI MACD Momentum ve Mum Formasyonu Stratejileri
**HAFTALIK TABLO GIRISI:** RSI MACD Momentum ve Mum Formasyonu Stratejileri | 8 saat

**YAZILACAKLAR:**
RSI (Relative Strength Index): asiri alim (>70) ve asiri satim (<30) bolgeleri, 14 periyot
MACD (Moving Average Convergence Divergence): 12/26/9 standart parametreler, sinyal cizgisi
rsi.py, macd.py, stochastic.py, williams_r.py, psar.py yazilmasi ve test edilmesi
Mum formasyonlari: Japonya'dan gelen teknik analiz teknigi
  Bullish Engulfing: onceki kirmizi mumu tamamen yutan buyuk yesil mum → alim sinyali
  Doji: acilis = kapanis, cok ince govde → kararsizlik sinyali
  Inside Bar: kucuk mumun bir onceki buyuk mumun icinde kalmasi → sikisman
engulfing.py, doji_reversal.py, inside_bar.py yazilmasi
78 kombinasyonda sifir islem sorunu: kosullar cok kati
Cozum: esik degerlerinin gevsetilmesi ve FutureWarning duzeltmesi

**Kullanilan Araclar:** Python, pandas shift() iloc[], vectorbt

**GORSEL:** Sekil 6: RSI stratejisi grafik ciktisi (THYAO veya GARAN hissesi)

**Ogrenilen:** RSI matematiksel hesabi: ortalama kari/ortalama zarara oran. MACD'nin trend takip mantigi. Mum formasyonlarinin matematiksel ifadesi. pandas shift() ile zaman serisi kaydirma.

**Sorun / Cozum:** 78 kombinasyonda sifir islem → engulfing/doji kosullari gevsetildi. FutureWarning fillna downcasting → .infer_objects(copy=False) eklendi.

---

### GUN 7 — Hacim Analizi Stratejileri: OBV CMF VPT AD-Line
**HAFTALIK TABLO GIRISI:** Hacim Analizi Stratejileri: OBV CMF VPT | 8 saat

**YAZILACAKLAR:**
Hacim verisinin onemi: fiyat hareketi + hacim = daha guvenilir sinyal
  Fiyat yukarsa + hacim artiyorsa → guclu trend (akilli para giriyor)
  Fiyat yukarsa + hacim dusuyorsa → zayif trend (sahte yukselis riski)
OBV (On-Balance Volume): hacim yonune gore birikimli toplam
CMF (Chaikin Money Flow): akilli para giris/cikis olcumu, -1 ile +1 arasi
VPT (Volume Price Trend): fiyat degisim yuzdesi x hacim
AD-Line (Accumulation/Distribution): para akisinin kumulatif izleme
Klinger, MFI, EOM, NVI, PVI, VWAP stratejilerinin eklenmesi
Bu stratejiler Hacim verisi gerektiriyor → importlib sistemi otomatik enjekte ediyor
CCI stratejisinde Series.mad() Deprecated hatasi ve cozumu:
  Pandas yeni surumlerde Series.mad() kaldirıldı
  Cozum: (df - df.mean()).abs().mean() ile elle hesaplama

**Kullanilan Araclar:** vectorbt, pandas, yfinance Volume sutunu

**GORSEL:** Sekil 7: Engulfing formasyonu semasi veya engulfing.py sinyal kodu ekran goruntusu

**Ogrenilen:** Hacim analizinin teknik analizdeki rolu. Akilli para kavrami. OBV/CMF matematigi. Pandas API degisikliklerine uyum saglamanin onemi.

**Sorun / Cozum:** CCI Series.mad() Deprecated → elle hesaplama ile cozuldu.

---

### GUN 8 — Istatistiksel ve Ileri Momentum Stratejileri
**HAFTALIK TABLO GIRISI:** Istatistiksel ve Ileri Momentum Stratejileri | 8 saat

**YAZILACAKLAR:**
Z-Score Mean Reversion: fiyatin uzun vadeli ortalamadan standart sapma cinsinden uzakligi
  z-score > 2 → asilama satil, z-score < -2 → dip satin al mantigi
Linear Regression Slope: egim acisiyla trend gucunu olcme
Historical Volatility: logaritmik kapanisların standart sapmasıyla hesaplanan oynaklık
HP Filter MA: Hodrick-Prescott filtresiyle trend/dongusal ayrimi
TSI (True Strength Index): cift yumusatilmis momentum gostergesi
KST (Know Sure Thing): dort farkli ROC'un agirlikli toplami
Coppock Curve: uzun vadeli dip donusu indikatoru (11+14+10 periyot isinma)
ALMA, HMA, TEMA, DEMA, WMA, ZLEMA alternatif hareketli ortalamalar
Elder Ray: boga ve ayi gucunun yuksek/dusuk bazli olcumu
VIX Fix: yerel volatilite zirveleri ile dip araması
fractl_breakout, squeeze, mass_index, rvi, ibs, trend_intensity eklenmesi

**Kullanilan Araclar:** numpy, scipy, vectorbt, pandas

**GORSEL:** Sekil 8: OBV veya CMF grafik ciktisi (BIMAS veya herhangi bir hisse)

**Ogrenilen:** Istatistiksel arbitraj temelleri. Z-score matematigi. Momentum ve mean-reversion stratejilerinin farkli piyasa kosullarindaki davranisi.

**Sorun / Cozum:** Bazi stratejilerde NaN propagation → .dropna() ve minimum bar sayisi kontrolleri eklendi.

---

### GUN 9 — 90 Strateji Kutuphanesi Tamamlandi
**HAFTALIK TABLO GIRISI:** 90 Strateji Kutuphanesi ve 5 Yillik Veri Gecisi | 8 saat

**YAZILACAKLAR:**
Projenin ana buyume hikayesi: 5 baslangic → 90 final strateji (18 kat buyume)
Final strateji sayisi: 90 strateji dosyasi (strategies/ klasorunde dogrulandi)
7 Kategori (final siniflandirma):
  1. Trend ve Hareketli Ortalamalar (16): ALMA, DEMA, EMA Cross, Golden Cross, HMA, MACD, PPO...
  2. Osilator ve Momentum (16): AO, CCI, CMO, Connors RSI, Coppock, DPO, KST, ROC, RSI...
  3. Volatilite ve Kanallar (14): ATR Breakout, Bollinger, Chandelier, Donchian, Keltner, Squeeze...
  4. Hacim ve Para Akisi (11): AD-Line, CMF, EOM, Klinger, MFI, OBV, VPT, VWAP...
  5. Fiyat Aksiyonu / Mum Formasyonlari (11): Doji, Engulfing, Fractal, Hammer, Inside Bar...
  6. Karmasik / Kantitatif Sistemler (13): Elder Ray, HP Filter MA, Ichimoku, VIX Fix, Z-Score...
  7. Kombine / Filtreli Stratejiler (8): ADX+MACD, BB+RSI, Supertrend+RSI, Triple Screen...
Veri tiplerine gore siniflandirma (Reflection mimarisinin temeli):
  Yalnizca Kapanis / Kapanis+Hacim / HLC / HLC+Hacim / Tam OHLC

**Kullanilan Araclar:** Python, importlib, inspect, os.scandir

**GORSEL:** Sekil 9: strategies/ klasoru tam listesi — 90 dosya gorunur (Explorer veya terminal)

**Ogrenilen:** 90 stratejinin 7 kategoride nasil siniflandirildigini. Her kategori hangi piyasa kosillarinda calisir. Veri bagimliligi ile sistem mimarisinin iliskisi.

**Sorun / Cozum:** Bazi strateji dosyalarinda sinyal oretmeyen (dead) stratejiler → debug ve duzeltme.

---

### GUN 10 — Coppock Isinma Sorunu ve 5 Yillik Veriye Gecis
**HAFTALIK TABLO GIRISI:** CCI mad() Hatasi ve Coppock Isinma Sorunu Cozumu | 8 saat

**YAZILACAKLAR:**
Coppock Curve stratejisi 2 yillik veride hic sinyal uretmiyor (0 islem)
Isinma suresi problemi: Coppock 11+14+10 = 35 aylik geriye bakar
  2 yillik (~504 gun) veri yeterli degil, strateji hicbir zaman aktif olmuyor
5 yillik veriye gecis karari: start=2020-01-01
BIST 2020-2025 makro rejimleri — neden 5 yil daha guclu veri saglar:
  2020: COVID krizi ve hizli toparlanma — yuksek volatilite
  2021-2022: yuksek enflasyon, kur krizi — trend stratejileri sinirda
  2023: secim donemlerinde piyasa carpikliği
  2024-2025: faiz stabilizasyonu, olgun piyasa davranisi
Tum analizlerin yeniden calistirilmasi — Smart Skip olmadan ~2 saat surerdi
Smart Skip sayesinde yalnizca eksik kombinasyonlar hesaplandi
Plotly NaN opacity hatasi: hic islem yoksa opacity array NaN oluyor
Cozum: portfoy.trades.count() > 0 kontrolu ile grafik uretimi kosullara baglandi

**Kullanilan Araclar:** yfinance, vectorbt, pandas, plotly

**GORSEL:** Sekil 10: 5 yillik veri indirme terminal ciktisi (toplam bar sayisi ~1250 gun)

**Ogrenilen:** Istatistiksel testlerde isinma suresi kavrami. Makro rejim analizi. Veri periyodunun backtest sonuclarına etkisi. Smart Skip'in buyuk olcekte kazandirdigi zaman.

**Sorun / Cozum:** Plotly NaN opacity → trades.count() > 0 kontrollü grafik uretimi.

---

### GUN 11 — Master Rapor Olusturma ve Yeni Metrikler
**HAFTALIK TABLO GIRISI:** Master Rapor Olusturma ve Yeni Metrikler | 8 saat

**YAZILACAKLAR:**
Problem: Binlerce CSV dosyasini tek tek acmak imkansiz
  63 hisse x 90 strateji = 5.670 kombinasyon → 8.370 CSV satiri (bazi hatalar icin bos)
Cozum: master_rapor_olustur.py
  glob ile tum *_ozet.csv dosyalari taranir, tek DataFrame'e birlestirilir
  Sonuc: 8.370 satir, 20+ sutun, tek Excel dosyasi
Temel metrikler (vectorbt otomatik uretir):
  Toplam Getiri (%): baslangic sermayeye gore net kar
  Sharpe Orani: risk basina getiri (>1 iyi, >2 cok iyi)
  Max Drawdown (%): en yuksek tepe-den-dibe dusus
  Profit Factor: toplam kar / toplam zarar (>1 karli)
  Islem Sayisi: kac alim-satim yapildi
Eklenen yeni metrikler:
  Alfa: Strateji getirisi - Benchmark (hisseyi al-tut) getirisi
  Risk-Ayarli Getiri: Kar% / Abs(Max Drawdown%) → risk basina getiri
  Akademik Gecerlilik Etiketi: + / | / - kategorileri
    + Istatistiksel Olarak Guvenilir: islem >= 10, PF < 15
    | Overfitting Suphesi: PF = sonsuz veya PF > 15 veya kar > %5000
    - Istatistiksel Yetersiz: islem < 10

**Kullanilan Araclar:** pandas, glob, openpyxl

**GORSEL:** Sekil 11: Master Excel 8.370 satir ekran goruntusu (sutun basliklar ve ilk satirlar gorunur)

**Ogrenilen:** Sharpe orani, Max Drawdown, Profit Factor kavramlari. Alfa nedir, neden onemli. Risk-ayarli getiri performansi daha dogru olcer.

**Sorun / Cozum:** PermissionError: Excel dosyasi acikken yazma girismei → dosyayi kapatip calistirma.

---

### GUN 12 — Anomali Analizi ve Metodolojik Degerlendirme
**HAFTALIK TABLO GIRISI:** Anomali Analizi: Overfitting Etiketi ve Alfa Metrigi | 8 saat

**YAZILACAKLAR:**
Master tablodaki anomalilerin analizi:
Anomali 1: 78 kombinasyonda sifir islem (engulfing ve coppock stratejileri)
  engulfing: kosullar hala fazla kati → daha fazla gevsetme gerekiyor
  coppock: 5 yillik veriyle artik calisiyor, sorun cozuldu
Anomali 2: Profit Factor = Sonsuz (hic zarar etmemis)
  Gercekte bu suphelidir: islem sayisi 1-2, istatistiksel anlamsiz
  Akademik Etiket: Overfitting Suphesi
Anomali 3: Yuzde 5000+ getiri (fractal_breakout - ASELS, ASTOR hisseleri)
  Bull market etkisi + small sample bias birlesimi
  Bu stratejiler gelecekte AYNI performansi gostermez
Overfitting kavrami derinlemesine tartisma:
  Bir strateji gecmis veriye cok iyi uyarsa, gelecekte cok kotü olur
  Sahte alpha: piyasayi yenmek degil, secansi secmek
Multiple Comparisons / Data Snooping problemi:
  8.370 kombinasyondan en iyiyi secmek istatistiksel olarak anlamsiz
  Bonferroni duzeltmesi: a/8370 ≈ 0.000006 kritik deger

**Kullanilan Araclar:** pandas, Excel

**GORSEL:** Sekil 12: Overfitting Suphesi etiketli satirlarin Excel filtreli goruntusu

**Ogrenilen:** Overfitting, survivorship bias, data snooping. Bonferroni duzeltmesi. Sonsuz Profit Factor neden suphelidir. Out-of-sample validation neden gerekli.

**Sorun / Cozum:** Akademik etiket kurallarinin belirlenmesi uzun tartisma gerektirdi → PF>15 veya islem<10 esikleri belirlendi.

---

### GUN 13 — Dashboard Mimari Tasarimi ve FastAPI Backend
**HAFTALIK TABLO GIRISI:** Dashboard Mimari Tasarimi ve FastAPI Backend | 8 saat

**YAZILACAKLAR:**
Problem: 8.370 satirlik Excel'de manuel filtre yetersiz ve zahmetli
Cozum: Web tabanli interaktif analiz dashboard'u
Mimari karari: FastAPI (backend) + React (frontend)
  Neden FastAPI: Python ekosistemiyle tam uyum, vectorbt entegrasyonu kolay
  Neden React: genis ekosistem, TanStack Virtual ile virtual scroll
Virtual scroll kavrami:
  8.370 satirin tumunu DOM'a yazmak tarayiciyi dondurur
  Virtual scroll: yalnizca ekranda gorunen ~15-20 satir DOM'a yaziliyor
  Geri kalan satirlar sanal olarak var ama DOM'da yok
FastAPI backend kurulumu ve temel endpointler:
  GET /api/metrics: Master Excel'i JSON olarak servis eder
  GET /api/chart/html/{hisse}/{strateji}: Plotly HTML grafigi uretir
  GET /api/chart/png/{hisse}/{strateji}: PNG formatinda grafik
pandas DataFrame → JSON donusumunde NaN degerleri None'a cevirme
CORS ayarlari: frontend localhost:5173 → backend localhost:8000

**Kullanilan Araclar:** FastAPI, uvicorn, pandas, Python

**GORSEL:** Sekil 13: Dashboard mimari akis diyagrami (veri akisi semasi)

**Ogrenilen:** REST API tasarimi. HTTP metodlari (GET/POST). JSON formati ve NaN sorunu. CORS nedir ve neden gerekli. Virtual scroll performans avantaji.

**Sorun / Cozum:** NaN degerleri JSON'a donustururken hata → df.fillna('') veya df.where(df.notna(), None) cozumu.

---

### GUN 14 — Monkey-Patching ile RAM Portfoy Yakalama
**HAFTALIK TABLO GIRISI:** Monkey-Patching ile RAM Portfoy Yakalama | 8 saat

**YAZILACAKLAR:**
Problem: Dashboard'da grafik gostermek icin backtest yeniden hesaplaniyor
  Her grafik isteginde strateji calistiriliyor ve Portfolio olusturuluyor
  Ancak sonuclari_kaydet() fonksiyonu CSV/HTML diske yaziyor — bize lazim degil
  Bize lazim olan: RAM'deki Portfolio nesnesi, dogrudan Plotly'e verecegiz
Cozum: Monkey-Patching teknigi
  Python'da fonksiyonlar runtime'da degistirilebilir
  sonuclari_kaydet() gecici olarak 'capture' adli yakalayici fonksiyona atanir
  Strateji calisirken kendi capture'i cagiriyor saniyor
  Portfolio objesi RAM'de yakalaniyor, diske hicbir sey yazilmiyor
  Islem bitince orijinal fonksiyon geri yukleniyor
run_in_executor: CPU-yogun backtest hesaplamasi async event loop'u bloklamalidir
  asyncio.get_event_loop().run_in_executor() ile thread pool'a offload
resolve_module_name() fonksiyonu:
  Excel'deki strateji klasor adi: rsi_14_30_70 (parametre iceriyor)
  Python modul adi: rsi (parametre yok, yalnizca fonksiyon adi)
  En uzun prefix eslesme algoritmasi: rsi_14_30_70 → rsi modulu bulunur

**Kullanilan Araclar:** Python, FastAPI, asyncio, concurrent.futures

**GORSEL:** Sekil 14: run_strategy_and_get_portfoy fonksiyonu kodu — monkey-patching satirlari gozukulur

**Ogrenilen:** Monkey-patching nedir ve Python'da nasil calisir. Async/await ve thread pool. CPU-bound vs IO-bound islemler. En uzun prefix esleme algoritmasi.

**Sorun / Cozum:** Global state race condition riski (cok kullanicili senaryoda): tek kullanicili yerel kullanim icin kabul edilebilir, uretim icin thread-local storage gerekirdi.

---

### GUN 15 — React Frontend Kurulumu ve Veri Entegrasyonu
**HAFTALIK TABLO GIRISI:** React Frontend Kurulumu ve Veri Entegrasyonu | 8 saat

**YAZILACAKLAR:**
Vite + React 19 ile frontend projesi olusturulmasi
TanStack Virtual (@tanstack/react-virtual) kurulumu
Backend'den veri cekme: fetch('/api/metrics') → JSON
React state yonetimi: useState ile tablo verisi, filter state
useEffect ile sayfa yuklendiginde veri cekme
TanStack Virtual'in useVirtualizer hook'u ile temel virtual scroll
Ilk calisan prototip: 8.370 satir tablo, sorunsuz scroll
Performans karsilastirmasi:
  Normal tablo (DOM'da 8370 satir): sayfa donuyor, ~5 saniye render
  Virtual scroll: anlik render, hicbir gecikme yok
filter fonksiyonu: filteredData = data.filter(row => kosullar)
Her filter degisikliginde virtualizer yeniden hesaplaniyor

**Kullanilan Araclar:** React 19, Vite, Node.js, npm, TanStack Virtual

**GORSEL:** Sekil 15: FastAPI api/metrics endpoint JSON ciktisi tarayicida

**Ogrenilen:** React component lifecyle. useState ve useEffect hook'lari. fetch API kullanimi. Virtual DOM ve Virtual Scroll arasindaki fark. Render performansi optimizasyonu.

**Sorun / Cozum:** CORS hatasi ilk denemede → FastAPI'de allow_origins=['*'] ayari eklendi.

---

### GUN 16 — Virtual Scroll ve HTML Table Hizalama Krizinin Cozumu
**HAFTALIK TABLO GIRISI:** Virtual Scroll ve HTML Table Hizalama Krizinin Cozumu | 8 saat

**YAZILACAKLAR:**
Kritik bug kesfedildi: HTML table + virtual scroll → basliklar ile degerler hizasiz
Sorunun koku (teknik): HTML table'in sutun genisligi algoritmas nasil calisir?
  Browser, td iceriklerine bakarak sutun genisliklerini otomatik hesaplar
  Ancak virtual scroll ile satirlar position:absolute ile yerlestirilir
  Bu satirlar tablo duzeninin sutun genisligi algoritmasindan kopar
  Sonuc: basliklar ile deger hucrleleri farkli genisliklerde gorunuyor
Cozum: HTML table tamamen terk edildi → CSS Grid tabanli div yapisi
  getColWidth() fonksiyonu: her sutun icin sabit pixel genisligi
  Header ve her satir ayni gridTemplateColumns CSS Grid sablonunu kullaniyor
  Header ve body ayni scroll container icinde
  Yatay kaydirmada da hizalama saglamligi korunuyor
  Bu yapiyla baslik ve deger hucrelerinin kayması MIMARI OLARAK IMKANSIZ
overscan parametresi: virtualizer'in ekranda gorunmeyenleri de hesaplamasi
  overscan=15 ile kaydirma sirasinda beyaz bosluk olusmuyor

**Kullanilan Araclar:** React, CSS Grid, TanStack Virtual, JavaScript

**GORSEL:** Sekil 16: Ilk React frontend prototip ekran goruntusu (basliklar ve veriler duzgun hizali)

**Ogrenilen:** CSS Grid vs HTML Table fark ve ne zaman hangisini kullanmali. Browser rendering ve layout algoritmalari. Virtual scroll'un DOM limitasyonlari. overscan optimizasyonu.

**Sorun / Cozum:** position:absolute ile table sutun hizalama uyumsuzlugu → tam mimari degisiklik zorunlu oldu.

---

### GUN 17 — Excel-Like Filtre Sidebar Gelistirmesi
**HAFTALIK TABLO GIRISI:** Excel-Like Filtre Sidebar Gelistirmesi | 8 saat

**YAZILACAKLAR:**
Ilk basit min/max input tasariminin yetersizligi:
  Kullanici tabloya bakarken filtreyi degistirmek zor
  Birden fazla kosul ayni anda uygulanamıyor
Yeni tasarim: Sol sidebar, accordion panel yapisi
Sayisal sutunlar icin filtre:
  Operator dropdown: > >= < <= = secenekleri
  Deger input alani
  'Kosul Ekle' butonu: birden fazla kosul ayni sutuna uygulanabilir
  Ornek: Sharpe > 1.5 VE Sharpe < 5.0
String sutunlar icin filtre:
  O sutundaki benzersiz degerlerin checkbox listesi
  'Tumumuzu Sec' ve 'Temizle' kisayollari
Aktif filtre gostergeleri:
  Aktif filtresi olan accordion panelde mavi nokta ve kenarlik
  Filtre sayisi badge olarak gosterilir
filteredData hesaplama: tum filtreler AND mantigi ile birlestirilir
Active filter count: filtrelerin kac tanesi aktif, ust kisimda gosterilir

**Kullanilan Araclar:** React, CSS, useState, useMemo

**GORSEL:** Sekil 17: Dashboard sol sidebar filtre panelinin tam ekran goruntusu

**Ogrenilen:** React controlled components. Accordion UI pattern. Kullanici deneyimi (UX) tasarimi. useMemo ile filtreleme performans optimizasyonu.

**Sorun / Cozum:** Cok sayida filtre degistiginde performans dusumu → useMemo ile filteredData memoization.

---

### GUN 18 — Canli Grafik Paneli iframe Entegrasyonu ve Excel Export
**HAFTALIK TABLO GIRISI:** Canli Grafik Paneli iframe Entegrasyonu ve Excel Export | 8 saat

**YAZILACAKLAR:**
Canli grafik paneli implementasyonu:
  Tabloda bir satira tiklandiginda backend'e /api/chart/html/{hisse}/{strateji} istegi
  Backend stratejiyi calistiriyor (monkey-patching ile), Plotly HTML donduruyor
  Frontend: <iframe srcDoc={chartHtml}> ile HTML React icine gomuldu
  Sonuc: tam interaktif Plotly grafigi sag panelde
HTML indirme (Blob): grafigin interaktif HTML versiyonu indiriliyor
PNG indirme: /api/chart/png/ endpoint'i, kaleido ile 1400x900 statik gorsel
Frontend Excel Export implementasyonu:
  xlsx kutuphanesi ile filtrelenmis verinin tamami indiriliyor
  Yalnizca ekranda goruntulenen 20 satir degil, TUM filtrelenmis veri
  Backend'e hicbir istek gitmez → sunucu yuku sifir
  Dosya adi: BIST_YYYY-MM-DD.xlsx formatinda otomatik tarih
Son dashboard ozellikleri:
  Sol: Excel-like filtre sidebar
  Orta: Virtual scroll tablosu (8.370 satir)
  Sag: Canli grafik paneli (HTML iframe)
  Ust: Excel indirme ve grafik indirme butonlari

**Kullanilan Araclar:** React, iframe, xlsx kutuphanesi, FastAPI, kaleido

**GORSEL:** Sekil 18: Dashboard sol sidebar filtre paneli tam ekran goruntusu

**Ogrenilen:** iframe sandbox guvenligi. srcDoc ile HTML gomme. Blob API ile dosya indirme. xlsx kutuphanesiyle frontend Excel uretimi.

**Sorun / Cozum:** iframe'deki Plotly grafiklerinde dark mode uyumsuzlugu → color-scheme:dark CSS eklendi.

---

### GUN 19 — Sistem Testleri Dashboard Polisleme ve Hata Duzeltme
**HAFTALIK TABLO GIRISI:** Sistem Testleri Dashboard Polisleme ve Hata Duzeltme | 8 saat

**YAZILACAKLAR:**
Backend + frontend entegrasyon testleri
Kesfedilen hatalar ve cozumleri:
  resolve_module_name() hatasi:
    rsi_14_30_70 → Python modul rsi eslemesi basarisiz oluyordu
    Cozum: strategies/ klasorunun tum .py dosyalarini tara, en uzun prefix bul
  Select dropdown arka plan beyaz gorundugu icin koyu temada secenek gorunmuyor
    Cozum: background-color ve color CSS ile sabit renk atamasi
  Grafik paneli yuksekligi sabit kaliyordu → CSS flex ile dinamik yukseklik
Performans testleri:
  8.370 satir: DOM render <100ms (virtual scroll sayesinde)
  Grafik uretimi: ortalama 3-5 saniye (backtest hesaplama suresi)
  Excel export: ~500ms (frontend, backend degil)
  API response time: /api/metrics icin ~200ms
Dashboard'un son hali ozellikleri:
  Sayisal filtreler: operator + deger, birden fazla kosul
  String filtreler: checkbox listesi
  Virtual scroll: 8.370 satir sorunsuz
  Canli grafik: tikla-goster
  HTML ve PNG indirme
  Filtrelenmis Excel export

**Kullanilan Araclar:** Browser DevTools, FastAPI logs, React DevTools

**GORSEL:** Sekil 19: Dashboard tam ekran goruntusu — tum paneller acik halde (filtre + tablo + grafik)

**Ogrenilen:** Entegrasyon testlerinin onemi. Browser DevTools ile network ve performans analizi. CSS z-index ve stacking context. Hata ayiklamada sistematik yaklasim.

**Sorun / Cozum:** Grafik paneli bos geliyor bazi stratejilerde → 0 islem stratejileri icin bos grafik yerine bilgi mesaji eklendi.

---

### GUN 20 — Genel Bulgular Alfa Analizi ve Staj Sonu Degerlendirme
**HAFTALIK TABLO GIRISI:** Genel Bulgular Alfa Analizi ve Staj Sonu Degerlendirme | 8 saat

**YAZILACAKLAR:**
5.670 kombinasyonun genel istatistikleri:
  Toplam analizler: 8.370 satir
  Istatistiksel Guvenilir (+): [yuzde X]
  Overfitting Suphesi (|): [yuzde Y]
  Istatistiksel Yetersiz (-): [yuzde Z]
Alfa analizi: piyasayi yenme
  Al-tut getirisi >= Strateji getirisi olan kombinasyonlar: hisseyi almak daha iyiydi
  Pozitif alfa ureten strateji kategorileri: [analiz sonucuna gore doldur]
  En tutarli alpha ureten strateji: [analiz sonucuna gore]
En basarili strateji kategorileri ve BIST'e ozgun bulgular:
  Momentum stratejileri: BIST'in 2021-2022 ve 2024 bull market donemlerinde iyi
  Reversal/mean-reversion: yuksek volatilite donemlerinde daha etkili
  Hacim stratejileri: BIST'te zayif — likidite ve hacim guvenilirligi sorunu
Projenin guclu yonleri:
  18 kat buyume: 5 → 90 strateji
  Moduler, genisletilebilir mimari (yeni strateji = yeni dosya)
  Tutarli ekonomi (ayni komisyon/slipaj tum stratejilerde)
  Lookahead bias cozumu (.shift(1))
  Akademik gecerlilik etiketi sistemi
  Web dashboard: 8.370 satir anlık filtrelenebiliyor
Projenin sinirlamalari (donust degerlendirme):
  Out-of-sample test yok → gercek performans bilinmiyor
  Walk-forward analizi yok
  Bonferroni duzeltmesi uygulanmadi
  Survivorship bias (halen BIST'te olan hisseler test edildi)
Gelecek calisma plani:
  Akademik makale: Out-of-sample validation ile overfitting saptama
  Temsili hisse secimi: 5 sektor x 1-2 hisse
  Piyasa rejimi analizi (2020-21 / 2022 / 2023 / 2024-25)
20 gunluk staj surecinde kazanilan deneyim:
  Python ile buyuk olcekli veri isleme
  vectorbt ile algoritmik backtest
  FastAPI + React ile full-stack web gelistirme
  Moduler yazilim mimarisi tasarimi
  Finansal kavramlar: 90 teknik analiz stratejisi, Sharpe, Alpha, Drawdown

**Kullanilan Araclar:** pandas, Master Excel, Dashboard

**GORSEL:** Sekil 20: Kategori bazli Alfa/getiri dagilimi tablosu veya dashboard final ekran

**Ogrenilen:** 20 gunluk surec icinde bir backtesting sisteminin sifirdan nasil insa edildigini. Algoritma tasariminda muhendislik prensiplerinin uygulanmasini. Finansal metrik yorumlamasini. Akademik metodoloji duzeyinde overfitting ve bias kavramlarini.

**Sorun / Cozum:** Proje boyunca karsilasilan en buyuk metodolojik sorun: out-of-sample test olmaksizin sonuclarin ne kadar guvenilebilir oldugunu belirlemek. Bu, akademik calismada cozulmesi gereken temel soru olarak not edildi.

---

## BOLUM E — HAFTALIK OZET TABLOLAR (Word'e Aktarilacak Hali)

### Hafta 1 (Gun 1-5)
| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Proje Tanitimi, Ortam Kurulumu, Ilk Veri Analizi | 2 | 8 |
| Sali | BIST Veri Mimarisi ve Ilk Backtest Denemeleri | 3 | 8 |
| Carsamba | Moduler Mimari: main.py ve strategies/ Klasoru | 4 | 8 |
| Persembe | Dinamik importlib Sistemi ve ATR Tabanli Stratejiler | 5 | 8 |
| Cuma | Buyuk Olcek Backtest ve Smart Skip Sistemi | 6 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 2 (Gun 6-10)
| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | RSI MACD Momentum ve Mum Formasyonu Stratejileri | 7 | 8 |
| Sali | Hacim Analizi Stratejileri: OBV CMF VPT AD-Line | 8 | 8 |
| Carsamba | Istatistiksel ve Ileri Momentum Stratejileri | 9 | 8 |
| Persembe | 90 Strateji Kutuphanesi Tamamlandi | 10 | 8 |
| Cuma | Coppock Isinma Sorunu ve 5 Yillik Veriye Gecis | 11 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 3 (Gun 11-15)
| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Master Rapor: 8.370 Satirlik Analiz ve Yeni Metrikler | 12 | 8 |
| Sali | Anomali Analizi: Overfitting Etiketi ve Alfa Metrigi | 13 | 8 |
| Carsamba | Dashboard Mimari Tasarimi ve FastAPI Backend Kurulumu | 14 | 8 |
| Persembe | Monkey-Patching ile RAM Portfoy Yakalama | 15 | 8 |
| Cuma | React Frontend Kurulumu ve Veri Entegrasyonu | 16 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

### Hafta 4 (Gun 16-20)
| Gun | Yapilan Isler | Sayfa No | Saat |
|---|---|---|---|
| Pazartesi | Virtual Scroll ve HTML Table Hizalama Krizinin Cozumu | 17 | 8 |
| Sali | Excel-Like Filtre Sidebar Gelistirmesi | 18 | 8 |
| Carsamba | Canli Grafik Paneli iframe Entegrasyonu ve Excel Export | 19 | 8 |
| Persembe | Sistem Testleri Dashboard Polisleme ve Hata Duzeltme | 20 | 8 |
| Cuma | Genel Bulgular Alfa Analizi ve Staj Sonu Degerlendirme | 21 | 8 |
| Cumartesi | (Calisilmadi) | - | - |
| Denetcinin Imzasi | [Islak imza] | Toplam Saat | 40 |

---

## BOLUM F — WORD'E AKTARMA KONTROL LISTESI

- [ ] Kapak tablosu dolduruldu (ogrenci bilgileri + sorumlu muhendis)
- [ ] Komisyon onay tablosu bos birakildi (komisyon dolduracak)
- [ ] Icerikler sayfasi tum gunlerle dolduruldu + sayfa numaralari
- [ ] Sekil, Cizelge ve Ekler Listesi tum 20 gorsel ile dolduruldu
- [ ] Kurum Tanitimi bolumu paragraf formatinda yazildi
- [ ] Giris bolumu paragraf formatinda yazildi
- [ ] Hafta 1-4 ozet tablolari dolduruldu (4 haftalik tablo = 20 gun)
- [ ] Her gunun sayfasinin USTUNDE Sayfa No yazili
- [ ] Her gunun sayfasinin ALTINDA tarih yazili
- [ ] Her sayfada sorumlu muhendis islak imzasi var
- [ ] Tum gorseller 6cm yuksekliginde
- [ ] Gorseller: Sekil X. [Aciklama] — gorselin ALTINDA
- [ ] Tablolar: Tablo X. [Aciklama] — tablonun USTUNDE
- [ ] Times New Roman 11pt, iki yana yasli
- [ ] Her sayfa tek yuz (arkali onlu degil)
- [ ] Her sayfanin en az yarisi dolu

---

## BOLUM G — ONCELIKLI GORSELLER (Mutlaka Hazirlanmali)

1. Dashboard tam ekran — tum paneller acik (Sekil 19)
2. Master Excel 8.370 satir goruntusu (Sekil 11)
3. strategies/ 90 dosya listesi (Sekil 9)
4. Terminal backtest ciktisi (Sekil 5)
5. Dashboard sol sidebar filtre paneli (Sekil 18)
6. Monkey-patching kodu (Sekil 14)

Ekran goruntusu alma: Windows + Shift + S ile bolge sec
PNG indirme: dashboard uzerinden /api/chart/png/ endpoint'inden indir

---
Hazirlayan: Antigravity AI — 15 Eylul 2026
20 Is Gunu / 4 Hafta