"""
Scheduler yang berjalan setiap menit untuk mengecek deadline
dan mengirimkan notifikasi otomatis H-1 hari & H-1 jam.
"""
import logging
from datetime import datetime
from telegram.ext import ContextTypes
from database.db import get_tugas_belum_notif, tandai_notif
from utils.helpers import TZ, format_deadline

logger = logging.getLogger(__name__)


async def cek_reminder(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(TZ)

    for level, jam_sebelum, label in [
        ("1d", 24, "1 hari"),
        ("1h", 1,  "1 jam"),
    ]:
        tasks = get_tugas_belum_notif(level)
        for t in tasks:
            try:
                deadline = TZ.localize(datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M"))
                selisih_jam = (deadline - now).total_seconds() / 3600

                # Notif ketika masuk window waktu yang sesuai
                if 0 < selisih_jam <= jam_sebelum:
                    mk = f" ({t['mata_kuliah']})" if t["mata_kuliah"] else ""
                    pesan = (
                        f"⏰ *PENGINGAT DEADLINE!*\n\n"
                        f"📌 *{t['nama_tugas']}*{mk}\n"
                        f"🗓 Deadline: {format_deadline(t['deadline'])}\n\n"
                        f"‼️ Tersisa kurang dari *{label}* lagi!\n"
                        f"Gunakan `/selesai {t['id']}` jika sudah selesai."
                    )
                    await context.bot.send_message(
                        chat_id=t["user_id"],
                        text=pesan,
                        parse_mode="Markdown",
                    )
                    tandai_notif(t["id"], level)
                    logger.info(f"Notif {level} terkirim → user {t['user_id']}, task {t['id']}")

            except Exception as e:
                logger.error(f"Gagal kirim notif task {t['id']}: {e}")
