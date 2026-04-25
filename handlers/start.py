from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama = update.effective_user.first_name
    teks = (
        f"👋 Halo, *{nama}*! Saya bot pengingat deadline tugas kamu.\n\n"
        "📋 *Perintah yang tersedia:*\n"
        "/tambah — Tambah tugas baru\n"
        "/list   — Lihat semua tugas aktif\n"
        "/selesai — Tandai tugas selesai\n"
        "/hapus  — Hapus tugas\n"
        "/help   — Bantuan lengkap\n"
    )
    await update.message.reply_text(teks, parse_mode="Markdown")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = (
        "📖 *Cara penggunaan:*\n\n"
        "*Tambah tugas:*\n"
        "`/tambah Nama Tugas | DD/MM/YYYY HH:MM | Mata Kuliah`\n"
        "Contoh:\n"
        "`/tambah UTS Aljabar | 25/12/2024 08:00 | Matematika`\n\n"
        "*Format tanpa jam* (default 23:59):\n"
        "`/tambah Laporan PKL | 30/12/2024`\n\n"
        "*Lihat tugas:*\n"
        "`/list`\n\n"
        "*Tandai selesai:*\n"
        "`/selesai <id>` — contoh: `/selesai 3`\n\n"
        "*Hapus tugas:*\n"
        "`/hapus <id>` — contoh: `/hapus 3`\n\n"
        "🔔 Bot akan otomatis mengingatkan H-1 hari dan H-1 jam sebelum deadline."
    )
    await update.message.reply_text(teks, parse_mode="Markdown")
