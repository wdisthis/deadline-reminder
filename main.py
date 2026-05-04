import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN, WEBHOOK_URL
from database.db import init_db
from handlers import start, help_cmd, cmd_tambah, cmd_list, cmd_selesai, cmd_hapus
from services.reminder import cek_reminder

# Setup Logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# 1. Inisialisasi PTB Application
app_ptb = ApplicationBuilder().token(BOT_TOKEN).build()

# 2. Inisialisasi Database
init_db()

# 3. Daftarkan Perintah
app_ptb.add_handler(CommandHandler("start",   start))
app_ptb.add_handler(CommandHandler("help",    help_cmd))
app_ptb.add_handler(CommandHandler("tambah",  cmd_tambah))
app_ptb.add_handler(CommandHandler("list",    cmd_list))
app_ptb.add_handler(CommandHandler("selesai", cmd_selesai))
app_ptb.add_handler(CommandHandler("hapus",   cmd_hapus))

# 4. Jadwalkan Job Queue
app_ptb.job_queue.run_repeating(cek_reminder, interval=60, first=10)

# 5. Flask App untuk Webhook (PythonAnywhere)
app_flask = Flask(__name__)

@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Endpoint yang akan dipanggil oleh Telegram."""
    if request.method == "POST":
        # Jalankan inisialisasi jika belum (penting untuk server WSGI)
        if not app_ptb.running:
            asyncio.run(app_ptb.initialize())
            asyncio.run(app_ptb.start())
            logger.info("PTB Application initialized and started.")

        update = Update.de_json(request.get_json(), app_ptb.bot)
        asyncio.run(app_ptb.process_update(update))
        return "OK", 200

@app_flask.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

def main():
    if WEBHOOK_URL:
        # Mode Webhook (untuk testing lokal atau server lain)
        logger.info(f"Berjalan dalam mode Webhook: {WEBHOOK_URL}/{BOT_TOKEN}")
        app_flask.run(port=8080)
    else:
        # Mode Polling (untuk development lokal)
        logger.info("Berjalan dalam mode Polling.")
        app_ptb.run_polling()

if __name__ == "__main__":
    main()
