# TrackPrice 📈

Rastreador automático de precios para MercadoLibre Argentina. Guarda el historial de precios y muestra la evolución en un dashboard web en tiempo real.

**[🌐 Ver Dashboard](https://thestrokes1.github.io/trackprice/)** · **[🔗 Ver API](https://trackprice-xw0u.onrender.com)**

![Dashboard](docs/screenshot_prod.png)

---

## ¿Qué hace?

- Scrapea precios de productos de MercadoLibre Argentina
- Guarda el historial completo en PostgreSQL
- Expone los datos via API REST (FastAPI)
- Muestra un dashboard interactivo con gráfico de evolución de precios
- Envía alertas por email cuando el precio cambia más de 1%

---

## Stack

| Capa | Tecnología |
|---|---|
| Scraping | Python · requests · BeautifulSoup4 |
| Base de datos | PostgreSQL (Render) |
| API | FastAPI · Uvicorn |
| Frontend | HTML · CSS · JavaScript · Chart.js |
| Deploy API | Render (free tier) |
| Deploy Frontend | GitHub Pages |
| Alertas | Gmail SMTP |

---

## Arquitectura

```
┌─────────────────────┐
│   scraper local     │  requests + BS4
│   (Python)          │──────────────────► MercadoLibre AR
└────────┬────────────┘
         │ guarda precio
         ▼
┌─────────────────────┐
│   PostgreSQL        │  Render cloud
│   trackprice-db     │
└────────┬────────────┘
         │ lee datos
         ▼
┌─────────────────────┐        ┌─────────────────────┐
│   FastAPI (Render)  │◄───────│  Dashboard          │
│   /productos        │  fetch │  GitHub Pages       │
│   /historial        │        │  Chart.js           │
└─────────────────────┘        └─────────────────────┘
```

---

## API Endpoints

Base URL: `https://trackprice-xw0u.onrender.com`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Info del servicio |
| GET | `/health` | Estado y conexión a DB |
| GET | `/productos` | Lista productos con precio actual |
| GET | `/productos/{id}/historial` | Historial de precios de un producto |
| POST | `/scrape` | Triggereal scraper manualmente |

**Ejemplo:**
```bash
curl https://trackprice-xw0u.onrender.com/productos
```
```json
[
  {
    "id": 1,
    "nombre": "Notebook Exo Smart T38",
    "precio_actual": 569999.0,
    "ultima_actualizacion": "2026-04-25T13:11:00"
  }
]
```

---

## Correr localmente

```bash
# 1. Clonar repo
git clone https://github.com/thestrokes1/trackprice.git
cd trackprice

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Correr el scraper
python scheduler/runner.py --once

# 6. Levantar la API
uvicorn api.main:app --reload
```

---

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

Luego corrés `python scheduler/runner.py --once` para scrapear.

---

## Variables de entorno

```env
EMAIL_SENDER=tu@gmail.com
EMAIL_PASSWORD=app_password_de_gmail
EMAIL_RECEIVER=tu@gmail.com
DATABASE_URL=postgresql://...  # opcional, usa SQLite si no se define
```

---

## Estructura del proyecto

```
trackprice/
├── scraper/
│   ├── ml_scraper.py      # scraper principal
│   └── utils.py           # headers, delays, helpers
├── db/
│   └── database.py        # SQLite / PostgreSQL
├── alerts/
│   └── email_alert.py     # alertas por email
├── scheduler/
│   └── runner.py          # orquestador
├── api/
│   └── main.py            # FastAPI
├── docs/
│   └── index.html         # dashboard web
├── productos.json          # lista de productos a trackear
└── render.yaml            # config de deploy
```

---

## Deploy

La API está deployada en **Render** con PostgreSQL gratis.
El dashboard está hosteado en **GitHub Pages** (carpeta `/docs`).

---

Desarrollado por **Cristian** · [GitHub](https://github.com/thestrokes1)
