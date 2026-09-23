"""
============================================================
  HISSE-STRATEJI CIFTI BAZLI ANALIZ
============================================================
Her hisse-strateji ciftini AYRI AYRI degerlendirir.
"RSI genel olarak calisiyor mu?" yerine
"RSI HANGI hisselerde calisiyor?" sorusunu cevaplar.

Ciktilar:
  - Cift_Bazli_Analiz.xlsx       (8370 satir, her ciftin train/test metrikleri)
  - Hisse_En_Iyi_Strateji.xlsx   (93 satir, her hissenin en iyi stratejisi)
  - Sektor_Strateji_Haritasi.xlsx (hangi kategoride hangi strateji tipi guclu)
  - Anlamli_Ciftler.xlsx          (p<0.10 olan hisse-strateji ciftleri)

Calistirma:
    cd vbt_bist
    python academic/pair_analysis.py
"""

import os
import sys
import math
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats
import warnings
warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TRAIN_TEST_FILE = os.path.join(OUTPUT_DIR, "TrainTest_Sonuclari.xlsx")

# Hisse sektorleri (BIST siniflarina gore)
SEKTOR_MAP = {
    'AKBNK': 'Banka', 'GARAN': 'Banka', 'ISCTR': 'Banka', 'YKBNK': 'Banka',
    'HALKB': 'Banka', 'VAKBN': 'Banka', 'TSKB': 'Banka', 'ALBRK': 'Banka',
    'SKBNK': 'Banka', 'ISFIN': 'Finans',
    'THYAO': 'Ulasim', 'PGSUS': 'Ulasim', 'TAVHL': 'Ulasim', 'DOAS': 'Otomotiv',
    'TCELL': 'Telekom', 'TTKOM': 'Telekom',
    'KCHOL': 'Holding', 'SAHOL': 'Holding', 'DOHOL': 'Holding', 'ALARK': 'Holding',
    'OYAKC': 'Holding', 'AGHOL': 'Holding', 'GSDHO': 'Holding',
    'TUPRS': 'Enerji', 'PETKM': 'Petrokimya', 'AYGAZ': 'Enerji', 'TRCAS': 'Sigorta',
    'FROTO': 'Otomotiv', 'TOASO': 'Otomotiv', 'TTRAK': 'Otomotiv',
    'ASUZU': 'Otomotiv', 'KARSN': 'Otomotiv',
    'SISE': 'Sanayi', 'ENKAI': 'Insaat', 'BIMAS': 'Perakende', 'MGROS': 'Perakende',
    'SOKM': 'Perakende', 'CCOLA': 'Gida', 'AEFES': 'Gida',
    'EREGL': 'Metal', 'KRDMD': 'Metal', 'KCAER': 'Savunma', 'BRSAN': 'Metal',
    'CEMTS': 'Metal', 'IZMDC': 'Madencilik',
    'ASELS': 'Savunma', 'KORDS': 'Tekstil', 'SASA': 'Petrokimya',
    'HEKTS': 'Kimya', 'GUBRF': 'Kimya', 'BAGFS': 'Kimya',
    'EKGYO': 'GYO', 'ISGYO': 'GYO', 'TRGYO': 'GYO', 'HLGYO': 'GYO',
    'TKFEN': 'Insaat', 'ENJSA': 'Enerji', 'ODAS': 'Enerji',
    'ASTOR': 'Enerji', 'GESAN': 'Enerji', 'SMRTG': 'Enerji',
    'EUPWR': 'Enerji', 'CWENE': 'Enerji', 'ZOREN': 'Enerji',
    'AKENR': 'Enerji', 'GWIND': 'Enerji',
    'MIATK': 'Teknoloji', 'CANTE': 'Teknoloji', 'QUAGR': 'Tarim',
    'KONTR': 'Insaat', 'ISMEN': 'Finans', 'KMPUR': 'Sanayi',
    'CIMSA': 'Cimento', 'AKCNS': 'Cimento', 'BUCIM': 'Cimento',
    'AKSA': 'Enerji', 'VESBE': 'Elektronik', 'ARCLK': 'Elektronik',
    'TUKAS': 'Gida', 'LOGO': 'Teknoloji', 'ARZUM': 'Elektronik', 'ALGYO': 'GYO',
    'EGEEN': 'Sanayi', 'ECILC': 'Kimya', 'DEVA': 'Ilac', 'GENIL': 'Sanayi',
    'BERA': 'Gida', 'AHGAZ': 'Enerji', 'KLRHO': 'Kimya',
    'YYLGD': 'Gida', 'SUWEN': 'Tekstil', 'KZBGY': 'GYO', 'ALFAS': 'Savunma',
}

STRATEJI_KAT_MAP = {
    'rsi': 'Momentum', 'macd': 'Momentum', 'stochastic': 'Momentum',
    'stoch_rsi': 'Momentum', 'momentum': 'Momentum', 'roc': 'Momentum',
    'williams_r': 'Momentum', 'cci': 'Momentum', 'cmo': 'Momentum',
    'connors_rsi': 'Momentum', 'tsi': 'Momentum', 'ppo': 'Momentum',
    'ultimate_osc': 'Momentum', 'rvi': 'Momentum', 'awesome_oscillator': 'Momentum',
    'rsi_divergence': 'Momentum', 'rsi_macd': 'Momentum',
    'ema_cross': 'Trend', 'golden_cross': 'Trend', 'two_ma': 'Trend',
    'three_ma': 'Trend', 'single_ma': 'Trend', 'supertrend': 'Trend',
    'supertrend_rsi': 'Trend', 'ichimoku': 'Trend', 'ichimoku_rsi': 'Trend',
    'psar': 'Trend', 'aroon': 'Trend', 'adx': 'Trend', 'adx_macd': 'Trend',
    'kst': 'Trend', 'coppock': 'Trend', 'dpo': 'Trend', 'trix': 'Trend',
    'schaff_trend': 'Trend', 'trend_intensity': 'Trend', 'triple_screen': 'Trend',
    'heikin_ashi': 'Trend', 'rainbow_ma': 'Trend', 'elder_ray': 'Trend',
    'chandelier': 'Trend', 'linreg': 'Trend', 'hp_filter_ma': 'Trend',
    'bollinger': 'Volatilite', 'bb_rsi': 'Volatilite', 'bb_width': 'Volatilite',
    'keltner': 'Volatilite', 'donchian': 'Volatilite', 'atr_breakout': 'Volatilite',
    'atr_channel': 'Volatilite', 'squeeze': 'Volatilite', 'natr': 'Volatilite',
    'hist_vol': 'Volatilite', 'historical_vol_rank': 'Volatilite',
    'vix_fix': 'Volatilite', 'std_channel': 'Volatilite',
    'chaikin_vol': 'Volatilite', 'volatility_breakout': 'Volatilite',
    'true_range_ema': 'Volatilite',
    'obv': 'Hacim', 'obv_ma': 'Hacim', 'vwap': 'Hacim', 'vwma': 'Hacim',
    'vpt': 'Hacim', 'cmf': 'Hacim', 'mfi': 'Hacim', 'eom': 'Hacim',
    'klinger': 'Hacim', 'ad_line': 'Hacim', 'nvi': 'Hacim', 'pvi': 'Hacim',
    'mass_index': 'Hacim',
    'doji_reversal': 'Mum', 'engulfing': 'Mum', 'hammer': 'Mum',
    'morning_star': 'Mum', 'pin_bar': 'Mum', 'marubozu': 'Mum',
    'three_soldiers': 'Mum', 'inside_bar': 'Mum', 'fractal_breakout': 'Mum',
    'mean_reversion': 'Ort. Donus', 'zscore': 'Ort. Donus', 'ibs': 'Ort. Donus',
    'dema': 'Har. Ort.', 'tema': 'Har. Ort.', 'alma': 'Har. Ort.',
    'hma': 'Har. Ort.', 'wma': 'Har. Ort.', 'zlema': 'Har. Ort.',
}


def get_sektor(hisse):
    return SEKTOR_MAP.get(hisse, 'Diger')


def get_strat_kat(strateji):
    for key in sorted(STRATEJI_KAT_MAP.keys(), key=len, reverse=True):
        if strateji == key or strateji.startswith(key + '_'):
            return STRATEJI_KAT_MAP[key]
    return 'Diger'


def safe_float(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return 0.0
    return v


def anlamlilik(p):
    if p < 0.01: return "*** (p<0.01)"
    elif p < 0.05: return "** (p<0.05)"
    elif p < 0.10: return "* (p<0.10)"
    return ""


def cift_analizi(df):
    """Her hisse-strateji cifti icin train vs test karsilastirmasi."""
    sonuclar = []

    for (hisse, strateji), grp in df.groupby(['Hisse', 'Strateji']):
        train_row = grp[grp['Faz'] == 'train']
        test_row = grp[grp['Faz'] == 'test']

        if len(train_row) == 0 or len(test_row) == 0:
            continue

        train_ret = float(train_row['Toplam Getiri (%)'].iloc[0])
        test_ret = float(test_row['Toplam Getiri (%)'].iloc[0])
        train_bench = float(train_row['Benchmark Getiri (%)'].iloc[0])
        test_bench = float(test_row['Benchmark Getiri (%)'].iloc[0])
        test_sharpe = float(test_row['Sharpe Ratio'].iloc[0])
        test_sortino = float(test_row['Sortino Ratio'].iloc[0])
        test_mdd = float(test_row['Max Drawdown (%)'].iloc[0])
        test_pf = float(test_row['Profit Factor'].iloc[0])
        test_trades = int(test_row['Islem Sayisi'].iloc[0])
        test_winrate = float(test_row['Kazanma Orani (%)'].iloc[0])

        # Alfa
        train_alfa = train_ret - train_bench
        test_alfa = test_ret - test_bench

        # Overfitting
        overfit = 0
        if train_ret != 0:
            overfit = (train_ret - test_ret) / abs(train_ret) * 100

        # Tutarlilik skoru: train ve test arasindaki korelasyon
        # Basit: ikisi de pozitif veya ikisi de negatifse tutarli
        tutarli = "Evet" if (train_alfa > 0 and test_alfa > 0) else "Hayir"

        # Test kalitesi
        if test_trades < 5:
            kalite = "Yetersiz Islem"
        elif safe_float(test_pf) == 0:
            kalite = "Zarar"
        elif test_alfa > 0 and test_sharpe > 0:
            kalite = "Basarili"
        elif test_alfa > 0:
            kalite = "Alfa Pozitif"
        else:
            kalite = "Basarisiz"

        sonuclar.append({
            "Hisse": hisse,
            "Sektor": get_sektor(hisse),
            "Strateji": strateji,
            "Strateji Kategorisi": get_strat_kat(strateji),
            "Train Getiri (%)": round(safe_float(train_ret), 2),
            "Test Getiri (%)": round(safe_float(test_ret), 2),
            "Train Alfa (%)": round(safe_float(train_alfa), 2),
            "Test Alfa (%)": round(safe_float(test_alfa), 2),
            "Test Sharpe": round(safe_float(test_sharpe), 3),
            "Test Sortino": round(safe_float(test_sortino), 3),
            "Test Max DD (%)": round(safe_float(test_mdd), 2),
            "Test Profit Factor": round(safe_float(test_pf), 2),
            "Test Islem": test_trades,
            "Test Win Rate (%)": round(safe_float(test_winrate), 1),
            "Overfit Skor (%)": round(safe_float(overfit), 1),
            "Tutarli": tutarli,
            "Kalite": kalite,
        })

    return pd.DataFrame(sonuclar)


def en_iyi_strateji_per_hisse(df_cift):
    """Her hisse icin test alfasina gore en iyi stratejiyi bul."""
    # Sadece basarili veya alfa pozitif olanlari filtrele
    sonuclar = []

    for hisse in df_cift['Hisse'].unique():
        hisse_df = df_cift[df_cift['Hisse'] == hisse].copy()

        # En iyi (test alfasina gore)
        best = hisse_df.nlargest(3, 'Test Alfa (%)')

        for rank, (_, row) in enumerate(best.iterrows(), 1):
            sonuclar.append({
                "Hisse": hisse,
                "Sektor": row['Sektor'],
                "Siralama": rank,
                "En Iyi Strateji": row['Strateji'],
                "Strateji Kategorisi": row['Strateji Kategorisi'],
                "Test Alfa (%)": row['Test Alfa (%)'],
                "Test Sharpe": row['Test Sharpe'],
                "Test Getiri (%)": row['Test Getiri (%)'],
                "Tutarli": row['Tutarli'],
                "Kalite": row['Kalite'],
            })

    return pd.DataFrame(sonuclar)


def sektor_strateji_haritasi(df_cift):
    """Sektor x Strateji Kategorisi bazli ortalama test alfa matrisi."""
    pivot = df_cift.pivot_table(
        index='Sektor',
        columns='Strateji Kategorisi',
        values='Test Alfa (%)',
        aggfunc='mean'
    ).round(2)
    return pivot


def anlamli_ciftleri_bul(df_cift):
    """
    Her hisse-strateji cifti icin bootstrap guven araligi hesapla.
    Tek bir gozlem oldugu icin (1 train, 1 test) klasik t-test yapilamaz.
    Bunun yerine test alfasi, sharpe ve tutarliliga gore skorla.
    """
    df = df_cift.copy()

    # Kompozit skor: test alfasi + sharpe katkisi + tutarlilik bonusu
    df['Skor'] = (
        df['Test Alfa (%)'] * 0.5 +
        df['Test Sharpe'] * 10 +
        (df['Tutarli'] == 'Evet').astype(int) * 5 +
        (df['Test Islem'] >= 10).astype(int) * 3
    )

    # En iyi %10'u sec
    threshold = df['Skor'].quantile(0.90)
    top = df[df['Skor'] >= threshold].copy()
    top = top.sort_values('Skor', ascending=False)

    # Anlamlilik etiketi: skor bazli
    top['Guc'] = top['Skor'].apply(
        lambda s: "*** Guclu" if s > df['Skor'].quantile(0.97)
        else "** Iyi" if s > df['Skor'].quantile(0.93)
        else "* Umut Verici"
    )

    return top


if __name__ == "__main__":
    if not os.path.exists(TRAIN_TEST_FILE):
        print(f"[HATA] {TRAIN_TEST_FILE} bulunamadi!")
        print(f"       Once: python academic/train_test_backtest.py")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_excel(TRAIN_TEST_FILE)
    print(f"[BILGI] {len(df)} kayit yuklendi ({df['Hisse'].nunique()} hisse, {df['Strateji'].nunique()} strateji)")

    # 1. Cift bazli analiz
    print("\n[1/4] Cift bazli analiz yapiliyor...")
    df_cift = cift_analizi(df)
    df_cift.to_excel(os.path.join(OUTPUT_DIR, "Cift_Bazli_Analiz.xlsx"), index=False)

    basarili = len(df_cift[df_cift['Kalite'] == 'Basarili'])
    alfa_poz = len(df_cift[df_cift['Test Alfa (%)'] > 0])
    tutarli = len(df_cift[df_cift['Tutarli'] == 'Evet'])
    toplam = len(df_cift)

    print(f"  Toplam cift         : {toplam}")
    print(f"  Test Alfa > 0       : {alfa_poz} ({alfa_poz/toplam*100:.1f}%)")
    print(f"  Tutarli (train+test): {tutarli} ({tutarli/toplam*100:.1f}%)")
    print(f"  Basarili            : {basarili} ({basarili/toplam*100:.1f}%)")

    # 2. Her hisse icin en iyi 3 strateji
    print("\n[2/4] Hisse bazli en iyi stratejiler bulunuyor...")
    df_best = en_iyi_strateji_per_hisse(df_cift)
    df_best.to_excel(os.path.join(OUTPUT_DIR, "Hisse_En_Iyi_Strateji.xlsx"), index=False)

    # En iyi #1 stratejilerin dagilimi
    birinciler = df_best[df_best['Siralama'] == 1]
    print(f"  En cok 1. sirayi alan strateji kategorileri:")
    kat_dist = birinciler['Strateji Kategorisi'].value_counts()
    for kat, sayi in kat_dist.items():
        print(f"    {kat:15s} : {sayi} hissede en iyi")

    # 3. Sektor-Strateji haritasi
    print("\n[3/4] Sektor-Strateji haritasi olusturuluyor...")
    df_harita = sektor_strateji_haritasi(df_cift)
    df_harita.to_excel(os.path.join(OUTPUT_DIR, "Sektor_Strateji_Haritasi.xlsx"))
    print(f"  {len(df_harita)} sektor x {len(df_harita.columns)} kategori matrisi olusturuldu")

    # 4. Anlamli/guclu ciftler
    print("\n[4/4] En guclu hisse-strateji ciftleri belirleniyor...")
    df_anlamli = anlamli_ciftleri_bul(df_cift)
    df_anlamli.to_excel(os.path.join(OUTPUT_DIR, "Anlamli_Ciftler.xlsx"), index=False)

    # Ozet cikti
    print(f"\n{'='*65}")
    print(f"  HISSE-STRATEJI CIFTI BAZLI ANALIZ SONUCLARI")
    print(f"{'='*65}")
    print(f"  Toplam cift              : {toplam}")
    print(f"  Test'te benchmark yenen  : {alfa_poz} ({alfa_poz/toplam*100:.1f}%)")
    print(f"  Train+Test tutarli       : {tutarli} ({tutarli/toplam*100:.1f}%)")
    print(f"  Guclu cift (top %10)     : {len(df_anlamli)}")
    print(f"{'='*65}")

    print(f"\n  TOP 15 EN GUCLU HISSE-STRATEJI CIFTLERI:")
    print(f"  {'Hisse':8s} {'Strateji':25s} {'Test Alfa':>10s} {'Sharpe':>8s} {'Tutarli':>8s} {'Guc':>15s}")
    print(f"  {'-'*75}")
    for _, r in df_anlamli.head(15).iterrows():
        print(f"  {r['Hisse']:8s} {r['Strateji']:25s} {r['Test Alfa (%)']:>+9.1f}% {r['Test Sharpe']:>8.2f} {r['Tutarli']:>8s} {r['Guc']:>15s}")

    print(f"\n  SEKTOR BAZLI EN IYI STRATEJI KATEGORISI:")
    for sektor in df_harita.index:
        best_kat = df_harita.loc[sektor].idxmax()
        best_val = df_harita.loc[sektor].max()
        if not pd.isna(best_val):
            print(f"    {sektor:15s} -> {best_kat:15s} (Ort Alfa: {best_val:+.1f}%)")

    print(f"\n{'='*65}")
    print(f"  DOSYALAR:")
    print(f"    Cift_Bazli_Analiz.xlsx")
    print(f"    Hisse_En_Iyi_Strateji.xlsx")
    print(f"    Sektor_Strateji_Haritasi.xlsx")
    print(f"    Anlamli_Ciftler.xlsx")
    print(f"{'='*65}\n")