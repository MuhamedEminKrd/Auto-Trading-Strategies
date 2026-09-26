<div align="center">

# 📈 AutoTradingStrategies: BIST Algorithmic Trading, Quantitative Backtest Engine & Terminal

**Borsa İstanbul (BIST) İçin 90 Strateji ve 93 Hisse Senedi Üzerinde Çok Çekirdekli, Vektörize Out-of-Sample Backtest Motoru, Ekonometrik Analiz Altyapısı ve İnteraktif Web Terminali**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![VectorBT](https://img.shields.io/badge/VectorBT-High--Speed%20Matrix-000000?style=for-the-badge)](https://vectorbt.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <a href="#-sistemin-amacı-ve-felsefesi">Proje Amacı</a> •
  <a href="#-temel-ampirik-bulgular-ve-akademik-çıktılar">Ampirik Bulgular</a> •
  <a href="#-sistem-mimarisi-ve-çalışma-mekanizması">Sistem Mimarisi</a> •
  <a href="#-90-strateji-ve-8-kategori-havuzu">Strateji Havuzu</a> •
  <a href="#-proje-klasör-yapısı">Klasör Hiyerarşisi</a> •
  <a href="#-kurulum-ve-çalıştırma-quickstart">Hızlı Başlangıç</a>
</p>

</div>

---

## 📌 İçindekiler
1. [Sistemin Amacı ve Felsefesi](#-sistemin-amacı-ve-felsefesi)
2. [Temel Ampirik Bulgular ve Akademik Çıktılar](#-temel-ampirik-bulgular-ve-akademik-çıktılar)
3. [Sistem Mimarisi ve Çalışma Mekanizması](#-sistem-mimarisi-ve-çalışma-mekanizması)
4. [90 Strateji ve 8 Kategori Havuzu](#-90-strateji-ve-8-kategori-havuzu)
5. [Akademik Metodoloji: In-Sample / Out-of-Sample Ayrımı](#-akademik-metodoloji-in-sample--out-of-sample-ayrımı)
6. [Web Dashboard (Finansal Veri Terminali)](#-web-dashboard-finansal-veri-terminali)
7. [Proje Klasör Yapısı](#-proje-klasör-yapısı)
8. [Kurulum ve Çalıştırma (Quickstart)](#-kurulum-ve-çalıştırma-quickstart)

---

## 🎯 Sistemin Amacı ve Felsefesi

Geleneksel finansal piyasa analizleri çoğunlukla sezgilere, öznel teknik analiz yorumlarına veya insan zihninin kısıtlı geriye dönük test kabiliyetine dayanır. Bu durum, piyasa anomalilerinin test edilmesinde **aşırı uyum (overfitting)**, **veri gözetimi (data-snooping)** ve **geleceği görme (look-ahead bias)** gibi metodolojik yanılgıları beraberinde getirir.

**AutoTradingStrategies projesinin temel amacı:**
İnsan duygularını ve bilişsel yanılgıları tamamen devre dışı bırakarak; Borsa İstanbul pay piyasasında (BIST100) işlem gören **93 hisse senedi** üzerinde **8 farklı disipline ait 90 bağımsız ticaret kuralını**, titiz bir **%70 Eğitim (In-Sample) / %30 Test (Out-of-Sample)** metodolojisiyle ve kurumsal piyasa sürtünmelerini (komisyon + slippage) hesaba katarak simüle etmektir. 

Toplam **8.370 hisse-strateji kombinasyonunun** her birini bağımsız birer gözlem birimi olarak ele alan sistem; **Etkin Piyasa Hipotezi (Fama, 1970)**, **Veri Gözetimi (Sullivan vd., 1999)** ve **Çoklu Karşılaştırma / p-hacking (Harvey vd., 2016)** zemininde ampirik ve ekonometrik olarak test eder.

---

## 🏆 Temel Ampirik Bulgular ve Akademik Çıktılar

Araştırma sonucunda elde edilen ve projeyle birlikte teslim edilen hakemli akademik makalede (`Tam_Akademik_Makale_v2_Revize.docx`) detaylandırılan 3 temel bulgu:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   8.370 HİSSE-STRATEJİ ÇİFTİ ANALİZ ÖZETİ                │
├──────────────────────────┬──────────────────────────┬────────────────────┤
│ Metrik                   │ Değer                    │ Akademik Anlam     │
├──────────────────────────┼──────────────────────────┼────────────────────┤
│ Piyasayı Yenen Çiftler   │ 4.252 Çift (%50,8)       │ Out-of-Sample Alfa │
│ Kesintisiz Tutarlı Alfa  │ 1.394 Çift (%16,7)       │ Train & Test > 0   │
│ Kaliteli / Üst Çiftler   │ 742 Çift (%8,9)          │ Alfa > 0, Sharpe >0│
│ Agrege Strateji Alfası   │ p > 0,05 (Anlamsız)      │ EMH Doğrulaması    │
└──────────────────────────┴──────────────────────────┴────────────────────┘
```

1. **Evrensel Değil, Bağlamsal Başarı:** Tüm piyasada ortalama olarak çalıştırılan hiçbir strateji istatistiksel olarak anlamlı alfa üretememektedir ($p > 0,05$). Bu durum **Etkin Piyasa Hipotezi'nin yarı-güçlü formunu** teyit etmektedir. Ancak hisse-strateji çifti bazında bakıldığında çiftlerin **%50,8'i piyasa endeksini geride bırakmış**, **%16,7'si ise kesintisiz alfa** üretmiştir.
2. **Sektör-Strateji Uyumunun Gücü:** 
   * **Bankacılık** hisselerinde *Hareketli Ortalama* kategorisi (+%21,1 ortalama alfa),
   * **Tekstil** hisselerinde *Hacim* tabanlı stratejiler (+%57,1 ortalama alfa),
   * **Elektronik ve Otomotiv** sektörlerinde *Mum Formasyonları* (+%24,2 ve +%16,6 alfa),
   * **Madencilik** sektöründe *Trend Takip* modelleri (+%14,7 alfa) en güçlü performansı sergilemiştir.
3. **Zirvedeki Eşleşmeler:** Out-of-sample test döneminde **Şekerbank (SKBNK) + TEMA_20** eşleşmesi **+%251,8 alfa** ve **3,01 Sharpe oranı** ile tüm veri setinin en yüksek kalite skorunu elde etmiştir.

---

## 🏗️ Sistem Mimarisi ve Çalışma Mekanizması

Proje, birbirine gevşek bağlı (loosely coupled), yüksek performanslı **4 katmanlı kurumsal mimari** üzerinde çalışır:

```
                                    ┌────────────────────────┐
                                    │  Yahoo Finance API     │
                                    └───────────┬────────────┘
                                                │ OHLCV Verisi
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ KATMAN 1: VERİ TOPLAMA VE ÖNİŞLEME (data_fetcher.py)                                   │
│ • 93 BIST hissesi için 5 yıllık günlük veri (2021-2026)                                │
│ • auto_adjust=True ile geriye dönük temettü ve bedelli/bedelsiz bölünme düzeltmesi      │
│ • Akıllı Güncelleme: Yalnızca eksik günleri çekip diske ekleyen akıllı önbellek        │
└───────────────────────────────────────┬────────────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ KATMAN 2: 90 STRATEJİLİK ALGORİTMA HAVUZU (vbt_bist/strategies/)                       │
│ • 8 Kategori: Trend, Momentum, Volatilite, Hacim, Mum, MA, Ortalamaya Dönüş, Hibrit   │
│ • Merkezi Portföy Yönetimi (utils.py): %0,1 komisyon, %0,2 kayma payı (slippage)       │
│ • Bağımsız fonksiyon imzaları ve Dependency Injection (kapanis, hacim, yuksek, vb.)   │
└───────────────────────────────────────┬────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
┌───────────────────────────────────────┐   ┌────────────────────────────────────────────┐
│ KATMAN 3A: GENEL PARALEL MOTOR        │   │ KATMAN 3B: AKADEMİK OUT-OF-SAMPLE MOTORU   │
│ (vbt_bist/main.py)                    │   │ (vbt_bist/academic/)                       │
│ • ProcessPoolExecutor (12 Çekirdek)   │   │ • train_test_backtest.py: %70 / %30 Split  │
│ • 93 Hisse x 90 Strateji Paralel Koşu │   │ • pair_analysis.py: 8.370 Çift Analizi     │
│ • Smart Skip: Güncel olanı atla       │   │ • statistical_tests.py: t-test & Wilcoxon  │
│ • master_rapor_olustur.py: Master XLS │   │ • paper_charts.py: 300 DPI Makale Grafiği  │
└───────────────────┬───────────────────┘   └─────────────────────┬──────────────────────┘
                    │                                             │
                    └───────────────────┬─────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ KATMAN 4: SUNUM VE KULLANICI ARAYÜZÜ                                                   │
│ • FastAPI Backend (dashboard/backend/main.py): RESTful API, asenkron metrik servisi    │
│ • React + Vite Frontend (dashboard/frontend/): TanStack Virtual DOM, canlı Plotly      │
│ • Akademik Doküman: Tam_Akademik_Makale_v2_Revize.docx (APA 7, 7 Tablo, 6 Şekil)       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 90 Strateji ve 8 Kategori Havuzu

Sistemde uygulanan 90 strateji, finansal teknik analizin 8 temel alt disiplinini eksiksiz kapsayacak biçimde sınıflandırılmıştır:

| No | Kategori Adı | Strateji Sayısı | Temsili Stratejiler ve Finansal Göstergeler |
|:--:|:---|:---:|:---|
| **1** | **Trend Takip** | **26** | EMA Kesişim (8/21), Süpertrend, Ichimoku Kinko Hyo, ADX, Parabolic SAR, Aroon, DMI, TRIX, Chandelier Exit, Schaff Trend Cycle, Triple Screen |
| **2** | **Volatilite** | **15** | Bollinger Bantları, Keltner Kanalları, ATR Kırılımı, Donchian Kanalları, Chaikin Volatilitesi, Standart Sapma Kanalı, Squeeze Momentum |
| **3** | **Momentum** | **15** | RSI (14, 30/70), MACD (12/26/9), Stokastik, Williams %R, CCI, ROC, Ultimate Osilatör, TSI, Awesome Osilatör (AO), Connors RSI, RSI Uyumsuzluk |
| **4** | **Hacim** | **13** | On-Balance Volume (OBV), VWAP, Para Akışı Endeksi (MFI), Klinger Osilatör, Chaikin Para Akışı (CMF), VWMA, Hacim Fiyat Trendi (VPT), NVI, PVI |
| **5** | **Mum Formasyonu** | **8** | Doji Dönüşü, Yutan Ayı/Boğa (Engulfing), Çekiç (Hammer), Asılı Adam, Marubozu, Sabah Yıldızı, Üç Beyaz Asker, İç Bar (Inside Bar) |
| **6** | **Hareketli Ortalama** | **6** | Çift Üstel MA (DEMA), Üçlü Üstel MA (TEMA), ALMA, Hull MA (HMA), Sıfır Gecikmeli MA (ZLEMA), Üçlü Hareketli Ortalama (5/20/50) |
| **7** | **Diğer / Hibrit** | **4** | Hodrick-Prescott (HP) Filtresi, Çizgisel Regresyon Eğimi, Fraktal Kırılım, Stokastik RSI |
| **8** | **Ortalamaya Dönüş** | **3** | Fiyat Z-Skoru, İç Bar Gücü (IBS), Basit Ortalamaya Dönüş Kanalı |
| — | **TOPLAM** | **90** | **8 Bağımsız Finansal Disiplin (93 Hisse ile 8.370 Kombinasyon)** |

---

## 🔬 Akademik Metodoloji: In-Sample / Out-of-Sample Ayrımı

Sistemin en ayırt edici akademik gücü, **geriye dönük testlerde yapılan aşırı uyumu (overfitting)** metodolojik olarak engellemesidir:

1. **Zaman Serisi Bölünmesi (%70 / %30):**
   * Her hissenin fiyat serisi kronolojik olarak ilk `%70` (In-Sample / Eğitim) ve son `%30` (Out-of-Sample / Test) olarak ayrılmıştır.
   * Stratejiler eğitim döneminde değerlendirilmiş, test döneminde ise **daha önce hiç görmedikleri** piyasa rejiminde teste tabi tutulmuştur.
2. **Piyasa Sürtünmeleri (İşlem Maliyetleri):**
   * Her işlem için **%0,1 komisyon** ve **%0,2 kayma payı (slippage)** peşinen düşülmüştür.
3. **Zaman Kaydırma (Shift - Lookahead Bias Önlemi):**
   * Sinyal $t$ gününün kapanışında üretilir; emir simülasyonu $t+1$ gününün fiyatından gerçekleştirilir.
4. **İstatistiksel Doğrulama:**
   * Tek örneklem $t$-testi ($H_0: \mu_{\alpha} = 0$),
   * İki örneklem eşleştirilmiş $t$-testi (Train vs. Test karşılaştırması),
   * Parametrik olmayan Wilcoxon işaretli sıralar testi,
   * Aşırı Uyum Skoru: $OS = \frac{R_{train} - R_{test}}{|R_{train}|} \times 100$.

---

## 💻 Web Dashboard (Finansal Veri Terminali)

Sonuçları statik tablolardan kurtarmak amacıyla modern bir finansal terminal geliştirilmiştir:

* **Hızlı REST API (FastAPI):** Python tabanlı asenkron backend; 8.370 satırlık analiz sonuçlarını, metrik özetlerini ve strateji grafiklerini milisaniyeler içinde sunar.
* **Sanal DOM (React + Vite + TanStack Virtual):** 8.000'den fazla satırı tarayıcı belleğini şişirmeden 60 FPS akıcılıkla görüntüler.
* **Dinamik Çoklu Filtreleme:** Tek tıkla `Sharpe > 1.5`, `Max Drawdown > -15%`, `Alfa > 20%` gibi karmaşık filtreler uygulanabilir.
* **İnteraktif Canlı Grafikler (Plotly):** Tıklanan herhangi bir hisse-strateji çiftinin al/sat sinyalleri ve sermaye büyüme eğrisi anında interaktif olarak çizilir.
* **Excel Dışa Aktarım (Export):** Filtrelenmiş tüm portföy listesi tek tıkla `.xlsx` formatında indirilebilir.

---

## 📁 Proje Klasör Yapısı

```bash
Auto_Trading_Strategies/
│
├── requirements.txt                   # Proje kök bağımlılıkları (tüm kütüphaneler)
├── README.md                          # Proje tanıtım ve dokümantasyon dosyası
├── .gitignore                         # Git hariç tutma kuralları (venv, node_modules vb.)
│
├── vbt_bist/                          # 🚀 ÇEKİRDEK BACKTEST MOTORU
│   ├── main.py                        # Çok çekirdekli (multiprocessing) ana yürütme scripti
│   ├── data_fetcher.py                # Yahoo Finance veri çekici ve akıllı güncelleyici
│   ├── master_rapor_olustur.py        # Tüm hisselerin sonuçlarını tek Excel'de toplayan modül
│   ├── requirements_vbt.txt           # vbt_bist modülü bağımlılıkları
│   │
│   ├── data/                          # 93 BIST hissesinin günlük OHLCV CSV verileri
│   │   ├── AKBNK.csv
│   │   ├── THYAO.csv
│   │   └── ... (93 hisse)
│   │
│   ├── strategies/                    # 💡 90 ADET BAĞIMSIZ STRATEJİ ALGORİTMASI
│   │   ├── utils.py                   # Merkezi portföy, komisyon, slippage ve kayıt motoru
│   │   ├── rsi.py                     # RSI (14, 30/70)
│   │   ├── supertrend.py              # SuperTrend
│   │   ├── ema_cross.py               # EMA Crossover
│   │   └── ... (90 dosya)
│   │
│   └── academic/                      # 🎓 AKADEMİK ANALİZ VE İSTATİSTİK MOTORU
│       ├── train_test_backtest.py     # %70 Eğitim / %30 Test split backtest yürütücüsü
│       ├── pair_analysis.py           # 8.370 hisse-strateji çifti kalite skorlayıcısı
│       ├── statistical_tests.py       # t-Testi, Wilcoxon ve overfitting test motoru
│       ├── paper_charts.py            # 300 DPI akademik makale grafik üreticisi
│       └── output/                    # Akademik Excel çıktıları ve makale figürleri
│           ├── TrainTest_Sonuclari.xlsx
│           ├── Cift_Bazli_Analiz.xlsx
│           ├── Anlamli_Ciftler.xlsx
│           ├── Sektor_Strateji_Haritasi.xlsx
│           ├── Hisse_En_Iyi_Strateji.xlsx
│           ├── Istatistik_Testleri.xlsx
│           └── figures/               # fig1'den fig6'ya yüksek çözünürlüklü grafikler
│
├── dashboard/                         # 🖥️ WEB DASHBOARD TERMINALİ
│   ├── backend/                       # FastAPI REST API servisi
│   │   └── main.py
│   └── frontend/                      # React.js + Vite arayüzü
│       ├── src/
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── package.json
│       └── vite.config.js
│
└── Staj_Raporlari/                    # 📄 STAJ, RAPOR VE NİHAİ MAKALE DOKÜMANLARI
    ├── Tam_Akademik_Makale_v2_Revize.docx  # APA 7 formatında tam akademik makale (Word)
    ├── Tam_Akademik_Makale_v2.md           # Makale Markdown metni
    └── ... (Sistem ve staj raporları)
```

---

## ⚡ Kurulum ve Çalıştırma (Quickstart)

### 1. Depoyu Klonlayın ve Sanal Ortam Kurun
```bash
git clone https://github.com/MuhamedEminKrd/Auto-Trading-Strategies.git
cd Auto-Trading-Strategies

# Python sanal ortamı oluşturun ve aktif edin
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Tüm kütüphaneleri yükleyin
pip install -r requirements.txt
```

### 2. Verileri İndirin veya Güncelleyin
```bash
python vbt_bist/data_fetcher.py
```

### 3. Çok Çekirdekli Backtest Motorunu Çalıştırın
Tüm hisseleri ve stratejileri 12 işlemci çekirdeğiyle paralel olarak simüle eder ve master raporu oluşturur:
```bash
python vbt_bist/main.py
```

### 4. Akademik Analiz ve İstatistik Motorunu Çalıştırın
```bash
# 1. In-Sample / Out-of-Sample Backtest:
python vbt_bist/academic/train_test_backtest.py

# 2. Çift Bazlı Performans ve Sektör Matrisi Analizi:
python vbt_bist/academic/pair_analysis.py

# 3. İstatistiksel Hipotez Testleri (t-Testi & Wilcoxon):
python vbt_bist/academic/statistical_tests.py

# 4. Makale Grafikleri Üretimi (300 DPI):
python vbt_bist/academic/paper_charts.py
```

### 5. Web Dashboard Terminalini Başlatın

**Terminal 1 (Backend - FastAPI):**
```bash
cd dashboard/backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend - React & Vite):**
```bash
cd dashboard/frontend
npm install
npm run dev
```
Tarayıcınızda `http://localhost:5173` adresine giderek terminali canlı olarak kullanabilirsiniz!

---


<div align="center">
  <sub>Bu çalışma bilimsel ve eğitim amaçlı geliştirilmiştir. Yatırım tavsiyesi (YTD) niteliği taşımaz.</sub>
</div>
