"""
============================================================
  BIST Algoritmik Strateji Test Sistemi — Komuta Merkezi
============================================================
"""

import sys
import os
import pandas as pd
import importlib
import inspect
import glob
import warnings

# Pandas Future Warnings (Sarı Uyarılar) Kapatma
pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

strateji_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strategies")
veri_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

if __name__ == "__main__":

    # TÜM HİSSELERİN ŞAMPİYONLARINI TUTACAK LİSTE
    genel_sampiyonlar = []

    # Veri klasöründeki tüm CSV dosyalarını al
    if not os.path.exists(veri_klasoru):
        print("Data klasörü bulunamadı. Lütfen önce data_fetcher.py çalıştırın.")
        sys.exit(1)

    csv_dosyalari = [f for f in os.listdir(veri_klasoru) if f.endswith('.csv')]
    
    if not csv_dosyalari:
        print("Data klasöründe CSV bulunamadı. Lütfen önce data_fetcher.py çalıştırın.")
        sys.exit(1)

    for csv_dosyasi in csv_dosyalari:
        HISSE_KODU = csv_dosyasi.replace('.csv', '')
        baslik = HISSE_KODU
        dosya_yolu = os.path.join(veri_klasoru, csv_dosyasi)

        print(f"\n{'='*50}")
        print(f"  {HISSE_KODU} yerel veritabanından okunuyor...")
        print(f"{'='*50}")

        try:
            # Pandas ile yerel disken veriyi oku (İnternetsiz O(1) okuma hızı)
            veri = pd.read_csv(dosya_yolu, index_col='Date', parse_dates=True)
            kapanis = veri['Close']
            acilis = veri['Open']
            yuksek = veri['High']
            dusuk = veri['Low']
            hacim = veri['Volume']
            print(f"  Toplam {len(kapanis)} günlük veri diskten okundu.\n")

            if len(kapanis) < 50:
                print(f"  [UYARI] {HISSE_KODU} için yeterli veri yok, atlanıyor.")
                continue

            sonuclar = {}

            moduller = [f[:-3] for f in os.listdir(strateji_klasoru) if f.endswith('.py') and f not in ('__init__.py', 'utils.py')]
            toplam_strateji = len(moduller)

            veri_deposu = {
                'kapanis_fiyatlari': kapanis,
                'kapanis': kapanis,
                'acilis': acilis,
                'yuksek': yuksek,
                'dusuk': dusuk,
                'hacim': hacim,
                'baslik': baslik
            }

            for i, modul_adi in enumerate(moduller, 1):
                try:
                    modul = importlib.import_module(f"strategies.{modul_adi}")
                    if not hasattr(modul, "calistir"):
                        continue

                    fonksiyon = modul.calistir
                    sig = inspect.signature(fonksiyon)
                    fonksiyon_argumanlari = {}

                    for arg_adi in sig.parameters:
                        if arg_adi in veri_deposu:
                            fonksiyon_argumanlari[arg_adi] = veri_deposu[arg_adi]

                    # --- AKILLI ATLAMA (SMART SKIP) ---
                    hedef_klasor_strateji = os.path.join("vbt_bist", "output", baslik)
                    zaten_var = False
                    mevcut_klasor = None
                    if os.path.exists(hedef_klasor_strateji):
                        for kl in os.listdir(hedef_klasor_strateji):
                            if kl.startswith(modul_adi) and os.path.isdir(os.path.join(hedef_klasor_strateji, kl)):
                                zaten_var = True
                                mevcut_klasor = os.path.join(hedef_klasor_strateji, kl)
                                break

                    if zaten_var:
                        print(f"--- [{i}/{toplam_strateji}] {modul_adi.upper()} Hazır, ATLANDI ---")
                        try:
                            ozet_dosyalari = glob.glob(os.path.join(mevcut_klasor, "*_ozet.csv"))
                            if ozet_dosyalari:
                                df_ozet = pd.read_csv(ozet_dosyalari[0], index_col=0)
                                if 'Total Return [%]' in df_ozet.index:
                                    val = df_ozet.loc['Total Return [%]'].iloc[0]
                                    if not pd.isna(val):
                                        sonuclar[modul_adi] = float(val)
                        except Exception as skip_err:
                            print(f"    [UYARI] {modul_adi} mevcut CSV okunamadi: {skip_err}")
                        continue
                    # ------------------------------------

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
    print(f"  TÜM HİSSELERİN ({len(csv_dosyalari)} ADET) ANALİZİ BAŞARIYLA TAMAMLANDI!")

    # ============================================================
    #  👑 GENEL ŞAMPİYONLAR EXCELİ (MASTER DOSYA) OLUŞTURMA
    # ============================================================
    if genel_sampiyonlar:
        df_genel = pd.DataFrame(genel_sampiyonlar)
        df_genel = df_genel.sort_values(by="Kâr / Zarar (%)", ascending=False)
        genel_excel_yolu = os.path.join("vbt_bist", "output", "Genel_Sampiyonlar.xlsx")
        df_genel.to_excel(genel_excel_yolu, index=False)
        print(f"\n  [SAMPİYONLAR] Genel Sampiyonlar Exceli Olusturuldu: {genel_excel_yolu}")
    print(f"{'='*50}\n")
