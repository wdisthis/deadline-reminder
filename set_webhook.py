import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def set_webhook():
    if not BOT_TOKEN or not WEBHOOK_URL:
        print("Error: BOT_TOKEN atau WEBHOOK_URL belum diatur di file .env!")
        return

    # URL path yang kita gunakan di main.py adalah token bot itu sendiri untuk keamanan
    target_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={target_url}"

    print(f"Mengatur webhook ke: {target_url}")
    response = requests.get(api_url)
    
    if response.status_code == 200:
        print("Berhasil! Telegram akan mengirim pesan ke server Anda.")
        print(response.json())
    else:
        print("Gagal mengatur webhook.")
        print(response.text)

if __name__ == "__main__":
    set_webhook()
