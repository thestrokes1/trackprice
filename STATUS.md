# STATUS.md — Estado actual del proyecto
> Actualizar este archivo después de CADA paso completado.

---

## ESTADO GENERAL
**Fase actual:** 3 — Deploy completado + DB poblada  
**Último paso completado:** DB de Render poblada con datos reales via scraper local  
**Próximo paso:** Dashboard web (D) para portfolio

---

## CHECKLIST FASE 1

- [x] CLAUDE.md creado
- [x] STATUS.md creado
- [x] Carpeta D:\Trackprice lista con estructura completa
- [x] venv creado y activado (D:\Trackprice\venv)
- [x] requirements.txt creado
- [x] Dependencias instaladas (requests, bs4, pandas, playwright, python-dotenv, schedule, fastapi, uvicorn, psycopg2-binary)
- [x] Playwright Chromium instalado
- [x] scraper/utils.py — headers, delay, limpiar_precio
- [x] db/database.py — SQLite operativo (tablas productos + precios)
- [x] scraper/ml_scraper.py — scraper MercadoLibre funcional
- [x] Primera corrida exitosa con datos guardados en DB
- [x] scheduler/runner.py — corre cada 6 horas, lee productos.json
- [x] alerts/email_alert.py — alerta por email (dispara si precio cambia >= 1%)

---

## NOTAS TÉCNICAS

- Deploy: Render (no Railway — free tier activo)
- ML bloquea requests desde EEUU (403) — scraping HTML solo funciona desde IPs argentinas
- Scraper corre localmente y guarda en DB de Render vía External URL
- ML API pública `/products/{id}` requiere OAuth — `/items/{id}` retorna 403 desde EEUU
- Selector de precio: `span.andes-money-amount__fraction` — funciona a 2026-04-25
- External DB URL habilitada para IP 45.237.222.17 (Cristian home)
- GitHub Actions workflow listo en .github/workflows/scrape.yml (falta setear secrets API_URL y SCRAPE_API_KEY)
- POST /scrape con header x-api-key: trackprice-secret-2026 triggereal scraper en Render (no funciona por geo-block)
- GET /debug muestra conteos de productos/precios en DB

---

## LOG DE SESIONES

### Sesión 1
- Creados CLAUDE.md y STATUS.md
- Stack definido: requests+BS4 / Playwright / SQLite / schedule / smtplib

### Sesión 2 (2026-04-24)
- Estructura de carpetas completa creada
- venv + todas las dependencias instaladas
- Playwright Chromium descargado
- scraper/utils.py, db/database.py, scraper/ml_scraper.py creados
- Primera corrida exitosa: Notebook EXO $569.999 guardado en SQLite

---

## ERRORES CONOCIDOS ACTIVOS
_Ninguno_
