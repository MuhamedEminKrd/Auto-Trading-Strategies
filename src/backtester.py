import yfinance as yf
import vectorbt as vbt
import pandas as pd
# Bir önceki adımda yazdığımız sinyal çeviricimizi içeri aktarıyoruz
from signals_adapter import normalize_signals
# Test edeceğimiz örnek stratejinin kendisini ve beklediği veri modelini içeri aktarıyoruz
from strategies.stocks.single_ma import single_ma, SingleMARequest
from strategies.stocks.two_ma import two_ma, TwoMARequest
def fetch_historical_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    1. AŞAMA: Yahoo Finance üzerinden belirtilen tarih aralığındaki fiyat verilerini çeker.
    """
    print(f"[VERİ] {ticker} için {start_date} - {end_date} arası veriler indiriliyor...")
    
    # yfinance ile veriyi indiriyoruz
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if df.empty:
        raise ValueError(f"{ticker} için veri bulunamadı. Tarihleri veya sembolü kontrol edin.")
    return df
def generate_signals_historically(prices: list[float], strategy_name: str, params: dict) -> list[int]:
    """
    2. AŞAMA: Yürüyen Pencere (Rolling Window) Mantığı
    Tarihsel fiyat listesini gün gün tarayarak her gün için strateji sinyali (1, -1, 0) üretir.
    """
    signals = []
    
    # Stratejimizin ihtiyaç duyduğu minimum gün sayısını hesaplıyoruz
    min_period = params.get("period", 20)
    if strategy_name == "two_ma":
        min_period = params.get("long_period", 50)
    
    # Tüm fiyat geçmişi üzerinde gün gün ilerliyoruz
    for i in range(len(prices)):
        # Stratejinin çalışabilmesi için gereken minimum gün sayısına henüz ulaşmadıysak,
        # işlem yapmıyor ve '0' (Bekle) sinyali üretiyoruz.
        if i < min_period:
            signals.append(0)
            continue
        
        # O güne kadar olan fiyatları içeren "pencereyi" alıyoruz. 
        # (Çok eskiye gitmemek için sadece son 100 günü almamız genelde yeterlidir)
        prices_slice = prices[max(0, i - 100):i + 1] 
        
        if strategy_name == "single_ma":
            period = params.get("period", 20)
            ma_type = params.get("ma_type", "sma")
            req = SingleMARequest(prices=prices_slice, period=period, ma_type=ma_type)
            res = single_ma(req)
            normalized = normalize_signals(res.model_dump(), default_symbol="ASSET")
            signals.append(normalized.get("ASSET", 0))
            
        elif strategy_name == "two_ma":
            short_period = params.get("short_period", 10)
            long_period = params.get("long_period", 50)
            ma_type = params.get("ma_type", "sma")
            req = TwoMARequest(prices=prices_slice, short_period=short_period, long_period=long_period, ma_type=ma_type)
            res = two_ma(req)
            normalized = normalize_signals(res.model_dump(), default_symbol="ASSET")
            signals.append(normalized.get("ASSET", 0))
            
        else:
            # Şimdilik sadece single_ma ve two_ma destekliyoruz
            signals.append(0)
            
    return signals
def run_backtest(ticker: str, strategy_name: str, params: dict, start_date: str, end_date: str):
    """
    3. AŞAMA: VectorBT ile Simülasyon
    Verileri çeker, sinyalleri üretir ve simülasyon sonucunu raporlar.
    """
    # 1. Geçmiş fiyat verilerini çek
    df = fetch_historical_data(ticker, start_date, end_date)
    
    # Sadece kapanış (Close) fiyatlarını bir liste olarak alıyoruz
    close_prices = df['Close'].squeeze().tolist()
    dates = df.index
    
    # 2. Döngüyü çalıştırıp geçmiş sinyalleri üret
    signals_list = generate_signals_historically(close_prices, strategy_name, params)
    
    # Fiyatları ve Sinyalleri VectorBT'nin anlayacağı formata (Pandas Series) çeviriyoruz
    signals_series = pd.Series(signals_list, index=dates)
    prices_series = pd.Series(close_prices, index=dates)
    
    # 3. VectorBT Sinyal Kurallarını Belirle
    entries = (signals_series == 1)               # Ne zaman alınacak? (Sinyal 1 ise)
    exits = (signals_series == 0) | (signals_series == -1)  # Ne zaman satılacak? (Sinyal 0 veya -1 ise)
    
    short_entries = (signals_series == -1)        # Ne zaman açığa satılacak? (Sinyal -1 ise)
    short_exits = (signals_series == 0) | (signals_series == 1) # Açığa satış ne zaman kapatılacak?
    
    # 4. Simülasyonu Çalıştır!
    portfolio = vbt.Portfolio.from_signals(
        close=prices_series,
        entries=entries,
        exits=exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=10000,   # Cebimizde 10.000 dolar var
        fees=0.001,         # Borsa bizden binde 1 komisyon kesiyor
        freq='1d' 
    )
    
    # 5. Raporu Ekrana Yazdır
    print(f"\n================ BACKTEST RAPORU: {ticker} ================")
    print(f"Strateji: {strategy_name}")
    print(f"Başlangıç Bakiyesi: 10,000.00 $")
    print(f"Bitiş Bakiyesi: {portfolio.value().iloc[-1]:.2f} $")
    print(f"Toplam Getiri: % {portfolio.total_return() * 100:.2f}")
    print(f"Maksimum Kayıp (Max Drawdown): % {portfolio.max_drawdown() * -100:.2f}")
    print(f"Sharpe Oranı: {portfolio.sharpe_ratio():.2f}")
    print(f"Toplam İşlem Sayısı: {portfolio.trades.count()}")
    print("===========================================================\n")
# Sadece bu dosya doğrudan çalıştırıldığında aşağıdaki test kodu çalışır
if __name__ == "__main__":
    
    # Test Ayarları
    ticker_sembolu = "ASELS.IS"       # Aselsan Hissesi
    strateji = "two_ma"               # Çift hareketli ortalama kesişimi (Golden/Death Cross)
    ayarlar = {"short_period": 10, "long_period": 50, "ma_type": "sma"} # 10 ve 50 günlük MA
    baslangic = "2026-01-01"          # Testin başlayacağı tarih
    bitis = "2026-07-18"          # Testin biteceği tarih
    
    # Testi başlat
    run_backtest(ticker_sembolu, strateji, ayarlar, baslangic, bitis)