import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TIMEZONE   = os.getenv("TIMEZONE", "Asia/Jakarta")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan di file .env!")
