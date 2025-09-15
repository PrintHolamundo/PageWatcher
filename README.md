# PageWatcher

Script en **Python** para monitorear una página web y enviar notificaciones por **Telegram** cuando esté en línea.  
Además, puede mandar recordatorios cada cierto tiempo y detenerse cuando recibe el comando `stop`.

---

## 🚀 Funcionalidades

- Verifica periódicamente si un dominio tiene resolución DNS.  
- Comprueba si la página responde correctamente (HTTP 200).  
- Envía un mensaje a un **chat de Telegram** cuando la página esté disponible.  
- Sigue notificando cada **5 minutos** mientras la página permanezca arriba.  
- Si envías el comando `stop` al bot, el script detiene las notificaciones y finaliza.  

---

## ⚙️ Requisitos

- Python **3.8+**  
- Librerías necesarias:  
  ```bash
  pip install requests

📥 Instalación

Clona el repositorio o copia los archivos en tu máquina:

```bash
git clone https://github.com/PrintHolamundo/PageWatcher.git
cd PageWatcher
```
Instala las dependencias:
```bash
pip install -r requirements.txt
```

🤖 Configuración de Telegram Bot

Crea un bot en Telegram con @[BotFather](https://t.me/botfather)
.

- Guarda tu BOT_TOKEN.

Obtén tu CHAT_ID:

- Manda un mensaje a tu bot.

- Abre en tu navegador:
```bash
https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```
Busca "chat":{"id": ... } → ese es tu CHAT_ID.

- Configura tu main.py editando las variables:
```bash
BOT_TOKEN = "TU_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"
```
▶️ Uso

Ejecuta el script:
```bash
python main.py
```
- El script monitorea la página definida en URL.

- Cuando esté disponible, envía una notificación a Telegram.

- Manda recordatorios cada 5 minutos mientras siga arriba.

- Si escribes stop en el chat del bot, el script termina.


