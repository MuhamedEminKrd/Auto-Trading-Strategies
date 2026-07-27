# 📈 BIST 100 Algoritmik Ticaret: Strateji ve İndikatör Rehberi

Borsa İstanbul (BIST 100) küresel piyasalardan farklı dinamiklere sahiptir. Yüksek enflasyon ortamı, sığ tahtalar (düşük hacimli hisseler) ve ani haber akışları nedeniyle çok sert ralliler (yükselişler) ve çok sert şelaleler (düşüşler) yaşanır.

Bu yüzden "Tek bir indikatör bulayım, her hissede çalışsın" mantığı BIST 100'de intihardır. Araştırmalarım ve kantitatif verilere dayanarak BIST 100'e en uygun stratejileri kategorize ettim.

---

## Kategori 1: Trend Takipçileri (Trend Followers)
BIST 100'de enflasyon veya yabancı girişi kaynaklı bir ralli başladığında haftalarca sürebilir. Bu devasa karları yakalamak için **Trend Takipçileri** zorunludur.

1. **Hareketli Ortalamalar (MA Kesişimleri) - (Şu an bizde VAR)**
   - **Avantajı:** ASELS örneğinde gördüğün gibi %400'leri yakalar.
   - **Kusuru:** Yatay piyasada çok fazla yanlış (fake) sinyal üretip komisyondan eritir.
2. **MACD (Hareketli Ortalama Yakınsaması) - (Şu an bizde VAR)**
   - **Avantajı:** MA'lara göre trendin gücünü de ölçer, daha az yanlış sinyal verir.
3. **🔥 SuperTrend (ATR Bazlı İzleyen Stop) - (YAPMALIYIZ)**
   - **Durum:** BIST 100'de Türk algoritmik trader'ların açık ara en çok kullandığı indikatördür.
   - **Mantığı:** Fiyatın volatilitesini (oynaklığını - ATR) hesaplar. Fiyat ATR kadar düşmediği sürece "Trend devam ediyor" der ve hisseyi elinde tutar. Düşüşlerde harika bir koruma kalkanıdır.

---

## Kategori 2: Osilatörler (Yatay/Testere Piyasalar İçin)
Trend yokken, fiyat belli bir bant içinde (örn: AKBNK, GARAN) gidip geliyorsa trend takipçileri para kaybeder. Burada osilatörler devreye girer.

1. **RSI (Göreceli Güç Endeksi) - (Şu an bizde VAR)**
   - **Durum:** 30 (Aşırı Satım) ve 70 (Aşırı Alım) referanslarıyla çok iyi tepki trade'i yaptırır.
2. **Bollinger Bantları - (Şu an bizde VAR)**
   - **Durum:** Bandın dışına taşmalarda "Tepki gelecek" mantığıyla çalışır.
3. **🔥 Stokastik Osilatör (Stochastic) - (YAPMALIYIZ)**
   - **Durum:** Yatay giden bankacılık veya holding hisselerinde RSI'dan bile daha hassas dip-tepe yakalar. "Fiyat son 14 günün neresinde?" sorusuna cevap verir.

---

## Kategori 3: Hacim ve Kırılım Onayı (BIST İçin Kritik)
BIST 100'de manipülasyon (tahta yapıcılık) çoktur. Fiyat bir direnci kırmış gibi yapar, küçük yatırımcı atlar ve fiyatı aşağı çakarlar (Bull Trap - Boğa Tuzağı). Bunu engellemenin tek yolu **HACİM** onayıdır.

1. **🔥 OBV (On-Balance Volume / Denge İşlem Hacmi) - (YAPMALIYIZ)**
   - **Mantığı:** Fiyat yükselirken hacim artıyorsa, bu "gerçek" bir yükseliştir (Para giriyordur). Fiyat artarken hacim düşüyorsa bu bir tuzaktır. Diğer stratejilerimize "Filtre" olarak eklenmesi hayati önem taşır.
2. **🔥 Donchian Kanalı Kırılımı (Fiyat Kanalı) - (YAPMALIYIZ)**
   - **Mantığı:** Efsanevi "Kaplumbağa (Turtle)" stratejisidir. Hisse son 20 günün en yüksek fiyatını yukarı kırarsa AL, en düşük fiyatını aşağı kırarsa SAT. Çok basittir ama devasa trendleri yakalar.

---

## 👨‍🏫 Hoca'nın Değerlendirmesi ve Yol Haritası

Araştırmalar ve piyasa gerçekleri gösteriyor ki; bizim elimizdeki MA, MACD, RSI ve Bollinger cephaneliği gayet sağlam bir temel oluşturdu. Ancak eksik olan çok güçlü 3 silahımız var:

1. **SuperTrend:** BIST'te trend sürmek için bir numaralı araç.
2. **Donchian Kanalı Kırılımı:** Saf bir breakout (kırılım) stratejisi.
3. **OBV (Hacim Filtresi):** Diğer stratejilerin ürettiği sahte sinyalleri elemek için.

Mevcut stratejilerimize (MA, MACD, vs.) "Slippage ve Stop-Loss" ameliyatını yapıp sistemi gerçek piyasaya uyumlu hale getirdikten sonra, bu üç yeni ağır topu da cephaneliğimize ekleyebiliriz.

Sıralama ve fikirler hakkında ne düşünüyorsun?
