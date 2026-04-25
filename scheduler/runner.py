import sys
import json
import schedule
import time
from datetime import datetime

sys.path.insert(0, ".")
from scraper.ml_scraper import registrar

PRODUCTOS_FILE = "productos.json"
INTERVALO_HORAS = 6


def cargar_productos() -> list:
    with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def correr_todos():
    productos = cargar_productos()
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Corriendo scraper ({len(productos)} productos)...")
    for p in productos:
        print(f"  -> {p['nombre']}")
        registrar(p["url"])
    print("Listo. Próxima corrida en {} horas.\n".format(INTERVALO_HORAS))


if __name__ == "__main__":
    if "--once" in sys.argv:
        correr_todos()
    else:
        print(f"Scheduler iniciado. Intervalo: cada {INTERVALO_HORAS} horas.")
        correr_todos()
        schedule.every(INTERVALO_HORAS).hours.do(correr_todos)
        while True:
            schedule.run_pending()
            time.sleep(60)
