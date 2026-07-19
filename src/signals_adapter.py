def normalize_signals(response_data: dict, default_symbol: str = "ASSET") -> dict[str, int]:
    """
    Herhangi bir strateji çıktısını alır ve standart {sembol: sinyal} formatına dönüştürür.
    Sinyal değerleri: 1 (Al), -1 (Sat), 0 (Tut/Çık)
    """
    normalized = {}

    # 1. DURUM: Doğrudan tekil 'signal' alanı varsa (Örn: ANNCrypto, SingleMA)
    if "signal" in response_data:
        # Tek bir varlık testi olduğu için default_symbol kullanıyoruz
        normalized[default_symbol] = int(response_data["signal"])
        return normalized
    # 2. DURUM: Ağırlıklar (weights) sözlüğü varsa
    elif "weights" in response_data and isinstance(response_data["weights"], dict):
        for symbol, weight in response_data["weights"].items():
            if weight > 0:
                normalized[symbol] = 1
            elif weight < 0:
                normalized[symbol] = -1
            else:
                normalized[symbol] = 0
        return normalized
    # 3. DURUM: Ayrı ayrı long ve short listeleri varsa (Örn: CommodityValue, PriceMomentum)
    longs = response_data.get("long_assets") or response_data.get("long_commodities") or response_data.get("long_futures") or response_data.get("long_pairs")
    shorts = response_data.get("short_assets") or response_data.get("short_commodities") or response_data.get("short_futures") or response_data.get("short_pairs")

    if longs is not None or shorts is not None:
        long_list = longs if longs else []
        short_list = shorts if shorts else []
        
        # Long listesindekiler -> 1
        for symbol in long_list:
            normalized[symbol] = 1
        # Short listesindekiler -> -1
        for symbol in short_list:
            normalized[symbol] = -1
        return normalized
    # 4. DURUM: Pozisyon listesi varsa
    elif "positions" in response_data and isinstance(response_data["positions"], list):
        for pos in response_data["positions"]:
            # pos bir sözlük veya pydantic nesnesi olabilir
            symbol = pos.get("symbol") if isinstance(pos, dict) else getattr(pos, "symbol", None)
            signal = pos.get("signal") if isinstance(pos, dict) else getattr(pos, "signal", None)
            
            if symbol is not None and signal is not None:
                normalized[symbol] = int(signal)
        return normalized
    return normalized
# Dosyanın en altına ekle:
if __name__ == "__main__":
    print("=== SİNYAL ADAPTÖRÜ TESTLERİ BAŞLATILDI ===\n")

    # 1. Test: Tekil Sinyal (Örn: single_ma)
    test_1 = {"strategy": "single_ma", "signal": -1}
    print("1. Tekil Sinyal Testi:")
    print("Girdi:", test_1)
    print("Çıktı:", normalize_signals(test_1, default_symbol="BTC-USD"))
    print("-" * 50)

    # 2. Test: Ağırlık Sözlüğü (Örn: price_momentum)
    test_2 = {
        "strategy": "price_momentum", 
        "weights": {"AAPL": 0.4, "MSFT": -0.2, "GOOG": 0.0}
    }
    print("2. Ağırlık Sözlüğü Testi:")
    print("Girdi:", test_2)
    print("Çıktı:", normalize_signals(test_2))
    print("-" * 50)

    # 3. Test: Long/Short Listesi (Örn: commodity_value)
    test_3 = {
        "strategy": "commodity_value",
        "long_commodities": ["GOLD", "SILVER"],
        "short_commodities": ["OIL"]
    }
    print("3. Long/Short Listesi Testi:")
    print("Girdi:", test_3)
    print("Çıktı:", normalize_signals(test_3))
    print("-" * 50)

    # 4. Test: Pozisyon Listesi (Örn: trend_following)
    test_4 = {
        "strategy": "trend_following",
        "positions": [
            {"symbol": "XBT", "signal": 1},
            {"symbol": "ETH", "signal": -1},
            {"symbol": "XRP", "signal": 0}
        ]
    }
    print("4. Pozisyon Listesi Testi:")
    print("Girdi:", test_4)
    print("Çıktı:", normalize_signals(test_4))
    print("\n=== TÜM TESTLER TAMAMLANDI ===")
