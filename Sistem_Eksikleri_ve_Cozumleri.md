# Sistemin Eksikleri ve Çözümleri — Basitleştirilmiş Anlatım
### (Bir öğrencinin ilk okuyuşta anlayabileceği şekilde yazılmıştır)

> **Bu belge ne yapar, ne yapmaz?** Aşağıda listelenen her madde; (1) sorunun **ne olduğunu**, günlük hayattan bir benzetmeyle, (2) bu sorun yüzünden **gerçekte ne ters gidebileceğini**, somut bir örnekle, (3) **çözümün mantığının** ne olduğunu açıklar. Bu belge **hiçbir kodu değiştirmez** — yalnızca "burada bir sorun var, çözümü kabaca şöyle olur" diye anlatır. Kodun kendisine dokunulmamıştır.
>
> Sorunlar dört ana gruba ayrılmıştır: **(A) Kod Kalitesi**, **(B) Dashboard Güvenliği**, **(C) Finansal/Akademik Metodoloji**, **(D) Öncelik Tablosu**.

---

## GRUP A — KOD KALİTESİ SORUNLARI

### A.1 — Sessiz Hatalar ("except: pass" Sorunu)

**Basit Anlatım:** Hayal edin ki bir sınıfta 90 öğrenciye (90 strateji) 93 farklı sınav (93 hisse) yaptırıyorsunuz. Bir öğrenci sınav kağıdını bir sebepten teslim edemezse (kalemi kırıldı, kağıdı yırtıldı, her ne olursa), öğretmen o öğrencinin adını **not defterine hiç yazmıyor** — sanki o öğrenci hiç var olmamış gibi davranıyor. Neden başarısız olduğunu, hatta başarısız olduğunu bile kimse bilmiyor.

**Kodda Nerede?** `vbt_bist/main.py` içinde, her strateji çalıştırılırken:
```python
except Exception as e:
    # Hatayi yoksayip diger stratejiye gec (Terminali kirletmemek icin print'i kaldirdik)
    pass
```

**Neden Sorun?** Bir strateji dosyasında küçük bir hata olsa (örneğin bir formülde sıfıra bölme, ya da beklenmedik bir veri tipi), bu satır o hatayı **tamamen yutuyor**. Sonuç tablosunda o hücre boş kalıyor ama *neden* boş kaldığı hiçbir yerde yazmıyor. Yüzlerce satırlık bir tabloda 5-10 tane "sessizce kaybolmuş" sonuç fark edilmeden aylarca durabilir.

**Çözümün Mantığı:** `pass` yerine, hatayı bir günlük (log) dosyasına yazmak gerekir:
```python
except Exception as e:
    logging.error(f"{modul_adi} - {baslik}: {type(e).__name__}: {e}")
```
Bu tek satır değişikliği, "hangi strateji hangi hissede neden çöktü" sorusunu saniyeler içinde cevaplanabilir hale getirir. Sistemin davranışı (hata olursa devam et) aynı kalır, sadece **görünürlük** eklenmiş olur.

---

### A.2 — Test Eksikliği (Hiçbir Strateji Test Edilmiyor)

**Basit Anlatım:** Bir araba fabrikasında her arabayı üretim hattından çıkardıktan sonra fren testi, direksiyon testi yapmadan doğrudan müşteriye satmak gibi düşünün. Arabaların çoğu sorunsuz çalışır ama içlerinden biri frensiz çıkmışsa, bunu ancak bir kaza olduktan sonra öğrenirsiniz.

**Somut Örnek (Bu Projede Zaten Yaşanmış):** `optimizingAlgo.md`'de anlatıldığı gibi, `coppock.py` ve `engulfing.py` stratejileri **2 yıllık veriyle hiç işlem üretmiyordu** (0 sinyal). Bu hata, sistemin otomatik bir mekanizmasıyla değil, birinin Excel çıktısına elle bakıp "bu satırlarda hep 0 var" demesiyle fark edildi. Eğer 5 yıllık veriye geçilmeseydi, bu hata muhtemelen hiç fark edilmeyecek ve "bu iki strateji BIST'te işe yaramıyor" diye yanlış bir sonuca varılacaktı.

**Neden Sorun?** 90 stratejinin **hiçbirinin** otomatik testi yok. Bir strateji dosyasında küçük bir değişiklik yapıldığında, o değişikliğin stratejiyi bozup bozmadığını anlamanın tek yolu **tüm sistemi baştan çalıştırıp** sonuç tablosuna bakmak — bu hem yavaş hem de insan gözünün fark edemeyeceği hataları (örneğin "%2 daha az işlem üretiyor ama hâlâ çalışıyor gibi görünüyor") gözden kaçırabilir.

**Çözümün Mantığı:** Her strateji için, elle hesaplanabilecek kadar basit, "sahte" (yapay) bir veri seti üzerinde bir **birim test (unit test)** yazılabilir. Örneğin: "Fiyat sürekli düz bir çizgi halinde yükseliyorsa, RSI stratejisi en az 1 AL sinyali üretmeli" gibi basit kontroller. Python'da bu iş için `pytest` kütüphanesi kullanılır:
```python
def test_rsi_yukselen_trend_sinyal_uretir():
    sahte_fiyat = pd.Series([100, 101, 102, ..., 150])  # düz yükselen
    sonuc = rsi.calistir(sahte_fiyat, baslik="TEST")
    assert sonuc['Total Trades'] > 0  # en az 1 işlem olmalı
```
Bu, "kod değişince bir şey bozuldu mu?" sorusunu insan gözü yerine bilgisayara sorduran bir güvenlik ağıdır.

---

### A.3 — Ayarların Kod İçine Gömülü Olması (Config Dosyası Yokluğu)

**Basit Anlatım:** Bir evin tüm elektrik anahtarlarının duvarların içine, sıva altına gömülü olduğunu düşünün — bir lambayı değiştirmek istediğinizde duvarı kırmanız gerekiyor. Oysa anahtarlar dışarıda, görünür ve erişilebilir olsa, aynı işi tek bir tıkla yapardınız.

**Kodda Nerede?** Hisse listesi (`data_fetcher.py` içinde 90+ hisse kodu doğrudan bir Python listesi olarak yazılı), test periyodu (`period="5y"`), başlangıç sermayesi (`utils.py` içinde `10000`), komisyon oranı (`0.001`) — hepsi doğrudan `.py` dosyalarının içine yazılmış.

**Neden Sorun?** Danışman hoca "komisyonu %0.2 yap, sonuçları tekrar üret" dediğinde, doğru dosyayı bulup içindeki sayıyı değiştirmek gerekiyor. Bu, tek bir değer için sorun değil — ama "hangi hisseleri test ediyoruz", "kaç yıllık veri kullanıyoruz" gibi birçok ayar aynı şekilde dağınık halde koda gömülüyse, "sistemin şu an tam olarak hangi ayarlarla çalıştığını" tek bakışta görmek imkânsız hale gelir.

**Çözümün Mantığı:** Tüm bu değerleri tek bir `config.py` (veya `config.yaml`) dosyasında toplamak:
```python
# config.py
HISSE_LISTESI = ["AKBNK", "GARAN", ...]
VERI_PERIYODU = "5y"
BASLANGIC_SERMAYESI = 10_000
KOMISYON = 0.001
KAYMA = 0.002
```
Diğer tüm dosyalar (`main.py`, `data_fetcher.py`, `utils.py`) bu değerleri `from config import ...` ile okur. Böylece "sistemin ayarları ne?" sorusunun cevabı tek bir dosyaya bakarak anlaşılır.

---

### A.4 — Göreli/Mutlak Yol Tutarsızlığı (Nereden Çalıştırırsan Çalıştır Sorunu)

**Basit Anlatım:** Bir arkadaşınıza "mutfaktaki dolaptan bardak al" dediğinizi düşünün. Eğer arkadaşınız zaten mutfaktaysa bu tarif işe yarar. Ama arkadaşınız bahçedeyse, "mutfaktaki dolap" onun için anlamsızdır — çünkü siz ona **nereden başlayacağını değil, göreli bir yön** tarif ettiniz. Doğrusu "evin girişinden mutfağa git, oradaki dolaptan bardak al" gibi, **her zaman aynı sabit noktadan** başlayan bir tarif vermektir.

**Kodda Nerede?** `main.py` dosyasının başında, veri ve strateji klasörleri şöyle **doğru** biçimde tanımlanmış:
```python
strateji_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strategies")
```
Bu satır "bu Python dosyasının bulunduğu yerden başla" der — script nereden çalıştırılırsa çalıştırılsın doğru sonucu verir. Ama birkaç satır aşağıda, **çıktı klasörü** şöyle tanımlanmış:
```python
hedef_klasor_strateji = os.path.join("vbt_bist", "output", baslik)
```
Bu, "bulunduğun yerden `vbt_bist/output`'a git" demek — yani **sizin o an hangi klasörde durduğunuza bağlı.**

**Neden Sorun?** Eğer birisi `Auto_Trading_Strategies/` klasöründeyken `python vbt_bist/main.py` çalıştırırsa her şey doğru çalışır. Ama biri `vbt_bist/` klasörüne girip (`cd vbt_bist`) sonra `python main.py` çalıştırırsa, sistem çıktıları yanlışlıkla `vbt_bist/vbt_bist/output/` gibi içe içe bir klasöre yazmaya çalışır. Bu durumda Smart Skip mekanizması (bkz. Bölüm 6.5, ana rapor) doğru klasörü bulamaz ve ya her şeyi gereksiz yere yeniden hesaplar ya da yanlış yere yazar.

**Çözümün Mantığı:** Aynı `__file__` tabanlı mutlak yol mantığını çıktı klasörüne de uygulamak:
```python
proje_kok = os.path.dirname(os.path.abspath(__file__))
hedef_klasor_strateji = os.path.join(proje_kok, "output", baslik)
```
Bu, dosyanın **nereden çalıştırıldığından bağımsız** olarak her zaman aynı, doğru klasöre yazmasını garanti eder. Aynı düzeltme `strategies/utils.py` içindeki `sonuclari_kaydet()` fonksiyonuna da uygulanmalıdır.

---

### A.5 — Loglama Sistemi Yerine `print()` Kullanımı

**Basit Anlatım:** Bir doktorun hastaya verdiği her ilacı bir deftere kaydetmek yerine, sadece odada yüksek sesle söylemesi gibi düşünün. O an odada olan duyar, ama bir hafta sonra "geçen hafta bu hastaya ne verilmişti?" diye sorulduğunda, hiç kimse hatırlamıyor çünkü hiçbir yere **kalıcı olarak** yazılmamış.

**Kodda Nerede?** Sistemdeki tüm bilgilendirme mesajları `print()` ile doğrudan terminale yazdırılıyor (`main.py`, `data_fetcher.py`, `master_rapor_olustur.py`).

**Neden Sorun?** Terminal penceresi kapatıldığında ya da 5.670 satırlık uzun bir çalıştırma sırasında ekran kaydırılıp geçmiş kaybolduğunda, "iki saat önce hangi hisse için hata alınmıştı?" sorusunun cevabı yok olur. Uzun süren (`data_fetcher.py` gibi 90+ hisseyi güncelleyen) işlemlerde, işlem bitene kadar kaç hissenin başarılı kaç tanesinin hatalı olduğunu takip etmek zorlaşır.

**Çözümün Mantığı:** Python'ın kendi `logging` modülü kullanılarak, hem terminale hem de tarihli bir dosyaya (`output/run_2026-08-27.log`) aynı anda yazan bir sistem kurulabilir:
```python
import logging
logging.basicConfig(
    filename=f"output/run_{tarih}.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info(f"{hisse} başarıyla işlendi")
```
Bu sayede geçmişteki her çalıştırmanın tam kaydı, bir dosyada kalıcı olarak saklanır.

---

### A.6 — Sonuçların Hangi Kod Versiyonuyla Üretildiğinin Bilinmemesi

**Basit Anlatım:** Bir öğretmenin sınav kağıtlarını topladığını ama hangi sınav kağıdının hangi müfredat yılına ait olduğunu not almadığını düşünün. Müfredat değiştiğinde, elindeki eski kağıtların hâlâ geçerli olup olmadığını anlayamaz.

**Neden Sorun?** Bir strateji dosyası (örneğin `hp_filter_ma.py`) düzeltildiğinde (bkz. ana rapor Bölüm 6.8 — bu strateji gerçekten düzeltilmişti), o stratejinin **eski, hatalı kod ile üretilmiş** `_ozet.csv` dosyaları diskte kalmaya devam eder. Smart Skip mekanizması, dosyanın var olup olmadığına bakar; içeriğin **hangi kod sürümüyle** üretildiğine bakmaz. Eğer kişi CSV'nin daha yeni olduğunu (mtime kontrolü) doğru şekilde görüp atlarsa sorun yok, ama strateji dosyası değiştirildiği halde CSV'nin mtime'ı bir şekilde daha yeni kalırsa (örn. dosya kopyalama, git işlemleri sırasında), **eski/yanlış sonuç sessizce doğru gibi kullanılmaya devam edebilir.**

**Çözümün Mantığı:** Her `_ozet.csv` dosyasının içine, o anki strateji dosyasının bir "parmak izini" (hash) veya versiyon numarasını da yazmak:
```python
import hashlib
kod_hash = hashlib.md5(open(strateji_dosya_yolu, 'rb').read()).hexdigest()[:8]
# ozet.csv'ye ek sütun: "kod_versiyonu": kod_hash
```
Böylece "bu sonuç, stratejinin hangi haliyle üretildi?" sorusu her zaman cevaplanabilir hale gelir.

---

### A.7 — Smart Skip'in İçerik Bütünlüğünü Kontrol Etmemesi

**Basit Anlatım:** Bir öğretmenin "bu ödev zaten teslim edilmiş mi?" diye kontrol ederken, sadece dosyanın **var olup olmadığına** bakması, içinde gerçekten bir ödev olup olmadığına (belki dosya bozuk, belki boş) hiç bakmaması gibi.

**Kodda Nerede?** `main.py`'deki Smart Skip mantığı, `*_ozet.csv` dosyasının **var olduğunu ve kaynak veriden daha yeni olduğunu** kontrol ediyor, ama dosyanın **içinde gerçekten geçerli bir sonuç olup olmadığını** kontrol etmiyor.

**Neden Sorun?** Eğer bir strateji ilk çalıştırmada yarıda kesilirse (örneğin bilgisayar kapanırsa) ve bozuk/yarım bir `_ozet.csv` bırakırsa, sistem bir sonraki çalıştırmada bu bozuk dosyayı "zaten tamamlanmış, atla" diye yorumlar — ve o hisse-strateji kombinasyonu **sonsuza kadar** yanlış/eksik sonuçla kalır, çünkü hiçbir zaman yeniden hesaplanmaz.

**Çözümün Mantığı:** Dosyayı atlamadan önce, içinde beklenen anahtar bir alanın (örneğin `"Total Return [%]"`) gerçekten var olup olmadığını kontrol etmek:
```python
try:
    df_ozet = pd.read_csv(ozet_dosyasi, index_col=0)
    if 'Total Return [%]' not in df_ozet.index or df_ozet.empty:
        zaten_var = False  # bozuk dosya, yeniden hesapla
except Exception:
    zaten_var = False
```

---

### A.8 — Dashboard'da Yarış Durumu (Race Condition) Riski

**Basit Anlatım:** Bir restoranda tek bir tabelanın üzerine "Masa 5: Tavuk" yazıp mutfağa gönderdiğinizi, ama aynı tabelayı hemen ardından "Masa 7: Balık" olarak silip yeniden yazdığınızı düşünün. Eğer mutfaktaki aşçı tam o anda tabelaya bakarsa, hangi siparişin hangi masaya ait olduğunu karıştırabilir. Doğrusu, her masaya **kendi ayrı** siparişi vermektir, ortak/paylaşılan tek bir tabela kullanmamaktır.

**Kodda Nerede?** `dashboard/backend/main.py`, bir kullanıcı bir grafiğe tıkladığında, `vbt_utils.sonuclari_kaydet` adlı **ortak/paylaşılan** bir fonksiyonu geçici olarak "yakalayıcı" bir fonksiyonla değiştiriyor, işlemi yapıyor, sonra eski haline geri döndürüyor (bkz. ana rapor Bölüm 4.6).

**Neden Sorun?** Eğer **iki farklı kullanıcı aynı anda** iki farklı grafiğe tıklarsa (ya da tek kullanıcı hızlıca iki satıra art arda tıklarsa), sistem şu an tek kullanıcılı/yerel kullanım için tasarlandığından, bu iki isteğin "yakalayıcı" fonksiyonları birbirine karışabilir. Teoride biri diğerinin sonucunu görebilir ya da patch erken geri alınıp gerçek diske-yazma fonksiyonu yanlışlıkla tetiklenebilir. Bu, tek kullanıcılı yerel kullanımda hiç fark edilmez ama çok kullanıcılı bir sunucuya taşındığında sessiz ve teşhisi zor hatalara yol açabilir.

**Çözümün Mantığı:** Global bir fonksiyonu geçici olarak değiştirmek yerine, her isteğe **kendi bağımsız** bir sonuç-yakalama nesnesi vermek (örneğin fonksiyonu parametre olarak strateji koduna geçirmek, ya da her istek için ayrı bir thread-local depolama kullanmak). Bu, mimarinin küçük bir yeniden tasarımını gerektirir ama "her kullanıcının isteği kendi kutusunda kalsın" prensibini garanti eder.

---

## GRUP B — DASHBOARD (WEB ARAYÜZÜ) GÜVENLİK EKSİKLİKLERİ

### B.1 — Girdi Doğrulama (Whitelist) Eksikliği

**Basit Anlatım:** Bir kütüphanede, ziyaretçinin istediği kitabın adını hiç kontrol etmeden doğrudan rafa gidip "bul" demek yerine, önce "bu gerçekten bizim kataloğumuzda var mı?" diye bakmak gerekir. Aksi halde biri "deponun anahtarını getir" gibi anlamsız/zararlı bir "kitap adı" isteyebilir.

**Kodda Nerede?** `GET /api/chart/html/{hisse}/{strateji}` endpoint'i, URL'den gelen `hisse` ve `strateji` isimlerini doğrudan dosya sistemi işlemlerinde kullanıyor (`resolve_module_name`, `load_data_for_stock`). Geçersiz bir isim gönderildiğinde yalnızca `try/except` ile genel bir hata dönülüyor; ama **önceden** "bu isim izin verilen hisseler listesinde mi?" diye bir kontrol yok.

**Neden Sorun?** Kötü niyetli ya da hatalı bir istek (`/api/chart/html/../../etc/../TEST`) sisteme gönderilirse, mevcut kod bunun zararsız bir şekilde hata vermesine güveniyor — ama bu bir **varsayım**, kesin bir güvenlik kuralı değil. Bugün yerel kullanımda risksiz olsa da, internete açık bir sunucuya taşınırsa bu tür bir "kontrolsüz girdi" güvenlik açığına dönüşebilir.

**Çözümün Mantığı:** İstek geldiği anda, adı yalnızca izin verilen karakterlerle (harf/rakam/alt çizgi) sınırlamak ve gerçek hisse/strateji listesiyle karşılaştırmak:
```python
import re
if not re.fullmatch(r"[A-Z0-9_]+", hisse):
    raise HTTPException(400, "Geçersiz hisse kodu")
if hisse not in gecerli_hisseler:
    raise HTTPException(404, "Hisse bulunamadı")
```

### B.2 — Hız Sınırlama (Rate Limiting) Yokluğu

**Basit Anlatım:** Bir kişinin, bir gişeye art arda binlerce kez aynı anda koşup sıraya girmesine izin vermek gibi — gişe (sunucu) tıkanır, gerçek müşteriler (diğer kullanıcılar) hizmet alamaz.

**Neden Sorun?** Her grafik isteği, arka planda gerçek bir backtest hesaplaması tetikliyor (CPU yoğun). Şu an sistemde "bir kullanıcı dakikada en fazla X istek atabilir" kuralı yok. Kasıtlı ya da kasıtsız (örneğin bir tarayıcı sekmesinin döngüsel olarak istek atması) çok sayıda ardışık istek, sunucunun tüm işlemci gücünü tüketebilir.

**Çözümün Mantığı:** `slowapi` gibi bir kütüphane ile IP başına dakikada belirli sayıda istek sınırı koymak:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/chart/html/{hisse}/{strateji}")
@limiter.limit("10/minute")
async def get_chart_html(...): ...
```

### B.3 — Zaman Aşımı (Timeout) Yokluğu

**Basit Anlatım:** Bir restoranda garsonun bir siparişi mutfağa verdikten sonra, mutfak ne kadar sürerse sürsün sonsuza kadar beklemesi gibi — eğer mutfakta bir sorun çıkarsa (örneğin ocak yanmıyorsa), garson da müşteri de sonsuza kadar bekler.

**Neden Sorun?** Bazı stratejiler (örneğin Ichimoku gibi ağır hesaplamalı olanlar, `Faz2_Strateji_Genisletme_Plani.md`'de de belirtildiği gibi) normalden uzun sürebilir. Eğer bir hesaplama beklenenden çok uzun sürer veya takılırsa (örneğin çok büyük bir veri kombinasyonunda), o isteği işleyen thread sonsuza kadar meşgul kalabilir ve zamanla thread havuzu tükenip sistem tüm kullanıcılar için yanıt vermez hale gelebilir.

**Çözümün Mantığı:** Her grafik isteğine bir üst zaman sınırı koymak:
```python
try:
    html_content = await asyncio.wait_for(
        loop.run_in_executor(None, generate_html_chart, hisse, strateji),
        timeout=30
    )
except asyncio.TimeoutError:
    raise HTTPException(504, "İşlem zaman aşımına uğradı")
```

---

## GRUP C — FİNANSAL / AKADEMİK METODOLOJİ EKSİKLİKLERİ

### C.1 — Survivorship Bias (Hayatta Kalanlık Önyargısı)

**Basit Anlatım:** Diyelim ki "başarılı girişimcilerin ortak özelliklerini" bulmak için bugün hayatta olan, zengin 100 girişimciyle röportaj yapıyorsunuz ve "hepsi risk almış, hepsi başarılı" sonucuna varıyorsunuz. Ama aynı riski alıp **batan** binlerce girişimciyi hiç görmediniz — çünkü onlar artık ortalıkta yok, röportaj veremiyorlar. Sonucunuz yanıltıcı, çünkü yalnızca "hayatta kalanları" incelediniz.

**Bu Projede Nasıl Görülüyor?** Sistem, **bugün** BİST100'de olan ~63-93 hisseyi test ediyor. Ama 2020-2025 arasında endeksten çıkan, iflas eden veya kottan düşen hisseler (kötü performans gösterdikleri için çıkmış olabilirler) analiz dışı bırakılıyor. Bu, "stratejilerimiz %72 oranında kârlı" gibi bir sonucun, gerçekte olduğundan **daha iyimser** görünmesine yol açar.

**Çözümün Mantığı:** "Historical index constituents" (BİST100'ün geçmiş dönemlerdeki gerçek üye listesi, bugünküyle aynı değil) verisi bulunup kullanılmalı. Bu veri Türkiye'de bulmak zor olabilir; bulunamıyorsa en azından **makalede bu sınırlılık açıkça belirtilmeli** ("bu çalışma survivorship bias içermektedir, bu nedenle sonuçlar iyimser bir üst sınır olarak yorumlanmalıdır").

### C.2 — Data Snooping / Çoklu Test Sorunu (Şans Eseri Başarı)

**Basit Anlatım:** 1.000 kişiye bozuk para attırıp "10 kez üst üste yazı gelsin" desek, aralarından mutlaka birkaç kişi bunu başarır — ama bu, o kişilerin "para atmada yetenekli" olduğu anlamına gelmez, sadece **çok fazla deneme** yapıldığı için şansın bir yerlerde tutması kaçınılmazdır.

**Bu Projede Nasıl Görülüyor?** Sistem 90 strateji × 63-93 hisse = **5.670-8.370 bağımsız test** yapıyor. İstatistiksel olarak, tamamen rastgele/anlamsız bir sistemde bile bu kadar çok testin **%5'i kadarı** (yaklaşık 280-420 tanesi) "anlamlı" görünecektir — sadece şans eseri. "En yüksek getirili strateji" olarak öne çıkan bir sonuç, gerçekten iyi bir strateji olabileceği gibi, 8.370 denemeden birinin şans eseri parlamış olması da olabilir.

**Çözümün Mantığı:** İstatistikte bu soruna karşı kullanılan standart yöntemler:
- **Bonferroni Düzeltmesi:** Anlamlılık eşiğini test sayısına bölerek çok daha katı hale getirmek (`0.05 / 8370 ≈ 0.000006`) — çok muhafazakâr ama basit.
- **Benjamini-Hochberg (FDR):** Daha az katı ama daha pratik bir düzeltme yöntemi.
- **En basit/anlaşılır pratik önlem:** Zaten uygulanan "İşlem Sayısı ≥ 25" ve "Profit Factor < 10" kuralları bu sorunu **kısmen** azaltıyor (az işlemli, "mucize" görünen sonuçları eliyor), ama tam bir istatistiksel düzeltme değil.

### C.3 — Walk-Forward / Out-of-Sample Test Yokluğu

**Basit Anlatım:** Bir öğrenciye sınav sorularının **cevap anahtarını önceden** verip sonra "bak, %100 aldı, çok başarılı" demek gibi. Gerçek başarıyı ölçmek için öğrenciyi **daha önce hiç görmediği** bir sınavla test etmek gerekir.

**Bu Projede Nasıl Görülüyor?** Sistemde kullanılan **tüm** 5 yıllık veri (2019-2024 gibi), hem "bu strateji parametreleri (örn. RSI periyodu 14) iyi mi?" sorusuna karar vermek hem de "bu strateji ne kadar kâr etti?" sonucunu raporlamak için **aynı veri havuzundan** kullanılıyor. Gerçek dünyada bu parametrelerin **gelecekte** de işe yarayıp yaramayacağı hiç test edilmiyor.

**Çözümün Mantığı:** Veriyi ikiye bölmek:
```
[----- Eğitim (2019-2023): Parametre seçimi -----][-- Test (2024-2025): Sadece ölçüm --]
```
Ya da daha gelişmiş biçimde **Walk-Forward** (kayan pencere) yöntemi: eğitim ve test pencerelerini zaman içinde kaydırarak birden fazla kez tekrarlamak. Kaynak belgelerde bu işin **ana sistemi bozmadan**, yalnızca makale için ayrı bir script (`makale_walk_forward_analizi.py` konsepti) olarak yapılması planlanmıştı — bu, riskli/deneysel değişiklikleri stabil sistemden izole tutmanın iyi bir örneğidir.

### C.4 — Long-Only / Boğa Piyasası Yanılgısı

**Basit Anlatım:** Bir yüzücünün "akıntıyla aynı yönde yüzerken" hızını ölçüp "ben çok hızlı yüzüyorum" demesi gibi — hızının bir kısmı kendi yeteneğinden değil, akıntının (piyasanın genel yükseliş trendinin) kendisinden geliyor olabilir.

**Bu Projede Nasıl Görülüyor?** Sistem yalnızca "AL ve SAT" (long-only) mantığıyla çalışıyor ve test edilen dönem BİST'in güçlü bir yükseliş dönemine denk geliyor. Bu dönemde neredeyse her "trend takip" stratejisi (Supertrend, ATR Breakout vb.) iyi sonuç verir — çünkü piyasa zaten yukarı gidiyordur, stratejinin "becerisi" değil piyasanın yönü asıl etken olabilir.

**Çözümün Mantığı:** Ayı piyasası (düşüş) dönemlerinde de test yapmak (örneğin 2018 veya farklı bir düşüş dönemi varsa), ya da en azından makalede "bu sonuçlar boğa piyasasına özgüdür, ayı piyasasında geçerliliği test edilmemiştir" şeklinde açıkça belirtmek.

### C.5 — Portföy Düzeyinde Risk Yönetimi Yokluğu

**Basit Anlatım:** Yumurtalarınızın hepsini tek bir sepete koyup "her sepet güvenli, çünkü her yumurtayı ayrı ayrı kontrol ettim" demek gibi. Sepetlerin **birbirine bağlı** olup olmadığına (örneğin hepsi aynı kamyonla taşınıyorsa, kamyon devrilirse hepsi birden kırılır) bakmamış olursunuz.

**Bu Projede Nasıl Görülüyor?** Sistem her hisseyi **birbirinden tamamen bağımsız** olarak test ediyor. "63 hisseye aynı anda para yatırsak ne olur?" sorusu hiç sorulmuyor. Örneğin sistem aynı anda tüm bankacılık hisselerine (AKBNK, GARAN, HALKB...) "AL" derse, bunlar genelde **birlikte** yükselir ya da **birlikte** düşer (yüksek korelasyon) — yani gerçekte risk dağıtılmış değil, aksine yoğunlaşmış olabilir; ama sistem bunu göremiyor çünkü her hisseye ayrı ayrı bakıyor.

**Çözümün Mantığı:** Hisseler arası korelasyon matrisi hesaplanıp, birbirine çok benzer davranan hisselere aynı anda "AL" verilmesinin gerçek çeşitlendirme sağlamadığı gösterilebilir. İleri seviye çözüm: Markowitz portföy optimizasyonu ya da eşit-risk-ağırlıklı (risk parity) portföy simülasyonu.

### C.6 — Enflasyona Göre Reel Getiri Hesaplanmaması

**Basit Anlatım:** Maaşınız bu yıl %50 arttı diye sevinmek, ama aynı yıl kira ve marketin de %60 zamlandığını hesaba katmamak gibi — nominal olarak daha çok kazanıyor gibi görünseniz de, **gerçekte (reel olarak)** daha az alım gücüne sahipsinizdir.

**Bu Projede Nasıl Görülüyor?** Bir strateji "%150 kâr etti" diyor, ama aynı 5 yıllık dönemde Türkiye'de kümülatif enflasyon %180'in üzerindeyse, bu strateji aslında **reel olarak para kaybettirmiş** olabilir. Şu anki tablo bu farkı hiç göstermiyor.

**Çözümün Mantığı:** TÜİK TÜFE (enflasyon) verisiyle her stratejinin getirisinden enflasyon oranını çıkararak "Reel Getiri" adında yeni bir sütun eklemek: `Reel Getiri (%) = Nominal Getiri (%) − Enflasyon (%)`.

### C.7 — Piyasa Rejimi Körlüğü

**Basit Anlatım:** Bir şemsiyenin "her hava koşulunda mükemmel çalıştığını" iddia etmek, ama testlerinizin tamamını yalnızca yağmurlu günlerde yapmış olmak gibi — güneşli ya da karlı havada aynı şemsiyenin nasıl davrandığını hiç bilmiyorsunuz.

**Bu Projede Nasıl Görülüyor?** Test edilen dönem (2022-2024 civarı), Türkiye'de seçim döngüsü, %50+ faiz oranları, hiper-devalüasyon gibi **olağanüstü** makroekonomik koşullar içeriyor. Bir stratejinin bu dönemde iyi çalışması, normal/sakin bir ekonomik dönemde de aynı şekilde çalışacağının garantisi değildir.

**Çözümün Mantığı:** Sonuçları "rejime bağımlı" (regime-dependent) olarak çerçevelemek ve mümkünse farklı makro dönemleri (COVID dönemi, seçim dönemi, yüksek faiz dönemi) ayrı ayrı analiz etmek.

### C.8 — Basit Komisyon Modeli

**Basit Anlatım:** Bir taksi ücretini hesaplarken sadece "kilometre başına sabit ücret" almak, ama trafik sıkışıklığında bekleme ücretini, gece zammını hesaba katmamak gibi — bazı özel durumlarda gerçek maliyet, hesapladığınızdan çok daha yüksek çıkar.

**Bu Projede Nasıl Görülüyor?** Tüm hisseler için sabit `%0.1 komisyon + %0.2 kayma (slippage)` kullanılıyor. Ama gerçekte, **düşük hacimli** (az işlem gören) hisselerde (örneğin BRSAN, TTRAK gibi) gerçek kayma çok daha yüksek olabilir, çünkü alıcı/satıcı bulmak zorlaşır. Ayrıca Türkiye'de komisyon üzerine eklenen **BSMV (%5 Banka Sigorta Muameleleri Vergisi)** de modele dahil edilmemiş.

**Çözümün Mantığı:** Hassasiyet analizi (sensitivity analysis) yapmak — farklı komisyon/kayma senaryolarıyla (%0.05, %0.1, %0.2, %0.5) sonuçların ne kadar değiştiğini göstermek. Bu, makalenin "robustness check" (sağlamlık kontrolü) bölümü için değerli bir tablo olur.

---

## GRUP D — ÖNCELİK SIRALI ÖZET TABLOSU

Aşağıdaki tablo, yukarıdaki tüm sorunları **"ne kadar kritik"** ve **"çözmesi ne kadar kolay"** eksenlerinde sıralar — hangi sorunla önce ilgilenilmesi gerektiğine karar vermek için:

| # | Sorun | Kritiklik | Çözüm Zorluğu | Öncelik |
|---|---|---|---|---|
| A.1 | Sessiz hatalar (`except: pass`) | Yüksek | Çok Kolay (birkaç satır) | 🔴 Hemen |
| A.4 | Göreli/mutlak yol tutarsızlığı | Yüksek (ama nadiren tetiklenir) | Çok Kolay | 🔴 Hemen |
| A.7 | Smart Skip bütünlük kontrolü | Orta-Yüksek | Kolay | 🟠 Yakında |
| A.3 | Config dosyası yokluğu | Orta | Kolay-Orta | 🟠 Yakında |
| A.5 | Loglama sistemi yokluğu | Orta | Kolay | 🟠 Yakında |
| C.2 | Data snooping / çoklu test | Çok Yüksek (akademik) | Orta (istatistik bilgisi gerekli) | 🔴 Makale İçin Kritik |
| C.3 | Walk-forward eksikliği | Çok Yüksek (akademik) | Zor (ayrı script gerektirir) | 🔴 Makale İçin Kritik |
| C.1 | Survivorship bias | Yüksek (akademik) | Zor (veri bulunması gerekiyor) | 🟡 En azından belirtilmeli |
| A.2 | Test eksikliği | Orta | Orta-Zor (90 test yazmak zaman alır) | 🟡 Uzun Vadeli |
| A.6 | Versiyon izlenebilirliği | Düşük-Orta | Kolay | 🟢 İsteğe Bağlı |
| A.8 | Dashboard race condition | Düşük (tek kullanıcıda risk yok) | Zor (mimari değişiklik) | 🟢 Çok kullanıcılı olursa |
| B.1-B.3 | Dashboard güvenlik açıkları | Düşük (yerel kullanımda) | Kolay-Orta | 🟢 İnternete açılırsa kritik |
| C.4-C.8 | Diğer akademik kısıtlamalar | Orta-Yüksek (akademik) | Zor/Veri gerektirir | 🟡 "Gelecek Çalışmalar" bölümünde dürüstçe belirtilmeli |

**En basit özet:** Kod kalitesi sorunlarının (A grubu) çoğu **birkaç satırlık, hızlı düzeltmelerdir** — bir öğrenci bunları bir günde tek tek çözebilir. Ama finansal/akademik metodoloji sorunları (C grubu) **kavramsal olarak daha derin** ve bazıları (survivorship bias gibi) **veri temini** gerektirdiği için daha zordur — bunların çoğu, "biz bu sınırlılığın farkındayız" diye makalede dürüstçe belirtilerek de savunulabilir; bu, akademik camiada kabul edilen, tamamen meşru bir yaklaşımdır.

---

*Bu belge, hiçbir kaynak kod dosyasını değiştirmeden, yalnızca mevcut kodun okunması ve önceki analiz raporunun (`Proje_Tam_Analiz_Raporu.md`) derinleştirilmesiyle hazırlanmıştır. Çözüm önerileri, uygulanmaya hazır kod parçaları değil, "mantığın ne olması gerektiğini" gösteren basitleştirilmiş örneklerdir.*
