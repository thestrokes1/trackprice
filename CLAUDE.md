# TRACKPRICE — CLAUDE.md
> Leer esto PRIMERO en cada sesión. Contiene todo el contexto necesario.

---

## PROYECTO
Price Tracker automático para MercadoLibre Argentina.
Scraping de precios → guardado en DB → historial → alertas por email/Telegram.
**Objetivo final:** 3 proyectos deployados listos para portfolio laboral.

## DUEÑO
Cristian — desarrollador con experiencia en Python, JS/TS, Android (Kotlin), iOS, Java.
No hace nada manualmente — Claude ejecuta todo en terminal.

## DIRECTORIO RAÍZ
```
D:\Trackprice
```

---

## STACK DECIDIDO (no cambiar sin actualizar este archivo)
| Capa | Herramienta | Motivo |
|---|---|---|
| Scraping estático | requests + BeautifulSoup | liviano, rápido |
| Scraping dinámico | Playwright | moderno, mejor que Selenium |
| Datos | pandas | limpieza y exportación |
| Base de datos | SQLite (fase 1) → PostgreSQL (fase 2) | sin setup inicial |
| Scheduling | schedule (local) → cron en VPS (deploy) | simple primero |
| Alertas | smtplib email → Telegram bot | por orden de complejidad |
| Deploy | Railway | free tier, fácil |
| Lenguaje | Python 3.11+ | |
| Entorno | venv en D:\Trackprice\venv | |

---

## ESTRUCTURA DE CARPETAS
```
D:\Trackprice
├── CLAUDE.md                  ← este archivo
├── STATUS.md                  ← estado actual del proyecto (actualizar siempre)
├── venv/                      ← entorno virtual Python
├── scraper/
│   ├── __init__.py
│   ├── ml_scraper.py          ← scraper principal MercadoLibre
│   ├── playwright_scraper.py  ← para sitios con JS dinámico
│   └── utils.py               ← helpers: delays, headers, limpieza
├── db/
│   ├── __init__.py
│   ├── database.py            ← conexión y operaciones SQLite/PostgreSQL
│   └── trackprice.db          ← base de datos SQLite local
├── alerts/
│   ├── __init__.py
│   ├── email_alert.py
│   └── telegram_alert.py
├── scheduler/
│   └── runner.py              ← orquesta todo, corre periódicamente
├── api/                       ← fase 2: exponer datos como API REST
│   └── main.py                ← FastAPI
├── tests/
│   └── test_scraper.py
├── .env                       ← variables secretas (nunca en git)
├── .env.example               ← plantilla sin valores reales
├── .gitignore
├── requirements.txt
└── README.md
```

---

## FASES DEL PROYECTO

### FASE 1 — Scraper local funcional ← ESTAMOS AQUÍ
- [ ] Estructura de carpetas creada
- [ ] venv creado e instalado
- [ ] Scraper MercadoLibre funciona (requests + BS4)
- [ ] Datos guardados en SQLite con historial
- [ ] Script corre sin errores de principio a fin

### FASE 2 — Automation
- [ ] Playwright integrado para sitios JS
- [ ] Scheduler automático (cada X horas)
- [ ] Alertas por email cuando precio baja X%
- [ ] Telegram bot opcional

### FASE 3 — Deploy + Portfolio
- [ ] API con FastAPI expone datos
- [ ] Deploy en Railway
- [ ] README con screenshots para GitHub
- [ ] Aplicar a roles remotos

---

## REGLAS DE EJECUCIÓN (Claude debe seguir siempre)

1. **Antes de escribir código** → revisar STATUS.md para saber el estado exacto
2. **Después de cada paso exitoso** → actualizar STATUS.md inmediatamente
3. **Si algo falla** → NO reescribir todo. Diagnosticar el error puntual primero
4. **Orden de operaciones:** instalar dependencias → crear archivo → probar → confirmar → siguiente paso
5. **Nunca asumir que algo ya está instalado** → verificar con `pip list` o `python -c "import X"`
6. **Un solo archivo a la vez** — no crear múltiples archivos de golpe sin testear el anterior
7. **Ante duda entre dos enfoques** → elegir el más simple que funcione
8. **Tokens:** respuestas cortas y directas. El código va completo, las explicaciones son mínimas

---

## VARIABLES DE ENTORNO (.env)
```
# Email alerts
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECEIVER=

# Telegram (opcional fase 2)
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=

# PostgreSQL (fase 2 deploy)
DATABASE_URL=
```

---

## COMANDOS ÚTILES (referencia rápida)

```bash
# Activar entorno virtual
# Windows:
D:\Trackprice\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# Correr scraper principal
python scraper/ml_scraper.py

# Correr scheduler
python scheduler/runner.py

# Ver base de datos rápido
python -c "import sqlite3; conn=sqlite3.connect('db/trackprice.db'); print([r for r in conn.execute('SELECT * FROM precios LIMIT 10')])"
```

---

## ANTI-PATTERNS (no hacer)
- ❌ No usar Selenium (usamos Playwright)
- ❌ No hardcodear credenciales en código
- ❌ No scrapear sin delays (mínimo 1–3 seg entre requests)
- ❌ No crear archivos nuevos sin testear el anterior
- ❌ No ignorar errores HTTP (siempre manejar status codes)
- ❌ No asumir que MercadoLibre no cambia su HTML (verificar selectores si falla)

---

## TROUBLESHOOTING FRECUENTE

| Error | Causa probable | Fix |
|---|---|---|
| `ModuleNotFoundError` | venv no activado o pip no corrido | activar venv + `pip install -r requirements.txt` |
| `AttributeError: NoneType` en BS4 | selector CSS/HTML cambió en ML | inspeccionar elemento en browser y actualizar selector |
| `403 Forbidden` | ML bloqueó el request | agregar headers realistas + delay |
| `playwright not found` | falta `playwright install` | `playwright install chromium` |
| DB locked | SQLite abierto en otro proceso | cerrar conexiones, usar `with` statement |

---
