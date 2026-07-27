# 🚀 Uygulama Planı: Strateji Cephaneliği (Faz 2)

Senin vizyonun kesinlikle doğru. Eğer BIST'teki yüzlerce hisseyi tarayacaksak, her piyasa koşuluna (Trend, Yatay, Hacimsiz, Kriz) uygun devasa bir "Strateji Kütüphanesine" ihtiyacımız var. Yaptığım küresel (QuantInsti, WorldQuant) ve yerel araştırmalar sonucunda, eksik olan ve sisteme mutlak suretle eklenmesi gereken **5 Elit Stratejiyi** belirledim.

## User Review Required
> [!CAUTION]
> Bu stratejilerin bazıları (özellikle Ichimoku) hesaplama açısından ağırdır. Yüzlerce hisseyi tararken işlem süremiz (şu anki 3 saniyeden) 10-15 saniyelere çıkabilir. Sistemimizin bunu kaldırabilecek gücü var, ancak bu gecikmeyi baştan kabul etmeliyiz.

## Open Questions
> [!WARNING]
> 1. Bu 5 stratejinin tamamını aynı anda mı sisteme kodlayalım, yoksa önem sırasına göre teker teker mi gidelim? (Sırayla gitmek hata ayıklamayı kolaylaştırır).
> 2. `main.py`'deki strateji listemiz uzayacağı için, sonuçları artık Excel (.xlsx) dosyasına da kaydetmek ister misin?

---

## Önerilen Yeni Stratejiler (Faz 2)

Bu stratejilerin her biri "farklı bir matematiksel açıdan" piyasaya bakar. Aynı şeyi ölçen iki indikatörü koymak yerine, birbirini tamamlayan 5 strateji seçtim (Confluence).

### 1. MFI (Money Flow Index - Para Akışı Endeksi)
- **Mantık:** RSI'ın "Hacim" (Volume) eklenmiş, daha zeki versiyonudur. Fiyat artarken hacim de artıyorsa (akıllı para giriyorsa) AL der. BIST gibi tahtacıların olduğu sığ borsalarda RSI'dan çok daha iyi çalışır.
- **Kategori:** Momentum / Hacim

### 2. Ichimoku Bulutu (Ichimoku Kinko Hyo)
- **Mantık:** Japonların efsanevi stratejisidir. Tek bir indikatörle hem destek/direnç, hem momentum, hem de trend yönü bulunur. Fiyat bulutun üstüne çıkarsa AL, bulutun içine girerse BEKLE, altına düşerse SAT.
- **Kategori:** Kompleks Trend Takibi

### 3. ADX (Average Directional Index)
- **Mantık:** Bize "Yönün ne olduğu" ile değil, **"Trendin gücü"** ile ilgilendiğini söyler. ADX > 25 ise hissede güçlü bir trend vardır (O zaman SuperTrend veya MA çalıştırırız). ADX < 20 ise hisse yataydır (O zaman RSI çalıştırırız).
- **Kategori:** Piyasa Rejimi (Trend Gücü)

### 4. Keltner Kanalları (Keltner Channels Breakout)
- **Mantık:** Bollinger Bantlarına benzer ama bant genişliğini standart sapma ile değil, ATR (oynaklık) ile belirler. Fiyat Keltner bandının dışına taştığında çok sert bir ralli habercisidir (Squeeze mantığı).
- **Kategori:** Volatilite / Kırılım

### 5. Stokastik Osilatör (Stochastic Fast/Slow)
- **Mantık:** Hissenin kapanış fiyatını, belirli bir periyottaki fiyat aralığına oranlar. BIST bankacılık ve holding endeksleri gibi dar bir bantta aylarca gidip gelen hisselerin diplerini ve tepelerini milimetrik yakalar.
- **Kategori:** Saf Osilatör

---

## Doğrulama Planı (Verification)
1. Seçtiğimiz stratejilerin dosyaları (`mfi.py`, `ichimoku.py` vb.) tek tek oluşturulacak.
2. `main.py` içerisindeki veri indirme (yfinance) modülüne `Volume` (Hacim) sütunu da eklenecek (Çünkü MFI hacim ister).
3. Dinamik `for` döngümüze bu 5 strateji eklenecek.
4. ASELS, GARAN gibi deneme hisselerimizde çalıştırıp kâr/zarar oranları teyit edilecek.
