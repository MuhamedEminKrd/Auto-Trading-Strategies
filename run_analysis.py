import os
import sys
import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import vectorbt as vbt
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Ekran acmadan PNG kaydeder
import matplotlib.pyplot as plt

# Strateji klasorunu Python'un arama yoluna ekliyoruz
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from strategies.stocks.single_ma import single_ma, SingleMARequest
from strategies.stocks.two_ma import two_ma, TwoMARequest
from strategies.stocks.three_ma import three_ma, ThreeMARequest
from strategies.stocks.channel import channel, ChannelRequest
from signals_adapter import normalize_signals

# ── Ayarlar ──────────────────────────────────────────
DOW30_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MS", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT", "CRM"
]

START_DATE = "2025-01-01"
END_DATE   = "2026-07-01"

STRATEGIES = {
    "single_ma": {"period": 20},
    "two_ma":    {"short_period": 10, "long_period": 50},
    "three_ma":  {"short_period": 5, "medium_period": 20, "long_period": 50},
     "channel":   {"lookback": 20, "channel_type": "donchian"},
}
# ─────────────────────────────────────────────────────


def fetch_data(ticker: str) -> pd.Series:
    """Hissenin kapanış fiyatlarını indirir."""
    df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True)
    return df["Close"].squeeze().ffill().bfill()


def generate_signals(prices_list: list, strategy_name: str, params: dict, ticker: str) -> list:
    """Verilen strateji ve fiyat listesi ile sinyal üretir."""
    signals = []
    min_period = params.get("long_period", params.get("period", 20))

    for i in range(len(prices_list)):
        if i < min_period:
            signals.append(0)
            continue

        prices_slice = prices_list[max(0, i - 100): i + 1]

        try:
            if strategy_name == "single_ma":
                req = SingleMARequest(prices=prices_slice, period=params["period"])
                res = single_ma(req)
            elif strategy_name == "two_ma":
                req = TwoMARequest(
                    prices=prices_slice,
                    short_period=params["short_period"],
                    long_period=params["long_period"]
                )
                res = two_ma(req)
            elif strategy_name == "three_ma":
                req = ThreeMARequest(
                    prices=prices_slice,
                    short_period=params["short_period"],
                    medium_period=params["medium_period"],
                    long_period=params["long_period"]
                )
                res = three_ma(req)
            elif strategy_name == "channel":
                req = ChannelRequest(
                    prices=prices_slice,
                    lookback=params["lookback"],
                    channel_type=params["channel_type"]
                )
                res = channel(req)
            else:
                signals.append(0)
                continue

            normalized = normalize_signals(res.model_dump(), default_symbol=ticker)
            signals.append(normalized.get(ticker, 0))

        except Exception:
            signals.append(0)

    return signals


def run_backtest_and_save_png(prices: pd.Series, signals: list, ticker: str, strategy_name: str, output_dir: str) -> dict:
    """VectorBT backtest çalıştırır, PNG kaydeder ve metrikleri Sözlük(dict) olarak döndürür."""
    signals_series = pd.Series(signals, index=prices.index)

    entries       = (signals_series == 1)
    exits         = (signals_series == -1) | (signals_series == 0)
    short_entries = (signals_series == -1)
    short_exits   = (signals_series == 1)  | (signals_series == 0)

    portfolio = vbt.Portfolio.from_signals(
        close=prices,
        entries=entries,
        exits=exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=10000,
        fees=0.001,
        freq="1d"
    )

    # 1) Grafik Çiz ve Kaydet
    fig, ax = plt.subplots(figsize=(12, 5))
    portfolio.value().plot(ax=ax)
    ax.set_title(f"{ticker} -- {strategy_name}")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Portföy Değeri ($)")
    ax.grid(True, alpha=0.3)

    png_path = os.path.join(output_dir, f"{strategy_name}.png")
    fig.savefig(png_path, dpi=100, bbox_inches="tight")
    plt.close(fig)

    # 2) Metrikleri Hesapla
    metrics = {
        "Hisse": ticker,
        "Strateji": strategy_name,
        "Getiri (%)": round(portfolio.total_return() * 100, 2),
        "Max Kayip (%)": round(portfolio.max_drawdown() * -100, 2),
        "Sharpe Orani": round(portfolio.sharpe_ratio(), 2),
        "Calmar Orani": round(portfolio.calmar_ratio(), 2),
        "Kar Faktoru": round(portfolio.trades.profit_factor(), 2),
        "Islem Sayisi": portfolio.trades.count()
    }
    return metrics


def main():
    print(f"\n{'='*55}")
    print(f"  DOW30 ANALIZ SISTEMI (FINAL V1.0)")
    print(f"  Tarih   : {START_DATE} -> {END_DATE}")
    print(f"  Hisse   : {len(DOW30_TICKERS)}  |  Strateji: {len(STRATEGIES)}")
    print(f"{'='*55}\n")

    # Tüm metrikleri toplayacağımız devasa liste
    all_results = []

    for ticker in DOW30_TICKERS:
        print(f"[{ticker}] isleniyor...")
        output_dir = os.path.join("results", ticker)
        os.makedirs(output_dir, exist_ok=True)

        prices = fetch_data(ticker)
        prices_list = prices.tolist()

        for strategy_name, params in STRATEGIES.items():
            signals = generate_signals(prices_list, strategy_name, params, ticker)
            
            # Fonksiyon artık bize metrikleri (sözlük olarak) döndürüyor
            metrics = run_backtest_and_save_png(prices, signals, ticker, strategy_name, output_dir)
            
            # Bu metrikleri ana listemize ekliyoruz
            all_results.append(metrics)
            
            print(f"  [OK] {strategy_name}.png kaydedildi")

        print()

    # ── CSV KAYDETME İŞLEMİ ───────────────────────────────
    print("[CSV] Tablo olusturuluyor...")
    df_results = pd.DataFrame(all_results)
    csv_path = os.path.join("results", "summary.csv")
    df_results.to_csv(csv_path, index=False)
    
    print(f"[BASARILI] Asama 3 tamamlandi! Ozet tablo kaydedildi: {csv_path}\n")


if __name__ == "__main__":
    main()
