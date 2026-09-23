import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def indir_guncelle(hisse_listesi, data_dir=None):
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    bugun = datetime.now()
    
    for hisse in hisse_listesi:
        dosya_yolu = os.path.join(data_dir, f"{hisse}.csv")
        ticker = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        
        try:
            if os.path.exists(dosya_yolu):
                df = pd.read_csv(dosya_yolu, index_col=0, parse_dates=True)
                df.index = df.index.tz_localize(None)
                son_tarih = df.index[-1]
                
                if son_tarih.date() < bugun.date() - timedelta(days=1):
                    print(f"[{hisse}] Guncelleniyor... Mevcut Son Tarih: {son_tarih.date()}")
                    start_date = (son_tarih + timedelta(days=1)).strftime('%Y-%m-%d')
                    yeni_veri = yf.download(ticker, start=start_date, progress=False, auto_adjust=True)
                    
                    if not yeni_veri.empty:
                        if isinstance(yeni_veri.columns, pd.MultiIndex):
                            yeni_veri.columns = yeni_veri.columns.get_level_values(0)
                        yeni_veri.index = yeni_veri.index.tz_localize(None)
                        df = pd.concat([df, yeni_veri])
                        df = df[~df.index.duplicated(keep='last')]
                        df.to_csv(dosya_yolu)
                        print(f"[{hisse}] Basariyla guncellendi.")
                    else:
                        print(f"[{hisse}] Yeni veri bulunamadi.")
                else:
                    print(f"[{hisse}] Zaten guncel. (Son Veri: {son_tarih.date()})")
            else:
                print(f"[{hisse}] İlk kez indiriliyor...")
                df = yf.download(ticker, period="5y", progress=False, auto_adjust=True)
                if not df.empty:
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
        "AKBNK", "GARAN", "ISCTR", "YKBNK", "HALKB", "VAKBN", "TSKB", "ALBRK", "SKBNK", "ISFIN",
        "THYAO", "PGSUS", "TAVHL", "DOAS", 
        "TCELL", "TTKOM", 
        "KCHOL", "SAHOL", "DOHOL", "ALARK", "OYAKC", "AGHOL", "GSDHO",
        "TUPRS", "PETKM", "AYGAZ", "TRCAS",
        "FROTO", "TOASO", "TTRAK", "ASUZU", "KARSN",
        "SISE", "ENKAI", "BIMAS", "MGROS", "SOKM", "CCOLA", "AEFES",
        "EREGL", "KRDMD", "KCAER", "BRSAN", "CEMTS", "IZMDC",
        "ASELS", "KORDS", "SASA", "HEKTS", "GUBRF", "BAGFS",
        "EKGYO", "ISGYO", "TRGYO", "HLGYO", 
        "TKFEN", "ENJSA", "ODAS", "ASTOR", "GESAN", "SMRTG", "EUPWR", "CWENE", "ZOREN", "AKENR", "GWIND",
        "MIATK", "CANTE", "QUAGR", "KONTR", "ISMEN", "KMPUR", "CIMSA", "AKCNS", "BUCIM",
        "AKSA", "VESBE", "ARCLK", "TUKAS", "LOGO", "ARZUM", "ALGYO",
        "EGEEN", "ECILC", "DEVA", "GENIL",
        "BERA", "AHGAZ", "KLRHO", "YYLGD", "SUWEN", "KZBGY", "ALFAS"
    ]
    bist100 = list(set(bist100))
    print(f"Toplam {len(bist100)} hisse kontrol ediliyor...")
    indir_guncelle(bist100)
