"""
============================================================
  MAKALE GORSEL URETICI
============================================================
Train/Test ve istatistik sonuclarindan akademik makale icin
yayina hazir grafikler uretir.

Calistirma:
    cd vbt_bist
    python academic/paper_charts.py

Cikti (vbt_bist/academic/output/figures/):
  - fig1_top10_train_vs_test.png
  - fig2_heatmap_strateji_hisse.png
  - fig3_overfit_scatter.png
  - fig4_sharpe_distribution.png
  - fig5_drawdown_boxplot.png
  - fig6_category_performance.png
  - fig7_cumulative_equity.png
"""

import os
import sys
import math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # GUI olmadan calis
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VBT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
TRAIN_TEST_FILE = os.path.join(OUTPUT_DIR, "TrainTest_Sonuclari.xlsx")
STATS_FILE = os.path.join(OUTPUT_DIR, "Istatistik_Testleri.xlsx")
MASTER_FILE = os.path.join(VBT_DIR, "output", "Tum_Strateji_Metrikleri.xlsx")

# Makale stili
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

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

    'mean_reversion': 'Ortalamaya Donus', 'zscore': 'Ortalamaya Donus',
    'ibs': 'Ortalamaya Donus',

    'dema': 'Hareketli Ortalama', 'tema': 'Hareketli Ortalama',
    'alma': 'Hareketli Ortalama', 'hma': 'Hareketli Ortalama',
    'wma': 'Hareketli Ortalama', 'zlema': 'Hareketli Ortalama',
    'vwma': 'Hareketli Ortalama',
}


def get_kategori(strateji_adi):
    """Strateji adinin base modulunu bul ve kategorisini dondur."""
    for key in sorted(KATEGORI_MAP.keys(), key=len, reverse=True):
        if strateji_adi == key or strateji_adi.startswith(key + '_'):
            return KATEGORI_MAP[key]
    return 'Diger'


def fig1_top10_train_vs_test(df_tt):
    """Top 10 stratejinin train vs test performans karsilastirmasi."""
    # Her strateji icin ortalama train ve test getirisi
    pivot = df_tt.groupby(['Strateji', 'Faz'])['Toplam Getiri (%)'].mean().unstack(fill_value=0)
    if 'train' not in pivot.columns or 'test' not in pivot.columns:
        print("  [ATLANDI] fig1: train/test sutunlari eksik")
        return

    pivot['test_rank'] = pivot['test'].rank(ascending=False)
    top10 = pivot.nsmallest(10, 'test_rank')

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(top10))
    w = 0.35
    ax.bar(x - w/2, top10['train'], w, label='In-Sample (Train %70)', color='#2196F3', alpha=0.85)
    ax.bar(x + w/2, top10['test'], w, label='Out-of-Sample (Test %30)', color='#FF9800', alpha=0.85)
    ax.set_xlabel('Strateji')
    ax.set_ylabel('Ortalama Getiri (%)')
    ax.set_title('Top 10 Strateji: In-Sample vs Out-of-Sample Performans')
    ax.set_xticks(x)
    ax.set_xticklabels(top10.index, rotation=45, ha='right')
    ax.legend()
    ax.axhline(y=0, color='black', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig1_top10_train_vs_test.png'))
    plt.close()
    print("  [OK] fig1_top10_train_vs_test.png")


def fig2_heatmap(df_master):
    """Strateji x Hisse performans heatmap (en aktif 15 strateji, 20 hisse)."""
    # En cok hissede kullanilan 15 strateji
    top_strats = df_master['Strateji'].value_counts().head(15).index.tolist()
    # En yuksek ortalama getirili 20 hisse
    top_stocks = df_master.groupby('Hisse')['K\u00e2r / Zarar (%)'].mean().nlargest(20).index.tolist()

    filtered = df_master[
        (df_master['Strateji'].isin(top_strats)) &
        (df_master['Hisse'].isin(top_stocks))
    ]
    pivot = filtered.pivot_table(index='Strateji', columns='Hisse', values='K\u00e2r / Zarar (%)', aggfunc='mean')

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn', center=0,
                linewidths=0.5, ax=ax, cbar_kws={'label': 'Getiri (%)'})
    ax.set_title('Strateji x Hisse Performans Matrisi (Top 15 Strateji, Top 20 Hisse)')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig2_heatmap_strateji_hisse.png'))
    plt.close()
    print("  [OK] fig2_heatmap_strateji_hisse.png")


def fig3_overfit_scatter(df_stats):
    """Overfitting skoru vs test getirisi scatter plot."""
    fig, ax = plt.subplots(figsize=(10, 7))

    colors = {'DUSUK': '#4CAF50', 'ORTA': '#FF9800', 'YUKSEK': '#F44336'}
    for risk, color in colors.items():
        mask = df_stats['Overfit Risk'] == risk
        subset = df_stats[mask]
        ax.scatter(subset['Overfit Skor (%)'], subset['Test Ort (%)'],
                   c=color, label=f'{risk} Risk ({len(subset)})', alpha=0.7, s=60, edgecolors='white')

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_xlabel('Overfit Skor (%)')
    ax.set_ylabel('Out-of-Sample Ortalama Getiri (%)')
    ax.set_title('Overfitting Analizi: Train-Test Performans Farki')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig3_overfit_scatter.png'))
    plt.close()
    print("  [OK] fig3_overfit_scatter.png")


def fig4_sharpe_distribution(df_tt):
    """Test fazindaki Sharpe Ratio dagilimi."""
    test_sharpe = df_tt[df_tt['Faz'] == 'test']['Sharpe Ratio'].dropna()
    test_sharpe = test_sharpe[(test_sharpe > -5) & (test_sharpe < 5)]  # aykiri degerleri temizle

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(test_sharpe, bins=50, color='#1976D2', alpha=0.7, edgecolor='white')
    ax.axvline(x=test_sharpe.median(), color='red', linestyle='--', label=f'Medyan: {test_sharpe.median():.2f}')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xlabel('Sharpe Ratio (Out-of-Sample)')
    ax.set_ylabel('Frekans')
    ax.set_title(f'Out-of-Sample Sharpe Ratio Dagilimi (N={len(test_sharpe)})')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig4_sharpe_distribution.png'))
    plt.close()
    print("  [OK] fig4_sharpe_distribution.png")


def fig5_drawdown_boxplot(df_tt):
    """Kategori bazli Max Drawdown box plot."""
    df_test = df_tt[df_tt['Faz'] == 'test'].copy()
    df_test['Kategori'] = df_test['Strateji'].apply(get_kategori)

    fig, ax = plt.subplots(figsize=(12, 6))
    kategoriler = df_test.groupby('Kategori')['Max Drawdown (%)'].median().sort_values().index
    data = [df_test[df_test['Kategori'] == k]['Max Drawdown (%)'].dropna().values for k in kategoriler]

    bp = ax.boxplot(data, tick_labels=kategoriler, patch_artist=True, showfliers=False)
    renk_paleti = ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5', '#2196F3', '#1E88E5', '#1565C0']
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(renk_paleti[i % len(renk_paleti)])

    ax.set_ylabel('Max Drawdown (%)')
    ax.set_title('Kategori Bazli Risk Analizi (Out-of-Sample Max Drawdown)')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig5_drawdown_boxplot.png'))
    plt.close()
    print("  [OK] fig5_drawdown_boxplot.png")


def fig6_category_performance(df_tt):
    """Kategori bazli ortalama test getirisi bar chart."""
    df_test = df_tt[df_tt['Faz'] == 'test'].copy()
    df_test['Kategori'] = df_test['Strateji'].apply(get_kategori)

    kat_perf = df_test.groupby('Kategori').agg(
        Getiri=('Toplam Getiri (%)', 'mean'),
        Sharpe=('Sharpe Ratio', 'mean'),
        N=('Toplam Getiri (%)', 'count')
    ).sort_values('Getiri', ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = ['#F44336' if v < 0 else '#4CAF50' for v in kat_perf['Getiri']]
    ax1.barh(kat_perf.index, kat_perf['Getiri'], color=colors, alpha=0.8)
    ax1.set_xlabel('Ortalama Getiri (%)')
    ax1.set_title('Kategori Bazli Out-of-Sample Getiri')
    ax1.axvline(x=0, color='black', linewidth=0.5)

    colors2 = ['#F44336' if v < 0 else '#2196F3' for v in kat_perf['Sharpe']]
    ax2.barh(kat_perf.index, kat_perf['Sharpe'], color=colors2, alpha=0.8)
    ax2.set_xlabel('Ortalama Sharpe Ratio')
    ax2.set_title('Kategori Bazli Out-of-Sample Sharpe')
    ax2.axvline(x=0, color='black', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig6_category_performance.png'))
    plt.close()
    print("  [OK] fig6_category_performance.png")


def fig7_pvalue_heatmap(df_stats):
    """Strateji anlamliligi ozet tablosu."""
    top20 = df_stats.head(20).copy()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    cols = ['Strateji', 'N (Hisse)', 'Test Ort (%)', 'Test Alfa Ort (%)',
            'Test Sharpe (Med)', 'p (alfa>0)', 'Alfa Anlamliligi', 'Overfit Risk']
    table_data = top20[cols].values.tolist()

    table = ax.table(cellText=table_data, colLabels=cols, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.5)

    # Basliklari kalinlastir
    for j in range(len(cols)):
        table[0, j].set_facecolor('#1976D2')
        table[0, j].set_text_props(color='white', fontweight='bold')

    # Anlamliligi renklendir
    anlamli_col = cols.index('Alfa Anlamliligi')
    overfit_col = cols.index('Overfit Risk')
    for i in range(len(table_data)):
        if table_data[i][anlamli_col] == 'EVET':
            table[i+1, anlamli_col].set_facecolor('#C8E6C9')
        else:
            table[i+1, anlamli_col].set_facecolor('#FFCDD2')

        risk = table_data[i][overfit_col]
        if risk == 'DUSUK':
            table[i+1, overfit_col].set_facecolor('#C8E6C9')
        elif risk == 'ORTA':
            table[i+1, overfit_col].set_facecolor('#FFF9C4')
        else:
            table[i+1, overfit_col].set_facecolor('#FFCDD2')

    ax.set_title('Top 20 Strateji: Istatistiksel Anlamlilik Ozeti', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'fig7_pvalue_summary_table.png'))
    plt.close()
    print("  [OK] fig7_pvalue_summary_table.png")


if __name__ == "__main__":
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  MAKALE GORSEL URETICI")
    print(f"{'='*60}\n")

    # Veri yukle
    has_tt = os.path.exists(TRAIN_TEST_FILE)
    has_stats = os.path.exists(STATS_FILE)
    has_master = os.path.exists(MASTER_FILE)

    if has_tt:
        df_tt = pd.read_excel(TRAIN_TEST_FILE)
        print(f"[OK] TrainTest: {len(df_tt)} kayit")
    else:
        print(f"[!] TrainTest dosyasi yok. Once train_test_backtest.py calistirin.")
        df_tt = None

    if has_stats:
        df_stats = pd.read_excel(STATS_FILE)
        print(f"[OK] Istatistik: {len(df_stats)} strateji")
    else:
        print(f"[!] Istatistik dosyasi yok. Once statistical_tests.py calistirin.")
        df_stats = None

    if has_master:
        df_master = pd.read_excel(MASTER_FILE)
        print(f"[OK] Master: {len(df_master)} kayit")
    else:
        print(f"[!] Master rapor yok.")
        df_master = None

    print(f"\nGorseller uretiliyor...\n")

    # Sirayla uret
    if df_tt is not None:
        fig1_top10_train_vs_test(df_tt)
        fig4_sharpe_distribution(df_tt)
        fig5_drawdown_boxplot(df_tt)
        fig6_category_performance(df_tt)

    if df_master is not None:
        fig2_heatmap(df_master)

    if df_stats is not None:
        fig3_overfit_scatter(df_stats)
        fig7_pvalue_heatmap(df_stats)

    print(f"\n{'='*60}")
    print(f"  TAMAMLANDI! Gorseller: {FIGURES_DIR}")
    print(f"{'='*60}\n")