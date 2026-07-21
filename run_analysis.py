import os
import sys
import yfinance as yf
import pandas as pd

# Test edeceğimiz hisse listesi
DOW30_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MS", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT", "CRM"
]

# Test tarihleri
START_DATE = "2025-01-01"
END_DATE   = "2026-07-01"


def fetch_data(ticker: str) -> pd.Series:
    """Tek bir hissenin kapanış fiyatlarını indirir."""
    print(f"  [VERİ] {ticker} indiriliyor...")
    df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True)
    close = df["Close"].squeeze()
    close = close.ffill().bfill()
    return close


def main():
    print(f"\n{'='*50}")
    print(f"  DOW30 ANALİZ SİSTEMİ BAŞLADI")
    print(f"  Tarih: {START_DATE} -> {END_DATE}")
    print(f"  Hisse Sayısı: {len(DOW30_TICKERS)}")
    print(f"{'='*50}\n")

    for ticker in DOW30_TICKERS:
        print(f"[{ticker}] işleniyor...")

        # 1. Klasörü oluştur
        output_dir = os.path.join("results", ticker)
        os.makedirs(output_dir, exist_ok=True)

        # 2. Veriyi indir
        prices = fetch_data(ticker)
        print(f"  [OK] {len(prices)} günlük veri alındı.\n")

    print("Aşama 1 tamamlandı: Tüm hisse verileri indirildi.")


if __name__ == "__main__":
    main()
