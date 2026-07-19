import yfinance as yf
import vectorbt as vbt
import pandas as pd
import numpy as np

from strategies.stocks.two_ma import two_ma , TwoMARequest
from signals_adapter import normalize_signals

DOW30_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MS", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT", "CRM"
]

def fetch_dow30_data(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
        ADIM 2: Yahoo Finance üzerinden verilen tüm sembollerin günlük Kapanış (Close) fiyatlarını tek seferde çeker.
    """
    print(f"\n[VERİ] {len(tickers)} adet hisse için {start_date} - {end_date} arası veriler indiriliyor...")
    
    # yfinance ile tüm listeyi tek bir komutla indiriyoruz
    raw_data = yf.download(tickers, start=start_date, end=end_date)
    
    # İndirilen devasa tablodan sadece Kapanış (Close) fiyatlarını alıyoruz
    close_prices = raw_data['Close']
    
    # Hafta sonu veya tatil gibi eksik veri olan günleri bir önceki günün fiyatıyla dolduruyoruz (hata almamak için)
    close_prices = close_prices.ffill().bfill()
    
    print("[VERİ] İndirme ve temizleme işlemi başarıyla tamamlandı.")
    return close_prices
def generate_signals_for_all(close_prices: pd.DataFrame, strategy_name: str, params: dict) -> pd.DataFrame:
    """
    ADIM 3: Her bir hisse için ayrı ayrı stratejiyi çalıştırıp sinyalleri (1, -1, 0) üretir.
    """
    print(f"\n[SİNYAL] {close_prices.shape[1]} hisse için {strategy_name} sinyalleri hesaplanıyor... (Bu işlem biraz sürebilir)")
    
    # Boş bir sinyal tablosu oluşturuyoruz (Tarihler satır, Hisse adları sütun olacak)
    all_signals = pd.DataFrame(index=close_prices.index, columns=close_prices.columns)
    
    # Strateji ayarları
    short_period = params.get("short_period", 10)
    long_period = params.get("long_period", 50)
    ma_type = params.get("ma_type", "sma")
    
    # Tablodaki her bir hisse sütunu için tek tek dönüyoruz
    for ticker in close_prices.columns:
        prices_list = close_prices[ticker].tolist()
        ticker_signals = []
        
        # Gün gün ilerleyen yürüyen pencere (Rolling Window)
        for i in range(len(prices_list)):
            if i < long_period:
                ticker_signals.append(0)
                continue
                
            prices_slice = prices_list[max(0, i - 100):i + 1]
            
            if strategy_name == "two_ma":
                req = TwoMARequest(prices=prices_slice, short_period=short_period, long_period=long_period, ma_type=ma_type)
                res = two_ma(req)
                normalized = normalize_signals(res.model_dump(), default_symbol=ticker)
                ticker_signals.append(normalized.get(ticker, 0))
            else:
                ticker_signals.append(0)
                
        # Hisse için hesaplanan sinyal listesini tablodaki kendi sütununa kaydediyoruz
        all_signals[ticker] = ticker_signals
        
    print("[SİNYAL] Tüm sinyaller başarıyla hesaplandı.")
    return all_signals
def run_dow30_backtest(strategy_name: str, params: dict, start_date: str, end_date: str):
    """
    ADIM 4: Tüm süreci birleştirip VectorBT simülasyonunu çalıştırır ve metrikleri tablo olarak hesaplar.
    """
    # 1. Verileri indir
    close_prices = fetch_dow30_data(DOW30_TICKERS, start_date, end_date)
    
    # 2. Sinyalleri üret
    all_signals = generate_signals_for_all(close_prices, strategy_name, params)
    
    print("\n[VECTORBT] Simülasyon başlatılıyor ve gelişmiş metrikler hesaplanıyor...")
    
    # 3. Sinyal kurallarını VectorBT'nin anlayacağı tablolara çeviriyoruz
    entries = (all_signals == 1)
    exits = (all_signals == -1) | (all_signals == 0)
    short_entries = (all_signals == -1)
    short_exits = (all_signals == 1) | (all_signals == 0)
    
    # 4. VectorBT portföyünü toplu olarak oluştur (30 hisse aynı anda hesaplanıyor!)
    portfolio = vbt.Portfolio.from_signals(
        close=close_prices,
        entries=entries,
        exits=exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=10000,   # Her hisse için 10.000$ bütçe ayırıyoruz
        fees=0.001,        # Komisyon oranı
        freq='1d'          # Veri sıklığı günlük
    )
    
    # 5. Hocanın istediği tüm metrikleri hesaplayıp bir tablo (DataFrame) oluşturuyoruz
    metrics_df = pd.DataFrame({
        "Getiri (%)": portfolio.total_return() * 100,
        "Max Kayip (%)": portfolio.max_drawdown() * -100,
        "Sharpe Orani": portfolio.sharpe_ratio(),
        "Calmar Orani": portfolio.calmar_ratio(),
        "Kar Faktoru": portfolio.trades.profit_factor(),
        "Islem Sayisi": portfolio.trades.count()
    })
    
    print("\n================ DOW 30 ANALİZ RAPORU ================")
    print(f"Strateji: {strategy_name}")
    print(f"Tarih: {start_date} -> {end_date}")
    print("-" * 65)
    # Tabloyu ekrana güzelce yuvarlayarak yazdırıyoruz
    print(metrics_df.round(2).to_string())
    print("========================================================\n")

# Kodu çalıştırmak için ana tetikleyici
if __name__ == "__main__":
    # Test ayarlarını belirliyoruz
    strateji = "two_ma"
    ayarlar = {"short_period": 10, "long_period": 50, "ma_type": "sma"}
    baslangic = "2025-01-01"
    bitis = "2026-07-01"
    
    # Simülasyonu başlatıyoruz
    run_dow30_backtest(strateji, ayarlar, baslangic, bitis)
   