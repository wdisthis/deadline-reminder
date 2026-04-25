import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, help_cmd, cmd_tambah, cmd_list, cmd_selesai, cmd_hapus
from services.reminder import cek_reminder

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    # Inisialisasi database
    init_db()
    logger.info("Database siap.")

    # Bangun aplikasi bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Daftarkan perintah
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("help",    help_cmd))
    app.add_handler(CommandHandler("tambah",  cmd_tambah))
    app.add_handler(CommandHandler("list",    cmd_list))
    app.add_handler(CommandHandler("selesai", cmd_selesai))
    app.add_handler(CommandHandler("hapus",   cmd_hapus))

    # Jadwalkan pengecekan reminder setiap 60 detik
    app.job_queue.run_repeating(cek_reminder, interval=60, first=10)

    logger.info("Bot berjalan... tekan Ctrl+C untuk berhenti.")
    app.run_polling()


if __name__ == "__main__":
    main()
