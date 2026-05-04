import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, help_cmd, cmd_tambah, cmd_list, cmd_selesai, cmd_hapus, cmd_jadwal
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

def main():
    # 1. Inisialisasi Database
    init_db()

    # 2. Inisialisasi PTB Application
    # Menggunakan context manager atau build() biasa
    app_ptb = ApplicationBuilder().token(BOT_TOKEN).build()

    # 3. Daftarkan Perintah
    app_ptb.add_handler(CommandHandler("start",   start))
    app_ptb.add_handler(CommandHandler("help",    help_cmd))
    app_ptb.add_handler(CommandHandler("tambah",  cmd_tambah))
    app_ptb.add_handler(CommandHandler("list",    cmd_list))
    app_ptb.add_handler(CommandHandler("selesai", cmd_selesai))
    app_ptb.add_handler(CommandHandler("hapus",   cmd_hapus))
    app_ptb.add_handler(CommandHandler("jadwal",  cmd_jadwal))

    # 4. Jadwalkan Job Queue
    if app_ptb.job_queue:
        app_ptb.job_queue.run_repeating(cek_reminder, interval=900, first=10)
        app_ptb.job_queue.run_daily(kirim_jadwal_harian, time=time(6, 0, tzinfo=TZ))
        logger.info("Job queue berhasil dijadwalkan.")
    else:
        logger.warning("Job queue tidak tersedia. Pastikan 'python-telegram-bot[job-queue]' terinstall.")

    # 5. Jalankan Bot dengan Polling
    logger.info("Bot dimulai menggunakan Polling (lebih cepat & stabil untuk lokal)...")
    app_ptb.run_polling()

if __name__ == "__main__":
    main()
