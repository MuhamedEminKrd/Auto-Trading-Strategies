import os
import sys
import pandas as pd
import yfinance as yf
import warnings

# Gecici Pandas hatalarini gizle
pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings('ignore')

# Bulundugumuz klasoru yola ekle ki strategies klasorunu taniyabilsin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from strategies import golden_cross

# main.py içerisindeki aynı hisse listesi
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
VERI_SURESI = "2y"

def yama_botunu_calistir():
    print("="*60)
    print("[BILGI] HIZLI YAMA BOTU BAŞLATILDI")
    print("Sadece Hatalı 2 Strateji (Engulfing ve Coppock) Yeniden Test Ediliyor...")
    print("="*60)

    for HISSE_KODU in HISSE_LISTESI:
        baslik = HISSE_KODU.split(".")[0]
        print(f"\n[+] {HISSE_KODU} verisi indiriliyor...")
        
        try:
            veri = yf.download(HISSE_KODU, period=VERI_SURESI, interval="1d", progress=False)
            
            if len(veri) < 50:
                print(f"  [UYARI] {HISSE_KODU} için yeterli veri yok, atlanıyor.")
                continue

            # Sadece bu iki stratejinin ihtiyaç duyduğu verileri çekiyoruz
            kapanis = veri['Close'][HISSE_KODU]
            kisa_periyot = 50
            uzun_periyot = 200
            
            print(f"  -> Golden Cross çalıştırılıyor...")
            golden_cross.calistir(kapanis, baslik, kisa_periyot, uzun_periyot)
            
        except Exception as e:
            print(f"  [HATA] {HISSE_KODU} islenirken hata oluştu: {e}")

    print("\n" + "="*60)
    print("[BASARILI] HIZLI YAMA SURECI TAMAMLANDI")
    print("="*60)

if __name__ == "__main__":
    yama_botunu_calistir()
