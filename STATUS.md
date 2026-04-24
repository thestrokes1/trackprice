# STATUS.md — Estado actual del proyecto
> Actualizar este archivo después de CADA paso completado.

---

## ESTADO GENERAL
**Fase actual:** 1 — Scraper local  
**Último paso completado:** Primera corrida exitosa — datos guardados en SQLite  
**Próximo paso:** scheduler/runner.py — ejecución automática cada X horas

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
- ML devuelve contenido estático correctamente con requests+BS4 para URLs tipo `/p/MLAXXX`
- Selector de precio: `span.andes-money-amount__fraction` — funciona a 2026-04-24
- Para obtener URL válida de producto usar formato: `https://www.mercadolibre.com.ar/<slug>/p/<MLAID>`

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
