# TrackPrice

Price tracker automático para MercadoLibre Argentina. Scrapeá precios, guardá historial y recibí alertas por email cuando un producto baja de precio.

## Features

- Scraping de productos de MercadoLibre con requests + BeautifulSoup
- Historial de precios guardado en SQLite (local) / PostgreSQL (deploy)
- Alertas por email automáticas cuando el precio cambia
- Scheduler que corre cada 6 horas sin intervención manual
- API REST con FastAPI para consultar productos e historial
- Deploy listo en Render

## Stack

| Capa | Herramienta |
|---|---|
| Scraping | requests + BeautifulSoup4 |
| Base de datos | SQLite / PostgreSQL |
| Scheduling | schedule |
| Alertas | smtplib (Gmail) |
| API | FastAPI + Uvicorn |
| Deploy | Render |

## Instalación local

```bash
# Clonar el repo
git clone https://github.com/TU_USUARIO/trackprice.git
cd trackprice

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
playwright install chromium

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de email
```

## Uso

```bash
# Scrapeár un producto una vez
python scraper/ml_scraper.py "https://www.mercadolibre.com.ar/..."

# Correr el scheduler automático (cada 6 horas)
python scheduler/runner.py

# Levantar la API
uvicorn api.main:app --reload
```

## API Endpoints

| Endpoint | Descripción |
|---|---|
| `GET /` | Info del proyecto |
| `GET /health` | Health check |
| `GET /productos` | Lista productos con precio actual |
| `GET /productos/{id}/historial` | Historial de precios de un producto |

## Agregar productos a trackear

Editá `productos.json`:

```json
[
  {
    "nombre": "Mi producto",
    "url": "https://www.mercadolibre.com.ar/.../p/MLAXXX"
  }
]
```

## Variables de entorno

```
EMAIL_SENDER=tu@gmail.com
EMAIL_PASSWORD=app-password-de-gmail
EMAIL_RECEIVER=destino@gmail.com
DATABASE_URL=           # Solo para deploy (PostgreSQL)
```

## Deploy en Render

Ver sección de deploy en la documentación del proyecto.
