"""
============================================================
  ISTATISTIKSEL ANLAMLILIK TESTI v2
============================================================
Train/Test sonuclarini okur ve su testleri uygular:
  1. One-sample t-test (test getirisi != 0 mi?) - iki yonlu
  2. Paired t-test (train vs test - farki olcmek icin)
  3. Wilcoxon signed-rank test (non-parametric)
  4. Benchmark-adjusted alfa t-test (alfa > 0 mi?)
  5. Overfitting skoru (train vs test performans farki)
  6. Strateji kategori bazli analiz

Not: p<0.10 Zayif Anlamli, p<0.05 Anlamli, p<0.01 Guclu Anlamli

Calistirma:
    cd vbt_bist
    python academic/statistical_tests.py

Cikti:
    vbt_bist/academic/output/Istatistik_Testleri.xlsx
    vbt_bist/academic/output/Kategori_Analizi.xlsx
"""

import os
import sys
import math
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TRAIN_TEST_FILE = os.path.join(OUTPUT_DIR, "TrainTest_Sonuclari.xlsx")

# Strateji kategorileri
KATEGORI_MAP = {
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
    'doji_reversal': 'Mum Formasyonu', 'engulfing': 'Mum Formasyonu',
    'hammer': 'Mum Formasyonu', 'morning_star': 'Mum Formasyonu',
    'pin_bar': 'Mum Formasyonu', 'marubozu': 'Mum Formasyonu',
    'three_soldiers': 'Mum Formasyonu', 'inside_bar': 'Mum Formasyonu',
    'fractal_breakout': 'Mum Formasyonu',
    'mean_reversion': 'Ort. Donus', 'zscore': 'Ort. Donus', 'ibs': 'Ort. Donus',
    'dema': 'Har. Ortalama', 'tema': 'Har. Ortalama', 'alma': 'Har. Ortalama',
    'hma': 'Har. Ortalama', 'wma': 'Har. Ortalama', 'zlema': 'Har. Ortalama',
}


def get_kategori(s):
    for key in sorted(KATEGORI_MAP.keys(), key=len, reverse=True):
        if s == key or s.startswith(key + '_'):
            return KATEGORI_MAP[key]
    return 'Diger'


def safe_float(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return 0.0
    return v


def anlamlilik_etiketi(p):
    if p < 0.01:
        return "*** (p<0.01)"
    elif p < 0.05:
        return "** (p<0.05)"
    elif p < 0.10:
        return "* (p<0.10)"
    else:
        return "Anlamsiz"


def strateji_bazli_test(df_full):
    """Her strateji icin istatistik testleri uygular."""
    sonuclar = []
    stratejiler = df_full['Strateji'].unique()

    for strat in stratejiler:
        df_s = df_full[df_full['Strateji'] == strat]
        train_df = df_s[df_s['Faz'] == 'train']
        test_df = df_s[df_s['Faz'] == 'test']

        train_ret = train_df['Toplam Getiri (%)'].dropna().values
        test_ret = test_df['Toplam Getiri (%)'].dropna().values
        test_bench = test_df['Benchmark Getiri (%)'].dropna().values
        test_sharpe = test_df['Sharpe Ratio'].dropna().values

        if len(train_ret) < 5 or len(test_ret) < 5:
            continue

        # === TESTLER ===

        # 1. One-sample t-test: Test getirisi 0'dan farkli mi? (iki yonlu)
        t_onesamp, p_onesamp = scipy_stats.ttest_1samp(test_ret, 0)

        # 2. Alfa t-test: Test alfa > 0 mi? (tek yonlu)
        alfa_values = test_ret[:min(len(test_ret), len(test_bench))] - test_bench[:min(len(test_ret), len(test_bench))]
        t_alfa, p_alfa_two = scipy_stats.ttest_1samp(alfa_values, 0)
        # Tek yonlu: alfa > 0 mi?
        p_alfa = p_alfa_two / 2 if t_alfa > 0 else 1 - p_alfa_two / 2

        # 3. Paired t-test: train vs test farki anlamli mi?
        min_n = min(len(train_ret), len(test_ret))
        t_paired, p_paired = scipy_stats.ttest_rel(train_ret[:min_n], test_ret[:min_n])

        # 4. Wilcoxon signed-rank (non-parametric)
        try:
            diff = train_ret[:min_n] - test_ret[:min_n]
            diff = diff[diff != 0]  # sifir farklari cikar
            if len(diff) >= 10:
                w_stat, p_wilcox = scipy_stats.wilcoxon(diff)
            else:
                w_stat, p_wilcox = 0, 1.0
        except Exception:
            w_stat, p_wilcox = 0, 1.0

        # 5. Overfitting metrikleri
        train_mean = np.mean(train_ret)
        test_mean = np.mean(test_ret)
        overfit_score = 0.0
        if train_mean != 0:
            overfit_score = (train_mean - test_mean) / abs(train_mean) * 100

        alfa_mean = np.mean(alfa_values) if len(alfa_values) > 0 else 0

        # 6. Kazanma orani (test fazinda kac hissede pozitif getiri)
        pozitif_hisse = np.sum(test_ret > 0)
        kazanma_orani = pozitif_hisse / len(test_ret) * 100

        # 7. Risk-adjusted: medyan Sharpe
        test_sharpe_med = np.median(test_sharpe) if len(test_sharpe) > 0 else 0

        # Overfitting risk siniflandirmasi (daha dengeli esikler)
        abs_overfit = abs(overfit_score)
        if abs_overfit < 50:
            overfit_risk = "DUSUK"
        elif abs_overfit < 80:
            overfit_risk = "ORTA"
        else:
            overfit_risk = "YUKSEK"

        sonuclar.append({
            "Strateji": strat,
            "Kategori": get_kategori(strat),
            "N (Hisse)": min_n,
            "Train Ort (%)": round(safe_float(train_mean), 2),
            "Test Ort (%)": round(safe_float(test_mean), 2),
            "Test Medyan (%)": round(safe_float(np.median(test_ret)), 2),
            "Test Alfa Ort (%)": round(safe_float(alfa_mean), 2),
            "Test Sharpe (Med)": round(safe_float(test_sharpe_med), 3),
            "Kazanma Orani (%)": round(safe_float(kazanma_orani), 1),
            "p (test!=0)": round(safe_float(p_onesamp), 4),
            "p (alfa>0)": round(safe_float(p_alfa), 4),
            "Alfa Anlamliligi": anlamlilik_etiketi(p_alfa),
            "p (train=test)": round(safe_float(p_paired), 4),
            "p (Wilcoxon)": round(safe_float(p_wilcox), 4),
            "Overfit Skor (%)": round(safe_float(overfit_score), 1),
            "Overfit Risk": overfit_risk,
            "Benchmark Yendi (%)": round(safe_float(kazanma_orani), 1),
        })

    return pd.DataFrame(sonuclar)


def kategori_analizi(df_stats):
    """Strateji kategorileri bazinda ozet tablo."""
    kat = df_stats.groupby('Kategori').agg(
        Strateji_Sayisi=('Strateji', 'count'),
        Ort_Test_Getiri=('Test Ort (%)', 'mean'),
        Ort_Alfa=('Test Alfa Ort (%)', 'mean'),
        Med_Sharpe=('Test Sharpe (Med)', 'median'),
        Ort_Kazanma=('Kazanma Orani (%)', 'mean'),
        Anlamli_Alfa=('Alfa Anlamliligi', lambda x: sum(1 for v in x if '***' in str(v) or '** ' in str(v))),
        Ort_Overfit=('Overfit Skor (%)', 'mean'),
    ).round(2)
    kat = kat.sort_values('Ort_Alfa', ascending=False)
    return kat


def genel_ozet(df_stats):
    """Konsola genel ozet yazdir."""
    toplam = len(df_stats)

    # Farkli anlamlilik seviyeleri
    guclu = len(df_stats[df_stats['Alfa Anlamliligi'].str.contains(r'\*\*\*', regex=True, na=False)])
    anlamli = len(df_stats[df_stats['Alfa Anlamliligi'].str.contains(r'\*\*', regex=True, na=False)])
    zayif = len(df_stats[df_stats['Alfa Anlamliligi'].str.contains(r'\*', regex=True, na=False)])

    overfit_dusuk = len(df_stats[df_stats['Overfit Risk'] == 'DUSUK'])
    overfit_orta = len(df_stats[df_stats['Overfit Risk'] == 'ORTA'])

    pozitif_test = len(df_stats[df_stats['Test Ort (%)'] > 0])
    pozitif_alfa = len(df_stats[df_stats['Test Alfa Ort (%)'] > 0])

    print(f"\n{'='*65}")
    print(f"  GENEL OZET")
    print(f"{'='*65}")
    print(f"  Toplam strateji                : {toplam}")
    print(f"  Test getirisi > 0              : {pozitif_test} ({pozitif_test/toplam*100:.1f}%)")
    print(f"  Benchmark'i yenen (Alfa > 0)   : {pozitif_alfa} ({pozitif_alfa/toplam*100:.1f}%)")
    print(f"  ----------------------------------------")
    print(f"  Alfa istatistiksel anlamli:")
    print(f"    *** Guclu  (p<0.01)          : {guclu}")
    print(f"    **  Anlamli (p<0.05)         : {anlamli}")
    print(f"    *   Zayif  (p<0.10)          : {zayif}")
    print(f"  ----------------------------------------")
    print(f"  Overfitting riski:")
    print(f"    DUSUK (<50%)                 : {overfit_dusuk}")
    print(f"    ORTA  (50-80%)               : {overfit_orta}")
    print(f"    YUKSEK (>80%)                : {toplam - overfit_dusuk - overfit_orta}")
    print(f"{'='*65}")

    # Benchmark'i yenen ve dusuk overfitli stratejiler
    savunulabilir = df_stats[
        (df_stats['Test Alfa Ort (%)'] > 0) &
        (df_stats['Overfit Risk'].isin(['DUSUK', 'ORTA']))
    ].sort_values('Test Alfa Ort (%)', ascending=False)

    if len(savunulabilir) > 0:
        print(f"\n  MAKALEDE KULLANILABILECEK STRATEJILER (Alfa>0 + Overfit<=ORTA):")
        for _, r in savunulabilir.head(15).iterrows():
            sig = r['Alfa Anlamliligi']
            print(f"    {r['Strateji']:25s}  Alfa={r['Test Alfa Ort (%)']:+.1f}%  "
                  f"Sharpe={r['Test Sharpe (Med)']:.2f}  Win={r['Kazanma Orani (%)']:.0f}%  "
                  f"Overfit={r['Overfit Skor (%)']:.0f}%  {sig}")
    else:
        print(f"\n  [!] Alfa>0 ve dusuk/orta overfitli strateji bulunamadi.")
        print(f"      En iyi 10 strateji (alfaya gore):")
        best = df_stats.nlargest(10, 'Test Alfa Ort (%)')
        for _, r in best.iterrows():
            print(f"    {r['Strateji']:25s}  Alfa={r['Test Alfa Ort (%)']:+.1f}%  "
                  f"Overfit={r['Overfit Skor (%)']:.0f}%  {r['Alfa Anlamliligi']}")

    print(f"{'='*65}\n")


if __name__ == "__main__":
    if not os.path.exists(TRAIN_TEST_FILE):
        print(f"[HATA] Train/Test dosyasi bulunamadi: {TRAIN_TEST_FILE}")
        print(f"       Once: python academic/train_test_backtest.py")
        sys.exit(1)

    df = pd.read_excel(TRAIN_TEST_FILE)
    print(f"[BILGI] {len(df)} kayit ({df['Strateji'].nunique()} strateji, {df['Hisse'].nunique()} hisse)")

    # Strateji bazli testler
    df_stats = strateji_bazli_test(df)

    if len(df_stats) > 0:
        df_stats = df_stats.sort_values('Test Alfa Ort (%)', ascending=False)

        kayit1 = os.path.join(OUTPUT_DIR, "Istatistik_Testleri.xlsx")
        df_stats.to_excel(kayit1, index=False)
        print(f"[KAYIT] {kayit1}")

        # Kategori analizi
        df_kat = kategori_analizi(df_stats)
        kayit2 = os.path.join(OUTPUT_DIR, "Kategori_Analizi.xlsx")
        df_kat.to_excel(kayit2)
        print(f"[KAYIT] {kayit2}")
        print(f"\nKategori Bazli Ozet:")
        print(df_kat.to_string())

        genel_ozet(df_stats)
    else:
        print("[UYARI] Yeterli veri bulunamadi.")