"""
============================================================
  BIST Algoritmik Strateji Test Sistemi — Komuta Merkezi
============================================================

KULLANIM:
  1. Aşağıdaki HISSE_LISTESI değişkenine istediğin hisseleri yaz.
  2. Dosyayı çalıştır. Sonuçlar otomatik olarak her hisse için ayrı ayrı kaydedilir.

BIST Hisse Örnekleri:
  GARAN.IS  → Garanti Bankası
  AKBNK.IS  → Akbank
  THYAO.IS  → Türk Hava Yolları
  ASELS.IS  → Aselsan
"""

import yfinance as yf
import sys
import os
import pandas as pd

# strategies klasörünün bulunduğu dizini Python'a tanıtalım
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from strategies import (
    single_ma, two_ma, three_ma, bollinger, mean_reversion, rsi, macd, 
    supertrend, donchian, mfi, ichimoku, adx, keltner, stochastic,
    zscore, vix_fix, hma, williams_r, awesome_oscillator, psar
)

# ============================================================
#  TEST ETMEK İSTEDİĞİN TÜM HİSSELERİ BU LİSTEYE YAZ
# ============================================================
HISSE_LISTESI = [
    "AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "VAKBN.IS",
    "THYAO.IS", "PGSUS.IS", "TAVHL.IS",
    "KCHOL.IS", "SAHOL.IS", "SISE.IS", "ENJSA.IS",
    "FROTO.IS", "TOASO.IS", "TUPRS.IS",
    "BIMAS.IS", "MGROS.IS", "SOKM.IS", "AEFES.IS", "CCOLA.IS",
    "ASELS.IS", "TCELL.IS", "TTKOM.IS", "MIATK.IS", "KONTK.IS",
    "EREGL.IS", "KRDMD.IS", "ASTOR.IS", "KOZAL.IS", "ODAS.IS",
    "ALFAS.IS", "ENKAI.IS", "GWIND.IS", "CWENE.IS", "EUPWR.IS",
    "EKGYO.IS", "HEKTS.IS", "SASA.IS", "GUBRF.IS", "VESBE.IS"
]
VERI_SURESI = "2y"  # Kaç yıllık veri? (ör: "1y", "2y", "3y")
# ============================================================

for HISSE_KODU in HISSE_LISTESI:
    baslik = HISSE_KODU.split(".")[0]

    # --- Veriyi Sadece 1 Kez İndir ---
    print(f"\n{'='*50}")
    print(f"  {HISSE_KODU} verisi indiriliyor ({VERI_SURESI})...")
    print(f"{'='*50}")

    try:
        veri = yf.download(HISSE_KODU, period=VERI_SURESI, interval="1d")
        kapanis = veri['Close'][HISSE_KODU]
        yuksek = veri['High'][HISSE_KODU]
        dusuk = veri['Low'][HISSE_KODU]
        hacim = veri['Volume'][HISSE_KODU]
        print(f"  Toplam {len(kapanis)} günlük veri indirildi.\n")
        
        # --- YENİ EKLENEN KONTROL ---
        if kapanis.empty or len(kapanis) == 0:
            print(f"  [UYARI] {HISSE_KODU} verisi BOŞ geldi. Atlanıyor...")
            continue
        # ----------------------------

    except Exception as e:
        print(f"  [HATA] {HISSE_KODU} verisi indirilemedi: {e}")
        continue


    sonuclar = {}


    # Format: (Ekran Adı, Sözlük Anahtarı, Fonksiyon, (Zorunlu Argümanlar), {Parametreler})
    stratejiler = [
        ("Single MA", "single_ma", single_ma.calistir, (kapanis, baslik), {'periyot': 20}),
        ("Two MA", "two_ma", two_ma.calistir, (kapanis, baslik), {'hizli_periyot': 10, 'yavas_periyot': 50}),
        ("Three MA", "three_ma", three_ma.calistir, (kapanis, baslik), {'hizli_periyot': 5, 'orta_periyot': 20, 'yavas_periyot': 50}),
        ("Bollinger Bantları", "bollinger", bollinger.calistir, (kapanis, baslik), {'periyot': 20, 'std_sapma': 2.0}),
        ("Mean Reversion", "mean_reversion", mean_reversion.calistir, (kapanis, baslik), {'periyot': 20, 'sapma_katsayisi': 1.5}),
        ("RSI", "rsi", rsi.calistir, (kapanis, baslik), {'periyot': 14, 'alt_sinir': 30, 'ust_sinir': 70}),
        ("MACD", "macd", macd.calistir, (kapanis, baslik), {'hizli': 12, 'yavas': 26, 'sinyal': 9}),
        ("SuperTrend", "supertrend", supertrend.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 10, 'carpan': 3.0}),
        ("Donchian Kanalı", "donchian", donchian.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 20}),
        ("Para Akışı (MFI)", "mfi", mfi.calistir, (yuksek, dusuk, kapanis, hacim, baslik), {'periyot': 14, 'alt_sinir': 20, 'ust_sinir': 80}),
        ("Ichimoku Bulutu", "ichimoku", ichimoku.calistir, (yuksek, dusuk, kapanis, baslik), {'t_periyot': 9, 'k_periyot': 26, 's_periyot': 52}),
        ("ADX Trend Gücü", "adx", adx.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 14, 'adx_sinir': 25}),
        ("Keltner Squeeze", "keltner", keltner.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 20, 'carpan': 2.0}),
        ("Stokastik Osilatör", "stochastic", stochastic.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 14, 'k_periyot': 3, 'alt_sinir': 20, 'ust_sinir': 80}),
        ("Z-Score Mean Reversion", "zscore", zscore.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 20, 'alt_sapma': -2.0, 'ust_sapma': 0.0}),
        ("Williams VIX Fix", "vix_fix", vix_fix.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 22, 'bb_periyot': 20, 'bb_sapma': 2.0}),
        ("Hull Moving Average", "hma", hma.calistir, (yuksek, dusuk, kapanis, baslik), {'hizli': 20, 'yavas': 50}),
        ("Williams %R", "williams_r", williams_r.calistir, (yuksek, dusuk, kapanis, baslik), {'periyot': 14, 'alt_sinir': -80, 'ust_sinir': -20}),
        ("Awesome Oscillator", "ao", awesome_oscillator.calistir, (yuksek, dusuk, kapanis, baslik), {'hizli': 5, 'yavas': 34}),
        ("Parabolic SAR", "psar", psar.calistir, (yuksek, dusuk, kapanis, baslik), {'accel_step': 0.02, 'accel_max': 0.2}),
    ]

    toplam_strateji = len(stratejiler)

    for i, strat in enumerate(stratejiler, 1):
        ekran_adi, sozluk_anahtari, fonksiyon, args, kwargs = strat
        
        print(f"--- [{i}/{toplam_strateji}] {ekran_adi} Çalışıyor ---")
        ozet = fonksiyon(*args, **kwargs)
        sonuclar[sozluk_anahtari] = ozet['Total Return [%]']


    # ============================================================
    #  ÖZET KARŞILAŞTIRMA TABLOSU
    # ============================================================
    print(f"\n{'='*50}")
    print(f"  {baslik} — STRATEJİ KARŞILAŞTIRMA SONUÇLARI")
    print(f"{'='*50}")
    print(f"  {'Strateji':<20} {'Net Kar / Zarar':>15}")
    print(f"  {'-'*36}")
    for strateji, getiri in sorted(sonuclar.items(), key=lambda x: x[1], reverse=True):
        isaret = "[KAR]" if getiri > 0 else "[ZAR]"
        print(f"  {isaret} {strateji:<18} %{getiri:>10.2f}")
    print(f"{'='*50}")
    print(f"  Ciktilar >> vbt_bist/output/{baslik}/ klasorunde")
    print(f"{'='*50}\n")
    
    # Sonuclari Excel'e kaydet
    df_sonuclar = pd.DataFrame(list(sonuclar.items()), columns=['Strateji', 'Net Kar [%]'])
    df_sonuclar = df_sonuclar.sort_values(by='Net Kar [%]', ascending=False)
    excel_yolu = os.path.join("vbt_bist", "output", baslik, f"{baslik}_Karsilastirma.xlsx")
    df_sonuclar.to_excel(excel_yolu, index=False)
    print(f"  [EXCEL] Sonuçlar başarıyla kaydedildi: {excel_yolu}\n")

print(f"\n{'='*50}")
print("  TÜM HİSSELERİN ANALİZİ BAŞARIYLA TAMAMLANDI!")
print(f"{'='*50}\n")
#test mesajı