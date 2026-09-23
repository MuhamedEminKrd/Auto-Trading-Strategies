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
import traceback
import warnings
import subprocess
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed


pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

strateji_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strategies")
veri_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def hisse_analiz_et(csv_dosyasi):
    """
    Her bir hisse icin tum stratejileri bagimsiz bir is parcacigi (process) olarak calistirir.
    """
    HISSE_KODU = csv_dosyasi.replace('.csv', '')
    baslik = HISSE_KODU
    dosya_yolu = os.path.join(veri_klasoru, csv_dosyasi)
    
    try:
        veri = pd.read_csv(dosya_yolu, index_col='Date', parse_dates=True)
        
        veri = veri.ffill().bfill()
        
        kapanis = veri['Close']
        acilis = veri['Open']
        yuksek = veri['High']
        dusuk = veri['Low']
        hacim = veri['Volume']
        
        csv_mtime = os.path.getmtime(dosya_yolu)

        if len(kapanis) < 50:
            return f"[UYARI] {HISSE_KODU} için yeterli veri yok, atlandı."

        sonuclar = {}
        moduller = [f[:-3] for f in os.listdir(strateji_klasoru) if f.endswith('.py') and f not in ('__init__.py', 'utils.py')]
        
        veri_deposu = {
            'kapanis_fiyatlari': kapanis,
            'kapanis': kapanis,
            'acilis': acilis,
            'yuksek': yuksek,
            'dusuk': dusuk,
            'hacim': hacim,
            'baslik': baslik
        }

        kac_tane_calisti = 0
        kac_tane_atlandi = 0

        for modul_adi in moduller:
            try:
                modul = importlib.import_module(f"strategies.{modul_adi}")
                if not hasattr(modul, "calistir"):
                    continue

                fonksiyon = modul.calistir
                sig = inspect.signature(fonksiyon)
                fonksiyon_argumanlari = {}
                
                # Fonksiyonun istedigi parametreleri otomatik eslestir (Dependency Injection)
                for arg_adi in sig.parameters:
                    if arg_adi in veri_deposu:
                        fonksiyon_argumanlari[arg_adi] = veri_deposu[arg_adi]

                # --- AKILLI ATLAMA (SMART SKIP) GUVENLIK YAMASI ---
                hedef_klasor_strateji = os.path.join("vbt_bist", "output", baslik)
                zaten_var = False
                mevcut_klasor = None
                if os.path.exists(hedef_klasor_strateji):
                    for kl in os.listdir(hedef_klasor_strateji):
                        # Tam eslesme klasor adi
                        if kl == modul_adi and os.path.isdir(os.path.join(hedef_klasor_strateji, kl)):
                            mevcut_klasor_temp = os.path.join(hedef_klasor_strateji, kl)
                            ozet_dosyalari = glob.glob(os.path.join(mevcut_klasor_temp, "*_ozet.csv"))
                            if ozet_dosyalari:
                                ozet_mtime = os.path.getmtime(ozet_dosyalari[0])
                                # Eger strateji ciktisi (ozet.csv), indirdigimiz datadan (veri.csv) YENIYSE atla.
                                # Degilse, veri guncellenmistir, bastan hesapla!
                                if ozet_mtime > csv_mtime:
                                    zaten_var = True
                                    mevcut_klasor = mevcut_klasor_temp
                            break

                if zaten_var:
                    kac_tane_atlandi += 1
                    try:
                        ozet_dosyalari = glob.glob(os.path.join(mevcut_klasor, "*_ozet.csv"))
                        if ozet_dosyalari:
                            df_ozet = pd.read_csv(ozet_dosyalari[0], index_col=0)
                            if 'Total Return [%]' in df_ozet.index:
                                val = df_ozet.loc['Total Return [%]'].iloc[0]
                                if not pd.isna(val):
                                    sonuclar[modul_adi] = float(val)
                    except Exception:
                        pass
                    continue
                # ------------------------------------
                
                # Stratejiyi calistir
                ozet = fonksiyon(**fonksiyon_argumanlari)
                sonuclar[modul_adi] = ozet['Total Return [%]']
                kac_tane_calisti += 1

            except Exception as e:
                # Hatayi yoksayip diger stratejiye gec (Terminali kirletmemek icin print'i kaldirdik)
                pass

        # HİSSEYE ÖZEL EXCEL KAYIT
        if sonuclar:
            sirali_sonuclar = sorted(sonuclar.items(), key=lambda x: x[1], reverse=True)
            sonuclar_listesi = [{"Hisse": baslik, "Strateji": strat, "Getiri (%)": round(getiri, 2)} for strat, getiri in sirali_sonuclar]
            
            hedef_klasor = os.path.join("vbt_bist", "output", baslik)
            os.makedirs(hedef_klasor, exist_ok=True)
            excel_yolu = os.path.join(hedef_klasor, f"{baslik}_Karsilastirma.xlsx")
            pd.DataFrame(sonuclar_listesi).to_excel(excel_yolu, index=False)

        # Temiz console ciktisi
        if kac_tane_calisti == 0 and kac_tane_atlandi > 0:
            return f"[ATLANDI] {HISSE_KODU} ({kac_tane_atlandi} strateji zaten hazir)"
        else:
            return f"[BASARILI] {HISSE_KODU} (Yeni Islenen: {kac_tane_calisti}, Atlanan: {kac_tane_atlandi})"
            
    except Exception as e:
        return f"[HATA] {HISSE_KODU} analiz edilemedi: {str(e)}"


if __name__ == "__main__":

    if not os.path.exists(veri_klasoru):
        print("Data klasörü bulunamadı. Lütfen önce data_fetcher.py çalıştırın.")
        sys.exit(1)

    csv_dosyalari = [f for f in os.listdir(veri_klasoru) if f.endswith('.csv')]
    
    if not csv_dosyalari:
        print("Data klasöründe CSV bulunamadı. Lütfen önce data_fetcher.py çalıştırın.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"🚀 BIST MULTIPROCESSING ANALİZ MOTORU BAŞLIYOR")
    print(f"📊 Toplam Hisse Sayısı: {len(csv_dosyalari)}")
    
    # 16 Thread var ise (16 - 4) = 12 Islemci kullanilir
    max_worker = max(1, multiprocessing.cpu_count() - 4)
    print(f"⚡ Kullanılan Çekirdek (Worker) Sayısı: {max_worker}")
    print(f"{'='*60}\n")

    # Multiprocessing Havuzu Kurulumu
    with ProcessPoolExecutor(max_workers=max_worker) as executor:
        # submit ile tüm hisseleri havuza gönderiyoruz
        futures = {executor.submit(hisse_analiz_et, csv): csv for csv in csv_dosyalari}
        
        # islem tamamlandikca ciktisini aliyoruz (Senkron bloklama yapmaz, hangisi once biterse o basilir)
        for i, future in enumerate(as_completed(futures), 1):
            try:
                sonuc = future.result()
                print(f"[{i}/{len(csv_dosyalari)}] {sonuc}")
            except Exception as exc:
                print(f"[{i}/{len(csv_dosyalari)}] Bir işlem hata fırlattı: {exc}")

    print(f"\n{'='*60}")
    print(f"🎉 TÜM HİSSELERİN ANALİZİ BAŞARIYLA TAMAMLANDI!")

    # ============================================================
    #  OTOMATIK TETİKLEME: MASTER RAPOR OLUŞTURUCU
    # ============================================================
    print("\n[OTOMATIK TETIKLEME] Master Rapor (Excel) oluşturuluyor...")
    rapor_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master_rapor_olustur.py")
    subprocess.run(["python", rapor_script])
    print(f"{'='*60}\n")
