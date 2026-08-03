"""
utils.py — Strateji Yardimci Fonksiyonlari

Tum stratejilerde tekrar eden kayit/grafik blogu buraya tasinmistir.
Yeni bir strateji yazarken bu modulu import edip sonuclari_kaydet() cagir.

Kullanim:
    from strategies.utils import sonuclari_kaydet
    return sonuclari_kaydet(portfoy, baslik, strateji_adi)
"""

import os
import vectorbt as vbt

# --- GLOBAL VECTORBT PORTFÖY AYARLARI (MERKEZİ) ---
# Bu ayarlar sayesinde 90 stratejinin içine tek tek fees yazmaya gerek kalmaz.
# Herhangi bir strateji bu modülü içe aktardığında, vectorbt motoru bu ayarları
# otomatik olarak tüm Portfolio işlemlerinde kullanacaktır.
vbt.settings.portfolio['init_cash'] = 10000
vbt.settings.portfolio['fees'] = 0.001
vbt.settings.portfolio['slippage'] = 0.002
vbt.settings.portfolio['freq'] = '1d'

def sonuclari_kaydet(portfoy, baslik, strateji_adi, grafik_baslik=None):
    """
    Portfoy sonuclarini CSV, HTML ve PNG olarak output klasorune kaydeder.

    Args:
        portfoy      : vectorbt Portfolio nesnesi
        baslik       : Hisse kodu (orn: 'AKBNK')
        strateji_adi : Strateji klasor adi (orn: 'rsi_14_30_70')
        grafik_baslik: Grafik uzerinde gorunecek baslik (None ise otomatik olusturulur)

    Returns:
        portfoy.stats() : Ana motorun ihtiyac duydugu ozet DataFrame
    """
    # --- Klasor Olustur ---
    klasor = os.path.join("vbt_bist", "output", baslik, strateji_adi)
    os.makedirs(klasor, exist_ok=True)

    # --- Ozet CSV (Her zaman kaydedilir) ---
    portfoy.stats().to_csv(
        os.path.join(klasor, f"{baslik}_{strateji_adi}_ozet.csv")
    )

    # --- Islemler CSV + Grafik (Sadece en az 1 islem varsa) ---
    # Islem yoksa grafik ciziminde NaN hatasi olusur (opacity=[nan]).
    # Bu kontrol o hatanin onune gecer.
    if portfoy.trades.count() > 0:
        portfoy.trades.records_readable.to_csv(
            os.path.join(klasor, f"{baslik}_{strateji_adi}_islemler.csv")
        )
        # try:
        #     baslik_str = grafik_baslik or f"{baslik} - {strateji_adi}"
        #     fig = portfoy.plot(title=baslik_str)
        #     fig.write_html(
        #         os.path.join(klasor, f"{baslik}_{strateji_adi}_grafik.html")
        #     )
        #     fig.write_image(
        #         os.path.join(klasor, f"{baslik}_{strateji_adi}_vbt.png"),
        #         width=1400, height=900
        #     )
        # except Exception:
        #     pass  # Grafik hatasi ozet CSV'yi etkilemez

    return portfoy.stats()
