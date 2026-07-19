import yfinance as yf
import vectorbt as vbt
import pandas as pd
import numpy as np

# 1. KULLANACAĞIMIZ STRATEJİLERİN FİŞLERİNİ (IMPORT) TAKIYORUZ
from strategies.stocks.single_ma import single_ma, SingleMARequest
from strategies.stocks.two_ma import two_ma, TwoMARequest
from strategies.stocks.three_ma import three_ma, ThreeMARequest

from signals_adapter import normalize_signals

DOW30_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MS", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT", "CRM"
]

def fetch_dow30_data(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    print(f"\n[VERİ] {len(tickers)} adet hisse için veriler indiriliyor...")
    raw_data = yf.download(tickers, start=start_date, end=end_date)
    close_prices = raw_data['Close'].ffill().bfill()
    print("[VERİ] İndirme tamamlandı.")
    return close_prices

def generate_signals_for_all(close_prices: pd.DataFrame, strategy_name: str, params: dict) -> pd.DataFrame:
    print(f"[SİNYAL] {strategy_name} için sinyaller hesaplanıyor...")
    all_signals = pd.DataFrame(index=close_prices.index, columns=close_prices.columns)
    
    for ticker in close_prices.columns:
        prices_list = close_prices[ticker].tolist()
        ticker_signals = []
        
        for i in range(len(prices_list)):
            # En az 50 günlük verimiz yoksa hesaplayamayız, bekleriz
            if i < 50:
                ticker_signals.append(0)
                continue
                
            prices_slice = prices_list[max(0, i - 100):i + 1]
            
            # --- STRATEJİ SANTRALİ (YENİ STRATEJİLER BURAYA EKLENİR) ---
            if strategy_name == "single_ma":
                req = SingleMARequest(prices=prices_slice, period=params.get("period", 20))
                res = single_ma(req)
            elif strategy_name == "two_ma":
                req = TwoMARequest(prices=prices_slice, short_period=params.get("short_period", 10), long_period=params.get("long_period", 50))
                res = two_ma(req)
            elif strategy_name == "three_ma":
                req = ThreeMARequest(prices=prices_slice, short_period=10, medium_period=20, long_period=50)
                res = three_ma(req)
            elif strategy_name == "support_resistance":
                req = SupportResistanceRequest(prices=prices_slice, window=20)
                res = support_resistance(req)
            else:
                ticker_signals.append(0)
                continue
            
            normalized = normalize_signals(res.model_dump(), default_symbol=ticker)
            ticker_signals.append(normalized.get(ticker, 0))
                
        all_signals[ticker] = ticker_signals
        
    return all_signals

def run_dow30_backtest(close_prices: pd.DataFrame, strategy_name: str, params: dict):
    all_signals = generate_signals_for_all(close_prices, strategy_name, params)
    
    entries = (all_signals == 1)
    exits = (all_signals == -1) | (all_signals == 0)
    short_entries = (all_signals == -1)
    short_exits = (all_signals == 1) | (all_signals == 0)
    
    portfolio = vbt.Portfolio.from_signals(
        close=close_prices, entries=entries, exits=exits,
        short_entries=short_entries, short_exits=short_exits,
        init_cash=10000, fees=0.001, freq='1d'
    )
    
    # Ekrana basmak yerine Excel'e yazabilmek için tabloyu (DataFrame) iade ediyoruz
    metrics_df = pd.DataFrame({
        "Getiri (%)": portfolio.total_return() * 100,
        "Max Kayip (%)": portfolio.max_drawdown() * -100,
        "Sharpe Orani": portfolio.sharpe_ratio(),
        "Calmar Orani": portfolio.calmar_ratio(),
        "Kar Faktoru": portfolio.trades.profit_factor(),
        "Islem Sayisi": portfolio.trades.count()
    })
    
    return metrics_df.round(2)

if __name__ == "__main__":
    baslangic = "2024-01-01"
    bitis = "2025-01-01"
    excel_dosya_adi = "DOW30_Strateji_Raporu.xlsx"
    
    # Veriyi bir kez indiriyoruz (strateji başına tekrar tekrar indirmemek için)
    fiyat_verileri = fetch_dow30_data(DOW30_TICKERS, baslangic, bitis)
    
    # Test edilecek stratejilerin ve ayarlarının listesi
    test_edilecekler = {
        "single_ma": {"period": 20},
        "two_ma": {"short_period": 10, "long_period": 50},
        "three_ma": {}
    }

    print(f"\n[EXCEL] Rapor hazırlanıyor, bu işlem seçilen strateji sayısına göre birkaç dakika sürebilir...")
    
    # Excel dosyasını oluştur ve içine yazmaya başla
    with pd.ExcelWriter(excel_dosya_adi, engine="openpyxl") as writer:
        for strateji_adi, ayarlar in test_edilecekler.items():
            print(f"-> {strateji_adi} test ediliyor ve Excel'e yazılıyor...")
            tablo = run_dow30_backtest(fiyat_verileri, strateji_adi, ayarlar)
            # Her tabloyu Excel'de kendi adıyla bir sekmeye (sheet) kaydet
            tablo.to_excel(writer, sheet_name=strateji_adi)
            
    print(f"\n[BAŞARILI] Tüm testler bitti! Rapor klasörde '{excel_dosya_adi}' adıyla oluşturuldu.")
