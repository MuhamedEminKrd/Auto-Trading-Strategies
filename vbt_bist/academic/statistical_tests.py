"""
============================================================
  ISTATISTIKSEL ANLAMLILIK TESTI
============================================================
Train/Test sonuclarini okur ve su testleri uygular:
  1. Paired t-test (train vs test getirileri)
  2. Wilcoxon signed-rank test
  3. One-sample t-test (test getirisi > 0 mi?)
  4. Overfitting skoru (train vs test performans farki)

Calistirma:
    cd vbt_bist
    python academic/statistical_tests.py

Cikti:
    vbt_bist/academic/output/Istatistik_Testleri.xlsx
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
MASTER_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), "output", "Tum_Strateji_Metrikleri.xlsx")


def safe_float(v):
    """NaN/Inf degerleri 0 yap."""
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return 0.0
    return v


def strateji_bazli_test(df_train_test):
    """
    Her strateji icin train ve test performansini karsilastirir.
    Cikti: strateji bazli istatistik tablosu.
    """
    sonuclar = []

    stratejiler = df_train_test['Strateji'].unique()

    for strat in stratejiler:
        df_strat = df_train_test[df_train_test['Strateji'] == strat]

        train = df_strat[df_strat['Faz'] == 'train']['Toplam Getiri (%)'].dropna().values
        test = df_strat[df_strat['Faz'] == 'test']['Toplam Getiri (%)'].dropna().values

        if len(train) < 5 or len(test) < 5:
            continue

        # 1. One-sample t-test: Test getirisi > 0 mi?
        t_one, p_one = scipy_stats.ttest_1samp(test, 0)

        # 2. Paired t-test: Train ve test getirileri arasinda anlamli fark var mi?
        min_len = min(len(train), len(test))
        t_paired, p_paired = scipy_stats.ttest_rel(train[:min_len], test[:min_len])

        # 3. Wilcoxon signed-rank test (non-parametric alternatif)
        try:
            w_stat, p_wilcoxon = scipy_stats.wilcoxon(train[:min_len], test[:min_len])
        except Exception:
            w_stat, p_wilcoxon = 0, 1.0

        # 4. Overfitting skoru: (train_mean - test_mean) / train_mean
        train_mean = np.mean(train)
        test_mean = np.mean(test)
        overfit_score = 0.0
        if train_mean != 0:
            overfit_score = (train_mean - test_mean) / abs(train_mean) * 100

        # 5. Alfa (test): ortalama test getirisi - ortalama test benchmark
        test_bench = df_strat[df_strat['Faz'] == 'test']['Benchmark Getiri (%)'].dropna().values
        alfa_test = test_mean - np.mean(test_bench) if len(test_bench) > 0 else 0

        sonuclar.append({
            "Strateji": strat,
            "N (Hisse)": min_len,
            "Train Ort Getiri (%)": round(safe_float(train_mean), 2),
            "Test Ort Getiri (%)": round(safe_float(test_mean), 2),
            "Test Alfa (%)": round(safe_float(alfa_test), 2),
            "Test Sharpe (Ort)": round(safe_float(np.mean(
                df_strat[df_strat['Faz'] == 'test']['Sharpe Ratio'].dropna().values
            )), 3),
            "t-test (test>0) p": round(safe_float(p_one), 4),
            "Anlamli mi? (p<0.05)": "EVET" if p_one < 0.05 and t_one > 0 else "HAYIR",
            "Paired t-test p": round(safe_float(p_paired), 4),
            "Wilcoxon p": round(safe_float(p_wilcoxon), 4),
            "Overfitting Skoru (%)": round(safe_float(overfit_score), 1),
            "Overfitting Riski": (
                "DUSUK" if abs(overfit_score) < 30 else
                "ORTA" if abs(overfit_score) < 60 else
                "YUKSEK"
            ),
        })

    return pd.DataFrame(sonuclar)


def genel_ozet(df_test_stats):
    """Tum stratejilerin genel istatistik ozeti."""
    toplam = len(df_test_stats)
    anlamli = len(df_test_stats[df_test_stats['Anlamli mi? (p<0.05)'] == 'EVET'])
    overfit_dusuk = len(df_test_stats[df_test_stats['Overfitting Riski'] == 'DUSUK'])

    print(f"\n{'='*60}")
    print(f"  GENEL OZET")
    print(f"{'='*60}")
    print(f"  Toplam strateji           : {toplam}")
    print(f"  Istatistiksel anlamli     : {anlamli} ({anlamli/toplam*100:.1f}%)")
    print(f"  Dusuk overfitting riski   : {overfit_dusuk} ({overfit_dusuk/toplam*100:.1f}%)")
    print(f"  Test>0 ve dusuk overfit   : ", end="")

    guclu = df_test_stats[
        (df_test_stats['Anlamli mi? (p<0.05)'] == 'EVET') &
        (df_test_stats['Overfitting Riski'] == 'DUSUK')
    ]
    print(f"{len(guclu)} strateji")

    if len(guclu) > 0:
        print(f"\n  EN GUCLU STRATEJILER (akademik olarak savunulabilir):")
        for _, row in guclu.sort_values('Test Ort Getiri (%)', ascending=False).head(10).iterrows():
            print(f"    - {row['Strateji']}: Test Getiri={row['Test Ort Getiri (%)']}%, "
                  f"Alfa={row['Test Alfa (%)']}%, p={row['t-test (test>0) p']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Oncelik: TrainTest sonuclari
    if os.path.exists(TRAIN_TEST_FILE):
        print(f"[BILGI] Train/Test sonuclari okunuyor: {TRAIN_TEST_FILE}")
        df = pd.read_excel(TRAIN_TEST_FILE)
    else:
        print(f"[HATA] Train/Test dosyasi bulunamadi!")
        print(f"       Once calistirin: python academic/train_test_backtest.py")
        sys.exit(1)

    print(f"[BILGI] Toplam {len(df)} kayit ({df['Strateji'].nunique()} strateji, {df['Hisse'].nunique()} hisse)")

    # Strateji bazli istatistik testleri
    df_stats = strateji_bazli_test(df)

    if len(df_stats) > 0:
        # Sirala: once anlamli olanlar, sonra test getirisine gore
        df_stats = df_stats.sort_values(
            by=['Anlamli mi? (p<0.05)', 'Test Ort Getiri (%)'],
            ascending=[False, False]
        )

        kayit_yolu = os.path.join(OUTPUT_DIR, "Istatistik_Testleri.xlsx")
        df_stats.to_excel(kayit_yolu, index=False)
        print(f"[KAYIT] {kayit_yolu}")

        genel_ozet(df_stats)
    else:
        print("[UYARI] Yeterli veri bulunamadi.")