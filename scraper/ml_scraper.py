import re
import sys
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, ".")
from scraper.utils import HEADERS, delay, limpiar_precio
from db.database import init_db, get_or_create_producto, guardar_precio, obtener_historial
from alerts.email_alert import enviar_alerta

UMBRAL_ALERTA_PCT = 1.0


def scrape_html(url: str) -> dict | None:
    """Scraping HTML — funciona desde Argentina."""
    delay()
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request fallido: {e}")
        return None

    soup = BeautifulSoup(resp.text, "lxml")

    nombre_tag = soup.find("h1", class_="ui-pdp-title") or soup.find("h1")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Sin nombre"

    precio_tag = soup.find("span", class_="andes-money-amount__fraction")
    if not precio_tag:
        print("[ERROR] Precio no encontrado — ML puede haber cambiado sus selectores.")
        return None

    try:
        precio = limpiar_precio(precio_tag.get_text(strip=True))
    except ValueError as e:
        print(f"[ERROR] No se pudo parsear el precio: {e}")
        return None

    return {"nombre": nombre, "precio": precio, "url": url}


def scrape_api(url: str) -> dict | None:
    """Scraping via ML API pública (items) — funciona desde cualquier servidor."""
    # Intentar extraer item ID de la URL (MLA seguido de dígitos largos)
    m = re.search(r"/(MLA\d{8,})", url)
    if not m:
        return None

    item_id = m.group(1)
    delay(0.5, 1.0)
    try:
        resp = requests.get(f"https://api.mercadolibre.com/items/{item_id}", timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return {
            "nombre": data.get("title", "Sin nombre"),
            "precio": float(data["price"]),
            "url": url,
        }
    except Exception as e:
        print(f"[ERROR] ML API items fallida: {e}")
        return None


def scrape_producto(url: str) -> dict | None:
    # Intentar API pública primero (sin geo-blocking)
    resultado = scrape_api(url)
    if resultado:
        print("[INFO] Precio obtenido via ML API")
        return resultado
    # Fallback a HTML scraping (requiere IP argentina)
    print("[INFO] Intentando scraping HTML...")
    return scrape_html(url)


def registrar(url: str) -> bool:
    init_db()
    resultado = scrape_producto(url)
    if not resultado:
        raise RuntimeError(f"Scraping fallido para {url} — precio no encontrado")

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

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scraper/ml_scraper.py <URL_MERCADOLIBRE>")
        sys.exit(1)
    registrar(sys.argv[1])
