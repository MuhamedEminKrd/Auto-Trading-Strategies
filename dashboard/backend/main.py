import os
import sys
import math
import json
import time
import importlib
import importlib.util
import inspect
import asyncio
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response, JSONResponse

# Yol ayarlari
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist"))

import strategies.utils as vbt_utils

# Sabitler
BASE_DIR      = os.path.join(os.path.dirname(__file__), "..", "..", "vbt_bist")
EXCEL_PATH    = os.path.join(BASE_DIR, "output", "Tum_Strateji_Metrikleri.xlsx")
DATA_DIR      = os.path.join(BASE_DIR, "data")
STRATEGY_DIR  = os.path.join(BASE_DIR, "strategies")

app = FastAPI(
    title="Auto Trading Strategies API",
    description="BIST100 strateji backtest dashboard API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)

# Metrics onbellegi
_metrics_cache = {
    "data": None,
    "loaded_at": None,
    "excel_mtime": None,
}
_refresh_lock = threading.Lock()
_refresh_status = {
    "running": False,
    "last_run": None,
    "last_result": None,
}


def _sanitize_value(v):
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
    return v


def _load_metrics() -> str:
    if not os.path.exists(EXCEL_PATH):
        return "[]"
    df = pd.read_excel(EXCEL_PATH)
    records = []
    for row in df.to_dict(orient="records"):
        records.append({k: _sanitize_value(v) for k, v in row.items()})
    return json.dumps(records, ensure_ascii=False)


def get_metrics_cached() -> str:
    try:
        mtime = os.path.getmtime(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None
    except OSError:
        mtime = None

    if _metrics_cache["data"] is not None and _metrics_cache["excel_mtime"] == mtime:
        return _metrics_cache["data"]

    data = _load_metrics()
    _metrics_cache["data"] = data
    _metrics_cache["loaded_at"] = time.time()
    _metrics_cache["excel_mtime"] = mtime
    return data


def load_data_for_stock(hisse: str) -> dict:
    dosya_yolu = os.path.join(DATA_DIR, f"{hisse}.csv")
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"{hisse} verisi bulunamadi: {dosya_yolu}")
    veri = pd.read_csv(dosya_yolu, index_col="Date", parse_dates=True).ffill().bfill()
    return {
        "kapanis_fiyatlari": veri["Close"],
        "kapanis": veri["Close"],
        "acilis": veri["Open"],
        "yuksek": veri["High"],
        "dusuk": veri["Low"],
        "hacim": veri["Volume"],
        "baslik": hisse,
    }


def _available_modules() -> list:
    return [
        f[:-3]
        for f in os.listdir(STRATEGY_DIR)
        if f.endswith(".py") and f not in ("__init__.py", "utils.py")
    ]


def resolve_module_name(strateji_klasor_adi: str) -> str:
    available = _available_modules()
    best = None
    for mod in available:
        if strateji_klasor_adi == mod or strateji_klasor_adi.startswith(mod + "_"):
            if best is None or len(mod) > len(best):
                best = mod
    if best is None:
        raise ValueError(f"Strateji modulu bulunamadi: '{strateji_klasor_adi}'")
    return best


def run_strategy_and_get_portfoy(hisse: str, strateji_klasor_adi: str):
    veri_deposu = load_data_for_stock(hisse)
    modul_adi = resolve_module_name(strateji_klasor_adi)
    modul = importlib.import_module(f"strategies.{modul_adi}")

    captured = {}
    original_kaydet_local  = getattr(modul, "sonuclari_kaydet", None)
    original_kaydet_global = vbt_utils.sonuclari_kaydet

    def capture(portfoy, baslik, strateji_adi, grafik_baslik=None):
        captured[strateji_adi] = portfoy
        return None

    if original_kaydet_local:
        setattr(modul, "sonuclari_kaydet", capture)
    vbt_utils.sonuclari_kaydet = capture

    try:
        fonksiyon = modul.calistir
        sig = inspect.signature(fonksiyon)
        fonksiyon_argumanlari = {
            arg: veri_deposu[arg]
            for arg in sig.parameters
            if arg in veri_deposu
        }
        fonksiyon(**fonksiyon_argumanlari)

        if strateji_klasor_adi in captured:
            return captured[strateji_klasor_adi]
        return list(captured.values())[0] if captured else None
    finally:
        if original_kaydet_local:
            setattr(modul, "sonuclari_kaydet", original_kaydet_local)
        vbt_utils.sonuclari_kaydet = original_kaydet_global


def generate_html_chart(hisse: str, strateji: str) -> str:
    portfoy = run_strategy_and_get_portfoy(hisse, strateji)
    if not portfoy:
        raise ValueError("Portfoy olusturulamadi (islem yapilmamis olabilir).")
    fig = portfoy.plot(title=f"{hisse} - {strateji.upper()}")
    return fig.to_html(full_html=True, include_plotlyjs="cdn")


def generate_png_chart(hisse: str, strateji: str) -> bytes:
    portfoy = run_strategy_and_get_portfoy(hisse, strateji)
    if not portfoy:
        raise ValueError("Portfoy olusturulamadi.")
    fig = portfoy.plot(title=f"{hisse} - {strateji.upper()}")
    return fig.to_image(format="png", width=1400, height=900)


def _run_master_rapor():
    with _refresh_lock:
        if _refresh_status["running"]:
            return
        _refresh_status["running"] = True
    try:
        spec = importlib.util.spec_from_file_location(
            "master_rapor_olustur",
            os.path.join(BASE_DIR, "master_rapor_olustur.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.master_raporu_olustur()

        # Onbellegi gecersiz kil
        _metrics_cache["data"] = None
        _metrics_cache["excel_mtime"] = None

        _refresh_status["last_result"] = "success"
        _refresh_status["last_run"] = datetime.now().isoformat()
    except Exception as e:
        _refresh_status["last_result"] = f"error: {e}"
        _refresh_status["last_run"] = datetime.now().isoformat()
    finally:
        _refresh_status["running"] = False


# ═══ API ENDPOINTS ════════════════════════════════════════════════════════════

@app.get("/api/metrics")
async def get_metrics():
    try:
        json_str = get_metrics_cached()
        return Response(content=json_str, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/strategies")
async def get_strategies():
    try:
        mods = sorted(_available_modules())
        return {"strategies": mods, "count": len(mods)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stocks")
async def get_stocks():
    try:
        stocks = sorted([
            f[:-4]
            for f in os.listdir(DATA_DIR)
            if f.endswith(".csv")
        ])
        return {"stocks": stocks, "count": len(stocks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/data-status")
async def get_data_status():
    try:
        status = []
        for f in sorted(os.listdir(DATA_DIR)):
            if not f.endswith(".csv"):
                continue
            hisse = f[:-4]
            dosya = os.path.join(DATA_DIR, f)
            try:
                df_tail = pd.read_csv(dosya, index_col=0, parse_dates=True).tail(1)
                son_tarih = str(df_tail.index[-1].date()) if len(df_tail) else "bilinmiyor"
            except Exception:
                son_tarih = "okunamadi"
            status.append({"hisse": hisse, "son_tarih": son_tarih})
        return {"count": len(status), "stocks": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/refresh")
async def refresh_metrics(background_tasks: BackgroundTasks):
    if _refresh_status["running"]:
        return JSONResponse(
            status_code=202,
            content={"message": "Refresh zaten calisiyor.", "status": _refresh_status},
        )
    background_tasks.add_task(_run_master_rapor)
    return JSONResponse(
        status_code=202,
        content={"message": "Metrik yenileme baslatildi.", "status": _refresh_status},
    )


@app.get("/api/refresh/status")
async def get_refresh_status():
    return {
        "running": _refresh_status["running"],
        "last_run": _refresh_status["last_run"],
        "last_result": _refresh_status["last_result"],
        "excel_last_modified": (
            datetime.fromtimestamp(os.path.getmtime(EXCEL_PATH)).isoformat()
            if os.path.exists(EXCEL_PATH) else None
        ),
    }


@app.get("/api/chart/html/{hisse}/{strateji}", response_class=HTMLResponse)
async def get_chart_html(hisse: str, strateji: str):
    loop = asyncio.get_event_loop()
    try:
        html_content = await loop.run_in_executor(executor, generate_html_chart, hisse, strateji)
        return html_content
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chart/png/{hisse}/{strateji}")
async def get_chart_png(hisse: str, strateji: str):
    loop = asyncio.get_event_loop()
    try:
        png_data = await loop.run_in_executor(executor, generate_png_chart, hisse, strateji)
        return Response(
            content=png_data,
            media_type="image/png",
            headers={"Content-Disposition": f"attachment; filename={hisse}_{strateji}.png"},
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    excel_exists = os.path.exists(EXCEL_PATH)
    data_count = len([f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]) if os.path.exists(DATA_DIR) else 0
    strategy_count = len(_available_modules())
    return {
        "status": "ok",
        "excel_exists": excel_exists,
        "excel_path": EXCEL_PATH,
        "data_files": data_count,
        "strategies": strategy_count,
        "excel_last_modified": (
            datetime.fromtimestamp(os.path.getmtime(EXCEL_PATH)).isoformat()
            if excel_exists else None
        ),
    }
