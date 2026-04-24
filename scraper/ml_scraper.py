import sys
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, ".")
from scraper.utils import HEADERS, delay, limpiar_precio
from db.database import init_db, get_or_create_producto, guardar_precio, obtener_historial
from alerts.email_alert import enviar_alerta

UMBRAL_ALERTA_PCT = 1.0  # enviar email si el precio cambia más de este %


def scrape_producto(url: str) -> dict | None:
    delay()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request fallido: {e}")
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    # Nombre del producto
    nombre_tag = soup.find("h1", class_="ui-pdp-title")
    if not nombre_tag:
        nombre_tag = soup.find("h1")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Sin nombre"

    # Precio principal
    precio_tag = soup.find("span", class_="andes-money-amount__fraction")
    if not precio_tag:
        print("[ERROR] No se encontró el precio. Puede que ML haya cambiado sus selectores.")
        return None

    try:
        precio = limpiar_precio(precio_tag.get_text(strip=True))
    except ValueError as e:
        print(f"[ERROR] No se pudo parsear el precio: {e}")
        return None

    return {"nombre": nombre, "precio": precio, "url": url}


def registrar(url: str):
    init_db()
    resultado = scrape_producto(url)
    if not resultado:
        return

    producto_id = get_or_create_producto(resultado["nombre"], resultado["url"])
    guardar_precio(producto_id, resultado["precio"])

    print(f"[OK] {resultado['nombre']}")
    print(f"     Precio: ${resultado['precio']:,.0f}")

    historial = obtener_historial(producto_id)
    if len(historial) > 1:
        ultimo, anterior = historial[0][0], historial[1][0]
        diff = ultimo - anterior
        signo = "+" if diff >= 0 else ""
        print(f"     Cambio desde ultima vez: {signo}{diff:,.0f}")

        variacion_pct = abs((ultimo - anterior) / anterior * 100)
        if variacion_pct >= UMBRAL_ALERTA_PCT:
            enviar_alerta(resultado["nombre"], ultimo, anterior, resultado["url"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scraper/ml_scraper.py <URL_MERCADOLIBRE>")
        sys.exit(1)
    registrar(sys.argv[1])
