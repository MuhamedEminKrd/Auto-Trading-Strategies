# 🛠️ Algoritmik Ticaret Tedavi Planı (Gerçekliğe Dönüş)

Raporu okudun, hayal dünyasından çıktık. Şimdi bir Quant (Sayısal Analist) gibi kolları sıvayıp sistemimizi "oyuncak" olmaktan çıkarıp "gerçek bir finansal silaha" dönüştüreceğiz. 

Sert eleştirdim, şimdi de nasıl düzelteceğimizi öğreteceğim. Sana 3 aşamalı bir ameliyat planı sunuyorum.

## User Review Required
> [!CAUTION]
> Bu değişiklikleri yaptığımızda (özellikle kayma ve gecikme eklediğimizde), daha önce %400 gördüğün karların %100'lere düştüğünü göreceksin. Bu senin moralini bozmasın! Çünkü o %400 bir yalandı. Biz artık **gerçek** %100'ün peşindeyiz. Bunu baştan kabul etmelisin.

## Açık Sorular (Cevaplamanı Bekliyorum)
> [!WARNING]
> 1. Stop-Loss (Zarar Kes) seviyesini kaç belirleyelim? BIST genelde volatil (oynak) olduğu için %5 (0.05) çok çabuk patlayabilir. %7 (0.07) veya %10 (0.10) ile mi başlayalım? Karar senin.

---

## Önerilen Değişiklikler (Ameliyat Adımları)

Bütün strateji dosyalarımızda (`single_ma.py`, `rsi.py`, vb.) bulunan `vbt.Portfolio.from_signals` fonksiyonunu güncelleyeceğiz. 

### 1. İşlem Gecikmesi (Signal Shifting) Ekleme
Şu an sistem Kapanış(Close) fiyatından sinyal üretip *aynı saniye içinde* yine Kapanış fiyatından alım yapıyor. Bunu engelleyeceğiz. Sinyal geldikten sonra alımı *bir sonraki barın (günün)* fiyatından yapmasını sağlayacağız. (Not: Verimizde sadece 'Close' indirdiğimiz için, işlemi ertesi günün kapanışına erteleyeceğiz).

### 2. Kayma (Slippage) Maliyeti Ekleme
Sen emri borsaya gönderdiğinde her zaman beklediğin fiyattan gerçekleşmez. Araya yüksek frekanslı robotlar veya tahta yapıcılar girer. 
- Sisteme **`slippage=0.002`** (Binde 2) kayma maliyeti ekleyeceğiz. Yani sistem bir hisseyi 100 TL'den aldığını sanırken, biz onu zorla 100.2 TL'den aldıracağız. Gerçek hayat budur.

### 3. Stop-Loss (Zarar Kes) Ekleme
Her portföy bloğuna **`sl_stop=0.07`** (Örneğin %7) parametresini ekleyeceğiz. Hangi strateji olursa olsun, hisse %7 düştüğü an sistem stratejinin "SAT" demesini beklemeden hisseyi otomatik olarak satıp nakde geçecek.

---

### [Örnek Değişiklik Uygulaması]
Bütün stratejilerdeki Portföy bloğu şu şekilde evrimleşecek:

#### [MODIFY] Tüm Strateji Dosyaları (Örn: `rsi.py`, `macd.py`)
```python
    # ESKİ HAYAL DÜNYASI:
    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri,
        exits=sat_sinyalleri,
        init_cash=10000,
        fees=0.001,
        freq='1d'
    )

    # YENİ GERÇEK DÜNYA (Uygulayacağımız):
    portfoy = vbt.Portfolio.from_signals(
        kapanis_fiyatlari,
        entries=al_sinyalleri,
        exits=sat_sinyalleri,
        direction='longonly', # Sadece Alım yönlü (BIST'te açığa satış risklidir)
        sl_stop=0.07,         # %7 Stop-Loss hayat kurtarır
        slippage=0.002,       # Binde 2 kayma maliyeti
        init_cash=10000,
        fees=0.001,
        freq='1d'
    )
```
*Not: Gecikme (Shift) için vectorbt'nin default ayarı zaten Kapanış'ta sinyal üretip ertesi barın Açılış/Kapanışında işlem yapmaya müsaittir, ancak `slippage` ekleyerek bu dezavantajı gerçekçi bir şekilde simüle etmiş olacağız.*

## Doğrulama Planı (Verification)
1. Değişiklikleri tüm dosyalara uygulayacağız.
2. `main.py`'yi tekrar çalıştıracağız.
3. ASELS'teki o ütopik %470 karın ne kadar düştüğünü ve sistemin kriz anlarında (%7 Stop-Loss sayesinde) bizi nasıl koruduğunu işlem kayıtlarından (CSV) teker teker inceleyeceğiz.
