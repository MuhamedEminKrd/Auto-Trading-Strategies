<div align="center">
  <h1>📈 BIST Algorithmic Trading & Quantitative Dashboard</h1>
  <p><strong>A High-Performance Algorithmic Trading Engine and Dynamic Dashboard for Borsa Istanbul (BIST)</strong></p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/VectorBT-Black?style=for-the-badge" />
</div>

<br>

## 🚀 Proje Hakkında (Overview)

Bu proje, **Borsa İstanbul (BIST)** verileri üzerinde yüzlerce farklı teknik analiz, momentum ve fiyat aksiyonu (price action) stratejisini eşzamanlı olarak geriye dönük test (backtest) edebilen, yüksek hızlı bir kantitatif finans motorudur.

Geleneksel döngü tabanlı (for-loop) sistemlerin aksine **VectorBT, Pandas ve NumPy** mimarisi kullanılarak vektörel (matrisel) hesaplamalar yapılır. Bu sayede **90 farklı algoritmik strateji modeli** kullanılarak üretilen toplam **8.370 adet backtest senaryosu** saniyeler içinde işlenir ve modern bir arayüz ile görselleştirilir.

---

## ✨ Temel Özellikler (Key Features)

- 🧠 **90+ Algoritmik Strateji:** RSI, MACD, Bollinger Bands, Williams %R, Supertrend, Ichimoku, Chandelier Exit, Connors RSI, Candlestick formasyonları ve daha fazlası.
- ⚡ **Vektörize Backtest Motoru:** Geleneksel sistemlerden 100x ile 1000x kat daha hızlı veri işleme kapasitesi.
- 📊 **Profesyonel Veri Terminali (UI):** React.js (Vite) ile kodlanmış, **Dark Mode** ve **Glassmorphism** tasarım diline sahip Bloomberg/Eikon kalitesinde kullanıcı arayüzü.
- 🎯 **Akademik İstatistik Filtreleri:** Stratejilerin güvenilirliğini ölçen *Sharpe Ratio, Sortino, Calmar, Profit Factor, Alpha (Piyasayı Yenme)* ve örneklem büyüklüğü (N > 25) üzerinden overfitting (aşırı uyum) testleri.
- 📈 **Sıfır Gecikmeli Canlı Grafikler:** Backend'de (FastAPI) çalışan anlık *Monkey-Patching* mimarisi sayesinde, hiçbir dosyaya I/O maliyeti bindirmeden tıklanılan stratejinin portföy grafiği anında tarayıcıya (Plotly ile) render edilir.
- 💾 **Büyük Veri Optimizasyonu:** DOM Sanallaştırma (TanStack Virtual) ile 8 binden fazla satır, bilgisayarı yormadan (sıfır lag) anında kaydırılır ve filtrelenir.

---

## 🏗️ Mimari Yapı (Architecture)

Proje 3 temel bileşenden oluşmaktadır:

1. **`vbt_bist/` (Algoritma & Veri Motoru)**
   - `strategies/`: İçerisinde bağımsız Python `.py` dosyaları olarak tasarlanmış 90 adet strateji.
   - `master_rapor_olustur.py`: Yüzlerce stratejinin sonucunu akademik eşiklerle tarayarak ana Excel veri setini oluşturur.

2. **`dashboard/backend/` (FastAPI Sunucusu)**
   - Algoritma motorunu UI ile birleştiren RESTful API katmanı.
   - Dinamik strateji çalıştırma ve Plotly grafik üretimi.

3. **`dashboard/frontend/` (React.js Arayüzü)**
   - `App.jsx` & `index.css`: Kullanıcı etkileşimini sağlayan, canlı sütun filtrelemeleri (>, <, =, Min/Max) ve XLSX ihracatı (Export) yapabilen son kullanıcı arayüzü.

---

## 🛠️ Kurulum ve Çalıştırma (Installation & Run)

### 1. Gereksinimleri Yükleyin
Proje dizininde gerekli kütüphaneleri yükleyin:
```bash
# Python kütüphaneleri
pip install pandas numpy vectorbt fastapi uvicorn openpyxl plotly

# Frontend kütüphaneleri
cd dashboard/frontend
npm install
```

### 2. Uygulamayı Başlatın
Uygulamayı tam kapasiteyle test etmek için iki ayrı terminal sekmesi açmalısınız:

**Terminal 1 (Backend - FastAPI):**
```bash
cd dashboard/backend
uvicorn main:app --reload
```

**Terminal 2 (Frontend - React):**
```bash
cd dashboard/frontend
npm run dev
```

Tarayıcınızdan `http://localhost:5173` adresine giderek Dashboard'a erişebilirsiniz!

---

## 🎓 Metrikler ve Akademik Geçerlilik
Bu sistemde stratejiler sadece kâr/zarara göre değil, 5 yıllık istatistiksel geçerliliğe göre ölçülür:
- **N < 25:** İşlem sayısı çok az, başarı muhtemelen tesadüfi.
- **PF > 10:** Strateji geçmiş veriyi ezberlemiş (Overfitting/Curve-fitting).
- **Alfa (α):** Stratejinin basitçe *"Hisse alıp hiç dokunmadan bekleme (Buy & Hold)"* senaryosunu yenip yenemediğinin kanıtı.

---
<div align="center">
  <i>Bu proje, Borsa İstanbul (BIST) üzerinde kantitatif araştırmalar ve algoritmik ticaret optimizasyonu için geliştirilmiştir.</i>
</div>
