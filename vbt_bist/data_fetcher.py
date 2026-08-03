import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def indir_guncelle(hisse_listesi, data_dir=None):
    if data_dir is None:
        # Scriptin bulundugu klasorun (vbt_bist) icindeki 'data' klasoru
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    bugun = datetime.now()
    
    for hisse in hisse_listesi:
        dosya_yolu = os.path.join(data_dir, f"{hisse}.csv")
        ticker = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        
        try:
            if os.path.exists(dosya_yolu):
                # Mevcut veriyi oku - Date hatasını önlemek için index_col=0 kullanıyoruz
                df = pd.read_csv(dosya_yolu, index_col=0, parse_dates=True)
                # Timestamp'ten timezone bilgisini kaldiralim
                df.index = df.index.tz_localize(None)
                son_tarih = df.index[-1]
                
                # Eğer son veri bugünden eski ise yeni veri indir
                if son_tarih.date() < bugun.date() - timedelta(days=1):
                    print(f"[{hisse}] Guncelleniyor... Mevcut Son Tarih: {son_tarih.date()}")
                    start_date = (son_tarih + timedelta(days=1)).strftime('%Y-%m-%d')
                    # auto_adjust=True eklenerek temettü ve bölünme düzeltmeleri (Adjusted Close) uygulandı
                    yeni_veri = yf.download(ticker, start=start_date, progress=False, auto_adjust=True)
                    
                    if not yeni_veri.empty:
                        # yfinance son güncellemelerinden dolayı MultiIndex dönüyorsa tek seviyeye indir
                        if isinstance(yeni_veri.columns, pd.MultiIndex):
                            yeni_veri.columns = yeni_veri.columns.get_level_values(0)
                        yeni_veri.index = yeni_veri.index.tz_localize(None)
                        df = pd.concat([df, yeni_veri])
                        # Tekrar eden gunleri silelim (guvenlik icin)
                        df = df[~df.index.duplicated(keep='last')]
                        df.to_csv(dosya_yolu)
                        print(f"[{hisse}] Basariyla guncellendi.")
                    else:
                        print(f"[{hisse}] Yeni veri bulunamadi.")
                else:
                    print(f"[{hisse}] Zaten guncel. (Son Veri: {son_tarih.date()})")
            else:
                # Dosya yoksa 2 yillik bastan indir
                print(f"[{hisse}] İlk kez indiriliyor...")
                # auto_adjust=True eklenerek temettü ve bölünme düzeltmeleri uygulandı
                df = yf.download(ticker, period="2y", progress=False, auto_adjust=True)
                if not df.empty:
                    # yfinance son güncellemelerinden dolayı MultiIndex dönüyorsa tek seviyeye indir
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.index = df.index.tz_localize(None)
                    df.to_csv(dosya_yolu)
                    print(f"[{hisse}] Kaydedildi.")
                else:
                    print(f"[{hisse}] Veri cekilemedi!")
        except Exception as e:
            print(f"[{hisse}] HATA: {e}")

if __name__ == "__main__":
    bist100 = [
        "AKBNK", "GARAN", "ISCTR", "YKBNK", "HALKB", "VAKBN", "TSKB", "ALBRK", 
        "THYAO", "PGSUS", "TAVHL", "DOAS", 
        "TCELL", "TTKOM", 
        "KCHOL", "SAHOL", "DOHOL", "ALARK", "OYAKC",
        "TUPRS", "PETKM", "AYGAZ",
        "FROTO", "TOASO", "TTRAK", "ASUZU",
        "SISE", "ENKAI", "BIMAS", "MGROS", "SOKM", 
        "EREGL", "KRDMD", "KCAER", "BRSAN",
        "ASELS", "KORDS", "SASA", "HEKTS", "GUBRF",
        "EKGYO", "TKFEN", "ENJSA", "ODAS", "ASTOR", "GESAN", "SMRTG", "EUPWR", "CWENE", 
        "MIATK", "CANTE", "QUAGR", "KONTR", "ISMEN", "KMPUR", "ZOREN", "CIMSA",
        "AKSA", "VESBE", "ARCLK", "TUKAS", "LOGO", "ARZUM"
    ]
    bist100 = list(set(bist100))
    print(f"Toplam {len(bist100)} hisse kontrol ediliyor...")
    indir_guncelle(bist100)
