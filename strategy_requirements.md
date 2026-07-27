# 68 Stratejinin Veri İhtiyaçları (Türkçe Açıklamalı)

Aşağıda her bir stratejinin çalışması için dışarıdan sisteme **tam olarak hangi verilerin** girilmesi gerektiği Türkçe ve anlaşılır bir dille özetlenmiştir.

---

## 1. HİSSELER (STOCKS)
*Sadece hisse fiyatları ile çalışanları sistemimize kolayca entegre edebiliriz.*
- **single_ma (Tekli Hareketli Ortalama):** Sadece `Geçmiş Fiyatlar` lazım.
- **two_ma (İkili Hareketli Ortalama):** Sadece `Geçmiş Fiyatlar` lazım.
- **three_ma (Üçlü Hareketli Ortalama):** Sadece `Geçmiş Fiyatlar` lazım.
- **channel (Fiyat Kanalı):** Sadece `Geçmiş Fiyatlar` lazım.
- **support_resistance (Destek-Direnç):** Sadece dünün `En Yüksek`, `En Düşük`, `Kapanış` ve bugünün `Güncel Fiyatı` lazım.
- **price_momentum (Fiyat Momentumu):** Kıyaslanacak **birden fazla** hissenin `Geçmiş Fiyatları` lazım.
- **low_volatility (Düşük Oynaklık):** Kıyaslanacak **birden fazla** hissenin `Günlük Getirileri` lazım.
- **value (Değer Yatırımı):** Hisselerin `Defter Değeri (Book Value)` ve `Güncel Fiyatları` lazım.
- **implied_volatility (Zımni Oynaklık):** Opsiyon piyasasından alınan `Volatilite Değişim Oranları` lazım.
- **earnings_momentum (Bilanço Momentumu):** Şirketlerin çeyreklik `Bilanço Karlılık (Earnings)` verileri lazım.
- **residual_momentum (Artık Momentum):** Hissenin getirisi, `Piyasa Getirisi (Endeks)` ve Fama-French faktörleri (Şirket ölçeği ve değer rasyoları) lazım.
- **multifactor (Çoklu Faktör):** Hisselerin `Momentum Skorları`, `Volatilite Skorları` gibi önceden hesaplanmış faktör puanları lazım.
- **pairs_trading (İkili Ticaret):** Birbiriyle korele **iki farklı hissenin** `Geçmiş Fiyatları` lazım (Örn: Coca Cola ve Pepsi).
- **stat_arb (İstatistiksel Arbitraj):** Hisselerin `Beklenen Getirileri` ve birbirleriyle olan `Kovaryans Matrisi (İlişki Tablosu)` lazım.
- **market_making (Piyasa Yapıcılığı):** `Orta Fiyat`, `Anlık Volatilite` ve elimizdeki `Hisse Stoğu (Envanter)` lazım.
- **event_driven (Olay Odaklı/Birleşme):** Satın alınan şirketin `Hedef Fiyatı`, satın alan şirketin `Kendi Fiyatı`, `Teklif Edilen Ücret` ve `Anlaşma Olasılığı` lazım.

## 2. KRİPTO PARALAR (CRYPTO)
- **ann_crypto (Yapay Zeka ile Kripto):** Kripto paranın `Fiyatları` ve `İşlem Hacimleri` lazım.
- **sentiment_crypto (Sosyal Medya Duyarlılığı):** Twitter/Reddit gibi yerlerden çekilmiş `Duyarlılık Puanı (Örn: 1 ile 10 arası)`, `Atılan Tweet Sayısı` ve `Kripto Fiyatı` lazım.

## 3. EMTİA (COMMODITIES - Altın, Petrol, Buğday)
- **commodity_value (Emtia Değeri):** Birden fazla emtianın `Geçmiş Fiyatları` lazım.
- **hedging_pressure (Korunma Baskısı):** Emtia piyasasındaki büyük oyuncuların (üreticiler ve spekülatörler) `Pozisyon Büyüklükleri (COT Raporu)` lazım.
- **portfolio_diversification (Portföy Çeşitlendirmesi):** Emtiaların birbirleriyle olan `İlişki (Korelasyon) Tablosu` ve `Banka Faiz Oranı (Risksiz Getiri)` lazım.
- **roll_yields (Vade Yuvarlama Getirisi):** Yakın vadeli sözleşme `Fiyatı`, bir sonraki ayın `Fiyatı` ve `Vadeye Kalan Gün` lazım.
- **skewness_premium (Çarpıklık Primi):** Emtiaların geçmiş fiyat dalgalanmalarının `Çarpıklık (Asimetri) Oranı` lazım.

## 4. MAKRO EKONOMİ (MACRO)
- **economic_announcements (Ekonomik Haberler):** Gelecek haberin `Beklenen Değeri` (Örn: Beklenen enflasyon %3) ve açıklanan `Gerçek Değeri` lazım.
- **fundamental_macro (Temel Makro):** Ülkelerin makro ekonomik puanları (GSYH, enflasyon) ve yatırım yapılacak `Risk Bütçesi` lazım.
- **global_inflation_hedge (Küresel Enflasyon Koruması):** Varlıkların listesi ve hedeflenen `Enflasyon Koruma Oranı` lazım.

## 5. SABİT GETİRİLİLER (TAHVİL VE BONOLAR)
*Tahvil ve bonoların kendine has özellikleri vardır (Faiz, vade vb.)*
- **carry_factor (Taşıma Getirisi):** Tahvilin `Vadesi (Kaç yıl kaldı)`, `Getiri Oranı`, `Kupon Faizi` ve `Güncel Fiyatı` lazım.
- **barbells (Halter Stratejisi):** `Kısa Vadeli Tahviller` ve `Uzun Vadeli Tahvillerin` listesi lazım.
- **bond_immunization (Tahvil Aşılama):** Ödenmesi gereken `Gelecekteki Borç Miktarı` ve piyasadaki `Güncel Faiz Oranları` lazım.
- **cds_basis_arbitrage (CDS Arbitrajı):** Şirketin `Tahvil Getirisi`, `CDS (Kredi Temerrüt Takası) Primi` ve `Borçlanma Maliyeti` lazım.
- **yield_curve_spreads (Getiri Eğrisi Farkı):** Kısa vadeli faiz ile uzun vadeli faiz arasındaki `Geçmiş Farklar (Spread)` lazım.

## 6. DÖVİZ (FX)
- **fx_carry_trade (Faiz Farkı Ticareti):** Düşük faizli ülkenin para birimi ile yüksek faizli ülkenin para biriminin `Faiz Oranları` lazım.
- **fx_moving_averages (Döviz Trendi):** Kurun (Örn: USD/TRY) `Geçmiş Fiyatları` lazım.
- **fx_triangular_arb (Üçgen Arbitrajı):** Üç farklı kurun birbirine karşı anlık değerleri lazım (Örn: EUR/USD, USD/JPY, EUR/JPY) ve `İşlem Komisyon Oranı` lazım.

## 7. GAYRİMENKUL (REAL ESTATE)
- **fix_and_flip (Al-Yenile-Sat):** Evin `Satın Alma Maliyeti`, `Tadilat Masrafı`, `Tahmini Satış Fiyatı`, `Elde Tutma Süresi` ve `Kredi Faiz Oranı` lazım.
- **real_estate_diversity (Emlak Çeşitlendirmesi):** Konut, Ofis, AVM gibi farklı emlak türlerinin `Geçmiş Getirileri` ve yatırımcının `Risk Toleransı` lazım.
- **real_estate_inflation_hedge (Emlak Enflasyon Koruması):** Mülklerin değerleri, `Beklenen Enflasyon Oranı` ve `Hedeflenen Reel Getiri` lazım.

## 8. VADELİ İŞLEMLER (FUTURES)
- **calendar_spread (Takvim Yayılması):** Aynı varlığın `Yakın Vadeli` ve `Uzak Vadeli` sözleşme fiyatları ile `Elde Tutma Maliyeti` lazım.
- **contrarian (Zıt Yönlü İşlem):** Birçok vadeli işlemin (Örn: Pamuk, Bakır, Petrol) `Haftalık Getirileri` ve `Piyasa Ortalaması` lazım.
- **trend_following (Trend Takibi):** Vadeli işlem sözleşmelerinin `Geçmiş Fiyatları` lazım.

## 9. ETF VE FONLAR
- **alpha_rotation (Sektör Rotasyonu):** Sektör fonlarının (Örn: Teknoloji, Sağlık, Bankacılık) ayrı ayrı `Geçmiş Getirileri` ve piyasa ortalaması lazım.
- **leveraged_etfs (Kaldıraçlı Fonlar):** Kaldıraçlı fonların (2x, 3x) `Fiyatları` ile dayanak varlığın (Örn: Nasdaq 100) `Fiyatları` lazım.
- **mean_reversion (Ortalamaya Dönüş - IBS):** Fonun dünkü `Açılış, Yüksek, Düşük ve Kapanış` fiyatları lazım.

## 10. ENDEKSLER (INDEX)
- **cash_and_carry (Spot-Vadeli Arbitrajı):** Endeksin `Anlık Fiyatı (Spot)`, `Vadeli İşlem Fiyatı`, `Banka Faizi` ve `Temettü Verimi` lazım.
- **volatility_targeting (Oynaklık Hedefleme):** Endeksin `Geçmiş Getirileri` ve bizim hedeflediğimiz `Maksimum Risk (Oynaklık) Oranı` lazım.

## 11. SIKINTILI VARLIKLAR (DISTRESSED)
- **active_distressed (Batık Şirket Alma):** Şirketin `Mevcut Fiyatı`, `Toplam Borcu`, `Firma Değeri`, `Danışmanlık/Avukatlık Masrafları` ve hedeflenen `Operasyonel İyileşme Oranı` lazım.
- **distressed_debt (Batık Tahvil):** Tahvilin piyasa fiyatı, `Kurtarma (Geri Alma) Tahmini Oranı` ve `Yeniden Yapılandırma İhtimali` lazım.

## 12. ÇEŞİTLİ & VERGİ (MISC & TAX)
- **weather_risk (Hava Durumu Riski):** Geçmiş yılların `Isıtma ve Soğutma Günü Dereceleri (Hava Sıcaklık Verisi)` ve gelir kaybı beklentisi lazım.
- **spark_spread (Enerji Arbitrajı):** `Elektrik Fiyatı`, `Doğalgaz Fiyatı`, `Karbon Vergisi Fiyatı` ve santralin `Isı Üretim Verimliliği` lazım.
- **cross_border_tax (Sınır Ötesi Vergi):** Yabancı hissenin `Temettü Verimi`, ülkeler arası `Stopaj Vergisi Oranları` ve `Vergi İadesi Oranları` lazım.
- **muni_tax_arbitrage (Belediye Tahvili Vergi Arbitrajı):** Vergisiz belediye tahvili getirisi ile vergili devlet tahvili getirisi ve `Kişisel Gelir Vergisi Diliminiz` lazım.

## 13. YAPILANDIRILMIŞ ÜRÜNLER (STRUCTURED)
- **mbs_trading (İpoteğe Dayalı Menkul Kıymet):** MBS'nin fiyatı, kupon faizi ve ev sahiplerinin `Erken Ödeme Hızı (Prepayment Speed)` lazım.
- **cdo_tranche (Teminatlı Borç Yükümlülüğü):** CDO dilimlerinin faiz oranları, beklenen `Temerrüt (Batağa Düşme) Oranları` ve `Kurtarma Oranları` lazım.
- **cdo_cds_hedging (CDO/CDS Riskten Korunma):** CDO'nun dilim özellikleri ve piyasadaki `Kredi Temerrüt Takas (CDS) Oranları` lazım.
