import time
import socket
import requests
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

URL = os.getenv("URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))
NOTIFY_INTERVAL = int(os.getenv("NOTIFY_INTERVAL", 300))
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def check_dns(domain):
    """Verifica si el dominio tiene resolución DNS."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def check_http(url):
    """Verifica si la página responde con HTTP 200."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def send_telegram_message(message):
    """Envía un mensaje al chat de Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data, timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False


def get_last_update_id():
    """Obtiene el último update_id existente para empezar limpio."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if not data.get("ok") or not data.get("result"):
            return 0
        return max(update["update_id"] for update in data["result"])
    except:
        return 0


def check_stop_command(last_update_id):
    """Revisa si el usuario mandó 'stop' al bot después de last_update_id."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id+1}"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if not data.get("ok"):
            return False, last_update_id

        for update in data["result"]:
            update_id = update["update_id"]
            message = update.get("message", {}).get("text", "").strip().lower()
            if message == "stop":
                return True, update_id
            last_update_id = update_id

        return False, last_update_id
    except:
        return False, last_update_id


if __name__ == "__main__":
    domain = URL.split("//")[-1].split("/")[0]  # extrae dominio
    page_up = False
    last_notify = 0

    # 🚀 Al inicio, consumimos todos los mensajes viejos
    last_update_id = get_last_update_id()

    while True:
        # 1️⃣ Revisar si mandaste "stop"
        stop, last_update_id = check_stop_command(last_update_id)
        if stop:
            print("🛑 Recibido 'stop'. Terminando script.")
            send_telegram_message("🛑 Notificaciones detenidas por comando 'stop'.")
            break

        # 2️⃣ Revisar si la página ya está arriba
        if not page_up:
            dns_ok = check_dns(domain)
            if dns_ok and check_http(URL):
                page_up = True
                print("🚀 La página ya está arriba:", URL)
                send_telegram_message(f"🚀 La página ya está disponible: {URL}")
                last_notify = time.time()
        else:
            # 3️⃣ Si ya está arriba, notificar cada NOTIFY_INTERVAL
            if time.time() - last_notify >= NOTIFY_INTERVAL:
                send_telegram_message(f"🔔 La página sigue arriba: {URL}")
                last_notify = time.time()

        time.sleep(CHECK_INTERVAL)
