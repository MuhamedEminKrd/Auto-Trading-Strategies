import os
import pandas as pd
import glob

def master_raporu_olustur():
    output_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_klasoru):
        print("[HATA] output klasörü bulunamadı!")
        return

    print("[BILGI] Sistemdeki tüm _ozet.csv dosyaları taranıyor...")
    
    tum_veriler = []
    
    # Tüm output klasöründe özyineli (recursive) arama
    csv_dosyalari = glob.glob(os.path.join(output_klasoru, "**", "*_ozet.csv"), recursive=True)
    
    for dosya in csv_dosyalari:
        try:
            # Klasör yapısından Hisse ve Strateji isimlerini çıkartma
            # Klasör yapısı: output / HISSE / strateji_adi / HISSE_strateji_adi_ozet.csv
            parcalar = dosya.split(os.sep)
            hisse = parcalar[-3]
            strateji = parcalar[-2]
            
            # CSV'yi oku. Sütun 0'ı indeks (isimler) yap, Sütun 1'i değerler yap.
            df = pd.read_csv(dosya, index_col=0)
            
            # Değerleri güvenli bir şekilde çekmek için yardımcı fonksiyon
            def get_val(key):
                if key in df.index:
                    val = df.loc[key].iloc[0]
                    # NaN kontrolü
                    if pd.isna(val):
                        return 0.0
                    try:
                        return float(val)
                    except ValueError:
                        return val
                return 0.0

            kâr_zarar = get_val("Total Return [%]")
            benchmark_return = get_val("Benchmark Return [%]")
            profit_factor = get_val("Profit Factor")
            max_drawdown = get_val("Max Drawdown [%]")
            islem_sayisi = get_val("Total Trades")
            win_rate = get_val("Win Rate [%]")
            sharpe_ratio = get_val("Sharpe Ratio")
            sortino_ratio = get_val("Sortino Ratio")
            calmar_ratio = get_val("Calmar Ratio")
            best_trade = get_val("Best Trade [%]")
            worst_trade = get_val("Worst Trade [%]")
            avg_win_trade = get_val("Avg Winning Trade [%]")
            avg_lose_trade = get_val("Avg Losing Trade [%]")
            expectancy = get_val("Expectancy")
            
            # --- YENI AKADEMIK METRIKLER ---
            alfa = 0.0
            if isinstance(kâr_zarar, float) and isinstance(benchmark_return, float):
                alfa = kâr_zarar - benchmark_return

            risk_adjusted = 0.0
            if isinstance(kâr_zarar, float) and isinstance(max_drawdown, float) and max_drawdown != 0:
                risk_adjusted = kâr_zarar / abs(max_drawdown)

            akademik_statu = " + İstatistiki Olarak Güvenilir"
            if islem_sayisi < 10:
                akademik_statu = " - Yetersiz Veri / Şans"
            elif profit_factor == float('inf') or profit_factor > 15:
                akademik_statu = " | Overfitting Şüphesi"
            # --------------------------------
            
            tum_veriler.append({
                "Hisse": hisse,
                "Strateji": strateji,
                "Akademik Geçerlilik": akademik_statu,
                "Alfa (α) Piyasayı Yenme": round(alfa, 2),
                "Risk-Ayarlı Getiri": round(risk_adjusted, 2),
                "Kâr / Zarar (%)": round(kâr_zarar, 2) if isinstance(kâr_zarar, float) else kâr_zarar,
                "Benchmark Getiri (%)": round(benchmark_return, 2) if isinstance(benchmark_return, float) else benchmark_return,
                "Profit Factor": round(profit_factor, 2) if isinstance(profit_factor, float) else profit_factor,
                "Max Drawdown (%)": round(max_drawdown, 2) if isinstance(max_drawdown, float) else max_drawdown,
                "İşlem Sayısı": int(islem_sayisi),
                "Kazanma Oranı (%)": round(win_rate, 2) if isinstance(win_rate, float) else win_rate,
                "Sharpe Ratio": round(sharpe_ratio, 2) if isinstance(sharpe_ratio, float) else sharpe_ratio,
                "Sortino Ratio": round(sortino_ratio, 2) if isinstance(sortino_ratio, float) else sortino_ratio,
                "Calmar Ratio": round(calmar_ratio, 2) if isinstance(calmar_ratio, float) else calmar_ratio,
                "En İyi İşlem (%)": round(best_trade, 2) if isinstance(best_trade, float) else best_trade,
                "En Kötü İşlem (%)": round(worst_trade, 2) if isinstance(worst_trade, float) else worst_trade,
                "Ort. Kâr (%)": round(avg_win_trade, 2) if isinstance(avg_win_trade, float) else avg_win_trade,
                "Ort. Zarar (%)": round(avg_lose_trade, 2) if isinstance(avg_lose_trade, float) else avg_lose_trade,
                "Beklenen Getiri (Expectancy)": round(expectancy, 2) if isinstance(expectancy, float) else expectancy
            })
            
        except Exception as e:
            # Okunamayan bir dosya varsa es geç ve devam et
            print(f"  [UYARI] Atlanan dosya ({dosya}): {e}")
            
    if not tum_veriler:
        print("[-] Hiç veri bulunamadı!")
        return
        
    print(f"[BASARILI] Toplam {len(tum_veriler)} adet strateji sonucu başarıyla çekildi.")
    
    # DataFrame oluştur
    df_master = pd.DataFrame(tum_veriler)
    
    # Kâra göre büyükten küçüğe sırala
    df_master = df_master.sort_values(by="Kâr / Zarar (%)", ascending=False)
    
    kayit_yolu = os.path.join(output_klasoru, "Tum_Strateji_Metrikleri.xlsx")
    df_master.to_excel(kayit_yolu, index=False)
    print(f"[MASTER EXCEL] OLUŞTURULDU: {kayit_yolu}")

if __name__ == "__main__":
    master_raporu_olustur()
