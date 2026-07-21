import os
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import yfinance as yf
import vectorbt as vbt
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Strateji klasörünü Python arama yoluna ekliyoruz
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 1: AYARLAR
# ═══════════════════════════════════════════════════════════════

DOW30_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MS", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WMT", "CRM"
]

START_DATE = "2025-01-01"
END_DATE   = "2026-07-01"
INIT_CASH  = 10_000

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 2: VERİ İNDİRME (OHLCV)
# ═══════════════════════════════════════════════════════════════

def fetch_data(ticker: str) -> pd.DataFrame:
    """Hissenin OHLCV verisini (Açılış, Yüksek, Düşük, Kapanış, Hacim) indirir."""
    df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True)
    df = df.ffill().bfill()
    return df

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 3: EVRENSEL SİNYAL ÇIKARICI
# ═══════════════════════════════════════════════════════════════

def extract_signal(response, ticker: str) -> int:
    """Herhangi bir stratejinin çıktısından sinyal çıkarır (1, -1, 0)."""
    try:
        r = response.model_dump()
        # Doğrudan 'signal' alanı
        if "signal" in r:
            return int(r["signal"])
        # 'signals' sözlüğü
        if "signals" in r and isinstance(r["signals"], dict):
            return int(r["signals"].get(ticker, 0))
        # 'positions' listesi
        if "positions" in r and isinstance(r["positions"], list):
            for pos in r["positions"]:
                if isinstance(pos, dict) and pos.get("symbol") == ticker:
                    return int(pos.get("signal", 0))
            # Genel pozisyon sinyali (tek varlık verilince)
            if r["positions"]:
                sig = r["positions"][0].get("signal", 0) if isinstance(r["positions"][0], dict) else 0
                return int(sig)
        # 'weights' sözlüğü
        if "weights" in r and isinstance(r["weights"], dict):
            w = r["weights"].get(ticker, 0)
            if w == 0 and r["weights"]:
                w = list(r["weights"].values())[0]
            return 1 if w > 0 else (-1 if w < 0 else 0)
        # 'long_assets' / 'short_assets'
        if "long_assets" in r:
            if ticker in r.get("long_assets", []) or (r.get("long_assets") and len(r["long_assets"]) > 0):
                return 1
            if ticker in r.get("short_assets", []) or (r.get("short_assets") and len(r["short_assets"]) > 0):
                return -1
        # 'risky_weight' > 1 → kaldıraçlı → AL; < 0.5 → düşük ağırlık → SAT
        if "risky_weight" in r:
            w = r["risky_weight"]
            if w > 1.0:
                return 1
            elif w < 0.5:
                return -1
            return 0
        # 'long_commodities' / 'short_commodities'
        if "long_commodities" in r:
            if r["long_commodities"]:
                return 1
            if r["short_commodities"]:
                return -1
        # 'top_sectors' → uzun pozisyon
        if "top_sectors" in r and r["top_sectors"]:
            return 1
        # 'expected_return' pozitifse AL
        if "expected_return" in r:
            return 1 if r["expected_return"] > 0 else (-1 if r["expected_return"] < 0 else 0)
    except Exception:
        pass
    return 0

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 4: STRATEJİ SARMALAYICILARI (68 Strateji)
# ═══════════════════════════════════════════════════════════════

def _prices_list(ohlcv: pd.DataFrame) -> list:
    return ohlcv["Close"].tolist()

def _returns_list(ohlcv: pd.DataFrame) -> list:
    closes = ohlcv["Close"].tolist()
    if len(closes) < 2:
        return [0.0]
    return [0.0] + [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]

def _weekly_returns(ohlcv: pd.DataFrame) -> list:
    weekly = ohlcv["Close"].resample("W").last().pct_change().dropna().tolist()
    return weekly if weekly else [0.0]

def _volumes_list(ohlcv: pd.DataFrame) -> list:
    return ohlcv["Volume"].tolist() if "Volume" in ohlcv.columns else [1000000.0] * len(ohlcv)

# ─── STOCKS ──────────────────────────────────────────────────

def sig_single_ma(ohlcv, ticker):
    from strategies.stocks.single_ma import single_ma, SingleMARequest
    prices = _prices_list(ohlcv)[-100:]
    res = single_ma(SingleMARequest(prices=prices, period=20))
    return extract_signal(res, ticker)

def sig_two_ma(ohlcv, ticker):
    from strategies.stocks.two_ma import two_ma, TwoMARequest
    prices = _prices_list(ohlcv)[-100:]
    res = two_ma(TwoMARequest(prices=prices, short_period=10, long_period=50))
    return extract_signal(res, ticker)

def sig_three_ma(ohlcv, ticker):
    from strategies.stocks.three_ma import three_ma, ThreeMARequest
    prices = _prices_list(ohlcv)[-100:]
    res = three_ma(ThreeMARequest(prices=prices, short_period=5, medium_period=20, long_period=50))
    return extract_signal(res, ticker)

def sig_channel(ohlcv, ticker):
    from strategies.stocks.channel import channel, ChannelRequest
    prices = _prices_list(ohlcv)[-50:]
    res = channel(ChannelRequest(prices=prices, lookback=20, channel_type="donchian"))
    return extract_signal(res, ticker)

def sig_support_resistance(ohlcv, ticker):
    from strategies.stocks.support_resistance import support_resistance, SupportResistanceRequest
    h = float(ohlcv["High"].iloc[-2])
    l = float(ohlcv["Low"].iloc[-2])
    c = float(ohlcv["Close"].iloc[-2])
    cur = float(ohlcv["Close"].iloc[-1])
    res = support_resistance(SupportResistanceRequest(high=h, low=l, close=c, current_price=cur))
    return extract_signal(res, ticker)

def sig_price_momentum(ohlcv, ticker):
    from strategies.stocks.price_momentum import price_momentum, PriceMomentumRequest
    prices = _prices_list(ohlcv)
    res = price_momentum(PriceMomentumRequest(prices={ticker: prices}, lookback=12, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_low_volatility(ohlcv, ticker):
    from strategies.stocks.low_volatility import low_volatility, LowVolatilityRequest
    rets = _returns_list(ohlcv)
    res = low_volatility(LowVolatilityRequest(returns={ticker: rets}, lookback=252, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_value(ohlcv, ticker):
    from strategies.stocks.value import value as value_strat, ValueRequest
    cur_price = float(ohlcv["Close"].iloc[-1])
    # Book value tahmini: Fiyatın %60'ı (P/B=1.67 varsayımı)
    book = cur_price * 0.6
    res = value_strat(ValueRequest(book_values={ticker: book}, prices={ticker: cur_price}, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_implied_volatility(ohlcv, ticker):
    from strategies.stocks.implied_volatility import implied_volatility as iv_strat, ImpliedVolatilityRequest
    rets = np.array(_returns_list(ohlcv))
    iv_recent = float(np.std(rets[-20:]) * np.sqrt(252)) if len(rets) >= 20 else 0.2
    iv_prev   = float(np.std(rets[-40:-20]) * np.sqrt(252)) if len(rets) >= 40 else 0.2
    iv_change = iv_recent - iv_prev
    res = iv_strat(ImpliedVolatilityRequest(iv_changes={ticker: iv_change}, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_earnings_momentum(ohlcv, ticker):
    from strategies.stocks.earnings_momentum import earnings_momentum, EarningsMomentumRequest
    rets = _returns_list(ohlcv)
    # Çeyreklik kazanç proxy: her 63 günde bir toplayarak kullan
    quarterly = [sum(rets[i:i+63]) for i in range(0, len(rets)-62, 63)]
    if len(quarterly) < 5:
        quarterly = rets[-8:]
    res = earnings_momentum(EarningsMomentumRequest(earnings={ticker: quarterly}, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_residual_momentum(ohlcv, ticker):
    from strategies.stocks.residual_momentum import residual_momentum, ResidualMomentumRequest
    rets = _returns_list(ohlcv)
    n = len(rets)
    zeros = [0.0] * n
    res = residual_momentum(ResidualMomentumRequest(
        stock_returns={ticker: rets}, market_returns=zeros, smb=zeros, hml=zeros,
        lookback=12, long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_multifactor(ohlcv, ticker):
    from strategies.stocks.multifactor import multifactor, MultifactorRequest
    rets = np.array(_returns_list(ohlcv))
    mom_score = float(np.sum(rets[-60:])) if len(rets) >= 60 else 0.0
    vol_score = -float(np.std(rets[-60:])) if len(rets) >= 60 else 0.0
    res = multifactor(MultifactorRequest(
        factors={"momentum": {ticker: mom_score}, "low_vol": {ticker: vol_score}},
        long_pct=1.0, short_pct=0.0))
    return extract_signal(res, ticker)

def sig_weighted_regression(ohlcv, ticker):
    from strategies.stocks.weighted_regression import weighted_regression, WeightedRegressionRequest
    rets = _returns_list(ohlcv)
    res = weighted_regression(WeightedRegressionRequest(
        returns={ticker: rets}, cluster_returns=rets, lookback=60))
    return extract_signal(res, ticker)

def sig_mean_reversion_cluster(ohlcv, ticker):
    from strategies.stocks.mean_reversion_cluster import mean_reversion_cluster, MeanReversionClusterRequest
    prices = _prices_list(ohlcv)
    res = mean_reversion_cluster(MeanReversionClusterRequest(
        prices={ticker: prices}, lookback=60, entry_zscore=2.0, exit_zscore=0.5))
    return extract_signal(res, ticker)

def sig_pairs_trading(ohlcv, ticker):
    from strategies.stocks.pairs_trading import pairs_trading, PairsTradingRequest
    prices = _prices_list(ohlcv)
    # Aynı hisseyi iki bacak olarak kullanıyoruz; spread sıfır olur → çoğunlukla 0 sinyal
    res = pairs_trading(PairsTradingRequest(
        prices_a=prices, prices_b=prices, lookback=60, entry_zscore=2.0, exit_zscore=0.5))
    return extract_signal(res, ticker)

def sig_stat_arb(ohlcv, ticker):
    from strategies.stocks.stat_arb import stat_arb, StatArbRequest
    rets = np.array(_returns_list(ohlcv))
    exp_ret = float(np.mean(rets[-60:])) if len(rets) >= 60 else 0.0
    vol = float(np.std(rets[-60:])) if len(rets) >= 60 else 0.01
    cov = [[vol**2]]
    res = stat_arb(StatArbRequest(
        expected_returns={ticker: exp_ret},
        covariance_matrix=cov,
        asset_order=[ticker],
        risk_aversion=1.0))
    return extract_signal(res, ticker)

def sig_market_making(ohlcv, ticker):
    from strategies.stocks.market_making import market_making, MarketMakingRequest
    rets = np.array(_returns_list(ohlcv))
    mid = float(ohlcv["Close"].iloc[-1])
    vol = float(np.std(rets[-20:])) if len(rets) >= 20 else 0.01
    # Market making çıktısı sinyal üretmez; spread yönüne göre proxy sinyal
    res = market_making(MarketMakingRequest(mid_price=mid, volatility=vol, inventory=0.0))
    # Spread küçükse likit piyasa → AL; büyükse volatil → SAT
    try:
        r = res.model_dump()
        spread_pct = r["spread"] / mid if mid > 0 else 0
        return 1 if spread_pct < 0.002 else 0
    except Exception:
        return 0

def sig_event_driven(ohlcv, ticker):
    from strategies.stocks.event_driven import event_driven, EventDrivenRequest
    cur = float(ohlcv["Close"].iloc[-1])
    # Varsayımsal birleşme: %5 prim ile teklif
    offer = cur * 1.05
    res = event_driven(EventDrivenRequest(
        target_price=cur, acquirer_price=cur, offer_price=offer,
        exchange_ratio=0.0, cash_component=offer, deal_probability=0.8))
    return extract_signal(res, ticker)

def sig_knn(ohlcv, ticker):
    from strategies.stocks.knn import knn, KNNRequest
    rets = np.array(_returns_list(ohlcv))
    if len(rets) < 30:
        return 0
    # 5 günlük pencereler ile özellik vektörleri oluştur
    features = []
    labels   = []
    for i in range(5, len(rets) - 1):
        feat = rets[i-5:i].tolist()
        lbl  = 1 if rets[i] > 0 else -1
        features.append(feat)
        labels.append(lbl)
    cur_feat = rets[-5:].tolist()
    if not features:
        return 0
    res = knn(KNNRequest(features=features, labels=labels, current_features=cur_feat, k=5))
    return extract_signal(res, ticker)

def sig_alpha_combos(ohlcv, ticker):
    from strategies.stocks.alpha_combos import alpha_combos, AlphaCombosRequest
    rets = np.array(_returns_list(ohlcv))
    mom = float(np.sum(rets[-60:])) if len(rets) >= 60 else 0.0
    vol = -float(np.std(rets[-60:])) if len(rets) >= 60 else 0.0
    res = alpha_combos(AlphaCombosRequest(
        alphas={"momentum": {ticker: mom}, "low_vol": {ticker: vol}},
        neutralize=False))
    return extract_signal(res, ticker)

# ─── ETFs ────────────────────────────────────────────────────

def sig_sector_momentum(ohlcv, ticker):
    from strategies.etfs.sector_momentum import sector_momentum, SectorMomentumRequest
    rets = _returns_list(ohlcv)
    res = sector_momentum(SectorMomentumRequest(sector_returns={ticker: rets}, lookback=60, top_n=1))
    return extract_signal(res, ticker)

def sig_alpha_rotation(ohlcv, ticker):
    from strategies.etfs.alpha_rotation import alpha_rotation, AlphaRotationRequest
    rets = _returns_list(ohlcv)
    res = alpha_rotation(AlphaRotationRequest(
        sector_returns={ticker: rets}, market_returns=rets,
        risk_free_rate=0.0, lookback=60, top_n=1))
    return extract_signal(res, ticker)

def sig_r_squared(ohlcv, ticker):
    from strategies.etfs.r_squared import r_squared, RSquaredRequest
    prices = _prices_list(ohlcv)
    res = r_squared(RSquaredRequest(prices={ticker: prices}, lookback=60))
    return extract_signal(res, ticker)

def sig_mean_reversion_ibs(ohlcv, ticker):
    from strategies.etfs.mean_reversion import mean_reversion_ibs, MeanReversionIBSRequest
    h = float(ohlcv["High"].iloc[-1])
    l = float(ohlcv["Low"].iloc[-1])
    c = float(ohlcv["Close"].iloc[-1])
    ohlc_dict = {ticker: {"open": c, "high": h, "low": l, "close": c}}
    res = mean_reversion_ibs(MeanReversionIBSRequest(ohlc=ohlc_dict))
    return extract_signal(res, ticker)

def sig_leveraged_etfs(ohlcv, ticker):
    from strategies.etfs.leveraged_etfs import leveraged_etfs, LeveragedETFsRequest
    rets = _returns_list(ohlcv)
    res = leveraged_etfs(LeveragedETFsRequest(
        etf_returns={ticker: rets}, leverage_factors={ticker: 2.0}, lookback=20))
    return extract_signal(res, ticker)

def sig_multi_asset_trend(ohlcv, ticker):
    from strategies.etfs.multi_asset_trend import multi_asset_trend, MultiAssetTrendRequest
    prices = _prices_list(ohlcv)
    res = multi_asset_trend(MultiAssetTrendRequest(prices={ticker: prices}, lookback=60))
    return extract_signal(res, ticker)

# ─── VOLATİLİTE ──────────────────────────────────────────────

def sig_volatility_carry(ohlcv, ticker):
    from strategies.volatility.volatility_carry import volatility_carry, VolatilityCarryRequest
    prices = _prices_list(ohlcv)
    cur = prices[-1]
    res = volatility_carry(VolatilityCarryRequest(
        vxx_price=cur, vxz_price=cur * 0.9,
        vxx_prices=prices, vxz_prices=[p * 0.9 for p in prices],
        lookback=20))
    return extract_signal(res, ticker)

def sig_vix_futures_basis(ohlcv, ticker):
    from strategies.volatility.vix_futures_basis import vix_futures_basis, VixFuturesBasisRequest
    prices = _prices_list(ohlcv)
    rets = np.array(_returns_list(ohlcv))
    spot_vix = float(np.std(rets[-20:]) * np.sqrt(252) * 100) if len(rets) >= 20 else 15.0
    res = vix_futures_basis(VixFuturesBasisRequest(
        spot_vix=spot_vix, futures_vix=spot_vix * 1.05, vix_history=[spot_vix] * 30))
    return extract_signal(res, ticker)

def sig_variance_swaps(ohlcv, ticker):
    from strategies.volatility.variance_swaps import variance_swaps, VarianceSwapsRequest
    rets = _returns_list(ohlcv)
    realized_var = float(np.var(rets[-20:]) * 252) if len(rets) >= 20 else 0.04
    strike_var = realized_var * 1.1
    res = variance_swaps(VarianceSwapsRequest(
        realized_variance=realized_var, strike_variance=strike_var, notional=1_000_000))
    return extract_signal(res, ticker)

# ─── FX ──────────────────────────────────────────────────────

def sig_fx_moving_averages(ohlcv, ticker):
    from strategies.fx.fx_moving_averages import fx_moving_averages, FxMovingAveragesRequest
    prices = _prices_list(ohlcv)[-120:]
    res = fx_moving_averages(FxMovingAveragesRequest(prices=prices, hp_lambda=1600, lookback=100))
    return extract_signal(res, ticker)

def sig_fx_carry_trade(ohlcv, ticker):
    from strategies.fx.fx_carry_trade import fx_carry_trade, FxCarryTradeRequest
    rets = np.array(_returns_list(ohlcv))
    ann_ret = float(np.mean(rets[-252:])) * 252 if len(rets) >= 252 else 0.05
    res = fx_carry_trade(FxCarryTradeRequest(
        currencies={ticker: {"spot_rate": 1.0, "interest_rate": max(0.01, ann_ret)}},
        funding_currency_rate=0.02))
    return extract_signal(res, ticker)

def sig_fx_triangular_arb(ohlcv, ticker):
    from strategies.fx.fx_triangular_arb import fx_triangular_arb, FxTriangularArbRequest
    cur = float(ohlcv["Close"].iloc[-1])
    # Üçgen arbitraj için 3 kur gerekli; syntetik olarak oluşturuyoruz
    res = fx_triangular_arb(FxTriangularArbRequest(
        rate_ab=1.0, rate_bc=cur / 100.0, rate_ac=cur / 100.0,
        transaction_cost=0.0001))
    return extract_signal(res, ticker)

# ─── EMTİA (Commodities) ──────────────────────────────────────

def sig_roll_yields(ohlcv, ticker):
    from strategies.commodities.roll_yields import roll_yields, RollYieldsRequest, CommodityContract
    prices = _prices_list(ohlcv)
    front = prices[-1]
    nxt   = prices[-30] if len(prices) >= 30 else prices[0]
    res = roll_yields(RollYieldsRequest(
        commodities=[CommodityContract(symbol=ticker, front_price=front, next_price=nxt, days_to_roll=30)],
        top_n=1, min_roll_yield=0.0))
    return extract_signal(res, ticker)

def sig_hedging_pressure(ohlcv, ticker):
    from strategies.commodities.hedging_pressure import hedging_pressure, HedgingPressureRequest
    rets = _returns_list(ohlcv)
    res = hedging_pressure(HedgingPressureRequest(
        commodity_returns={ticker: rets},
        producer_hedging={ticker: -0.5},
        speculator_positions={ticker: 0.3}))
    return extract_signal(res, ticker)

# ─── VEİLİ SÖZLEŞMELER (Futures) ─────────────────────────────

def sig_trend_following(ohlcv, ticker):
    from strategies.futures.trend_following import trend_following, TrendFollowingRequest, TrendAsset
    prices = _prices_list(ohlcv)
    asset = TrendAsset(symbol=ticker, prices=prices)
    res = trend_following(TrendFollowingRequest(
        assets=[asset], short_lookback=20, medium_lookback=60, long_lookback=120))
    return extract_signal(res, ticker)

def sig_contrarian(ohlcv, ticker):
    from strategies.futures.contrarian import contrarian, ContrarianRequest, FuturesAsset
    weekly = _weekly_returns(ohlcv)
    asset = FuturesAsset(symbol=ticker, weekly_returns=weekly)
    res = contrarian(ContrarianRequest(
        assets=[asset], market_returns=weekly, lookback=4, top_n=1))
    return extract_signal(res, ticker)

def sig_hedging_with_futures(ohlcv, ticker):
    from strategies.futures.hedging_with_futures import hedging_with_futures, HedgingWithFuturesRequest
    rets = _returns_list(ohlcv)
    res = hedging_with_futures(HedgingWithFuturesRequest(
        spot_returns=rets, futures_returns=rets, spot_position=1.0))
    return extract_signal(res, ticker)

# ─── KRİPTO ──────────────────────────────────────────────────

def sig_ann_crypto(ohlcv, ticker):
    from strategies.crypto.ann_crypto import ann_crypto, ANNCryptoRequest
    prices  = _prices_list(ohlcv)
    volumes = _volumes_list(ohlcv)
    res = ann_crypto(ANNCryptoRequest(prices=prices, volumes=volumes, lookback=14))
    return extract_signal(res, ticker)

def sig_sentiment_crypto(ohlcv, ticker):
    from strategies.crypto.sentiment_crypto import sentiment_crypto, SentimentCryptoRequest
    rets = _returns_list(ohlcv)
    prices = _prices_list(ohlcv)
    # Getiriyi normalize edip sentiment proxy olarak kullan
    sentiments = [max(-1.0, min(1.0, r * 10)) for r in rets]
    volumes_int = [max(1, int(abs(r) * 1000)) for r in rets]
    res = sentiment_crypto(SentimentCryptoRequest(
        sentiment_scores=sentiments, sentiment_volumes=volumes_int,
        prices=prices, lookback=24))
    return extract_signal(res, ticker)

# ─── SABİT GELİR (Fixed Income) ───────────────────────────────

def _make_dummy_bond(ticker, price):
    """Tahvil stratejileri için sentetik bono verisi oluşturur."""
    from strategies.fixed_income.carry_factor import CarryBond
    return CarryBond(cusip=ticker, issuer=ticker, yield_to_maturity=0.045,
                     maturity_years=10.0, duration=8.0, coupon_rate=0.04,
                     price=price, yield_1y_shorter=0.04)

def sig_carry_factor(ohlcv, ticker):
    from strategies.fixed_income.carry_factor import carry_factor, CarryFactorRequest
    price = float(ohlcv["Close"].iloc[-1])
    bond = _make_dummy_bond(ticker, price)
    res = carry_factor(CarryFactorRequest(bond_universe=[bond], funding_rate=0.025,
                                          holding_period=1.0, portfolio_value=10000, top_n=1))
    return 1 if res.expected_return > 0 else 0

def sig_bullets(ohlcv, ticker):
    from strategies.fixed_income.bullets import bullets, BulletsRequest
    price = float(ohlcv["Close"].iloc[-1])
    bond = _make_dummy_bond(ticker, price)
    res = bullets(BulletsRequest(bond_universe=[bond], target_maturity=10.0,
                                  maturity_band=2.0, portfolio_value=10000, top_n=1))
    return extract_signal(res, ticker)

def sig_barbells(ohlcv, ticker):
    from strategies.fixed_income.barbells import barbells, BarbellsRequest
    price = float(ohlcv["Close"].iloc[-1])
    short_bond = _make_dummy_bond(ticker + "_S", price)
    short_bond.maturity_years = 2.0
    long_bond  = _make_dummy_bond(ticker + "_L", price)
    long_bond.maturity_years  = 20.0
    res = barbells(BarbellsRequest(bond_universe=[short_bond, long_bond],
                                    short_maturity_max=3.0, long_maturity_min=15.0,
                                    portfolio_value=10000))
    return extract_signal(res, ticker)

def sig_ladders(ohlcv, ticker):
    from strategies.fixed_income.ladders import ladders, LaddersRequest
    price = float(ohlcv["Close"].iloc[-1])
    bonds = []
    for yr in [1, 2, 3, 5, 7, 10]:
        b = _make_dummy_bond(f"{ticker}_{yr}Y", price)
        b.maturity_years = float(yr)
        bonds.append(b)
    res = ladders(LaddersRequest(bond_universe=bonds, num_rungs=5,
                                  min_maturity=1.0, max_maturity=10.0, portfolio_value=10000))
    return extract_signal(res, ticker)

def _fi_signal_from_returns(ohlcv, func_name, req_class_name):
    """Fixed income stratejileri için genel sarmalayıcı; try/except ile güvenli."""
    try:
        import importlib
        mod = importlib.import_module(f"strategies.fixed_income.{func_name}")
        fn  = getattr(mod, func_name)
        RC  = getattr(mod, req_class_name)
        rets = _returns_list(ohlcv)
        res = fn(RC(returns=rets))
        return extract_signal(res, "")
    except Exception:
        return 0

def sig_bond_immunization(ohlcv, ticker):
    try:
        from strategies.fixed_income.bond_immunization import bond_immunization, BondImmunizationRequest
        price = float(ohlcv["Close"].iloc[-1])
        bond = _make_dummy_bond(ticker, price)
        res = bond_immunization(BondImmunizationRequest(
            bond_universe=[bond], liability_duration=7.0,
            liability_amount=10000, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_dollar_duration_butterfly(ohlcv, ticker):
    try:
        from strategies.fixed_income.dollar_duration_butterfly import dollar_duration_butterfly, DollarDurationButterflyRequest
        price = float(ohlcv["Close"].iloc[-1])
        short = _make_dummy_bond(ticker + "_S", price); short.maturity_years = 2.0
        belly = _make_dummy_bond(ticker + "_M", price); belly.maturity_years = 7.0
        long  = _make_dummy_bond(ticker + "_L", price); long.maturity_years  = 20.0
        res = dollar_duration_butterfly(DollarDurationButterflyRequest(
            short_bond=short, belly_bond=belly, long_bond=long, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_fifty_fifty_butterfly(ohlcv, ticker):
    try:
        from strategies.fixed_income.fifty_fifty_butterfly import fifty_fifty_butterfly, FiftyFiftyButterflyRequest
        price = float(ohlcv["Close"].iloc[-1])
        short = _make_dummy_bond(ticker + "_S", price); short.maturity_years = 2.0
        belly = _make_dummy_bond(ticker + "_M", price); belly.maturity_years = 7.0
        long  = _make_dummy_bond(ticker + "_L", price); long.maturity_years  = 20.0
        res = fifty_fifty_butterfly(FiftyFiftyButterflyRequest(
            short_bond=short, belly_bond=belly, long_bond=long, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_regression_butterfly(ohlcv, ticker):
    try:
        from strategies.fixed_income.regression_butterfly import regression_butterfly, RegressionButterflyRequest
        price = float(ohlcv["Close"].iloc[-1])
        short = _make_dummy_bond(ticker + "_S", price); short.maturity_years = 2.0
        belly = _make_dummy_bond(ticker + "_M", price); belly.maturity_years = 7.0
        long  = _make_dummy_bond(ticker + "_L", price); long.maturity_years  = 20.0
        res = regression_butterfly(RegressionButterflyRequest(
            short_bond=short, belly_bond=belly, long_bond=long, history_length=60, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_low_risk_factor(ohlcv, ticker):
    try:
        from strategies.fixed_income.low_risk_factor import low_risk_factor, LowRiskFactorRequest
        price = float(ohlcv["Close"].iloc[-1])
        bond = _make_dummy_bond(ticker, price)
        res = low_risk_factor(LowRiskFactorRequest(
            bond_universe=[bond], top_pct=1.0, bottom_pct=0.0, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_value_factor(ohlcv, ticker):
    try:
        from strategies.fixed_income.value_factor import value_factor, ValueFactorRequest
        price = float(ohlcv["Close"].iloc[-1])
        bond = _make_dummy_bond(ticker, price)
        res = value_factor(ValueFactorRequest(
            bond_universe=[bond], top_pct=1.0, bottom_pct=0.0, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_rolling_down(ohlcv, ticker):
    try:
        from strategies.fixed_income.rolling_down_yield_curve import rolling_down_yield_curve, RollingDownYieldCurveRequest
        price = float(ohlcv["Close"].iloc[-1])
        bond = _make_dummy_bond(ticker, price)
        res = rolling_down_yield_curve(RollingDownYieldCurveRequest(
            bond_universe=[bond], holding_period=1.0,
            yield_curve_points={2: 0.04, 5: 0.043, 10: 0.045, 20: 0.047},
            portfolio_value=10000, top_n=1))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_yield_curve_spreads(ohlcv, ticker):
    try:
        from strategies.fixed_income.yield_curve_spreads import yield_curve_spreads, YieldCurveSpreadsRequest
        rets = np.array(_returns_list(ohlcv))
        spread = float(np.mean(rets[-20:])) * 252 if len(rets) >= 20 else 0.002
        res = yield_curve_spreads(YieldCurveSpreadsRequest(
            short_yield=0.04, long_yield=0.045,
            short_bond_duration=2.0, long_bond_duration=10.0,
            historical_spread=[spread] * 60, entry_zscore=1.5, portfolio_value=10000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_cds_basis(ohlcv, ticker):
    try:
        from strategies.fixed_income.cds_basis_arbitrage import cds_basis_arbitrage, CDSBasisArbitrageRequest
        res = cds_basis_arbitrage(CDSBasisArbitrageRequest(
            bond_spread=0.02, cds_spread=0.025, funding_rate=0.015,
            notional=1_000_000, maturity_years=5.0))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_swap_spread(ohlcv, ticker):
    try:
        from strategies.fixed_income.swap_spread_arbitrage import swap_spread_arbitrage, SwapSpreadArbitrageRequest
        res = swap_spread_arbitrage(SwapSpreadArbitrageRequest(
            swap_rate=0.045, treasury_yield=0.043, repo_rate=0.025,
            maturity_years=10.0, notional=1_000_000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── İNDEKS ──────────────────────────────────────────────────

def sig_cash_and_carry(ohlcv, ticker):
    try:
        from strategies.index.cash_and_carry import cash_and_carry, CashAndCarryRequest
        prices = _prices_list(ohlcv)
        spot = prices[-1]
        futures_price = spot * 1.02
        res = cash_and_carry(CashAndCarryRequest(
            spot_price=spot, futures_price=futures_price,
            risk_free_rate=0.05, time_to_expiry=0.25, dividend_yield=0.02))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_intraday_index_arb(ohlcv, ticker):
    try:
        from strategies.index.intraday_index_arb import intraday_index_arb, IntradayIndexArbRequest
        prices = _prices_list(ohlcv)
        spot = prices[-1]
        res = intraday_index_arb(IntradayIndexArbRequest(
            index_spot=spot, futures_price=spot * 1.001,
            basket_value=spot, transaction_cost=0.0005))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_volatility_targeting(ohlcv, ticker):
    from strategies.index.volatility_targeting import volatility_targeting, VolatilityTargetingRequest
    rets = _returns_list(ohlcv)
    res = volatility_targeting(VolatilityTargetingRequest(
        returns=rets, target_volatility=0.15, lookback=20))
    return extract_signal(res, ticker)

# ─── MAKRO ────────────────────────────────────────────────────

def sig_fundamental_macro(ohlcv, ticker):
    try:
        from strategies.macro.fundamental_macro import fundamental_macro, FundamentalMacroRequest
        rets = np.array(_returns_list(ohlcv))
        gdp_growth = float(np.mean(rets[-60:])) * 252 if len(rets) >= 60 else 0.02
        res = fundamental_macro(FundamentalMacroRequest(
            gdp_growth=gdp_growth, inflation=0.03, interest_rate=0.05,
            unemployment=0.04, current_account=-0.02))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_economic_announcements(ohlcv, ticker):
    try:
        from strategies.macro.economic_announcements import economic_announcements, EconomicAnnouncementsRequest
        rets = np.array(_returns_list(ohlcv))
        surprise = float(np.mean(rets[-5:])) if len(rets) >= 5 else 0.0
        res = economic_announcements(EconomicAnnouncementsRequest(
            announcement_type="gdp", expected_value=2.0,
            actual_value=2.0 + surprise * 100, asset_returns=rets[-60:].tolist()))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── ÇEŞİTLİ (Misc) ──────────────────────────────────────────

def sig_inflation_swaps(ohlcv, ticker):
    try:
        from strategies.misc.inflation_swaps import inflation_swaps, InflationSwapsRequest
        rets = np.array(_returns_list(ohlcv))
        breakeven = float(np.mean(rets[-252:])) * 252 if len(rets) >= 252 else 0.025
        res = inflation_swaps(InflationSwapsRequest(
            breakeven_inflation=breakeven, inflation_swap_rate=breakeven + 0.003,
            notional=1_000_000, maturity_years=5.0))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_weather_risk(ohlcv, ticker):
    try:
        from strategies.misc.weather_risk import weather_risk, WeatherRiskRequest
        res = weather_risk(WeatherRiskRequest(
            temperature_forecast=20.0, temperature_normal=18.0,
            hdd_strikes=[0.0], cdd_strikes=[10.0],
            energy_price_correlation=0.3))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── SIKINTILI VARLIKLARI (Distressed) ───────────────────────

def sig_distressed_debt(ohlcv, ticker):
    try:
        from strategies.distressed.distressed_debt import distressed_debt, DistressedDebtRequest
        rets = np.array(_returns_list(ohlcv))
        # Son dönem düşük getiri → sıkıntılı varlık simülasyonu
        avg_ret = float(np.mean(rets[-60:])) * 252 if len(rets) >= 60 else 0.0
        res = distressed_debt(DistressedDebtRequest(
            face_value=100.0, market_price=max(20.0, 100.0 + avg_ret * 100),
            recovery_rate=0.4, default_probability=0.1, yield_to_maturity=0.15))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_distress_risk_puzzle(ohlcv, ticker):
    try:
        from strategies.distressed.distress_risk_puzzle import distress_risk_puzzle, DistressRiskPuzzleRequest
        rets = np.array(_returns_list(ohlcv))
        res = distress_risk_puzzle(DistressRiskPuzzleRequest(
            altman_z_score=2.5, market_leverage=0.3,
            stock_returns=rets[-60:].tolist(), market_returns=[0.0] * 60))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── GAYRİMENKUL (Real Estate) ───────────────────────────────

def sig_real_estate_diversity(ohlcv, ticker):
    try:
        from strategies.real_estate.real_estate_diversity import real_estate_diversity, RealEstateDiversityRequest
        rets = _returns_list(ohlcv)
        res = real_estate_diversity(RealEstateDiversityRequest(
            property_returns={ticker: rets}, property_types={ticker: "residential"}))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_fix_and_flip(ohlcv, ticker):
    try:
        from strategies.real_estate.fix_and_flip import fix_and_flip, FixAndFlipRequest
        price = float(ohlcv["Close"].iloc[-1])
        res = fix_and_flip(FixAndFlipRequest(
            purchase_price=price * 100, renovation_cost=price * 20,
            arv=price * 150, holding_months=6, financing_rate=0.08))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── YAPILANDIRILMIŞ ÜRÜNLER (Structured) ────────────────────

def sig_cdo_tranche(ohlcv, ticker):
    try:
        from strategies.structured.cdo_tranche import cdo_tranche, CDOTrancheRequest
        res = cdo_tranche(CDOTrancheRequest(
            attachment_point=0.03, detachment_point=0.07,
            default_correlations=[[1.0]], recovery_rate=0.4,
            hazard_rates=[0.02], notional=1_000_000))
        return extract_signal(res, ticker)
    except Exception:
        return 0

def sig_mbs(ohlcv, ticker):
    try:
        from strategies.structured.mbs import mbs, MBSRequest
        res = mbs(MBSRequest(
            mortgage_rate=0.065, market_rate=0.055, prepayment_speed=150.0,
            outstanding_balance=1_000_000, wam=300))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── DÖNÜŞTÜRÜLEBİLİR TAHVİL (Convertibles) ─────────────────

def sig_convertible_arbitrage(ohlcv, ticker):
    try:
        from strategies.convertibles.arbitrage import convertible_arbitrage, ConvertibleArbitrageRequest
        price = float(ohlcv["Close"].iloc[-1])
        rets = np.array(_returns_list(ohlcv))
        vol = float(np.std(rets[-60:])) * np.sqrt(252) if len(rets) >= 60 else 0.3
        res = convertible_arbitrage(ConvertibleArbitrageRequest(
            stock_price=price, conversion_ratio=5.0,
            bond_face=1000.0, bond_price=950.0,
            stock_volatility=vol, risk_free_rate=0.05,
            time_to_maturity=3.0, coupon_rate=0.03))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ─── VERGİ ARBİTRAJI (Tax) ───────────────────────────────────

def sig_muni_arbitrage(ohlcv, ticker):
    try:
        from strategies.tax.muni_arbitrage import muni_arbitrage, MuniArbitrageRequest
        res = muni_arbitrage(MuniArbitrageRequest(
            muni_yield=0.035, taxable_yield=0.05,
            tax_rate=0.37, state_tax_rate=0.05))
        return extract_signal(res, ticker)
    except Exception:
        return 0

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 5: STRATEJİ KAYIT DEFTERİ (68 Strateji)
# ═══════════════════════════════════════════════════════════════

STRATEGY_REGISTRY = {
    # STOCKS (20)
    "single_ma":             sig_single_ma,
    "two_ma":                sig_two_ma,
    "three_ma":              sig_three_ma,
    "channel":               sig_channel,
    "support_resistance":    sig_support_resistance,
    "price_momentum":        sig_price_momentum,
    "low_volatility":        sig_low_volatility,
    "value":                 sig_value,
    "implied_volatility":    sig_implied_volatility,
    "earnings_momentum":     sig_earnings_momentum,
    "residual_momentum":     sig_residual_momentum,
    "multifactor":           sig_multifactor,
    "weighted_regression":   sig_weighted_regression,
    "mean_reversion_cluster":sig_mean_reversion_cluster,
    "pairs_trading":         sig_pairs_trading,
    "stat_arb":              sig_stat_arb,
    "market_making":         sig_market_making,
    "event_driven":          sig_event_driven,
    "knn":                   sig_knn,
    "alpha_combos":          sig_alpha_combos,
    # ETFs (6)
    "sector_momentum":       sig_sector_momentum,
    "alpha_rotation":        sig_alpha_rotation,
    "r_squared":             sig_r_squared,
    "mean_reversion_ibs":    sig_mean_reversion_ibs,
    "leveraged_etfs":        sig_leveraged_etfs,
    "multi_asset_trend":     sig_multi_asset_trend,
    # Volatility (3)
    "volatility_carry":      sig_volatility_carry,
    "vix_futures_basis":     sig_vix_futures_basis,
    "variance_swaps":        sig_variance_swaps,
    # FX (3)
    "fx_moving_averages":    sig_fx_moving_averages,
    "fx_carry_trade":        sig_fx_carry_trade,
    "fx_triangular_arb":     sig_fx_triangular_arb,
    # Commodities (2)
    "roll_yields":           sig_roll_yields,
    "hedging_pressure":      sig_hedging_pressure,
    # Futures (3)
    "trend_following":       sig_trend_following,
    "contrarian":            sig_contrarian,
    "hedging_with_futures":  sig_hedging_with_futures,
    # Crypto (2)
    "ann_crypto":            sig_ann_crypto,
    "sentiment_crypto":      sig_sentiment_crypto,
    # Fixed Income (14)
    "carry_factor":          sig_carry_factor,
    "bullets":               sig_bullets,
    "barbells":              sig_barbells,
    "ladders":               sig_ladders,
    "bond_immunization":     sig_bond_immunization,
    "dollar_duration_butterfly": sig_dollar_duration_butterfly,
    "fifty_fifty_butterfly": sig_fifty_fifty_butterfly,
    "regression_butterfly":  sig_regression_butterfly,
    "low_risk_factor":       sig_low_risk_factor,
    "value_factor":          sig_value_factor,
    "rolling_down_yield_curve": sig_rolling_down,
    "yield_curve_spreads":   sig_yield_curve_spreads,
    "cds_basis_arbitrage":   sig_cds_basis,
    "swap_spread_arbitrage": sig_swap_spread,
    # Index (3)
    "cash_and_carry":        sig_cash_and_carry,
    "intraday_index_arb":    sig_intraday_index_arb,
    "volatility_targeting":  sig_volatility_targeting,
    # Macro (2)
    "fundamental_macro":     sig_fundamental_macro,
    "economic_announcements":sig_economic_announcements,
    # Misc (2)
    "inflation_swaps":       sig_inflation_swaps,
    "weather_risk":          sig_weather_risk,
    # Distressed (2)
    "distressed_debt":       sig_distressed_debt,
    "distress_risk_puzzle":  sig_distress_risk_puzzle,
    # Real Estate (2)
    "real_estate_diversity": sig_real_estate_diversity,
    "fix_and_flip":          sig_fix_and_flip,
    # Structured (2)
    "cdo_tranche":           sig_cdo_tranche,
    "mbs":                   sig_mbs,
    # Convertibles (1)
    "convertible_arbitrage": sig_convertible_arbitrage,
    # Tax (1)
    "muni_arbitrage":        sig_muni_arbitrage,
}

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 6: BACKTEST VE PNG KAYDETME
# ═══════════════════════════════════════════════════════════════

def run_backtest_and_save_png(prices: pd.Series, signal: int, ticker: str,
                               strategy_name: str, output_dir: str) -> dict:
    """VectorBT backtest çalıştırır, PNG kaydeder, metrikleri döndürür."""
    n = len(prices)
    entries       = pd.Series([False] * n, index=prices.index)
    exits         = pd.Series([False] * n, index=prices.index)
    short_entries = pd.Series([False] * n, index=prices.index)
    short_exits   = pd.Series([False] * n, index=prices.index)

    if signal == 1:
        entries.iloc[0]  = True
        exits.iloc[-1]   = True
    elif signal == -1:
        short_entries.iloc[0] = True
        short_exits.iloc[-1]  = True

    portfolio = vbt.Portfolio.from_signals(
        close=prices, entries=entries, exits=exits,
        short_entries=short_entries, short_exits=short_exits,
        init_cash=INIT_CASH, fees=0.001, freq="1d")

    # PNG çiz ve kaydet
    fig, ax = plt.subplots(figsize=(12, 4))
    portfolio.value().plot(ax=ax)
    ax.set_title(f"{ticker} — {strategy_name}  (Sinyal: {signal})")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Portföy Değeri ($)")
    ax.grid(True, alpha=0.3)
    fig.savefig(os.path.join(output_dir, f"{strategy_name}.png"), dpi=90, bbox_inches="tight")
    plt.close(fig)

    try:
        total_return = round(portfolio.total_return() * 100, 2)
        max_drawdown = round(portfolio.max_drawdown() * -100, 2)
        sharpe       = round(portfolio.sharpe_ratio(), 2)
        calmar       = round(portfolio.calmar_ratio(), 2)
        pf           = round(portfolio.trades.profit_factor(), 2)
        trade_count  = portfolio.trades.count()
    except Exception:
        total_return = max_drawdown = sharpe = calmar = pf = 0.0
        trade_count = 0

    return {
        "Hisse": ticker, "Strateji": strategy_name, "Sinyal": signal,
        "Getiri (%)": total_return, "Max Kayip (%)": max_drawdown,
        "Sharpe": sharpe, "Calmar": calmar,
        "Kar Faktoru": pf, "Islem Sayisi": trade_count,
    }

# ═══════════════════════════════════════════════════════════════
#  BÖLÜM 7: ANA DÖNGÜ
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*60)
    print("  DOW30 TAM ANALIZ SISTEMI -- 68 STRATEJI")
    print(f"  Tarih   : {START_DATE} -> {END_DATE}")
    print(f"  Hisse   : {len(DOW30_TICKERS)}  |  Strateji: {len(STRATEGY_REGISTRY)}")
    print("="*60 + "\n")

    all_results = []  # Tüm hisseler için devasa CSV

    for ticker in DOW30_TICKERS:
        print(f"[{ticker}] isleniyor... ({len(STRATEGY_REGISTRY)} strateji)")
        output_dir = os.path.join("results", ticker)
        os.makedirs(output_dir, exist_ok=True)

        # OHLCV veriyi indir
        ohlcv = fetch_data(ticker)
        prices = ohlcv["Close"].squeeze()

        ticker_results = []  # Bu hisseye özgü CSV

        for strategy_name, signal_fn in STRATEGY_REGISTRY.items():
            try:
                # Strateji sinyalini hesapla
                signal = signal_fn(ohlcv, ticker)
            except Exception:
                signal = 0

            # Backtest + PNG
            metrics = run_backtest_and_save_png(prices, signal, ticker, strategy_name, output_dir)
            ticker_results.append(metrics)
            all_results.append(metrics)

        # Bu hissenin kendi summary.csv dosyasını kaydet
        ticker_csv_path = os.path.join(output_dir, "summary.csv")
        pd.DataFrame(ticker_results).to_csv(ticker_csv_path, index=False)
        print(f"  [OK] {len(ticker_results)} strateji tamamlandi -> {ticker_csv_path}")
        print("")

    # Tüm hisseleri ve stratejileri kapsayan devasa özet CSV
    all_csv_path = os.path.join("results", "summary_all.csv")
    pd.DataFrame(all_results).to_csv(all_csv_path, index=False)

    print("\n" + "="*60)
    print("  TAMAMLANDI!")
    print(f"  Toplam kayit  : {len(all_results)} satir")
    print(f"  Ozet tablo    : {all_csv_path}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
