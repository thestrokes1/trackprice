import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = bool(DATABASE_URL)


def get_conn():
    if USE_POSTGRES:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    return sqlite3.connect("db/trackprice.db")


def ph():
    """Placeholder: %s para postgres, ? para sqlite."""
    return "%s" if USE_POSTGRES else "?"


def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS productos (
                id {'SERIAL' if USE_POSTGRES else 'INTEGER'} PRIMARY KEY {'AUTOINCREMENT' if not USE_POSTGRES else ''},
                nombre TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS precios (
                id {'SERIAL' if USE_POSTGRES else 'INTEGER'} PRIMARY KEY {'AUTOINCREMENT' if not USE_POSTGRES else ''},
                producto_id INTEGER NOT NULL,
                precio REAL NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        conn.commit()


def get_or_create_producto(nombre: str, url: str) -> int:
    p = ph()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM productos WHERE url = {p}", (url,))
        row = cur.fetchone()
        if row:
            return row[0]
        if USE_POSTGRES:
            cur.execute(f"INSERT INTO productos (nombre, url) VALUES ({p}, {p}) RETURNING id", (nombre, url))
            return cur.fetchone()[0]
        cur.execute(f"INSERT INTO productos (nombre, url) VALUES ({p}, {p})", (nombre, url))
        conn.commit()
        return cur.lastrowid


def guardar_precio(producto_id: int, precio: float):
    p = ph()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO precios (producto_id, precio, fecha) VALUES ({p}, {p}, {p})",
            (producto_id, precio, datetime.now().isoformat())
        )
        conn.commit()


def obtener_historial(producto_id: int) -> list:
    p = ph()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT precio, fecha FROM precios WHERE producto_id = {p} ORDER BY fecha DESC",
            (producto_id,)
        )
        return cur.fetchall()


def listar_productos() -> list:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.nombre, p.url, pr.precio, pr.fecha
            FROM productos p
            LEFT JOIN precios pr ON pr.id = (
                SELECT id FROM precios WHERE producto_id = p.id ORDER BY fecha DESC LIMIT 1
            )
            ORDER BY p.id
        """)
        return cur.fetchall()
