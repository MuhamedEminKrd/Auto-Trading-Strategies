<div align="center">
  <h1>📈 BIST Algorithmic Trading & Quantitative Dashboard</h1>
  <p><strong>Borsa İstanbul (BIST) İçin Geliştirilmiş, Vektörize Tabanlı Yüksek Hızlı Backtest Motoru ve Kantitatif Veri Terminali</strong></p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/VectorBT-Black?style=for-the-badge" />
</div>

<br>

## 🎯 Sistemin Amacı
Geleneksel yatırım kararları genellikle duygulara, spekülasyonlara veya insan beyninin kısıtlı analiz yeteneğine dayanır. Bu projenin temel amacı; insan faktörünü ve duyguları tamamen devreden çıkararak, yatırım kararlarını **matematiksel olarak kanıtlanmış, geriye dönük testleri (backtest) yapılmış istatistiksel verilere** dayandırmaktır. 

Sistem, Borsa İstanbul'daki (BIST) tüm hisse senetleri üzerinde yüzlerce farklı algoritmik stratejiyi insanüstü bir hızda test ederek, "Hangi hissede, hangi strateji, hangi parametrelerle en yüksek başarıyı sağlar?" sorusuna kesin ve analitik cevaplar üretir.

## ⚙️ Sistemde Ne Yapıldı?
Finansal piyasalarda yaygın olarak kullanılan RSI, MACD, Bollinger Bantları, Ichimoku, Supertrend gibi indikatörlerin yanı sıra karmaşık fiyat aksiyonu (price action) ve mum formasyonlarını içeren **90 adet bağımsız strateji algoritması** kodlandı. 

Bu stratejiler, BIST hisselerinin son 5 yıllık fiyat hareketleri (OHLCV) üzerinde çeşitli parametre kombinasyonlarıyla koşturularak tam **8.370 adet farklı backtest senaryosu** oluşturuldu. Tüm bu sonuçlar, yüzbinlerce satırlık hantal Excel dosyalarında boğulmak yerine, saniyeler içinde filtrelenebilen, aranabilen ve canlı grafiklerle desteklenen modern bir **Web Dashboard (Veri Terminali)** üzerine taşındı.

## 🧠 Nasıl Yapıldı? (Sistem Mantığı)
Sistemin sıradan borsa tarama yazılımlarından ayrılan en büyük özelliği **hesaplama mantığıdır**:

1. **Vektörize İşlem (Vectorized Processing):** Klasik yazılımlardaki satır-satır hesaplama yapan yavaş "for-loop" döngüleri tamamen terk edilmiştir. Bunun yerine `VectorBT` ve `Pandas` kullanılarak tüm fiyat verileri devasa matrisler halinde belleğe (RAM) alınır ve doğrusal cebir (vektör) işlemleriyle **100x ile 1000x kat arası daha hızlı** hesaplanır.
2. **Çalışma Zamanı Müdahalesi (Monkey-Patching):** Kullanıcı arayüzde bir grafiğe tıkladığında, arka plan (backend) diske (Excel/CSV) gereksiz dosya yazma işlemlerini durdurur. İlgili stratejinin Python koduna "havada (runtime)" müdahale ederek sonucu sadece RAM üzerinde yakalar ve grafiği milisaniyeler içinde ekrana çizer.
3. **Akademik Eleme Mantığı:** Karlı görünen her strateji başarılı kabul edilmez. Sistem arka planda sonuçları Merkezi Limit Teoremi'ne göre filtreler; yeterli işlem sayısına (N > 25) ulaşmamış şans eseri kazançları ve geçmiş veriyi ezberlemiş (Overfitting / PF > 10) yanıltıcı modelleri otomatik olarak işaretler.

## 💻 Kullanıcı Arayüzü (Dashboard) Özellikleri
Geliştirilen ön yüz, sıradan bir tablodan ziyade interaktif bir finansal terminal olarak çalışır:
- **Dinamik Sütun Filtreleme:** Her bir sütunun altında yer alan özel filtreler sayesinde veriler anlık olarak elenir. Örneğin; `Sharpe Ratio > 1.5`, `Max Drawdown < -20` ve `Win Rate > 60` gibi kompleks sorgular aynı anda çalıştırılabilir.
- **Canlı Grafik Çizimi (Plotly):** Tablodaki herhangi bir strateji satırına tıklandığında, o stratejinin tüm al/sat (buy/sell) noktaları ve portföy büyüme eğrisi, interaktif bir grafik üzerinde (zoom, pan, hover destekli) saniyeler içinde ekrana gelir.
- **Excel'e İhraç (Export):** Ekranda uyguladığınız tüm dinamik filtrelerin sonucunda kalan veri seti, tek tıkla cihazınıza `.xlsx` formatında indirilebilir.
- **Sıralama (Sorting):** Herhangi bir metriğe (örn: En Yüksek Kâr, En Düşük Drawdown) göre tek tıkla büyükten küçüğe / küçükten büyüğe sıralama yapılabilir.

## 🏗️ Mimari Yapı (Architecture)
Proje, her biri kendi alanında uzmanlaşmış modern bir 3-katmanlı (3-Tier) mimari üzerine inşa edilmiştir:

1. **Veri ve Algoritma Katmanı (Python, VectorBT):** 
   - `vbt_bist/strategies/` dizinindeki 90 adet Python modülünden oluşur. Piyasadan gelen ham verileri işler, al/sat sinyallerini üretir ve backtest raporlarını derler.
2. **API ve Mantık Katmanı (FastAPI, Uvicorn):**
   - `dashboard/backend/` dizininde çalışır. Ön yüz ile Algoritma motoru arasında köprü kurar. Asenkron (non-blocking) yapısı sayesinde ağır finansal hesaplamaları arka plan iş parçacıklarında (thread pool) yaparak API'nin tıkanmasını engeller.
3. **İstemci ve Görselleştirme Katmanı (React.js, Vite):**
   - `dashboard/frontend/` dizininde bulunur. 8.370 satırlık devasa veri setini tarayıcıyı çökertmeden gösterebilmek için **DOM Sanallaştırma (TanStack Virtual)** teknolojisini kullanır. Glassmorphism tasarım stili ile Bloomberg/Eikon terminallerine rakip bir kullanıcı deneyimi sunar.

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

Tarayıcınızdan `http://localhost:5173` adresine giderek Dashboard'a erişebilirsiniz.
