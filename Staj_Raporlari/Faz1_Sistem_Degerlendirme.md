# 🚨 Algoritmik Ticaret Sistemi: Acımasız Gerçeklik Raporu

İkimizin projesi olduğu için hiçbir şeyi süslemeden, bir fon yöneticisi (Quant) gözüyle sistemimizi acımasızca eleştiriyorum. İyi yaptıklarımız da var, ancak bizi canlı piyasada batıracak devasa eksiklerimiz de var.

## ✅ Yaptığımız Mantıklı ve Doğru Şeyler

### 1. Yazılım Mimarisi (Kusursuz)
- **Modülerlik:** Stratejileri `main.py` içine çorba gibi yığmadık. `strategies/` klasörü altında paketledik. Yarın 100. stratejiyi eklesek bile ana sistemimiz çökmeyecek.
- **Hata Yönetimi (Try/Except):** Bugün AKBNK verisi gelmediğinde sistemin çökmesini engelledik. Gerçek piyasada veri akışı sürekli kopar, bu refleksimiz hayat kurtardı.
- **Kayıt Sistemi:** Her hisse/strateji için özel klasör açıp `.csv` ve `.html` raporları kaydetmemiz muazzam. Geri dönüp "Ben nerede hata yaptım" demek için elimizde kanıt var.

### 2. Stratejilerin Matematiksel Davranışı (Beklenen Sonuç)
Sonuçlara baktığımızda stratejilerin tam da kitaplarda yazdığı gibi davrandığını (yani doğru kodlandığını) görüyoruz:
- **ASELS (Trend Piyasası):** Hisse ralli yaparken trend takipçileri (`three_ma` %470, `macd` %371) çıldırdı. Yatay piyasa indikatörü olan `Bollinger` ise trendin başında malı satıp zarar etti (%-4.5). **Bu %100 mantıklı ve doğru bir sonuçtur.**
- **GARAN / AKBNK (Yatay/Testere Piyasası):** Hisse bir aşağı bir yukarı testere yaparken hareketli ortalamalar (`two_ma` %-28) sürekli yanlış sinyal verip para kaybetti. Ama yatay piyasanın kralları olan `RSI` (%61) ve `Bollinger` (%53) harika kar yazdı. **Bu da %100 mantıklı.**

---

## ❌ Acı Gerçekler: Bizi Batıracak Mantıksızlıklar

Eğer bu sistemi yarın canlı paraya bağlarsak büyük ihtimalle paramızı kaybederiz. Neden mi?

### 1. İşleme Giriş Fiyatı (Lookahead Bias - Geleceği Görme Yanılgısı)
> [!CAUTION]
> Kritik Mantık Hatası
> Şu an sistemimiz alım-satımı **Kapanış (Close)** fiyatından yapıyor. Ancak gerçek hayatta saat 18:10'da kapanış fiyatı belli olduğunda piyasa kapanmış olur! O fiyattan işlem yapamazsın. Gerçekte sinyali akşam alır, ertesi sabah **Açılış (Open)** fiyatından işleme girersin. Bizim simülasyonumuz şu an imkansız bir fiyattan işlem yapıyor.

### 2. Kayma (Slippage) Hesaplanmıyor
Komisyonu (`fees=0.001`) binde 1 olarak ekledik, bu güzel. Ama "Slippage" (Kayma) eklemedik. Gerçek piyasada sen "100 TL'den al" dediğinde tahtada o an satıcı yoksa 100.5 TL'den alırsın. Çok işlem yapan stratejilerde (örneğin MACD) bu kaymalar karları eritip bitirir.

### 3. Tüm Hisselere Körlemesine Saldırıyoruz
En büyük stratejik hatamız bu: **Her hisseye her stratejiyi deniyoruz.**
Bir hisse trenddeyse RSI çalıştırmak intihardır. Bir hisse yataydaysa MA çalıştırmak intihardır.
**Çözüm:** Sisteme bir "Piyasa Rejimi (Market Regime) Filtresi" eklemeliyiz. Sistem önce hisseye bakmalı: "Bu hisse trendde mi, yoksa yatay mı?" Trenddeyse sadece MACD ve MA çalıştırmalı, yataydaysa RSI ve Bollinger.

### 4. Risk Yönetimi ve Stop-Loss Yok!
> [!WARNING]
> Ölümcül Hata
> Fark ettiysen parametrelerde hiç Stop-Loss (Zarar Kes) yok. Sistem "AL" dedikten sonra hisse %40 çökse bile, indikatör "SAT" diyene kadar malda kalıyor (bknz: GARAN three_ma zararı). Algoritmik ticarette koruyucu bir Stop mekanizması (örneğin Trailing Stop - İzleyen Stop) olmadan yaşayamazsın.

---

## 🎯 Staj Hocanın Haklılığı (Overfitting)

Hocanın "Parametre optimizasyonuna girmeyin" uyarısı şimdi daha da anlam kazanıyor. Biz henüz **Stop-Loss**, **Slippage** ve **Açılış fiyatından işlem yapma** gibi gerçek piyasa dinamiklerini sisteme dahil etmedik. 

Eğer bu eksikler varken "Hangi periyot daha iyi çalışır" diye optimizasyon (Grid Search) yaparsak, sistem "Hayal dünyasındaki" sahte karlara göre en iyi parametreyi seçecek. Gerçek piyasaya çıktığımızda o parametreler çöp olacak (Overfitting'in sözlük anlamı budur).
