"""
============================================================
  AKADEMIK BACKTEST MOTORU - Train/Test Split
============================================================
Mevcut 86 stratejiyi degistirmeden, tum hisseler uzerinde
In-Sample (egitim %70) ve Out-of-Sample (test %30) ayrimli
backtest yapar.

Calistirma:
    cd vbt_bist
    python academic/train_test_backtest.py

Cikti:
    vbt_bist/academic/output/TrainTest_Sonuclari.xlsx
"""

import os
import sys
import math
import pandas as pd
import importlib
import inspect
import warnings
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# Uyarilari kapat
pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings('ignore')

# Path ayarlari
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VBT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, VBT_DIR)

import vectorbt as vbt
import strategies.utils as vbt_utils

DATA_DIR = os.path.join(VBT_DIR, "data")
STRATEGY_DIR = os.path.join(VBT_DIR, "strategies")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

TRAIN_RATIO = 0.70  # %70 egitim, %30 test


def get_safe_val(stats_df, key):
    """stats() sonucundan guvenli deger cek."""
    if key in stats_df.index:
        val = stats_df.loc[key]
        if hasattr(val, 'iloc'):
            val = val.iloc[0]
        if pd.isna(val):
            return 0.0
        try:
            v = float(val)
            if math.isinf(v):
                return 0.0
            return v
        except (ValueError, TypeError):
            return 0.0
    return 0.0


def backtest_split(hisse, modul_adi, kapanis_full, veri_deposu_full, split_idx):
    """Tek bir hisse-strateji cifti icin train ve test backtesti yapar."""
    modul = importlib.import_module(f"strategies.{modul_adi}")
    if not hasattr(modul, "calistir"):
        return None

    fonksiyon = modul.calistir
    sig = inspect.signature(fonksiyon)

    results = []

    for phase, start, end in [("train", 0, split_idx), ("test", split_idx, len(kapanis_full))]:
        # Veri deposunun bu dilimini olustur
        veri_slice = {}
        for key, val in veri_deposu_full.items():
            if isinstance(val, pd.Series):
                veri_slice[key] = val.iloc[start:end]
            else:
                veri_slice[key] = val

        fonksiyon_args = {
            arg: veri_slice[arg]
            for arg in sig.parameters
            if arg in veri_slice
        }

        # sonuclari_kaydet yerine portfoyu yakala
        captured = {}

        def capture(portfoy, baslik, strateji_adi, grafik_baslik=None):
            captured[strateji_adi] = portfoy
            return portfoy.stats()

        original_local = getattr(modul, "sonuclari_kaydet", None)
        original_global = vbt_utils.sonuclari_kaydet
        if original_local:
            setattr(modul, "sonuclari_kaydet", capture)
        vbt_utils.sonuclari_kaydet = capture

        try:
            fonksiyon(**fonksiyon_args)
        except Exception:
            pass
        finally:
            if original_local:
                setattr(modul, "sonuclari_kaydet", original_local)
            vbt_utils.sonuclari_kaydet = original_global

        if not captured:
            continue

        for strat_adi, portfoy in captured.items():
            stats = portfoy.stats()
            results.append({
                "Hisse": hisse,
                "Strateji": strat_adi,
                "Faz": phase,
                "Toplam Getiri (%)": get_safe_val(stats, "Total Return [%]"),
                "Benchmark Getiri (%)": get_safe_val(stats, "Benchmark Return [%]"),
                "Sharpe Ratio": get_safe_val(stats, "Sharpe Ratio"),
                "Sortino Ratio": get_safe_val(stats, "Sortino Ratio"),
                "Max Drawdown (%)": get_safe_val(stats, "Max Drawdown [%]"),
                "Profit Factor": get_safe_val(stats, "Profit Factor"),
                "Islem Sayisi": int(get_safe_val(stats, "Total Trades")),
                "Kazanma Orani (%)": get_safe_val(stats, "Win Rate [%]"),
                "Calmar Ratio": get_safe_val(stats, "Calmar Ratio"),
            })

    return results


def analiz_hisse(csv_dosyasi):
    """Tek bir hisse icin tum stratejileri train/test olarak calistir."""
    hisse = csv_dosyasi.replace('.csv', '')
    dosya_yolu = os.path.join(DATA_DIR, csv_dosyasi)

    try:
        veri = pd.read_csv(dosya_yolu, index_col='Date', parse_dates=True).ffill().bfill()
        if len(veri) < 100:
            return []

        split_idx = int(len(veri) * TRAIN_RATIO)

        veri_deposu_full = {
            'kapanis_fiyatlari': veri['Close'],
            'kapanis': veri['Close'],
            'acilis': veri['Open'],
            'yuksek': veri['High'],
            'dusuk': veri['Low'],
            'hacim': veri['Volume'],
            'baslik': hisse,
        }

        moduller = [
            f[:-3] for f in os.listdir(STRATEGY_DIR)
            if f.endswith('.py') and f not in ('__init__.py', 'utils.py')
        ]

        tum_sonuclar = []
        for modul_adi in moduller:
            try:
                sonuc = backtest_split(hisse, modul_adi, veri['Close'], veri_deposu_full, split_idx)
                if sonuc:
                    tum_sonuclar.extend(sonuc)
            except Exception:
                pass

        return tum_sonuclar

    except Exception as e:
        print(f"[HATA] {hisse}: {e}")
        return []


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    csv_dosyalari = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    print(f"\n{'='*60}")
    print(f"  AKADEMIK TRAIN/TEST BACKTEST MOTORU")
    print(f"  Hisse: {len(csv_dosyalari)} | Train: %{int(TRAIN_RATIO*100)} | Test: %{int((1-TRAIN_RATIO)*100)}")
    print(f"{'='*60}\n")

    max_worker = max(1, multiprocessing.cpu_count() - 4)
    print(f"  Cekirdek sayisi: {max_worker}")

    tum_sonuclar = []
    with ProcessPoolExecutor(max_workers=max_worker) as executor:
        futures = {executor.submit(analiz_hisse, csv): csv for csv in csv_dosyalari}
        for i, future in enumerate(as_completed(futures), 1):
            try:
                sonuc = future.result()
                if sonuc:
                    tum_sonuclar.extend(sonuc)
                print(f"[{i}/{len(csv_dosyalari)}] {futures[future].replace('.csv','')} - {len(sonuc)} sonuc")
            except Exception as exc:
                print(f"[{i}/{len(csv_dosyalari)}] HATA: {exc}")

    if tum_sonuclar:
        df = pd.DataFrame(tum_sonuclar)
        kayit_yolu = os.path.join(OUTPUT_DIR, "TrainTest_Sonuclari.xlsx")
        df.to_excel(kayit_yolu, index=False)
        print(f"\n{'='*60}")
        print(f"  TAMAMLANDI! Toplam {len(df)} kayit")
        print(f"  Kayit: {kayit_yolu}")
        print(f"{'='*60}")
    else:
        print("Hicbir sonuc uretilmedi!")