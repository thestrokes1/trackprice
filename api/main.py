import sys
sys.path.insert(0, ".")

from fastapi import FastAPI, HTTPException
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
    init_db()


@app.get("/")
def root():
    return {"proyecto": "TrackPrice", "version": "1.0", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


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
