import os
import sys
import pandas as pd
import importlib
import inspect
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist"))

import strategies.utils as vbt_utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist", "output", "Tum_Strateji_Metrikleri.xlsx")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist", "data")

def load_data_for_stock(hisse):
    dosya_yolu = os.path.join(DATA_DIR, f"{hisse}.csv")
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"{hisse} verisi bulunamadi.")
    veri = pd.read_csv(dosya_yolu, index_col='Date', parse_dates=True).ffill().bfill()
    return {
        'kapanis_fiyatlari': veri['Close'],
        'kapanis': veri['Close'],
        'acilis': veri['Open'],
        'yuksek': veri['High'],
        'dusuk': veri['Low'],
        'hacim': veri['Volume'],
        'baslik': hisse
    }

STRATEGY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist", "strategies")

def resolve_module_name(strateji_klasor_adi: str) -> str:
    """
    Excel'deki strateji klasör adını (orn: 'vpt_14', 'williams_r_14', 'rsi_14_30_70')
    gerçek Python modül adına çevirir (orn: 'vpt', 'williams_r', 'rsi').
    
    Yöntem: strategies/ klasöründeki .py dosyalarından en uzun eşleşeni bul.
    """
    available = [
        f[:-3] for f in os.listdir(STRATEGY_DIR)
        if f.endswith('.py') and f not in ('__init__.py', 'utils.py')
    ]
    # En uzun eşleşeni bul (örn: williams_r, rsi_macd gibi alt çizgi içerenlerde doğru eşleşme için)
    best = None
    for mod in available:
        if strateji_klasor_adi == mod or strateji_klasor_adi.startswith(mod + '_'):
            if best is None or len(mod) > len(best):
                best = mod
    if best is None:
        raise ValueError(f"Strateji modülü bulunamadı: '{strateji_klasor_adi}'")
    return best

def run_strategy_and_get_portfoy(hisse, strateji_klasor_adi):
    veri_deposu = load_data_for_stock(hisse)
    modul_adi = resolve_module_name(strateji_klasor_adi)
    modul = importlib.import_module(f"strategies.{modul_adi}")
    
    # Portfoy nesnesini yakalamak icin Monkey-Patch
    captured = {}
    
    # "from strategies.utils import sonuclari_kaydet" kullanimi varsa
    # hedef moduldeki (orn: williams_r.py) referansi direkt yamaliyoruz.
    original_kaydet_local = getattr(modul, "sonuclari_kaydet", None)
    original_kaydet_global = vbt_utils.sonuclari_kaydet
    
    def capture(portfoy, baslik, strateji_adi, grafik_baslik=None):
        # Eger calistir() icinde dongu varsa hepsini yakala
        captured[strateji_adi] = portfoy
        # Geriye hicbir sey dondurme ve orijinal kaydet'i CAGIRMA! 
        # Cagirirsan csv/excel'e gereksiz yere yazar, UI'i yavaslatir.
        return None
        
    if original_kaydet_local:
        setattr(modul, "sonuclari_kaydet", capture)
    
    vbt_utils.sonuclari_kaydet = capture
    
    try:
        fonksiyon = modul.calistir
        sig = inspect.signature(fonksiyon)
        fonksiyon_argumanlari = {arg: veri_deposu[arg] for arg in sig.parameters if arg in veri_deposu}
        
        # Stratejiyi çalıştır. Eger modül argümanlarına ragmen loop iceriyorsa, tum stratejiler capture edilecek.
        fonksiyon(**fonksiyon_argumanlari)
        
        # Sadece frontend'in istedigi ozel stratejiyi (orn: williams_r_14) dondur
        if strateji_klasor_adi in captured:
            return captured[strateji_klasor_adi]
        else:
            # Eger birebir eslesme bulunamazsa (isim uyusmazligi vb.), yakalanan ilk portfoyu dondur (fallback)
            return list(captured.values())[0] if captured else None
    finally:
        # Patch'leri geri al
        if original_kaydet_local:
            setattr(modul, "sonuclari_kaydet", original_kaydet_local)
        vbt_utils.sonuclari_kaydet = original_kaydet_global

def generate_html_chart(hisse, strateji):
    portfoy = run_strategy_and_get_portfoy(hisse, strateji)
    if not portfoy:
        raise Exception("Portfoy olusturulamadi (islem yapilmamis olabilir).")
    fig = portfoy.plot(title=f"{hisse} - {strateji.upper()}")
    # iframe icinde gosterilmek uzere full_html=True
    return fig.to_html(full_html=True, include_plotlyjs='cdn')

def generate_png_chart(hisse, strateji):
    portfoy = run_strategy_and_get_portfoy(hisse, strateji)
    if not portfoy:
        raise Exception("Portfoy olusturulamadi.")
    fig = portfoy.plot(title=f"{hisse} - {strateji.upper()}")
    return fig.to_image(format="png", width=1400, height=900)


@app.get("/api/metrics")
async def get_metrics():
    if not os.path.exists(EXCEL_PATH):
        return Response(content="[]", media_type="application/json")
    try:
        df = pd.read_excel(EXCEL_PATH)
        # Pandas'in kendi JSON donusturucusunu kullanmak NaN ve ozel tiplerdeki seri hatalarini onler
        json_str = df.to_json(orient='records')
        return Response(content=json_str, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chart/html/{hisse}/{strateji}", response_class=HTMLResponse)
async def get_chart_html(hisse: str, strateji: str):
    loop = asyncio.get_event_loop()
    try:
        # Event loop bloklanmamasi icin run_in_executor
        html_content = await loop.run_in_executor(None, generate_html_chart, hisse, strateji)
        return html_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chart/png/{hisse}/{strateji}")
async def get_chart_png(hisse: str, strateji: str):
    loop = asyncio.get_event_loop()
    try:
        png_data = await loop.run_in_executor(None, generate_png_chart, hisse, strateji)
        return Response(content=png_data, media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename={hisse}_{strateji}.png"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
