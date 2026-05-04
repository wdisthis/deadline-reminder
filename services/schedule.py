"""
Service untuk mengirimkan jadwal matkul harian secara rutin.
"""
import logging
from datetime import datetime
from telegram.ext import ContextTypes
from database.db import get_all_users
from utils.helpers import TZ

logger = logging.getLogger(__name__)

# Data Jadwal Matkul
JADWAL = {
    0: [ # Senin
        "09.20 – 11.50 : Metode Numerik (F303)",
        "13.00 – 14.40 : Praktikum PBF (LABKOM MAT)"
    ],
    1: [ # Selasa
        "07.30 - 09.10 : KWN (GK2-411)",
        "10.10 – 11.50 : Statistika Sains Data (F304)",
        "13.00 – 14.40 : Struktur Data (F007)",
        "16.30 - 18.00 : Praktikum Struktur Data (LABKOM MAT)"
    ],
    2: [ # Rabu
        "10.10 – 11.50 : Praktikum SSD (LABKOM 4)",
        "14.50 – 16.30 : Aljabar Strategi (F007)"
    ],
    3: [ # Kamis
        "07.30 – 09.10 : Basis Data (F310)",
        "13.00 – 14.40 : PBF (F214)"
    ],
    4: [ # Jumat
        "09.20 – 11.05 : Kewarganegaraan (GK2 411)",
        "14.50 – 16.30 : Praktikum Basis Data (LABKOM 4)"
    ]
}

NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

def get_jadwal_msg(hari_idx: int) -> str:
    """Mengembalikan teks jadwal berdasarkan index hari (0-6)."""
    if hari_idx not in JADWAL:
        return f"📭 Tidak ada jadwal kuliah untuk hari *{NAMA_HARI[hari_idx]}*."

    daftar_matkul = JADWAL[hari_idx]
    pesan = f"📅 *JADWAL MATKUL HARI INI ({NAMA_HARI[hari_idx]})*\n\n"
    pesan += "\n".join([f"🔹 {m}" for m in daftar_matkul])
    return pesan

async def kirim_jadwal_harian(context: ContextTypes.DEFAULT_TYPE):
    """Job rutin (opsional) untuk mengirim jadwal matkul."""
    now = datetime.now(TZ)
    hari_idx = now.weekday()
    
    pesan = get_jadwal_msg(hari_idx)
    if "Tidak ada jadwal" in pesan:
        logger.info(f"Skip kirim: {pesan}")
        return

    users = get_all_users()
    if not users:
        return

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=pesan, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Gagal kirim jadwal ke {user_id}: {e}")
