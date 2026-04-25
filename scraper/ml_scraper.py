import re
import sys
import requests

sys.path.insert(0, ".")
from scraper.utils import delay
from db.database import init_db, get_or_create_producto, guardar_precio, obtener_historial
from alerts.email_alert import enviar_alerta

ML_API = "https://api.mercadolibre.com"
UMBRAL_ALERTA_PCT = 1.0


def extraer_id(url: str) -> tuple[str, str]:
    """Retorna (tipo, id): tipo = 'product' o 'item'."""
    m = re.search(r"/p/(MLA\w+)", url)
    if m:
        return ("product", m.group(1))
    m = re.search(r"/(MLA\d+)", url)
    if m:
        return ("item", m.group(1))
    raise ValueError(f"No se pudo extraer ID de MercadoLibre de: {url}")


def scrape_producto(url: str) -> dict | None:
    delay(0.5, 1.5)
    try:
        tipo, ml_id = extraer_id(url)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return None

    try:
        if tipo == "product":
            resp = requests.get(f"{ML_API}/products/{ml_id}", timeout=15)
            resp.raise_for_status()
            data = resp.json()
            nombre = data.get("name", "Sin nombre")
            winner = data.get("buy_box_winner") or {}
            precio = winner.get("price")
            if precio is None:
                # Intentar via search si buy_box_winner no tiene precio
                resp2 = requests.get(
                    f"{ML_API}/sites/MLA/search",
                    params={"catalog_product_id": ml_id, "limit": 1, "sort": "price_asc"},
                    timeout=15,
                )
                resp2.raise_for_status()
                results = resp2.json().get("results", [])
                if not results:
                    print(f"[ERROR] Sin resultados en ML API para {ml_id}")
                    return None
                precio = results[0].get("price")
                nombre = nombre or results[0].get("title", "Sin nombre")
        else:
            resp = requests.get(f"{ML_API}/items/{ml_id}", timeout=15)
            resp.raise_for_status()
            data = resp.json()
            nombre = data.get("title", "Sin nombre")
            precio = data.get("price")

        if precio is None:
            print(f"[ERROR] Precio no encontrado en API para {ml_id}")
            return None

        return {"nombre": nombre, "precio": float(precio), "url": url}

    except requests.RequestException as e:
        print(f"[ERROR] API request fallida: {e}")
        return None


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
