# pyrefly: ignore [missing-import]
import yfinance as yf

hisse_kodu= "GARAN.IS"# BIST hisselerini yfinance'ten çekerken sonuna her zaman .IS (İstanbul) ekliyoruz.
print(f"--- {hisse_kodu} verileri yfinance'ten indiriliyor ---")

veri=yf.download(hisse_kodu, period="1y", interval="1d")# Sadece son 1 yıllık, günlük verileri çekiyoruz

print("\nİndirilen Verinin İlk 5 Satırı (OHLCV):")# Veri başarılı şekilde geldi mi diye ilk 5 günü ekrana yazdıralım

print(veri.head())