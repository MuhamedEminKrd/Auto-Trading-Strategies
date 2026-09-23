# AutoTradingStrategies Projesi — Uçtan Uca Analiz Raporu
### (151-trading-strategies'den Kantitatif BIST Terminaline: Mimari, Veri Akışı, Kodlama Mantığı ve Gelişim Tarihçesi)

> **Raporu Hazırlayan Bağlam:** Bu belge, projenin tüm kaynak kodu (`vbt_bist/`, `dashboard/backend/`, `dashboard/frontend/`), kök dizindeki 4 AI-sohbet özeti (`AIWriting.md`, `clainingvektor.md`, `optimizingAlgo.md`, `suanakadarki.md`) ve `Staj_Raporlari/` klasöründeki 29 belgenin tamamı okunarak, hiçbir koda dokunulmadan, yalnızca **analiz amacıyla** hazırlanmıştır. Amaç; staj sunumu ve makale yazımı için jüriye/okuyucuya sistemin mantığını, veri akışını, mimari kararlarını ve **neden-sonuç zinciriyle geçirdiği evrimi** eksiksiz aktarmaktır.
>
> **Önemli Not — Kaynakların Düzensizliği Hakkında:** `Staj_Raporlari/` klasöründeki dosyalar kronolojik sırayla adlandırılmamıştır (örn. "Faz3" etiketli bir belge, "Faz2" etiketli bir belgeden mantıksal olarak önce gelmektedir). Bu raporun 8. Bölümü, tüm belgeleri **gerçek zaman çizelgesine ve içerik bağımlılıklarına göre** yeniden sıralamaktadır.

---

## BÖLÜM 1 — Giriş ve Kapsam

### 1.1 Bu Rapor Ne İçin Var?

Elinizdeki proje, tek bir oturuşta yazılmış bir yazılım değil; **Temmuz 2026'dan Ağustos 2026'ya kadar**, bir staj danışmanının (kaynaklarda "Hüseyin Hoca" olarak geçiyor; ilerleyen aşamalarda walk-forward önerisiyle "Yunus Hoca" adı da anılıyor — iki isim de kaynak belgelerde farklı bağlamlarda geçtiği için burada olduğu gibi aktarılmıştır) yönlendirmesiyle, birden fazla yapay zeka asistanıyla (Gemini 3.1 Pro, Claude Sonnet 4.6 dahil) iteratif olarak inşa edilmiş, **üç kez mimari olarak yeniden doğmuş** bir kantitatif finans sistemidir. Bu rapor:

1. Sistemin **bugünkü** kodlama mantığını ve veri akışını teknik olarak açıklar (Bölüm 3-5),
2. Projenin **151-trading-strategies** adlı bir kitap/repo uyarlamasından, bugünkü **AutoTradingStrategies** BIST terminaline nasıl evrildiğini, hangi krizlerin hangi mimari kararları doğurduğunu anlatır (Bölüm 2, 6),
3. `Staj_Raporlari/` klasöründeki dağınık belgeleri gerçek zaman çizelgesine oturtur (Bölüm 8),
4. Sistemin akademik/metodolojik kör noktalarını, güçlü yanlarını ve makale/savunma için kullanılabilecek çerçeveyi özetler (Bölüm 7, 9, 10).

### 1.2 Metodoloji

Bu analiz sırasında **hiçbir kaynak kod dosyası değiştirilmemiş, düzeltilmemiş veya çalıştırılmamıştır.** Aşağıdaki tüm bulgular, statik kod okuması ve belge içeriklerinin çapraz karşılaştırılmasıyla elde edilmiştir:

- **Kod:** `vbt_bist/main.py`, `data_fetcher.py`, `master_rapor_olustur.py`, `strategies/utils.py`, örnek strateji dosyaları (`rsi.py`, `ema_cross.py`), `dashboard/backend/main.py`, `dashboard/frontend/src/App.jsx`, `package.json`, `README.md`
- **Gelişim günlükleri (kök dizin):** `suanakadarki.md`, `optimizingAlgo.md`, `clainingvektor.md`, `AIWriting.md`
- **Staj Raporları (29 belge):** Faz raporları, mimari şemalar, strateji rehberleri, hata/düzeltme planları, akademik analiz raporları, dashboard danışmanlık raporları, metrik sözlüğü, sonuç analizleri

---

## BÖLÜM 2 — Projenin Kökeni: "151 Trading Strategies"den BIST'e Geçiş

### 2.1 Başlangıç Noktası (Temmuz 2026)

Proje, GitHub üzerinde bulunan **`151-trading-strategies`** adlı bir repodan başlamıştır (kaynak: `suanakadarki.md`, kullanıcı adı `MuhamedEminKrd/151-trading-strategies`). Bu repo, "151 Trading Strategies" adlı bir kitaptaki stratejilerin Python/FastAPI uyarlamalarını içeriyordu:

- Stratejiler `src/strategies/` altında varlık sınıfına göre klasörlenmişti: `stocks/`, `crypto/`, `fx/`, `commodities/`, `fixed_income/`, `futures/`, `etfs/`, `macro/`, `real_estate/`, `distressed/`, `misc/tax/`, `structured/`, `index/`.
- Her strateji, bir **FastAPI endpoint**'i olarak tasarlanmıştı (HTTP isteğiyle çağrılan Pydantic Request/Response modelleri).
- **Hiçbir backtest motoru yoktu.** Stratejiler teorik olarak "çalışıyordu" ama gerçek geçmiş veriyle test edilmemişti.
- Görev: Hocanın talimatıyla, **68 stratejiyi DOW30'daki 30 hisseye uygulayarak backtest sonucu üretmek.**

### 2.2 İlk Kritik Keşif: Üç Farklı Çıktı Formatı

Kod incelendiğinde stratejilerin üç farklı formatta sinyal ürettiği görüldü:
1. **`signal`** döndürenler (45 adet) — tekil `1/-1/0`
2. **`weights`** döndürenler (14 adet) — varlık başına ağırlık sözlüğü
3. **`long_assets`/`short_assets`** listesi döndürenler (9 adet)

Bu heterojenliği çözmek için `signals_adapter.py` yazılmış, `normalize_signals()` fonksiyonu her formatı standart `{VARLIK: SİNYAL}` biçimine çeviren bir **adaptör katmanı** olarak kurulmuştur. Bu, projenin ilk ciddi mühendislik soyutlamasıdır.

### 2.3 İlk Çalışan Sistem ve Büyük Kriz

`run_analysis.py` ile **rolling (yürüyen pencere) sinyal üretimi** kuruldu: her gün için son 100 fiyatlık dilim stratejiye veriliyor, sinyal üretiliyor, `vectorbt.Portfolio.from_signals()` ile backtest yapılıyordu. Bu, `single_ma`, `two_ma`, `three_ma`, `channel` için başarıyla çalıştı (30 hisse × 4 strateji = 120 backtest).

Ardından **68 stratejinin tamamını zorla entegre etme** girişimi yapıldı. Rolling pencere mimarisi terk edilip "tek seferlik snapshot sinyal" mantığına geçildi. **Sonuç tam bir felaketti:** Çalışan 4 strateji dahil tüm sistem 0 işlem üretmeye başladı. Kullanıcının o anki tepkisi kayıtlara şöyle geçmiştir:

> *"sence bu mantıklı bir kod mu oldu saçma sapan bir şey yaptık öncesinde en azından 4 tane grafiğimiz doğru çalışırken şuan tüm stratejiler 0 a 0 üretiyor çalışanlar da bozuldu her şey gitti kardeşim böyle"*

**Kurtarma:** `git log --oneline` ile çalışan son commit (`ea4a2cf — channel stratejisi sisteme eklendi`) bulundu, `git checkout ea4a2cf -- run_analysis.py` ile dosya geri alındı, bozuk `results/` klasörü silinip yeniden üretildi. **Bu olay projede git disiplinin öğrenildiği dönüm noktasıdır.**

### 2.4 Kök Neden Analizi: Neden 64/68 Strateji Çalışmadı?

AST (Soyut Sözdizim Ağacı) ile tüm 68 stratejinin Request sınıfları otomatik analiz edildi ve üç kısıt kategorisi tespit edildi:

| Kategori | Örnek Stratejiler | Sorun |
|---|---|---|
| **Eksik dışsal veri** | `sentiment_crypto`, `weather_risk`, `economic_announcements`, `hedging_pressure` | Twitter/Reddit duyarlılığı, hava durumu, COT raporu gibi yfinance'te olmayan veriler istiyor |
| **Yapısal uyumsuzluk** | `carry_factor`, `fix_and_flip`, `cdo_tranche`, `roll_yields` | Tahvil vadesi, gayrimenkul tadilat masrafı, vadeli işlem fiyatı gibi hisse senedinde matematiksel karşılığı olmayan parametreler |
| **Çoklu varlık zorunluluğu** | `pairs_trading`, `stat_arb`, `contrarian`, `alpha_rotation` | Tek hisse yönü değil, korelasyon matrisi veya çoklu varlık karşılaştırması gerektiriyor |

Bu bulgular hem hocaya gönderilen açıklayıcı mailin temelini oluşturdu hem de `Staj_Raporlari/strategy_requirements.md` adlı **Türkçe açıklamalı veri kataloğu**nun kaynağı oldu (bkz. Bölüm 8.1). Buradan çıkarılan ders nettir: *"Hisse senedi fiyatı yerine 0 atayıp bu stratejileri zorla çalıştırmak, 0 sinyal üretmez — anlamsız sinyal üretir. İkisi çok farklı şeydir."*

### 2.5 Pivot Kararı: Sıfırdan BIST'e Özel Bir Sistem

Bu noktada projenin en kritik mimari kararı verildi (kaynak: `optimizingAlgo.md` §1.2): **"Bu 151 repo üzerine mi çalışalım, yoksa sıfırdan mı kuralım?"** sorusuna cevap: **sıfırdan, temiz bir `vbt_bist/` klasörü kurmak.** Gerekçe: eski, DOW30/çoklu-varlık odaklı kodlara dokunmak daha fazla karmaşıklık yaratacaktı; BIST'e özel, sadece OHLCV (Açılış/Yüksek/Düşük/Kapanış/Hacim) verisiyle çalışan modüler bir sistem inşa etmek çok daha sürdürülebilirdi.

Bu karar, projenin **"151 strateji" mirasından yalnızca 5 tanesinin doğrudan kullanılabilir olduğu** gerçeğinin kabullenilmesi ve teknoloji yığınının tamamen değiştirilmesi anlamına geliyordu:

| Katman | Eski Yaklaşım (151-repo) | Yeni Yaklaşım (vbt_bist) |
|---|---|---|
| Sinyal üretimi | FastAPI endpoint + rolling for-loop | Doğrudan `vectorbt` vektörize hesaplama |
| Veri kaynağı | Karma (bazı stratejiler dışsal veri istiyor) | Sadece `yfinance` OHLCV |
| Ölçek | 30 hisse × 4-68 strateji (elle) | 63-93 hisse × 90 strateji (otomatik keşif) |
| Sinyal normalize | `signals_adapter.py` | Gerek yok — vectorbt doğrudan boolean seri kullanıyor |

**Bu pivot, raporun geri kalanının konusu olan tüm sistemin (vbt_bist + dashboard) doğduğu andır.**

---

## BÖLÜM 3 — Genel Sistem Mimarisi

### 3.1 Üç Katmanlı Mimari (Bugünkü Hal)

Proje bugün üç ana bileşenden oluşuyor:

```
1. vbt_bist/           → Backtest Motoru (Python + VectorBT)
2. dashboard/backend/   → API Katmanı (FastAPI)
3. dashboard/frontend/  → Görselleştirme Katmanı (React + Vite)
```

### 3.2 Uçtan Uca Veri Akışı

```
┌─────────────────────────────────────────────────────────────────┐
│  1) VERİ KATMANI                                                 │
│     yfinance API ──► data_fetcher.py ──► vbt_bist/data/*.csv     │
│     (auto_adjust=True: temettü/bölünme düzeltmesi)               │
│     (Artımlı/Delta güncelleme: sadece eksik son günler indirilir)│
└───────────────────────────────┬───────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│  2) ORKESTRASYON KATMANI — main.py                                │
│     • csv oku → ffill().bfill() ile NaN temizliği                 │
│     • strategies/ klasöründe dinamik modül keşfi (importlib)      │
│     • inspect.signature ile "hangi strateji hangi veriyi istiyor?"│
│       otomatik tespiti (Dependency Injection)                     │
│     • Smart Skip: çıktı zaten var ve veri güncel ise atla         │
│     • ProcessPoolExecutor ile HİSSE bazlı multiprocessing          │
└───────────────────────────────┬───────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│  3) STRATEJİ KATMANI — strategies/*.py (90 modül)                 │
│     her modül: calistir(**kwargs) → vbt.Portfolio.from_signals()  │
│     → utils.sonuclari_kaydet(portfoy, hisse, strateji_adi)        │
│     utils.py: merkezi ayar → init_cash=10000, fees=0.001,         │
│                              slippage=0.002, freq='1d'             │
└───────────────────────────────┬───────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│  4) ÇIKTI KATMANI — output/HISSE/strateji_adi/                    │
│     • HISSE_strateji_ozet.csv (16 metrik: Sharpe, Sortino, PF...) │
│     • HISSE_strateji_islemler.csv (yalnızca işlem varsa)          │
│     • HISSE_Karsilastirma.xlsx (hisse bazlı özet)                 │
└───────────────────────────────┬───────────────────────────────────┘
                                │ subprocess.run() (main.py bitince otomatik)
┌───────────────────────────────▼───────────────────────────────────┐
│  5) MASTER RAPORLAMA — master_rapor_olustur.py                    │
│     glob(**/*_ozet.csv) → tüm sonuçları birleştir                 │
│     + Alfa (α) = Kâr% − Benchmark%                                │
│     + Risk-Ayarlı Getiri = Kâr% / |MaxDD%|                        │
│     + Akademik Geçerlilik etiketi (N<25 / PF>10 kuralları)        │
│     → Tum_Strateji_Metrikleri.xlsx (binlerce satır × 19 sütun)    │
└───────────────────────────────┬───────────────────────────────────┘
                                │
┌───────────────────────────────▼───────────────────────────────────┐
│  6) DASHBOARD                                                     │
│     backend (FastAPI): /api/metrics, /api/chart/html, /chart/png  │
│     frontend (React+Vite): TanStack Virtual tablo + Excel export  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Mimarinin Dört Anahtar Tasarım İlkesi

1. **Dinamik Keşif (Open/Closed Principle):** `main.py` hiçbir stratejiyi tek tek `import` etmiyor. `strategies/` klasörüne yeni bir `.py` dosyası bırakmak, sisteme otomatik olarak yeni bir strateji eklemek için yeterli. Kod: `moduller = [f[:-3] for f in os.listdir(strateji_klasoru) if f.endswith('.py') and f not in ('__init__.py', 'utils.py')]`
2. **Bağımlılık Enjeksiyonu (Reflection):** `inspect.signature(fonksiyon)` ile her stratejinin `calistir()` fonksiyonunun hangi parametreleri istediği (örn. sadece `kapanis`, ya da `yuksek+dusuk+kapanis+hacim`) çalışma zamanında tespit edilip yalnızca o veriler gönderiliyor. Bu, hem RAM tasarrufu sağlıyor hem de orkestratörün strateji detaylarını hiç bilmesine gerek bırakmıyor.
3. **Smart Skip (Önbellekleme):** Bir hisse-strateji kombinasyonunun `_ozet.csv` dosyası, kaynak veri CSV'sinden (mtime karşılaştırması) daha yeniyse, o kombinasyon tekrar hesaplanmadan diskten okunuyor. Bu, sistemin kesintiye uğrayıp yeniden başlatılabilmesini (idempotency) sağlıyor.
4. **Merkezi Ekonomik Model (`utils.py`):** Tüm 90 stratejinin komisyon/kayma/başlangıç sermayesi tek bir dosyadan yönetiliyor — bu, stratejiler arası **adil karşılaştırma** için akademik açıdan kritik bir tasarım kararı.

---

## BÖLÜM 4 — Kodlama Mantığı: Dosya Dosya Derinlemesine İnceleme

### 4.1 `data_fetcher.py` — Veri Katmanı

- `indir_guncelle(hisse_listesi)`: her hisse için CSV dosyası varsa **son tarihten bugüne kadar delta indirme** yapıyor (`son_tarih + timedelta(days=1)` başlangıç noktası); yoksa `period="5y"` ile sıfırdan indiriyor.
- `auto_adjust=True` parametresi kritik: BİST'te sık görülen bedelli/bedelsiz sermaye artırımı ve temettü ödemelerinin fiyatta yarattığı sahte "çöküş" görüntüsünü engelliyor (bu, ayrı bir hata-düzeltme dalgasında sonradan eklenmiş bir iyileştirmedir — bkz. Bölüm 6.4).
- `yeni_veri.columns.get_level_values(0)` satırı, yfinance'in bazı sürümlerinde döndürdüğü `MultiIndex` sütun yapısını düzleştiriyor — küçük ama kritik bir uyumluluk yaması.
- `main` bloğunda BIST100'e yakın **93 hisselik** sabit bir liste tanımlı (bankacılık, holding, sanayi, enerji, gayrimenkul, sağlık gibi çeşitli sektörlerden).

### 4.2 `main.py` — Orkestrasyon Motoru

`hisse_analiz_et(csv_dosyasi)` fonksiyonu, **her hisseyi bağımsız bir process olarak** işliyor (`ProcessPoolExecutor`, `cpu_count() - 4` worker). Akış:

1. CSV oku → `.ffill().bfill()` ile veri doğrulama/temizlik katmanı
2. `veri_deposu` sözlüğü oluştur (kapanış, açılış, yüksek, düşük, hacim, başlık)
3. `strategies/` klasöründeki tüm modülleri listele
4. Her modül için: Smart Skip kontrolü → geçilemezse `inspect.signature` ile doğru argümanları eşle → `calistir()` çağır → sonucu topla
5. Hisseye özel `_Karsilastirma.xlsx` üret
6. `__main__` bloğunun sonunda `subprocess.run(["python", "master_rapor_olustur.py"])` ile **otomatik tetikleme** — kullanıcının ayrıca ikinci bir komut çalıştırmasına gerek bırakmıyor.

Dikkat çekici mühendislik detayı: Smart Skip mantığı `if kl == modul_adi` (**tam eşleşme**) kullanıyor. Bu, projenin gelişim tarihinde ciddi bir hatanın (bkz. Bölüm 6.5 — `startswith()` hatası) düzeltilmiş halidir.

### 4.3 `strategies/utils.py` — Merkezi Ekonomik Motor

```python
vbt.settings.portfolio['init_cash'] = 10000
vbt.settings.portfolio['fees'] = 0.001      # %0.1 komisyon
vbt.settings.portfolio['slippage'] = 0.002  # %0.2 kayma
vbt.settings.portfolio['freq'] = '1d'
```

Bu dört satır, **90 strateji dosyasının hiçbirinde artık tekrar yazılmıyor** — modül import edildiği an tüm `vbt.Portfolio` nesnelerine otomatik uygulanıyor. `sonuclari_kaydet()` fonksiyonu ise CSV/Excel kaydını standardize ediyor ve **grafik üretimini (HTML/PNG) devre dışı bırakmış durumda** (kod içinde yorum satırına alınmış) — bu, Bölüm 6.2'de anlatılan I/O krizinin kalıcı çözümünün izidir.

### 4.4 Tipik Bir Strateji Dosyası — Örnek: `rsi.py`

```python
def calistir(kapanis_fiyatlari, baslik, periyot=14, alt_sinir=30, ust_sinir=70):
    rsi = vbt.RSI.run(kapanis_fiyatlari, window=periyot)
    al_sinyalleri  = rsi.rsi < alt_sinir
    sat_sinyalleri = rsi.rsi > ust_sinir
    portfoy = vbt.Portfolio.from_signals(kapanis_fiyatlari, entries=al_sinyalleri.astype(bool), exits=sat_sinyalleri.astype(bool))
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
```

Her strateji dosyası aynı **üçlü şablonu** izliyor: (1) indikatör hesapla, (2) boolean AL/SAT serileri üret, (3) `vbt.Portfolio.from_signals()` ile backtest edip `utils.sonuclari_kaydet()`'e devret. Bu şablon disiplini, 90 dosyanın birbirinden bağımsız yazılmasına rağmen tutarlı kalmasını sağlıyor.

**Not — Sinyal Kesişimi Disiplini:** `ema_cross.py` gibi kesişim tabanlı stratejilerde `(ema_hizli > ema_yavas) & (ema_hizli.shift(1) <= ema_yavas.shift(1))` kalıbı kullanılıyor — yani "şimdi üstte VE bir önceki gün altında/eşitti" mantığıyla yalnızca **kesişim anı** yakalanıyor, sürekli tekrar eden yanlış sinyaller önleniyor.

### 4.5 `master_rapor_olustur.py` — Akademik Değerlendirme Motoru

`glob(output/**/*_ozet.csv, recursive=True)` ile tüm sonuç dosyaları toplanıyor. Her satır için 14 ham VBT metriğinin yanına **3 türetilmiş akademik sütun** ekleniyor:

- **Alfa (α):** `Kâr% − Benchmark%` — stratejinin basit "al-tut"a göre ürettiği ekstra değer
- **Risk-Ayarlı Getiri:** `Kâr% / |MaxDD%|`
- **Akademik Geçerlilik:** kural tabanlı etiket — `İşlem Sayısı < 25` → "Yetersiz Veri"; `Profit Factor = inf veya > 10` → "Overfitting Şüphesi"; aksi halde → "İstatistiki Olarak Güvenilir"

Bu dosyanın mimari olarak **`main.py`'den bağımsız, ayrı bir aggregation adımı** olarak tasarlanması bilinçli bir karardır (bkz. Bölüm 8, `optimizingAlgo.md` §6.1): eski tasarımda `main.py` çalışırken Excel'e yazmaya çalışmak dosya kilitlenmesi (`PermissionError`) yaratıyordu; ayrıştırma bu sorunu kökten çözdü.

### 4.6 `dashboard/backend/main.py` — API ve "Çalışma Zamanı Müdahalesi"

FastAPI üzerine kurulu backend, üç endpoint sunuyor:

| Endpoint | Görev |
|---|---|
| `GET /api/metrics` | `Tum_Strateji_Metrikleri.xlsx`'i JSON olarak servis eder |
| `GET /api/chart/html/{hisse}/{strateji}` | İlgili stratejiyi runtime'da çalıştırıp Plotly HTML grafiği döner |
| `GET /api/chart/png/{hisse}/{strateji}` | Aynısını `kaleido` ile statik PNG olarak döner |

Buradaki en özgün mühendislik çözümü **`run_strategy_and_get_portfoy()`** fonksiyonudur — bu, Bölüm 6.2'de anlatılan "Monkey-Patching" tekniğinin gerçek kod karşılığıdır:

```python
def capture(portfoy, baslik, strateji_adi, grafik_baslik=None):
    captured[strateji_adi] = portfoy
    return None   # orijinal kaydet'i ÇAĞIRMA — diske yazma!

setattr(modul, "sonuclari_kaydet", capture)
vbt_utils.sonuclari_kaydet = capture
try:
    fonksiyon(**fonksiyon_argumanlari)   # stratejiyi normal şekilde çalıştır
    return captured[strateji_klasor_adi]
finally:
    # patch'i geri al (diğer isteklerin etkilenmemesi için)
```

Strateji fonksiyonu, kendi kodunu hiç bilmeden, normalde `utils.sonuclari_kaydet()`'i çağırıyor sanıyor; ama backend bu referansı çalışma anında bir "yakalayıcı" (`capture`) ile değiştiriyor. Sonuç: **diske hiçbir CSV/HTML yazılmadan**, `Portfolio` nesnesi doğrudan RAM'de yakalanıp Plotly grafiğine dönüştürülüyor. `run_in_executor` ile bu CPU-yoğun işlem ayrı bir thread'e devredilerek FastAPI'nin `async` event loop'unun bloklanması engelleniyor.

Ayrıca `resolve_module_name()` fonksiyonu, Excel'deki strateji **klasör adını** (örn. `rsi_14_30_70`, parametreleri içerir) gerçek Python **modül adına** (`rsi`) çevirmek için "en uzun prefix eşleşmesi" algoritması kullanıyor. Bu, Bölüm 6.6'da anlatılan bir hatanın kalıcı çözümüdür.

**Gözlemlenen Bir Boşluk:** `Staj_Raporlari/Dashboard_Mimari_Danismanlik_Raporu.md` belgesinde önerilen bazı güvenlik önlemleri (whitelist regex doğrulaması `[A-Z0-9_]`, `slowapi` ile rate-limiting, `asyncio.wait_for` ile timeout sınırı) **bugünkü `dashboard/backend/main.py` dosyasında görülmemektedir** — yalnızca `resolve_module_name()`'in `ValueError` fırlatması dolaylı bir doğrulama sağlıyor. Bu, danışmanlık raporundaki önerilerin tamamının uygulamaya geçmediğini gösteren, sadece gözleme dayalı bir tespittir (bu raporun kapsamı gereği herhangi bir düzeltme önerilmemiştir).

### 4.7 `dashboard/frontend/src/App.jsx` — Sanallaştırılmış Terminal Arayüzü

React 19 + Vite üzerine kurulu tek dosyalık (454 satır) bir uygulama. Üç ana bölüm:

1. **Sol Sidebar — Filtre Akordiyonu:** Her sütun için ayrı bir `FilterAccordion` bileşeni. Sayısal sütunlarda operatör (`>,>=,<,<=,=`) + değer girişi, birden fazla koşul eklenebiliyor (`NumericFilterRow`). Metinsel sütunlarda checkbox listesi (`StringFilterPanel`, "Tümü/Temizle" kısayollarıyla).
2. **Orta — Sanallaştırılmış Tablo:** `@tanstack/react-virtual`'ın `useVirtualizer` hook'u, binlerce satırdan yalnızca ekranda görünen ~15-20 satırı DOM'a yazıyor (`overscan: 15`). Hem başlık hem satırlar **aynı `gridTemplateColumns`** ve **aynı scroll container**'ı paylaşıyor — bu, Bölüm 6.3'te anlatılan hizalama krizinin kalıcı mimari çözümüdür.
3. **Sağ Panel — Canlı Grafik:** Bir satıra tıklanınca backend'in `/api/chart/html/{hisse}/{strateji}` endpoint'i çağrılıyor, dönen HTML bir `<iframe srcDoc={chartHtml}>` içine gömülüyor. HTML indirme (Blob) ve PNG indirme (`window.location.href` ile backend redirect) iki ayrı buton.

Excel export tamamen **frontend'de** (`xlsx` kütüphanesiyle `filteredData` üzerinden) yapılıyor — backend'e hiçbir istek gitmiyor, bu da sunucu yükünü sıfırlıyor.

---

## BÖLÜM 5 — Strateji Kütüphanesi: 90 Algoritmanın Anatomisi

### 5.1 Kaç Strateji, Nereden Geldi?

Kod tabanında bugün **90 adet** `.py` strateji dosyası bulunuyor (`vbt_bist/strategies/`, `__init__.py` ve `utils.py` hariç doğrulanmıştır). Bu sayı, `Tum_Stratejiler_Rehberi.md`, `optimizingAlgo.md` ve `clainingvektor.md`'de tutarlı biçimde "90+" olarak anılıyor. **Kullanıcının belirttiği "151 strateji" rakamı, projenin başladığı orijinal GitHub reposundaki (kitap uyarlaması, çoklu varlık sınıfı) toplam strateji sayısıdır — bugünkü 90 BIST stratejisinin doğrudan devamı değil, o mirastan yalnızca birkaç fikrin (single_ma, two_ma, three_ma, mean_reversion) taşındığı, gerisinin BIST'e özel sıfırdan yazıldığı bir kütüphanedir** (bkz. Bölüm 2.5).

### 5.2 Gelişim Dalgaları (Stratejilerin Zamana Yayılmış Eklenme Sırası)

| Dalga | Yaklaşık Ölçek | İçerik | Kaynak |
|---|---|---|---|
| **Dalga 0** | 5 strateji | `single_ma`, `two_ma`, `three_ma`, `bollinger`, `mean_reversion` — yalnızca kapanış fiyatı | `optimizingAlgo.md` §3.1 |
| **Dalga 1** | ~9-12 strateji | RSI, MACD, SuperTrend, Donchian, ADX, Keltner, Ichimoku, MFI, Stochastic, Williams %R, AO, PSAR | `Faz1_Bist100_Rehberi.md` + `Faz2_Strateji_Genisletme_Plani.md` |
| **Dalga 2 (Faz 2.5)** | ~20 strateji | Z-Score, VIX Fix, HMA, Williams %R, AO, PSAR (ileri kurumsal quant seti) | `i_p_2.md` |
| **Dalga 3** | 40 strateji | İstatistiksel özgünlük dalgası: Golden Cross, StochRSI, Elder Ray, ATR Turtle, Chaikin Vol, VWAP, Klinger, Triple Screen, Pin Bar, Squeeze, Heikin Ashi (araştırma dokümanı: 12 öneri) | `strateji_onerileri.md`, `sistem_analizi.md` (40×40 referansı) |
| **Dalga 4 (Final)** | 90+ strateji | Hacim (OBV/CMF/VPT/AD-Line), mum formasyonları (Engulfing/Doji/Inside Bar/Fractal/Marubozu/Morning Star), istatistiksel (LinReg/HistVol/StdChannel), momentum ailesi (TSI/CCI/Aroon/KST/Coppock/CMO/ROC), alternatif MA'lar (ALMA/WMA/TEMA/HMA), kombinasyon filtreleri (ADX+MACD, BB+RSI, Supertrend+RSI, Triple Screen) | `optimizingAlgo.md` §3.3, `Tum_Stratejiler_Rehberi.md` |

### 5.3 Yedi Kategori (Final Sınıflandırma — `Tum_Stratejiler_Rehberi.md`)

1. **Trend ve Hareketli Ortalamalar** (16 strateji): alma, dema, ema_cross, golden_cross, hma, macd, ppo, rainbow_ma, single_ma, tema, three_ma, trix, two_ma, vwma, wma, zlema
2. **Osilatörler ve Momentum** (16): awesome_oscillator, cci, cmo, connors_rsi, coppock, dpo, kst, momentum, roc, rsi, schaff_trend, stoch_rsi, stochastic, tsi, ultimate_osc, williams_r
3. **Volatilite ve Kanallar** (14): atr_breakout, atr_channel, bb_width, bollinger, chaikin_vol, chandelier, donchian, hist_vol, historical_vol_rank, keltner, natr, squeeze, std_channel, true_range_ema
4. **Hacim ve Para Akışı** (11): ad_line, cmf, eom, klinger, mfi, nvi, obv, obv_ma, pvi, vpt, vwap
5. **Fiyat Aksiyonu / Mum Formasyonları** (11): doji_reversal, engulfing, fractal_breakout, hammer, heikin_ashi, inside_bar, marubozu, morning_star, pin_bar, rsi_divergence, three_soldiers
6. **Karmaşık/Kantitatif Sistemler** (13): elder_ray, hp_filter_ma, ibs, ichimoku, linreg, mass_index, mean_reversion, rvi, supertrend, trend_intensity, vix_fix, volatility_breakout, zscore
7. **Kombine/Filtreli Stratejiler** (8): adx, adx_macd, bb_rsi, ichimoku_rsi, psar, rsi_macd, supertrend_rsi, triple_screen

### 5.4 Veri İhtiyacına Göre Sınıflandırma (Reflection Mimarisinin Temeli)

`Veri_Tiplerine_Gore_Stratejiler.md`, tüm 90 stratejiyi hangi OHLCV bileşenine ihtiyaç duyduklarına göre 5 seviyeye ayırıyor: (1) Sadece Kapanış, (2) Kapanış+Hacim, (3) Yüksek/Düşük/Kapanış (HLC), (4) HLC+Hacim, (5) Tam OHLC (mum formasyonları). Bu sınıflandırma, Bölüm 3.3'te açıklanan `inspect.signature` tabanlı bağımlılık enjeksiyonunun **neden mümkün ve gerekli** olduğunu açıklıyor: her strateji yalnızca kendi ihtiyacı olan seriyi talep ediyor, motor buna göre veriyi seçici olarak paslıyor.

---

## BÖLÜM 6 — Mühendislik Krizleri ve Çözümleri (Neden → Sonuç Zinciri)

Bu bölüm, projenin karşılaştığı büyük teknik krizleri, **her birinin doğurduğu somut mimari kararla birlikte** kronolojik olarak sunar.

### 6.1 Kriz: "68 Strateji Zorlaması" (Temmuz 2026, en erken kriz)
- **Neden:** Rolling sinyal mimarisinin, tek-seferlik "snapshot" mimarisiyle değiştirilmesi.
- **Sonuç:** Tüm sistem (çalışanlar dahil) 0 işlem üretti.
- **Çözüm:** `git checkout <hash> -- dosya` ile kurtarma.
- **Kalıcı Miras:** Projede git disiplini ve "çalışan sisteme dokunma, önce izole test et" prensibi yerleşti.

### 6.2 Kriz: I/O (Disk Okuma/Yazma) Darboğazı
- **Neden:** 93 hisse × 90 strateji = 8.370 backtest senaryosu, her biri için Plotly HTML+PNG grafiği diske yazılıyordu. Disk %100 doluyor, işlem saatlerce/günlerce sürüyordu.
- **Çözüm:** Grafik üretimi kalıcı olarak diskten kaldırıldı (`utils.py`'de yorum satırına alındı). Dashboard'da **"Monkey-Patching"** tekniğiyle, kullanıcı bir grafiğe tıkladığında strateji runtime'da çalıştırılıp `Portfolio` nesnesi RAM'den doğrudan Plotly'ye çevriliyor (bkz. Bölüm 4.6).
- **Önem:** Bu, kaynak belgelerde *"projeyi kurtaran en büyük mimari karar"* olarak nitelendiriliyor (`clainingvektor.md` §2).

### 6.3 Kriz: Frontend Büyük Veri Çöküşü ve Hizalama Hatası
- **Neden 1:** 8.370 satırlık veri standart HTML tabloya basılınca tarayıcı donuyordu.
- **Çözüm 1:** `TanStack Virtual` ile DOM sanallaştırma — ekranda her an yalnızca ~15-20 satır render ediliyor.
- **Neden 2:** Virtual scroll, `position:absolute` ile yerleştirilen `<tr>` satırlarının `<table>`'ın otomatik sütun genişliği hesaplamasına dahil olamaması nedeniyle başlık/veri hizalaması bozuldu.
- **Çözüm 2:** `<table>` tamamen terk edildi; her sütun için sabit piksel genişliği (`getColWidth()`) tanımlanan **CSS Grid** düzenine geçildi. Header ve body aynı `gridTemplateColumns`'u ve **aynı scroll container**'ı paylaşıyor — mimari olarak kayma imkânsız hale getirildi.
- **Yan Olay — "Dokunma" Politikası:** Frontend'de CSS düzeltmeleri denenirken bazı değişiklikler beklenmedik layout bozulmalarına yol açtı. Kullanıcı net bir talimat verdi: *"Bir yeri yaparken diğer yeri bozuyorsun, Claude ile yaptığım frontta karışma."* Bundan sonra stabil frontend koduna dokunulmadı, odak backend/algoritma mantığına kaydırıldı (`clainingvektor.md` §3).

### 6.4 Kriz: Veri Bozulması (`BadZipFile`)
- **Neden:** `master_rapor_olustur.py`, Excel dosyasını yazarken Uvicorn sunucusunun otomatik yeniden yüklenmesi (reload) veya manuel durdurulması I/O'yu kesintiye uğrattı; dosya bozuldu, `HTTP 500` hataları başladı.
- **Çözüm:** Bozuk dosya silinip 5.670+ satır sıfırdan yeniden tarandı. Kural: I/O işlemleri sırasında sunucu kesintiye uğratılmayacak.

### 6.5 Kriz: Smart Skip'in `startswith()` Hatası
- **Neden:** `main.py`'deki eşleşme mantığı `startswith(strateji)` kullanıyordu; bu yüzden `rsi_macd` klasörünü gören sistem, saf `rsi` stratejisini "zaten hesaplanmış" sanıp atlıyor, **yanlış sonucu** kabul ediyordu.
- **Çözüm:** Tam kelime eşleşmesi (`==`) mantığına geçildi (bugünkü `main.py`'de doğrulanmıştır: `if kl == modul_adi`).

### 6.6 Kriz: Lookahead Bias (Geleceği Görme Yanılgısı)
- **Neden:** Sinyal, o günün **Kapanış** fiyatıyla üretiliyor, işlem de **aynı günün Kapanış** fiyatından yapılıyordu. Borsada kapanış anını gördüğünüzde piyasa zaten kapanmıştır — o fiyattan işlem imkânsızdır. Bu, sistemin %10.000 gibi imkânsız kârlar göstermesine yol açıyordu (`implementation_plan_update_2.md`, `Faz1_Sistem_Degerlendirme.md`).
- **Çözüm (aşamalı):** Önce `implementation_plan_updates` içinde 7 maddelik bir düzeltme listesi önerildi; `walkthrough_2`'de yalnızca 5 maddesi (1,3,4,5,6) — lookahead bias'ın kendisi (madde 2) **o aşamada henüz uygulanmamıştı.** Daha sonra, `optimizingAlgo.md` §4.9'da belgelendiği üzere, **tüm strateji dosyalarında** `.shift(1)` ile sinyaller bir gün öteye kaydırılarak *"bugün sinyal, yarın açılıştan işlem"* mantığı tutarlı biçimde uygulandı.

### 6.7 Kriz: Strateji Modül Adı Çözümleme
- **Neden:** Backend, Excel'deki klasör adını (`vpt_14`, parametre içeriyor) doğrudan Python modül adı (`vpt`) sanıp `import` etmeye çalışıyor, hata alıyordu.
- **Çözüm:** `resolve_module_name()` — `strategies/` klasöründeki dosya adları arasında **en uzun prefix eşleşmesini** bulan bir çözümleyici (bkz. Bölüm 4.6).

### 6.8 Diğer Küçük Ama Öğretici Hatalar
- **CCI / `Series.mad()`:** Pandas yeni sürümünde kaldırılan bu metod yerine `(df - df.mean()).abs().mean()` ile elle hesaplama yapıldı.
- **Bullish Engulfing / Coppock Curve — 0 işlem:** Koşullar çok katıydı (Engulfing) veya periyot (Coppock: 11+14+10 gün) 2 yıllık veriye sığmıyordu. Çözüm: koşullar gevşetildi, veri periyodu **2 yıldan 5 yıla** çıkarıldı.
- **Plotly NaN Opacity Hatası:** Hiç işlem yapılmayan stratejilerde grafik çizimi `[nan]` hatası veriyordu → `portfoy.trades.count() > 0` koşulu eklendi.
- **HP Filter (Hodrick-Prescott):** Matematiksel doğası gereği tüm zaman serisini baştan sona okuyarak **gelecekteki günlere bakıyordu** (lookahead bias'ın bir başka türü) → `statsmodels` bağımlılığı kaldırılıp saf EMA ile değiştirildi.
- **Doji/Heikin Ashi Açılış Fiyatı:** Bu stratejiler `Open` verisine ihtiyaç duyuyordu ama motor bunu göndermiyordu; "bir önceki günün kapanışını açılış" sayarak yanlış hesaplıyorlardı → `calistir()` imzasına `acilis` parametresi eklendi.
- **Delist Hisseler:** KOZAA, KOZAL gibi kottan çıkmış hisseler 404 hatası veriyordu → listeden çıkarıldı, sessiz `except` blokları `traceback` loglamayla değiştirildi.

---

## BÖLÜM 7 — Terk Edilen, Ertelenen ve Geri Alınan Kararlar

Aşağıdaki liste, projenin **hangi fikirlerin neden vazgeçildiğini** açıkça belgelemesi bakımından önemlidir (jüri sorularına hazırlık için özellikle değerlidir):

| Fikir | Durum | Gerekçe |
|---|---|---|
| **Stop-Loss mekanizması** (`Faz3_Gerceklige_Donus_Ameliyati.md`'de `sl_stop=0.07` önerilmişti) | **Terk edildi** | Stop-loss seviyesi de optimize edilmesi gereken bir parametredir; eklenmesi tüm 8.370 senaryonun yeniden hesaplanmasını gerektirirdi; akademik karşılaştırma için tüm stratejileri **aynı koşullarda** tutmak önceliklendirildi |
| **Gerçek zamanlı sinyal botu** | **Ertelendi** (kapsam dışı) | Düzenleyici kısıtlar, API entegrasyonu, backtest metodolojisinin henüz tamamlanmamış olması |
| **ML/Random Forest ile strateji seçimi** | **Ertelendi** (kapsam dışı) | Feature engineering gerektiriyor; out-of-sample test yapılmadan bu modeli beslemek yeni bir overfitting riski doğurur; danışman onayı yok |
| **`hizli_yama_botu.py`** (yeni strateji eklenince sadece onu çalıştıran geçici script) | **Smart Skip ile değiştirildi** | Smart Skip aynı işlevi kalıcı ve genel biçimde çözdü |
| **CSV/PNG/HTML çıktılarını Git'e gönderme** | **Terk edildi** | `output/` binlerce dosya içeriyor, ikili (binary) dosyalar diff'lenemiyor → `.gitignore`'a eklendi |
| **`main.py` içinde canlı Excel üretimi** | **Terk edildi** | Dosya kilidi + `PermissionError` riski → bağımsız `master_rapor_olustur.py` adımına ayrıştırıldı |
| **Walk-Forward analizi doğrudan ana sisteme entegre etme** | **Ertelendi, izole edildi** | Ana dashboard pipeline'ını bozmamak için, yalnızca makale amaçlı **ayrı bir script** (`makale_walk_forward_analizi.py` konsepti) fikri benimsendi |
| **Destek-Direnç stratejisi** (erken öneri, `suanakadarki.md` §12) | **Askıya alındı** | Kullanıcı yanlışlıkla eklenen kodu geri aldı, hocadan dönüş bekleniyordu |

---

## BÖLÜM 8 — `Staj_Raporlari/` Klasörünün Gerçek Kronolojik Haritası

> Kullanıcının uyardığı gibi, bu klasördeki 29 belge **dosya adlarına göre sıralı değildir.** Aşağıda, belgelerin içerik referanslarına (bahsedilen strateji sayısı, hisse sayısı, hangi belgeye atıfta bulunulduğu) dayanarak çıkarılmış **gerçek mantıksal/zaman sırası** sunulmaktadır.

### AŞAMA 0 — Miras ve Veri Kataloğu (Temmuz 2026, 151-repo dönemi)
- **`strategy_requirements.md`** — *"68 Stratejinin Veri İhtiyaçları"*: `suanakadarki.md` Aşama 10'da bahsedilen AST-tabanlı otomatik kod analizinin çıktısı. Projenin **BIST'e taşınamayan** mirasının tam dökümü (sentiment, makro, tahvil, gayrimenkul, emtia stratejileri). Bu belge, projenin *neden* sıfırdan yazıldığının kanıtıdır.

### AŞAMA 1 — İlk BIST Stratejileri ve İlk Sert Eleştiri
- **`Faz1_Sistem_Degerlendirme.md`** — *"Acımasız Gerçeklik Raporu"*: Yalnızca birkaç strateji (three_ma, macd, RSI, Bollinger, two_ma) varken yazılmış ilk kapsamlı öz-eleştiri. Lookahead bias, slippage eksikliği, "her hisseye her strateji" naifliği ve stop-loss yokluğunu tespit ediyor.
- **`Faz1_Bist100_Rehberi.md`** — Aynı erken dönemde, "elimizde MA/MACD/RSI/Bollinger var" tespitinden yola çıkarak SuperTrend, Stochastic, OBV, Donchian eklenmesini öneriyor.
- **`Faz3_Gerceklige_Donus_Ameliyati.md`** *(dosya adı "Faz3" olsa da, içerik olarak doğrudan `Faz1_Sistem_Degerlendirme.md`'nin cevabıdır ve kronolojik olarak ona hemen bitişiktir)* — Sinyal kaydırma (`shift`), slippage ve stop-loss (`sl_stop=0.07`, `direction='longonly'`) önerisi. **Not:** Buradaki stop-loss önerisi daha sonra Bölüm 7'de açıklandığı gibi terk edilmiştir — bu, dosya adlandırmasının kronolojiyi yanıltabileceğinin somut bir örneğidir.

### AŞAMA 2 — Strateji Genişletme (Faz 2 ve Faz 2.5)
- **`Faz2_Strateji_Genisletme_Plani.md`** ve **`implementation_plan.md`** *(neredeyse birebir aynı içerik — muhtemelen aynı planın iki farklı kayıt noktası)* — MFI, Ichimoku, ADX, Keltner, Stochastic önerisi (5 "Elit Strateji").
- **`Faz2_Uygulama_Gorevleri.md`** — Yukarıdaki 5 stratejinin görev takip listesi (`[x]` tamamlanan, `[/]` devam eden maddelerle).
- **`i_p_2.md`** — *"Faz 2.5"*: Z-Score, VIX Fix, HMA, Williams %R, Awesome Oscillator, Parabolic SAR. Metinde *"toplam strateji sayımız 20'ye ulaşacak"* denilerek bu aşamanın ölçeği netleştiriliyor.

### AŞAMA 3 — Offline Veri Mimarisine Geçiş
- **`implementation_plan_update`** — *Plan:* "Offline Veri Mimarisi ve BİST100 Genişlemesi" — `data_fetcher.py`'nin ayrı bir script olarak doğuşu, internet bağımlılığının `main.py`'den koparılması önerisi.
- **`implementation_plan_new`** — *Sonuç Raporu:* "Data Lake Mimarisine Geçiş" tamamlandı, AKBNK/GARAN ile test edildi, offline çalışma doğrulandı.

### AŞAMA 4 — Derin Kod Denetimi ve Hata Düzeltme Dalgası
- **`implementation_plan_update_2`** — *"Derin Kod Analiz Raporu"*: Lookahead bias ve "az işlemli şanslı strateji" tuzağının ilk kez sistematik olarak tespit edildiği belge.
- **`implementation_plan_updates`** — Yukarıdaki denetimden çıkan **7 maddelik** numaralandırılmış hata/çözüm planı (Smart Skip hatası, lookahead bias, fractal_breakout/HP filter mantık çöküşü, delist hisseler, adjusted close eksikliği, doji/heikin_ashi açılış fiyatı, işlem sayısı filtresi).
- **`walkthrough_2`** — Kullanıcının seçtiği maddelerin (1, 3, 4, 5, 6) uygulandığını raporlayan sonuç belgesi. *(Not: madde 2 — lookahead bias — bu aşamada henüz kapatılmamıştı; nihai çözümü `optimizingAlgo.md`'de belgelenmiştir.)*

### AŞAMA 5 — Genişletilmiş Strateji Araştırması (40 Strateji Dönemi)
- **`strateji_onerileri.md`** — *"Mevcut 40 stratejimizi inceledim"* ifadesiyle açıkça 40-strateji dönemine tarihlenen, akademik atıflı (QuantInsti, WorldQuant referanslı) 12 yeni strateji araştırması (Golden Cross, MACD Histogram, StochRSI, Elder Ray, ATR Turtle, Chaikin Vol, VWAP, Klinger, Triple Screen, Pin Bar, Squeeze, Heikin Ashi). Bu 12 önerinin **tamamı** bugünkü final 90-strateji listesinde mevcuttur.
- **`egitim_ve_araclar.md`** — Aynı dönemin daha kısa/eğitim odaklı kardeş belgesi: AI araç önerileri, benzer strateji fikirleri, "bir strateji başarılı mı?" değerlendirme metodolojisi (Max Drawdown → Profit Factor → Sharpe → Win Rate → Kâr sırasıyla bakılmalı), okuma listesi (*A Random Walk Down Wall Street*, *Quantitative Trading*).
- **`sistem_analizi.md`** — *"Kırk hisse, kırk strateji, 1.600 kombinasyon"* ifadesiyle yine 40×40 döneminde yazılmış, 6 farklı meslek perspektifinden (Yazılımcı/İstatistikçi/Trader/Ekonomist/Veri Bilimci/Finansçı) 360° değerlendirme.

### AŞAMA 6 — Ölçeklenme, Yeniden Denetim ve Nihai Temizlik (63-93 Hisse, 88-90 Strateji Dönemi)
- **`sistem_ekspertiz_raporu.md`** — *"88 stratejiyi entegre etmek"* referansıyla neredeyse-final ölçekte yazılmış sert bir denetim: Long-only/boğa piyasası yanılgısı, survivorship bias, yfinance veri kalitesi riski, "karanlık oda" (execution) riski, all-in/all-out pozisyon büyüklüğü sorunu.
- **`BIST_Sistem_Analiz_Raporu_update`** — 63 hisse × 90 strateji ile açıkça final ölçekte yazılmış, staj süresince yapılan **15 değişikliğin** eksiksiz dökümünü içeren en kapsamlı teknik denetim belgesi. Puanlama tablosu (Mimari Tasarım 8/10, Backtest Geçerliliği 5/10 vb.) içeriyor.
- **`analysis_results.md`** ve **`analysis_summary.txt`** — Final sonuç verisinden (63 hisse, 90 strateji) çıkarılmış en iyi/en kötü strateji ve hisse analizleri (Ultimate Oscillator, RSI en tutarlı; RVI/IBS en kötü; ASELS/ASTOR en kazandıran; KONTR/VESBE en kaybettiren).

### AŞAMA 7 — Dashboard İnşası
- **`Dashboard_Mimari_Danismanlik_Raporu.md`** — Danışmanlık raporu: FastAPI+React kararının gerekçesi, `run_in_executor` ile async-blocking çözümü, virtual scrolling vs. pagination tartışması, SheetJS ile frontend Excel export kararı, on-demand grafik üretimi için güvenlik kontrol listesi.
- **`implementation_plan_updates3`** — *"BIST Kantitatif Dashboard Uygulama Planı"*: Yukarıdaki danışmanlık raporuna **doğrudan referans vererek** ("Dashboard Mimari Danışmanlık Raporu'ndaki kararlara... dayanılarak hazırlanmıştır") somut endpoint ve bileşen planını ortaya koyuyor — bu iki belge arasındaki referans ilişkisi, sıralamayı kesinleştiriyor.

### AŞAMA 8 — Mimari Şema ve Final Referans Belgeleri (Sistem Donduktan Sonra)
- **`Sistem_Mimarisi_Semasi.md`** — Mermaid diyagramlı, final mimariyi (90 strateji, Smart Skip, Reflection) özetleyen şema.
- **`Tum_Stratejiler_Rehberi.md`**, **`Veri_Tiplerine_Gore_Stratejiler.md`** — 90 stratejinin final kategorik ve veri-tipi bazlı tam kataloğu.
- **`metric_formulas.md`** — 15 metriğin (Alfa, Sharpe, Sortino, Calmar, Expectancy vb.) formül sözlüğü.

### AŞAMA 9 — Akademik Olgunlaşma ve Makale Hazırlığı (En Son Aşama)
- **`bist_system_analysis.md`** — Projenin en akademik/olgun belgesi: Survivorship Bias (Elton, Gruber & Blake 1996), Data Snooping/Multiple Testing (Harvey, Liu & Zhu 2016), PF=∞ ve N=1 anomalilerinin akademik yorumu (Bailey & López de Prado 2014), Bonferroni/FDR/White's Reality Check önerileri, tam makale iskeleti (Giriş → Literatür → Metodoloji → Bulgular → Tartışma → Sonuç), hedef dergiler (Journal of Financial Economics, Quantitative Finance, Borsa Istanbul Review).
- **`yeni.md`** — *"üniversite staj jürisine... sunulacak"* ifadesiyle açıkça jüri sunumu için hazırlanmış, kısa ve öz bir mimari-savunma özeti.
- **`makale_taslagi.md`** — Akademik makale taslağının kendisi (Özet, Giriş, Metodoloji, Bulgular placeholder, Gelecek Çalışmalar).
- **`README.md`** *(kök dizin)* — Projenin GitHub'daki profesyonel tanıtım metni; `151-trading-strategies` → `Auto_Trading_Strategies` yeniden markalaşmasının son ürünü.

### 8.1 Bu Sıralamanın Doğrulanması: Kök Dizindeki Sohbet Özetleriyle Çapraz Kontrol
`suanakadarki.md` (Temmuz 2026, en erken) → `optimizingAlgo.md` ve `clainingvektor.md` (Ağustos 2026, projenin **tamamını** geriye dönük özetleyen iki "final" günlük) — her ikisi de yukarıdaki 9 aşamayı, farklı bir anlatı sırasıyla ama **aynı olgusal içerikle** doğruluyor. `AIWriting.md` ise teknik içerik taşımıyor; yalnızca makale yazımı için hangi yapay zeka modelinin seçileceğine dair meta bir sohbeti belgeliyor (27 Ağustos 2026, projenin tamamlanmasından sonra).

---

## BÖLÜM 9 — Akademik/Metodolojik Değerlendirme: Güçlü Yanlar ve Kör Noktalar

### 9.1 Güçlü Yanlar (Kaynak belgelerde tutarlı biçimde vurgulanan)

- **Ölçek:** 63-93 hisse × 90 strateji = 5.670-8.370 backtest senaryosu, saniyeler içinde (vektörize hesaplama sayesinde) tamamlanıyor.
- **Mimari olgunluk:** Plug-and-play strateji sistemi, Dependency Injection, Smart Skip — "Open/Closed Principle"e tam uyum.
- **Ekonomik gerçekçilik:** Tüm stratejiler aynı komisyon (%0.1) ve kayma (%0.2) modeliyle test ediliyor — adil karşılaştırma.
- **Lookahead bias çözümü:** `.shift(1)` disiplini tüm stratejilerde tutarlı uygulanmış.
- **Akademik etiketleme:** Overfitting şüphesi (PF>10) ve yetersiz veri (N<25) otomatik işaretleniyor — çıplak "en yüksek kâr" tablosu yerine istatistiksel süzgeç var.
- **Dashboard:** Kurumsal düzeyde (Bloomberg/Eikon esintili) sanallaştırılmış, sıfır-backend-yükü filtreleme deneyimi.

### 9.2 Kör Noktalar (Kaynak belgelerde tekrar tekrar, farklı yazarlar/dönemler tarafından tespit edilmiş)

| Kör Nokta | Açıklama | En Çok Bahsedildiği Belge |
|---|---|---|
| **Survivorship Bias** | Yalnızca bugün BİST100'de olan hisseler test ediliyor; 2022-2024 arası delist/endeksten çıkan hisseler analiz dışı → başarı oranı olduğundan yüksek görünüyor | `bist_system_analysis.md`, `sistem_ekspertiz_raporu.md` |
| **Data Snooping / Multiple Testing** | 5.670-8.370 bağımsız test yapılıyor; saf şansla bile testlerin ~%5'i "anlamlı" görünür; Bonferroni/FDR düzeltmesi uygulanmamış | `bist_system_analysis.md` |
| **Walk-Forward / Out-of-Sample eksikliği** | Tüm veri hem parametre seçimi hem performans ölçümü için kullanılıyor; ayrı bir eğitim/test bölünmesi yok | `bist_system_analysis.md`, `BIST_Sistem_Analiz_Raporu_update` |
| **Long-Only / Boğa Piyasası Yanılgısı** | Test dönemi (2020-2025 civarı) BİST'in güçlü yükseliş dönemine denk geliyor; ayı piyasasında test edilmemiş | `sistem_ekspertiz_raporu.md` |
| **Portföy Düzeyinde Risk Yönetimi Yok** | Her hisse izole test ediliyor; korelasyon, pozisyon boyutlandırma, çeşitlendirme analizi yok | `sistem_analizi.md`, `BIST_Sistem_Analiz_Raporu_update` |
| **VBT Ayar Tutarsızlığı (kısmen giderilmiş)** | Bazı eski strateji dosyalarında hâlâ manuel parametre olabileceği belirtiliyor; `clainingvektor.md`'de regex ile büyük ölçüde temizlendiği belgeleniyor | `BIST_Sistem_Analiz_Raporu_update` → `clainingvektor.md` §1 |
| **Enflasyon/Reel Getiri Ayarlaması Yok** | Türkiye'nin yüksek enflasyon ortamında nominal getiriler reel getiriyi yanıltabilir | `bist_system_analysis.md` |
| **Rejim Bağımlılığı** | 2022-2024 Türkiye'sinin olağanüstü makro koşulları (seçim, kur krizi, yüksek faiz) genellenebilirliği sınırlıyor | `bist_system_analysis.md` |

Bu tabloyu makale/savunma için özellikle değerli kılan şey, sistemin bu eksiklikleri **kendi geliştirme sürecinde defalarca, farklı zaman noktalarında kendi kendine tespit etmiş** olmasıdır — bu, metodolojik dürüstlüğün ve iteratif öz-eleştirinin somut kanıtı olarak sunulabilir.

---

## BÖLÜM 10 — Bulgular Özeti (Mevcut Sonuç Verisinden)

`analysis_results.md` ve `analysis_summary.txt`'den (63 hisse × 90 strateji, final veri seti):

**En Tutarlı Strateji:** RSI(14,30,70) — ortalama %21.77, medyan %21.80 (ortalamaya çok yakın → düşük çarpıklık), %71.98 kazanma oranı. Ortalama ile medyanın birbirine yakınlığı, sonucun birkaç aşırı değerden değil genel bir eğilimden kaynaklandığını gösteriyor.

**En Yüksek Ortalama Getiri:** Ultimate Oscillator(7,14,28) — %31.97 ortalama, ancak standart sapması yüksek (%62.5) — riski de yüksek.

**Yanıltıcı Görünen Strateji:** ATR Breakout(14) — %23.30 ortalama ama medyan yalnızca %1.31 — birkaç büyük kazanç ortalamayı yukarı çekiyor, tipik işlem başa-baş civarında.

**En Kötü Stratejiler:** RVI(10,4) (%-24.56), IBS (%-22.85), Klinger (%-12.82), Heikin Ashi (%-12.03).

**En Kazandıran Hisseler:** ASELS (%164.25), ASTOR (%105.40), TKFEN (%94.41) — muhtemelen test döneminde güçlü ana trend içindeydiler (bu da Bölüm 9.2'deki "Long-Only/Boğa Piyasası Yanılgısı" bulgusunu destekliyor).

**En Kaybettiren Hisseler:** KONTR (%-54.76), VESBE (%-36.84), ARZUM (%-30.46).

---

## BÖLÜM 11 — Sonuç: Sistem Bugün Nerede Duruyor?

`BIST_Sistem_Analiz_Raporu_update`'daki puanlama tablosu, sistemin bugünkü olgunluk düzeyini iyi özetliyor:

| Boyut | Puan |
|---|---|
| Mimari Tasarım | 8/10 |
| Veri Mühendisliği | 7/10 |
| Kod Kalitesi | 6/10 |
| Backtest Geçerliliği | 5/10 |
| Raporlama | 7/10 |
| Staj Projesi Olarak | 9/10 |

Bu proje, **151 farklı varlık sınıfına yönelik bir kitap uyarlamasının** BIST'e uygun 5 stratejiyle başlayıp, üç büyük mimari kriz (rolling→snapshot felaketi, I/O darboğazı, frontend hizalama krizi), en az iki sistematik hata-düzeltme dalgası (lookahead bias, smart skip) ve dört farklı bağımsız öz-eleştiri turu (Faz1 → sistem_analizi → sistem_ekspertiz → bist_system_analysis) geçirerek, **90 stratejilik, 63-93 hisseli, akademik etiketleme katmanlı, sanallaştırılmış web terminaline sahip bir kantitatif araştırma platformuna** dönüşmüştür.

Sistemin kendisi bir "canlı ticaret botu" değildir ve kaynak belgelerin kendisi de bunu defalarca vurgulamaktadır — ama **disiplinli bir karar destek ve araştırma altyapısı** olarak, hem mimari olgunluğu hem de kendi sınırlarını tanıma dürüstlüğü bakımından bir staj projesinin standart beklentilerinin belirgin biçimde üzerindedir.

---

*Bu rapor, herhangi bir kaynak kodu değiştirmeden, yalnızca statik analiz ve belge çapraz karşılaştırması yoluyla hazırlanmıştır.*
