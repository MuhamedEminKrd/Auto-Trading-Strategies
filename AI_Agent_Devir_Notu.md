# AI Agent Devir Notu — AutoTradingStrategies Projesi Tam Bağlamı
### (Bir sonraki yapay zeka asistanının, bu projeyi sıfırdan keşfetmeden devralabilmesi için hazırlanmıştır)

> **Bu belge ne için var?** Kullanıcı bu konuşmadan sonra farklı bir yapay zeka asistanına/aracına geçecek. Bu belge, o yeni asistanın (1) projeyi teknik olarak, (2) kullanıcının kim olduğunu ve nasıl çalıştığını, (3) bu ana kadar nelerin yapılıp nelerin yapılmadığını, (4) hangi kararların neden alındığını **hiçbir ek araştırma yapmadan** anlayabilmesi için yazılmış, kasıtlı olarak uzun ve kendi içinde yeterli (self-contained) bir devir/bağlam belgesidir. Yeni asistan bu belgeyi okuduktan sonra, sanki bu konuşmanın tamamını kendisi yürütmüş gibi devam edebilmelidir.
>
> **Bu belgeyi kim, ne zaman yazdı?** Claude (Anthropic, Sonnet 5 modeli), Ağustos 2026 sonunda, kullanıcının "AutoTradingStrategies" adlı projesini uçtan uca analiz ettiği bir oturumun sonunda, oturumdan ayrılmadan önceki son adım olarak hazırlanmıştır. **Bu oturumda hiçbir kaynak kod dosyası değiştirilmemiştir** — yalnızca okuma/analiz yapılmış, üç yeni Markdown raporu üretilmiştir (bu belge dahil).

---

## BÖLÜM 0 — HIZLI ÖZET (30 Saniyede Proje)

Kullanıcı, bir üniversite stajı kapsamında, Borsa İstanbul (BIST) hisseleri üzerinde **90 farklı algoritmik ticaret stratejisini** (RSI, MACD, Bollinger, Ichimoku, mum formasyonları vb.), **VectorBT** kütüphanesiyle vektörize biçimde, 63-93 hisse üzerinde geriye dönük test eden (backtest) bir sistem geliştirdi. Sistem `Python` (backtest motoru + FastAPI backend) ve `React` (web dashboard) olmak üzere iki ana parçadan oluşuyor. Proje, **`151-trading-strategies`** adlı bir GitHub reposundan (kitap uyarlaması, DOW30 odaklı, 151 çok-varlıklı strateji) başlayıp, üç büyük mimari krizden geçerek bugünkü **`Auto_Trading_Strategies`** (BIST'e özel, 90 strateji, akademik metrik katmanlı) haline evrildi. Kullanıcı şu an bu sistemi konu alan bir **akademik makale** yazıyor ve bir **staj jürisine sunum** yapacak. Bu oturumda kullanıcının talebi üzerine üç analiz belgesi üretildi (bkz. Bölüm 8), hiçbir kod değiştirilmedi.

---

## BÖLÜM 1 — KULLANICI PROFİLİ

- **Kim:** Bir mühendislik/bilgisayar öğrencisi, staj kapsamında algoritmik ticaret/kantitatif finans projesi yürütüyor. E-posta: `muhammedkrd0124@gmail.com` (yalnızca kimlik/attribution amaçlı biliniyor, dış bir servise gönderilmemeli).
- **Teknik seviye:** Python, pandas, VectorBT, React/Vite konusunda ileri düzeyde uygulamalı bilgiye sahip; git kullanıyor (commit geçmişiyle kurtarma yapabilecek kadar). Finans/backtest kavramlarına (Sharpe, Sortino, overfitting, lookahead bias) hakim.
- **Danışman(lar):** Kaynak belgelerde **"Hüseyin Hoca"** (ilk görevi veren — 68 stratejiyi DOW30'a uygulama talimatı) ve **"Yunus Hoca"** (daha sonra walk-forward analizi önerisini mail ile ileten) isimleri geçiyor. İki isim farklı bağlamlarda anılıyor — aynı kişi mi farklı kişiler mi olduğu belgelerden kesin anlaşılamıyor, bu haliyle aktarılmalı, varsayımda bulunulmamalı.
- **Hedefi:** (1) Akademik bir makale yazmak (muhtemelen Borsa Istanbul Review, Quantitative Finance gibi bir dergiye), (2) staj bitiminde jüriye sunum yapmak.
- **Çalışma tarzı (bu oturumdan gözlemlenen):**
  - **Doğrudan ve nettir.** Belirsiz/geniş listeler yerine "en iyisini söyle" der (bkz. `AIWriting.md`'deki "saçma sapan modeller değil" örneği).
  - **Birden fazla AI aracı/model kullanıyor** ve bunları bilinçli olarak karşılaştırıyor (Gemini 3.1 Pro, Claude Sonnet 4.6, Antigravity IDE — VSCode tabanlı çok-modelli bir ortam). Şimdi de "başka bir agent'a geçeceğim" diyerek bu davranışını sürdürüyor — **bu normal, tekrarlayan bir davranış paterni, endişe edilecek bir şey değil.**
  - **Uzun, kapsamlı, bölümlere ayrılmış raporlar istiyor** ("uzun olabildiğince uzun" ifadesi hem `AIWriting.md`'de hem bu oturumda tekrar etti — bu, kullanıcının **tekrarlayan bir tercihi**).
  - **Bazen "öğrenciye anlatır gibi en basite indirgeyerek" açıklama istiyor** — teknik derinlik ile pedagojik sadelik arasında geçiş yapabiliyor, talebe göre ayarlanmalı.
  - **Kod değişikliği konusunda çok nettir ve talimatlarına harfiyen uyulmasını bekler.** Bu oturumda "hiçbir koda dokunma, hiçbir düzeltme yapma" dedi ve buna tam uyuldu — sadece analiz/rapor üretildi. **Önceki bir oturumda ise (kaynak: `clainingvektor.md`) frontend'e yapılan istenmeyen bir CSS müdahalesi için net bir uyarı verdiği kayıtlı:** *"Bir yeri yaparken diğer yeri bozuyorsun, Claude ile yaptığım frontta karışma."* → **Ders: Bu kullanıcı, istenmeyen/istek dışı kod değişikliklerine karşı çok hassas. Yeni bir görev başladığında, "kod değiştirebilir miyim yoksa sadece mi analiz/tavsiye istiyorsun?" ayrımını baştan netleştirmek güvenli bir yaklaşımdır.**
  - Dosyaları hem proje kök dizinine (örn. `AIWriting.md`, `clainingvektor.md`) hem de `Staj_Raporlari/` klasörüne kaydediyor; yeni analiz belgeleri genelde `Staj_Raporlari/` içine gidiyor.
  - Belgelerini kronolojik/düzenli tutmuyor — kendisi de bunu kabul ediyor ("md dosyaları sıralı ve düzenli değil haberin olsun" dedi bu oturumda). Yeni asistan bunu bir kusur olarak değil, kullanıcının doğal çalışma tarzı olarak kabul etmeli.

---

## BÖLÜM 2 — PROJENİN TAM KRONOLOJİK TARİHÇESİ (Kendi İçinde Yeterli Anlatı)

### 2.1 Başlangıç: "151 Trading Strategies" (Temmuz 2026)

Proje, GitHub'daki `151-trading-strategies` (kullanıcı adı: `MuhamedEminKrd`) reposundan başladı — bu, "151 Trading Strategies" adlı bir kitabın Python/FastAPI uyarlamasıydı. Stratejiler varlık sınıfına göre klasörlenmişti (`stocks/`, `crypto/`, `fx/`, `commodities/`, `fixed_income/`, `futures/`, `etfs/`, `macro/`, `real_estate/`, `distressed/`, `misc/`, `structured/`, `index/`), her biri bir FastAPI endpoint'iydi, **hiç backtest motoru yoktu**. Görev: Danışmanın talimatıyla 68 stratejiyi DOW30'daki 30 hisseye uygulayıp backtest sonucu üretmek.

**Kritik keşif:** Stratejiler 3 farklı formatta çıktı üretiyordu (`signal` / `weights` / `long_assets`+`short_assets`). Bunu birleştirmek için `signals_adapter.py` (`normalize_signals()`) yazıldı.

**İlk çalışan sistem:** `run_analysis.py`, rolling (yürüyen pencere — her gün için son 100 fiyat stratejiye veriliyor) sinyal üretimiyle 4 strateji (single_ma, two_ma, three_ma, channel) × 30 hisse (DOW30) = 120 backtest başarıyla çalıştı.

**Büyük Kriz #1 — "68 Strateji Zorlaması Felaketi":** Kalan 64 stratejiyi de zorla eklemeye çalışırken, rolling mimari "tek seferlik snapshot sinyal" mantığıyla değiştirildi. **Sonuç: çalışan 4 strateji dahil TÜM sistem 0 işlem üretmeye başladı.** Kullanıcının o anki tepkisi: *"tüm stratejiler 0 a 0 üretiyor çalışanlar da bozuldu her şey gitti kardeşim böyle."* **Kurtarma:** `git checkout <hash> -- run_analysis.py` ile son çalışan commit'e (`ea4a2cf`) dönüldü.

**Kök Neden Analizi:** AST ile 68 stratejinin tamamı otomatik analiz edildi, 3 engel kategorisi bulundu:
1. **Eksik dışsal veri** (sentiment_crypto, weather_risk, economic_announcements, hedging_pressure — Twitter, hava durumu, COT raporu gibi yfinance'te olmayan veriler)
2. **Yapısal uyumsuzluk** (carry_factor, fix_and_flip, cdo_tranche, roll_yields — tahvil/gayrimenkul/türev'e özgü parametreler)
3. **Çoklu varlık zorunluluğu** (pairs_trading, stat_arb, contrarian — korelasyon matrisi gerektiren stratejiler)

Bu analiz `Staj_Raporlari/strategy_requirements.md` (68 stratejinin Türkçe veri kataloğu) olarak belgelendi ve hocaya açıklayıcı bir mail yazıldı.

### 2.2 Pivot Kararı: Sıfırdan BIST'e Özel Sistem

**En kritik mimari karar:** *"Bu 151 repo üzerine mi çalışalım, yoksa sıfırdan mı kuralım?"* → **Sıfırdan, temiz bir `vbt_bist/` klasörü kurmak.** Gerekçe: eski, çoklu-varlık odaklı kodlara dokunmak daha fazla karmaşıklık yaratacaktı. Bu andan itibaren proje, 151-repodan yalnızca birkaç basit fikri (single_ma, two_ma, three_ma, mean_reversion mantığı) miras alarak, BIST'e özel, sadece OHLCV verisiyle çalışan **sıfırdan bir sistem** olarak yeniden inşa edildi.

**Teknoloji yığını değişti:** FastAPI-endpoint + manuel rolling for-loop → doğrudan `vectorbt` vektörize backtest. Veri kaynağı → `yfinance`. Grafik → `plotly`+`kaleido`. Raporlama → `master_rapor_olustur.py`.

### 2.3 Mimari Evrim Aşamaları (vbt_bist içinde)

1. **Tek dosyalı "spagetti" kod** (`two_ma_strategy.py`, `three_ma_strategy.py` — her biri kendi veri çekme+backtest+kayıt mantığını içeriyordu) → **terk edildi**, hisse kodu hardcoded ve yeni strateji eklemek çok zordu.
2. **Merkezi `main.py` + `strategies/` klasörü:** Her strateji ayrı `.py` dosyası, tek bir `calistir()` fonksiyonu.
3. **Dinamik `importlib` sistemi:** `main.py`'ye hiç dokunmadan, sadece `strategies/` klasörüne dosya atarak yeni strateji eklenebilir hale geldi.
4. **`inspect.signature` ile Dependency Injection:** Her stratejinin `calistir()` imzası otomatik okunuyor, yalnızca ihtiyaç duyduğu veri (kapanış/açılış/yüksek/düşük/hacim) gönderiliyor.
5. **`strategies/utils.py` ile merkezi VBT ayarları:** `init_cash=10000`, `fees=0.001` (%0.1), `slippage=0.002` (%0.2), `freq='1d'` — tek yerden yönetiliyor, 90 dosyanın hiçbirinde artık hardcoded değil (bu oturumda grep ile doğrulandı).
6. **Smart Skip (Akıllı Atlama):** Çıktı klasörü zaten varsa ve veri kaynağından güncel ise, o hisse-strateji kombinasyonu tekrar hesaplanmadan atlanıyor. **Önemli bug ve düzeltmesi:** Başlangıçta `startswith()` kullanılıyordu, bu yüzden `rsi_macd` klasörünü gören sistem `rsi` stratejisini yanlışlıkla "zaten hesaplanmış" sanıyordu → tam eşleşme (`==`) ile düzeltildi (bugünkü `main.py`'de doğrulandı).

### 2.4 Strateji Kütüphanesinin Büyümesi (Dalga Dalga)

| Dalga | Ölçek | İçerik |
|---|---|---|
| Dalga 0 | 5 strateji | single_ma, two_ma, three_ma, bollinger, mean_reversion |
| Dalga 1 | ~9-12 | RSI, MACD, SuperTrend, Donchian, ADX, Keltner, Ichimoku, MFI, Stochastic, Williams %R, AO, PSAR |
| Dalga 2 ("Faz 2.5") | ~20 | Z-Score, VIX Fix, HMA, Williams %R, AO, PSAR (kurumsal quant seti) |
| Dalga 3 | 40 | Golden Cross, StochRSI, Elder Ray, ATR Turtle, Chaikin Vol, VWAP, Klinger, Triple Screen, Pin Bar, Squeeze, Heikin Ashi (12 önerinin tamamı kabul edildi) |
| Dalga 4 (Final) | **90+** | Hacim (OBV/CMF/VPT/AD-Line), mum formasyonları, istatistiksel, momentum ailesi, alt. MA'lar, kombinasyon filtreleri |

**Bugün `vbt_bist/strategies/` klasöründe tam olarak 90 adet `.py` strateji dosyası var** (bu oturumda `find` komutu ile doğrulandı, `__init__.py` ve `utils.py` hariç).

### 2.5 Veri Mimarisi Evrimi: "Offline Data Lake"

Başlangıçta `main.py` her çalıştığında `yfinance`'den canlı veri çekiyordu (I/O bekleme darboğazı). **Çözüm:** Sistem ikiye bölündü:
- `data_fetcher.py`: Bağımsız script, **artımlı/delta** güncelleme yapıyor (sadece eksik son günleri indiriyor), `auto_adjust=True` ile temettü/bölünme düzeltmesi uyguluyor, sonucu `vbt_bist/data/*.csv`'ye yazıyor.
- `main.py`: İnternetle bağı tamamen koptu, yalnızca yerel CSV'leri okuyor.

Bu, "Offline Data Lake" mimarisi olarak adlandırıldı — tekrarlanabilirlik (reproducibility) ve hız sağladı.

### 2.6 Büyük Kriz #2 — I/O (Disk) Darboğazı ve Monkey-Patching Çözümü

93 hisse × 90 strateji = **8.370 backtest senaryosu**, her biri için Plotly HTML+PNG grafiği diske yazılıyordu → disk %100 doluyor, işlem saatlerce sürüyordu. **Çözüm (projeyi kurtaran en büyük mimari karar):** Grafik üretimi kalıcı olarak diskten kaldırıldı. Dashboard backend'de **"Monkey-Patching"** tekniği kullanıldı: kullanıcı bir grafiğe tıkladığında, `dashboard/backend/main.py` içindeki `run_strategy_and_get_portfoy()` fonksiyonu, `strategies.utils.sonuclari_kaydet` referansını çalışma anında bir "yakalayıcı" (`capture`) closure'ıyla değiştiriyor; strateji kodu normal şekilde çalışıyor ama sonucu diske yazmak yerine bir sözlükte (`captured`) yakalıyor; `Portfolio` nesnesi doğrudan RAM'den Plotly HTML/PNG'ye dönüştürülüp kullanıcıya gönderiliyor, hiçbir dosya diske yazılmıyor.

### 2.7 Büyük Kriz #3 — Frontend Çöküşü ve CSS Grid Çözümü

8.370 satırlık veri standart HTML tabloya basılınca tarayıcı donuyordu. **Çözüm 1:** `TanStack Virtual` ile DOM sanallaştırma (her an yalnızca ~15-20 satır render ediliyor). **Kriz 1.5:** Virtual scroll + `<table>` birlikte kullanılınca, `position:absolute` satırlar tablo sütun genişliği hesabına dahil olamadığından başlık/veri hizalaması bozuldu. **Çözüm 2:** `<table>` tamamen terk edildi, sabit piksel genişlikli **CSS Grid** düzenine geçildi (header ve satırlar aynı `gridTemplateColumns` ve aynı scroll container'ı paylaşıyor).

**Yan olay — "dokunma" politikası:** Frontend'de CSS düzeltmeleri denenirken bazı beklenmedik bozulmalar oldu, kullanıcı net talimat verdi (bkz. Bölüm 1), o andan sonra stabil frontend koduna dokunulmadı.

### 2.8 Hata Düzeltme Dalgası (Kod Denetimi → Plan → Uygulama)

Sıra: `implementation_plan_update_2` (derin kod denetimi, lookahead bias ve "az işlemli şanslı strateji" tuzağı tespit edildi) → `implementation_plan_updates` (7 maddelik numaralı düzeltme planı) → `walkthrough_2` (kullanıcının seçtiği 5 madde — 1,3,4,5,6 — uygulandı; **lookahead bias'ın kendisi o aşamada henüz düzeltilmemişti**). Lookahead bias'ın nihai/tam çözümü daha sonra (`optimizingAlgo.md`'de belgelendiği üzere) **tüm 90 strateji dosyasında** `.shift(1)` uygulanarak yapıldı — *"bugün sinyal, yarın açılıştan işlem"* mantığı.

Diğer önemli düzeltmeler: `hp_filter_ma.py` (Hodrick-Prescott filtresi matematiksel olarak geleceğe bakıyordu — lookahead bias'ın bir türü — saf EMA ile değiştirildi), `fractal_breakout.py` (imkânsız çıkış koşulu düzeltildi), `doji_reversal.py`/`heikin_ashi.py` (gerçek Açılış fiyatı eksikti, eklendi), delist hisseler (KOZAA, KOZAL) listeden çıkarıldı, `auto_adjust=True` eklendi.

### 2.9 Akademik Dönüşüm

Ham kâr/zarar raporlamasından, istatistiksel geçerlilik odaklı bir sisteme geçildi:
- **Alfa (α)** = Strateji Getirisi − Benchmark (Al-Tut) Getirisi
- **Risk-Ayarlı Getiri** = Kâr% / |Max Drawdown%|
- **Akademik Geçerlilik etiketi:** N (işlem sayısı) < 25 → "Yetersiz Veri"; Profit Factor = ∞ veya > 10 → "Overfitting Şüphesi"; aksi → "İstatistiki Olarak Güvenilir" (eşik değerleri zamanla sertleşti: önce N<10/PF>15 tartışıldı, sonra N<25/PF>10'a çekildi — daha katı akademik standart).
- **Walk-Forward önerisi** ("Yunus Hoca"dan gelen mail sonrası): Ana dashboard'u bozmamak için **ayrı, bağımsız bir script** (`makale_walk_forward_analizi.py` konsepti) olarak planlandı, ana sisteme entegre edilmedi — riskli deneysel işi stabil sistemden izole tutma kararı.

### 2.10 Rebranding ve Dashboard İnşası

Proje adı `151-trading-strategies` → `Auto_Trading_Strategies` (yerel klasör) / `Auto-Trading-Strategies` (GitHub) olarak değişti, git remote yeniden yapılandırıldı, profesyonel bir `README.md` yazıldı. Dashboard (`FastAPI` backend + `React`/`Vite` frontend), önce bir "Mimari Danışmanlık Raporu" (teknoloji seçimi gerekçeleri, güvenlik kontrol listesi, UX kararları) hazırlanıp sonra somut bir uygulama planına (`implementation_plan_updates3`) dönüştürülerek inşa edildi.

### 2.11 Bugünkü Durum (Ağustos 2026 sonu, bu devir belgesinin yazıldığı an)

- 90 strateji, 63-93 hisse, ~5.670-8.370 backtest senaryosu tamamlanmış durumda.
- Dashboard (backend+frontend) çalışır durumda, monkey-patching ve virtual scroll ile.
- Master Excel raporu (`Tum_Strateji_Metrikleri.xlsx`) 19 sütunlu, Alfa/Risk-Ayarlı/Akademik Etiket içeriyor.
- **Yapılmamış olanlar:** Walk-forward/out-of-sample test, survivorship bias düzeltmesi, portföy düzeyinde risk yönetimi, multiple testing düzeltmesi (Bonferroni/FDR), enflasyon ayarlaması, stop-loss (kasıtlı olarak terk edildi — bkz. Bölüm 6).
- Kullanıcı şu an makale yazım ve jüri sunumu hazırlığı aşamasında.

---

## BÖLÜM 3 — PROJE DOSYA/KLASÖR HARİTASI

```
Auto_Trading_Strategies/                    (proje kök dizini)
├── README.md                               (profesyonel proje tanıtımı, final haliyle)
├── AIWriting.md                            (kök) — AI model seçimi meta-sohbeti (teknik içerik yok)
├── clainingvektor.md                       (kök) — mühendislik günlüğü, I/O krizi + monkey-patching + akademik dönüşüm anlatımı
├── optimizingAlgo.md                       (kök) — EN KAPSAMLI gelişim günlüğü (mimari evrim, kriz listesi, ders çıkarımları)
├── suanakadarki.md                         (kök) — EN ERKEN belge (Temmuz 2026), 151-repo dönemi, DOW30, kök neden analizi
│
├── vbt_bist/                               ÇEKİRDEK BACKTEST MOTORU
│   ├── main.py                             orkestratör (importlib+inspect+multiprocessing+Smart Skip)
│   ├── data_fetcher.py                     yfinance veri indirme (artımlı, auto_adjust=True)
│   ├── master_rapor_olustur.py             tüm sonuçları birleştirip Alfa/Akademik Etiket ekleyen script
│   ├── requirements_vbt.txt
│   ├── data/                               93 hisse × CSV (Date,Open,High,Low,Close,Volume)
│   ├── output/                             HISSE/strateji_adi/ altında _ozet.csv, _islemler.csv + Tum_Strateji_Metrikleri.xlsx
│   └── strategies/                         90 adet .py strateji dosyası + utils.py (merkezi VBT ayarları) + __init__.py
│
├── dashboard/
│   ├── backend/main.py                     FastAPI: /api/metrics, /api/chart/html/{h}/{s}, /api/chart/png/{h}/{s}
│   └── frontend/                           React 19 + Vite
│       ├── package.json                    (@tanstack/react-table, react-virtual, lucide-react, xlsx)
│       └── src/App.jsx                     tek dosyalık ana UI (454 satır) — virtual scroll tablo + filtre sidebar + grafik paneli
│
├── venv/                                   Python sanal ortamı
│
└── Staj_Raporlari/                         TÜM AI-ÜRETİMİ ANALİZ/PLAN BELGELERİ (29+ dosya, kronolojik SIRALI DEĞİL)
    ├── Proje_Tam_Analiz_Raporu.md          ★ BU OTURUMDA ÜRETİLDİ — 11 bölümlük tam analiz (bkz. Bölüm 8 aşağıda)
    ├── Sistem_Eksikleri_ve_Cozumleri.md    ★ BU OTURUMDA ÜRETİLDİ — öğrenci-seviyesi eksik/çözüm belgesi
    ├── AI_Agent_Devir_Notu.md              ★ BU BELGENİN KENDİSİ
    ├── strategy_requirements.md            (Aşama 0) 68 stratejinin veri ihtiyacı kataloğu
    ├── Faz1_Sistem_Degerlendirme.md        (Aşama 1) ilk sert öz-eleştiri
    ├── Faz1_Bist100_Rehberi.md             (Aşama 1) SuperTrend/Stochastic/OBV/Donchian önerisi
    ├── Faz3_Gerceklige_Donus_Ameliyati.md  (Aşama 1, isim yanıltıcı!) Faz1'in cevabı — shift/slippage/stop-loss önerisi
    ├── Faz2_Strateji_Genisletme_Plani.md / implementation_plan.md (aynı içerik) (Aşama 2) MFI/Ichimoku/ADX/Keltner/Stochastic
    ├── Faz2_Uygulama_Gorevleri.md          (Aşama 2) görev takip listesi
    ├── i_p_2.md                            (Aşama 2, "Faz 2.5") Z-Score/VIX Fix/HMA/Williams%R/AO/PSAR
    ├── implementation_plan_update          (Aşama 3) Offline veri mimarisi PLANI
    ├── implementation_plan_new             (Aşama 3) Offline veri mimarisi SONUÇ raporu
    ├── implementation_plan_update_2        (Aşama 4) derin kod denetimi (lookahead bias keşfi)
    ├── implementation_plan_updates         (Aşama 4) 7 maddelik düzeltme planı
    ├── walkthrough_2                       (Aşama 4) düzeltmelerin uygulanma raporu (5/7 madde)
    ├── strateji_onerileri.md               (Aşama 5, "40 strateji" dönemi) 12 yeni strateji araştırması, akademik atıflı
    ├── egitim_ve_araclar.md                (Aşama 5) AI araçları + strateji önerisi + "strateji nasıl değerlendirilir" rehberi
    ├── sistem_analizi.md                   (Aşama 5, "40×40" dönemi) 6 meslek perspektifinden 360° değerlendirme
    ├── sistem_ekspertiz_raporu.md          (Aşama 6, "88 strateji" dönemi) sert denetim — long-only bias, survivorship bias
    ├── BIST_Sistem_Analiz_Raporu_update    (Aşama 6, final ölçek) 15 değişiklik dökümü + puan tablosu (Kod Kalitesi 6/10 dahil)
    ├── analysis_results.md / analysis_summary.txt (Aşama 6) final sonuç istatistikleri
    ├── Dashboard_Mimari_Danismanlik_Raporu.md (Aşama 7) dashboard teknoloji/güvenlik danışmanlığı
    ├── implementation_plan_updates3        (Aşama 7) somut dashboard uygulama planı (yukarıdaki rapora referans veriyor)
    ├── Sistem_Mimarisi_Semasi.md           (Aşama 8) Mermaid diyagramlı final mimari şeması
    ├── Tum_Stratejiler_Rehberi.md          (Aşama 8) 90 stratejinin final 7-kategori kataloğu
    ├── Veri_Tiplerine_Gore_Stratejiler.md  (Aşama 8) 90 stratejinin veri-tipi (Close/HLC/OHLC vb.) sınıflandırması
    ├── metric_formulas.md                  (Aşama 8) 15 metriğin formül sözlüğü
    ├── bist_system_analysis.md             (Aşama 9, EN AKADEMİK) survivorship/data-snooping bias, literatür atıfları, makale iskeleti
    ├── yeni.md                             (Aşama 9) jüri-sunumu için kısa mimari savunma özeti
    ├── makale_taslagi.md                   (Aşama 9) akademik makale taslağının kendisi
    ├── implementation_plan_update_2, walkthrough.md, implementation_plan_updates (yukarıda listelendi)
    ├── Filtrleri_Tum_Strateji_Metrikleri.xlsx  (Excel veri dosyası, açılmadı — binary)
    └── js/                                  (boş/kullanılmayan alt klasör)
```

**Kronoloji için altın kural:** Dosya adlarındaki "Faz1/Faz2/Faz3" numaraları **gerçek zaman sırasını yansıtmıyor.** Gerçek sıralama için yukarıdaki "(Aşama N)" etiketlerine güvenilmeli, dosya adına değil. Ayrıntılı gerekçe `Proje_Tam_Analiz_Raporu.md` Bölüm 8'de.

---

## BÖLÜM 4 — TEKNİK MİMARİ (Özet — Ayrıntı için `Proje_Tam_Analiz_Raporu.md` Bölüm 3-4)

```
yfinance API → data_fetcher.py (artımlı, auto_adjust=True) → vbt_bist/data/*.csv
                                                                        │
main.py (importlib dinamik keşif + inspect.signature DI + Smart Skip  │
         + ProcessPoolExecutor multiprocessing) ◄──────────────────────┘
    │
    ├─► strategies/*.py (90 modül, her biri calistir() içerir)
    │       └─► vbt.Portfolio.from_signals() (utils.py'deki merkezi
    │           fees=0.001, slippage=0.002, init_cash=10000 ile)
    │       └─► utils.sonuclari_kaydet() → output/HISSE/strateji/*.csv
    │
    └─► (bitince otomatik) subprocess.run(master_rapor_olustur.py)
            └─► glob(**/*_ozet.csv) → Alfa/Risk-Ayarlı/Akademik-Etiket
                ekle → Tum_Strateji_Metrikleri.xlsx

dashboard/backend/main.py (FastAPI)
    ├─► /api/metrics → Excel'i JSON olarak servis eder
    └─► /api/chart/html|png/{hisse}/{strateji}
            └─► "Monkey-Patching": strategies.utils.sonuclari_kaydet'i
                runtime'da bir capture() closure'ıyla değiştirir,
                stratejiyi tekrar çalıştırır, Portfolio nesnesini
                RAM'den yakalar, diske hiç yazmadan Plotly HTML/PNG üretir
                (run_in_executor ile thread pool'a devredilir — async
                event loop bloklanmaz)

dashboard/frontend/src/App.jsx (React 19 + Vite)
    ├─► TanStack Virtual: 8.370 satırdan yalnızca ekrandaki ~20'si DOM'da
    ├─► CSS Grid (getColWidth + ortak gridTemplateColumns): header/body
    │   hizalaması table yerine grid ile garanti altına alınmış
    ├─► Sol sidebar: her sütun için accordion filtre (sayısal: operatör+
    │   değer; metinsel: checkbox listesi)
    └─► xlsx kütüphanesiyle tamamen frontend'de Excel export
```

**Anahtar tasarım ilkeleri:** (1) Dinamik keşif/Open-Closed Principle, (2) Dependency Injection (inspect.signature), (3) Smart Skip/caching, (4) Merkezi ekonomik model (utils.py).

---

## BÖLÜM 5 — 90 STRATEJİNİN 7 KATEGORİSİ (Kısa Referans)

1. **Trend/MA** (16): alma, dema, ema_cross, golden_cross, hma, macd, ppo, rainbow_ma, single_ma, tema, three_ma, trix, two_ma, vwma, wma, zlema
2. **Osilatör/Momentum** (16): awesome_oscillator, cci, cmo, connors_rsi, coppock, dpo, kst, momentum, roc, rsi, schaff_trend, stoch_rsi, stochastic, tsi, ultimate_osc, williams_r
3. **Volatilite/Kanal** (14): atr_breakout, atr_channel, bb_width, bollinger, chaikin_vol, chandelier, donchian, hist_vol, historical_vol_rank, keltner, natr, squeeze, std_channel, true_range_ema
4. **Hacim/Para Akışı** (11): ad_line, cmf, eom, klinger, mfi, nvi, obv, obv_ma, pvi, vpt, vwap
5. **Fiyat Aksiyonu/Mum** (11): doji_reversal, engulfing, fractal_breakout, hammer, heikin_ashi, inside_bar, marubozu, morning_star, pin_bar, rsi_divergence, three_soldiers
6. **Karmaşık/Kantitatif** (13): elder_ray, hp_filter_ma, ibs, ichimoku, linreg, mass_index, mean_reversion, rvi, supertrend, trend_intensity, vix_fix, volatility_breakout, zscore
7. **Kombine/Filtreli** (8): adx, adx_macd, bb_rsi, ichimoku_rsi, psar, rsi_macd, supertrend_rsi, triple_screen

**Bulgular (final veri, 63 hisse):** En tutarlı strateji **RSI(14,30,70)** (ortalama≈medyan≈%21.8, %72 kazanma oranı). En yüksek ortalama getiri **Ultimate Oscillator(7,14,28)** (%31.97, ama yüksek std). En kötüler: RVI, IBS, Klinger, Heikin Ashi. En kazandıran hisseler: ASELS, ASTOR, TKFEN. En kaybettirenler: KONTR, VESBE, ARZUM.

---

## BÖLÜM 6 — BİLİNEN EKSİKLİKLER (Tam Liste `Sistem_Eksikleri_ve_Cozumleri.md`'de)

**Kod Kalitesi:** sessiz `except: pass` hataları (main.py:126-128, hâlâ mevcut), test yokluğu (90 stratejinin hiçbiri test edilmiyor), hardcoded ayarlar (config dosyası yok), **göreli/mutlak yol tutarsızlığı** (main.py'de `strateji_klasoru` mutlak yol ile doğru hesaplanırken, çıktı yolu `os.path.join("vbt_bist", "output", ...)` göreli — bu, bu oturumda Claude'un kendi başına bulduğu, hiçbir kaynak belgede geçmeyen bir sorun), loglama sistemi yok (`print()` kullanılıyor), versiyon izlenebilirliği yok, Smart Skip bozuk dosyayı fark etmiyor, dashboard'daki monkey-patching global state kullandığı için **çok kullanıcılı senaryoda teorik race condition riski taşıyor** (yine Claude'un kendi tespiti).

**Dashboard Güvenliği:** whitelist/girdi doğrulama yok, rate limiting yok, timeout yok (Dashboard Mimari Danışmanlık Raporu'nda önerilmişti ama `dashboard/backend/main.py`'nin bugünkü halinde uygulanmamış — bu oturumda karşılaştırılarak tespit edildi).

**Akademik/Finansal (Kod kalitesinden daha ciddi, makale için önemli):** Survivorship bias, data snooping/çoklu test sorunu (5.670-8.370 test, Bonferroni/FDR düzeltmesi yok), walk-forward/out-of-sample test yok, long-only/boğa piyasası yanılgısı, portföy düzeyinde risk yönetimi yok, enflasyona göre reel getiri hesaplanmıyor, piyasa rejimi körlüğü, basit/tek-tip komisyon modeli (BSMV dahil değil).

**Not — Kod Kalitesi "6/10" puanı:** Bu puan `BIST_Sistem_Analiz_Raporu_update` belgesinin kendi öz-değerlendirmesidir, Claude'un bağımsız değerlendirmesi değildir. Claude'un bağımsız değerlendirmesi bu konuşmada verildi: ~6.5-7/10, çünkü belgenin gerekçelerinden biri (VBT ayar tutarsızlığı) artık geçersiz (grep ile doğrulandı — tüm strateji dosyaları merkezi `utils.py` ayarlarını kullanıyor), ama sessiz hata yutma ve test eksikliği hâlâ geçerli.

---

## BÖLÜM 7 — TERK EDİLEN / ERTELENEN KARARLAR (Tekrar Sorulmasın Diye)

| Fikir | Durum | Neden |
|---|---|---|
| Stop-Loss (`sl_stop=0.07`) | **Bilinçli olarak terk edildi** | Ayrı bir optimize edilmesi gereken parametre; eklemek 8.370 senaryonun yeniden hesaplanmasını gerektirir; akademik karşılaştırma için tüm stratejiler aynı koşulda tutulmalı |
| Gerçek zamanlı sinyal botu | Ertelendi (kapsam dışı) | Düzenleyici kısıtlar, API entegrasyonu, backtest metodolojisi henüz olgunlaşmadı |
| ML/Random Forest strateji seçimi | Ertelendi (kapsam dışı) | Danışman onayı yok, out-of-sample test olmadan yeni overfitting riski |
| Walk-Forward'ı ana sisteme entegre etme | Ertelendi, izole edildi | Ana dashboard'u bozmamak için ayrı script planlanıyor, henüz yazılmadı |
| CSV/PNG/HTML çıktılarını Git'e gönderme | Terk edildi | `.gitignore`'a eklendi, binary dosyalar diff'lenemiyor |

---

## BÖLÜM 8 — BU OTURUMDA ÜRETİLEN ÜÇ BELGE (Ne İşe Yararlar)

1. **`Proje_Tam_Analiz_Raporu.md`** (11 bölüm, en kapsamlı): Giriş → Proje kökeni (151→BIST pivot) → Sistem mimarisi → Kodlama mantığı (dosya dosya) → Strateji kütüphanesi → Mühendislik krizleri (neden-sonuç) → Terk edilenler → **`Staj_Raporlari/` klasörünün gerçek kronolojik haritası (9 aşama)** → Akademik kör noktalar → Bulgular özeti → Sonuç. **Makale ve jüri sunumu için birincil referans.**
2. **`Sistem_Eksikleri_ve_Cozumleri.md`**: Tüm eksiklikler (kod kalitesi + dashboard güvenliği + akademik metodoloji), her biri günlük-hayat benzetmesi + somut örnek + çözüm mantığıyla, öğrenci-seviyesinde basitleştirilmiş. **Öncelik tablosu içeriyor** (hangi sorun kritik/kolay). Kod değiştirilmedi, yalnızca "çözümün mantığı ne olurdu" gösterildi.
3. **`AI_Agent_Devir_Notu.md`** — bu belgenin kendisi.

**Bu üç belge birbirini tamamlıyor:** 1. genel bağlam+tarih, 2. eksik/çözüm detayı, 3. bir sonraki asistan için hızlı devir. Yeni asistan, kullanıcının talebine göre bunlardan uygun olanı referans alabilir veya doğrudan güncelleyebilir (kullanıcı "bu raporu güncelle" derse, `url`/`file_path` aynı tutulup üzerine yazılabilir — ayrı bir dosya açmaya gerek yok, kullanıcı zaten bu üç dosyayı `Staj_Raporlari/` altında tutuyor).

---

## BÖLÜM 9 — YENİ ASİSTAN İÇİN ÖNERİLEN SONRAKİ ADIMLAR (Olası Senaryolar)

Kullanıcının bir sonraki adımda ne isteyeceği belirtilmedi, ama bağlamdan üç olası senaryo öngörülebilir:

**Senaryo A — Makale yazımı:** `makale_taslagi.md` ve `bist_system_analysis.md` zaten iyi bir iskelet sunuyor. `Proje_Tam_Analiz_Raporu.md`'deki Bölüm 9-10 (kör noktalar, bulgular) doğrudan "Tartışma" ve "Bulgular" bölümlerine aktarılabilir.

**Senaryo B — Jüri sunumu hazırlığı:** `yeni.md` zaten kısa bir savunma özeti. `Sistem_Eksikleri_ve_Cozumleri.md`'deki öncelik tablosu, "jüri şunu sorarsa böyle cevap ver" tarzı hazırlık için kullanılabilir.

**Senaryo C — Kod düzeltmelerinin fiilen uygulanması:** `Sistem_Eksikleri_ve_Cozumleri.md`'deki A grubu (kod kalitesi) maddeleri **hızlı ve düşük riskli** düzeltmelerdir (özellikle A.1 sessiz hatalar, A.4 yol tutarsızlığı) — kullanıcı isterse bunlar uygulanabilir. **Ancak: önceki oturumlarda kullanıcı frontend'e izinsiz dokunulmasından rahatsız olmuştu — herhangi bir kod değişikliğine başlamadan önce onay istemek güvenli bir yaklaşımdır**, özellikle strateji dosyalarında (90 dosya, sonuçların yeniden hesaplanması saatler sürebilir) veya dashboard frontend'inde.

**Genel tavsiye:** Yeni asistan, göreve başlamadan önce kullanıcıya *"bu görevde kod değiştirebilir miyim, yoksa yalnızca analiz/öneri mi istiyorsun?"* diye netleştirmeli — bu, kullanıcının önceki davranış paternine (Bölüm 1) dayanan en güvenli açılış hamlesidir.

---

## BÖLÜM 10 — DİKKAT EDİLMESİ GEREKEN İNCE NOKTALAR

- **"151" ile "90" rakamlarını karıştırma.** 151, projenin *terk edilen* orijinal mirasındaki toplam strateji sayısı (çoklu varlık sınıfı). 90, bugünkü BIST-özel, gerçekten çalışan strateji sayısı. İkisi arasında doğrudan bir "eleme" ilişkisi yok — 90'ın çoğu sıfırdan BIST için yazıldı, 151'den yalnızca birkaç basit fikir miras kaldı.
- **Danışman ismi tutarsızlığı** ("Hüseyin Hoca" / "Yunus Hoca") kaynak belgelerde olduğu gibi aktarılmalı, biri diğerinin yanlış yazımı gibi varsayılmamalı.
- **Faz numaraları kronolojiyi yansıtmıyor** — `Faz3_Gerceklige_Donus_Ameliyati.md` aslında `Faz1_Sistem_Degerlendirme.md`'nin doğrudan devamıdır, `Faz2` belgelerinden *önce* gelir.
- **Bu oturumda hiçbir kod dosyası değiştirilmedi.** Yalnızca üç yeni `.md` dosyası (Bölüm 8) oluşturuldu. `vbt_bist/`, `dashboard/` altındaki hiçbir dosyaya `Edit`/`Write` uygulanmadı — yalnızca `Read`/`Grep`/`Glob`/`Bash(find)` kullanıldı.
- **Kullanıcının e-postası** (`muhammedkrd0124@gmail.com`) yalnızca kimlik amaçlı biliniyor; hiçbir dış servise/isteğe dahil edilmemeli.
- Kullanıcı Windows/PowerShell + VSCode uzantısı (Claude Code) ortamında çalışıyor; proje kök dizini `c:\Users\MS\Desktop\Auto_Trading_Strategies`.

---

*Bu belge, `Proje_Tam_Analiz_Raporu.md` ve `Sistem_Eksikleri_ve_Cozumleri.md` ile birlikte okunduğunda, herhangi bir yapay zeka asistanının bu projeyi sıfırdan araştırmadan devralabilmesi için yeterli olacak şekilde tasarlanmıştır. Üçü birlikte toplam ~15.000 kelimelik bir bağlam paketi oluşturur.*
