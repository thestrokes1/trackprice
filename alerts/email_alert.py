import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_RECEIVER")


def enviar_alerta(nombre: str, precio_actual: float, precio_anterior: float, url: str):
    if not all([SENDER, PASSWORD, RECEIVER]):
        print("[ALERTA] Variables de email no configuradas en .env — omitiendo.")
        return

    variacion = ((precio_actual - precio_anterior) / precio_anterior) * 100
    signo = "+" if variacion >= 0 else ""

    subject = f"TrackPrice: {nombre} cambió {signo}{variacion:.1f}%"
    body = f"""
<h2>Cambio de precio detectado</h2>
<p><b>{nombre}</b></p>
<p>Precio anterior: <b>${precio_anterior:,.0f}</b></p>
<p>Precio actual: <b>${precio_actual:,.0f}</b></p>
<p>Variación: <b>{signo}{variacion:.1f}%</b></p>
<p><a href="{url}">Ver en MercadoLibre</a></p>
"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
        print(f"[EMAIL] Alerta enviada a {RECEIVER}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
