import sys
import os
sys.path.insert(0, ".")

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db, listar_productos, obtener_historial

app = FastAPI(title="TrackPrice API", description="Price tracker para MercadoLibre Argentina")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    try:
        init_db()
        print("[OK] DB inicializada")
    except Exception as e:
        print(f"[WARNING] DB init fallida: {e}")


@app.get("/")
def root():
    return {"proyecto": "TrackPrice", "version": "1.0", "status": "ok"}


@app.get("/health")
def health():
    try:
        from db.database import get_conn
        with get_conn() as conn:
            conn.cursor().execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "ok", "db": f"error: {e}"}


@app.get("/productos")
def get_productos():
    rows = listar_productos()
    return [
        {
            "id": r[0],
            "nombre": r[1],
            "url": r[2],
            "precio_actual": r[3],
            "ultima_actualizacion": r[4],
        }
        for r in rows
    ]


@app.get("/productos/{producto_id}/historial")
def get_historial(producto_id: int):
    historial = obtener_historial(producto_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Producto no encontrado o sin historial")
    return [{"precio": h[0], "fecha": h[1]} for h in historial]


@app.post("/scrape")
def trigger_scrape(x_api_key: str = Header(default=None)):
    secret = os.getenv("SCRAPE_API_KEY")
    if secret and x_api_key != secret:
        raise HTTPException(status_code=401, detail="Unauthorized")
    import json
    from scraper.ml_scraper import registrar
    with open("productos.json", "r", encoding="utf-8") as f:
        productos = json.load(f)
    results = []
    for p in productos:
        try:
            registrar(p["url"])
            results.append({"nombre": p["nombre"], "status": "ok"})
        except Exception as e:
            results.append({"nombre": p["nombre"], "status": f"error: {e}"})
    return {"scraped": len(results), "results": results}
