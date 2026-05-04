import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN, WEBHOOK_URL
from database.db import init_db
from handlers import start, help_cmd, cmd_tambah, cmd_list, cmd_selesai, cmd_hapus
from services.reminder import cek_reminder
from services.schedule import kirim_jadwal_harian
from utils.helpers import TZ
from datetime import time

# Setup Logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# 1. Inisialisasi PTB Application secara Global
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
app_ptb.job_queue.run_daily(kirim_jadwal_harian, time=time(6, 0, tzinfo=TZ))

# 5. Flask App
app_flask = Flask(__name__)

# Inisialisasi loop global untuk performa lebih baik
loop = asyncio.get_event_loop()

@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            # Pastikan bot sudah diinisialisasi sekali saja
            if not app_ptb.running:
                loop.run_until_complete(app_ptb.initialize())
                loop.run_until_complete(app_ptb.start())
            
            update = Update.de_json(request.get_json(), app_ptb.bot)
            loop.run_until_complete(app_ptb.process_update(update))
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            
        return "OK", 200

@app_flask.route("/", methods=["GET"])
def index():
    return "Bot is running efficiently!", 200

def main():
    if WEBHOOK_URL:
        app_flask.run(port=8080)
    else:
        app_ptb.run_polling()

if __name__ == "__main__":
    main()
