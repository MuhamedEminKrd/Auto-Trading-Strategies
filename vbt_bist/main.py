"""
============================================================
  BIST Algoritmik Strateji Test Sistemi — Komuta Merkezi
============================================================
"""

import yfinance as yf
import sys
import os
import pandas as pd
import importlib
import inspect

# Pandas Future Warnings (Sarı Uyarılar) Kapatma
pd.set_option('future.no_silent_downcasting', True)
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
VERI_SURESI = "2y"  # Tekrar 2 Yıla çıkarıldı
# ============================================================

strateji_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strategies")

# TÜM HİSSELERİN ŞAMPİYONLARINI TUTACAK LİSTE
genel_sampiyonlar = []

for HISSE_KODU in HISSE_LISTESI:
    baslik = HISSE_KODU.split(".")[0]

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
        
        if len(kapanis) < 50:
            print(f"  [UYARI] {HISSE_KODU} için yeterli veri yok, atlanıyor.")
            continue

        sonuclar = {}

        moduller = [f[:-3] for f in os.listdir(strateji_klasoru) if f.endswith('.py') and f != '__init__.py']
        toplam_strateji = len(moduller)

        veri_deposu = {
            'kapanis_fiyatlari': kapanis,
            'kapanis': kapanis,
            'yuksek': yuksek,
            'dusuk': dusuk,
            'hacim': hacim,
            'baslik': baslik
        }

        for i, modul_adi in enumerate(moduller, 1):
            try:
                modul = importlib.import_module(f"strategies.{modul_adi}")
                if not hasattr(modul, "calistir"): continue
                    
                fonksiyon = modul.calistir
                sig = inspect.signature(fonksiyon)
                fonksiyon_argumanlari = {}
                
                for arg_adi in sig.parameters:
                    if arg_adi in veri_deposu:
                        fonksiyon_argumanlari[arg_adi] = veri_deposu[arg_adi]
                        
                print(f"--- [{i}/{toplam_strateji}] {modul_adi.upper()} Çalışıyor ---")
                
                ozet = fonksiyon(**fonksiyon_argumanlari)
                sonuclar[modul_adi] = ozet['Total Return [%]']
                
            except Exception as e:
                print(f"[HATA] {modul_adi} calisirken hata olustu: {e}")

        # SONUÇLAR VE LİSTELEME
        print(f"\n{'='*50}")
        print(f"  {baslik} — STRATEJİ KARŞILAŞTIRMA SONUÇLARI")
        
        sirali_sonuclar = sorted(sonuclar.items(), key=lambda x: x[1], reverse=True)
        
        # 👑 BU HİSSENİN ŞAMPİYONUNU GENEL LİSTEYE EKLE 👑
        if sirali_sonuclar:
            en_iyi_strat = sirali_sonuclar[0][0]
            en_iyi_getiri = sirali_sonuclar[0][1]
            genel_sampiyonlar.append({
                "Hisse": baslik,
                "En Iyi Strateji": en_iyi_strat,
                "Kâr / Zarar (%)": round(en_iyi_getiri, 2)
            })

        sonuclar_listesi = []
        for strateji, getiri in sirali_sonuclar:
            etiket = "[KAR]" if getiri > 0 else "[ZAR]"
            print(f"  {etiket} {strateji:<20} % {getiri:9.2f}")
            sonuclar_listesi.append({"Hisse": baslik, "Strateji": strateji, "Getiri (%)": round(getiri, 2)})
            
        # HİSSEYE ÖZEL EXCEL KAYIT
        hedef_klasor = os.path.join("vbt_bist", "output", baslik)
        os.makedirs(hedef_klasor, exist_ok=True)
        excel_yolu = os.path.join(hedef_klasor, f"{baslik}_Karsilastirma.xlsx")
        pd.DataFrame(sonuclar_listesi).to_excel(excel_yolu, index=False)
        print(f"\n  [EXCEL] {baslik} başarıyla kaydedildi: {excel_yolu}\n")

    except Exception as e:
        print(f"  [HATA] {HISSE_KODU} analizinde sorun oluştu: {e}")


print(f"\n{'='*50}")
print(f"  TÜM HİSSELERİN (40 ADET) ANALİZİ BAŞARIYLA TAMAMLANDI!")

# ============================================================
#  👑 GENEL ŞAMPİYONLAR EXCELİ (MASTER DOSYA) OLUŞTURMA
# ============================================================
if genel_sampiyonlar:
    df_genel = pd.DataFrame(genel_sampiyonlar)
    df_genel = df_genel.sort_values(by="Kâr / Zarar (%)", ascending=False) # En çok kâr edenden aşağıya sırala
    genel_excel_yolu = os.path.join("vbt_bist", "output", "Genel_Sampiyonlar.xlsx")
    df_genel.to_excel(genel_excel_yolu, index=False)
    print(f"\n  [KRAL TACI] 👑 Genel Şampiyonlar Exceli Oluşturuldu: {genel_excel_yolu}")
print(f"{'='*50}\n")
