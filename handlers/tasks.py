from telegram import Update
from telegram.ext import ContextTypes
from database.db import tambah_tugas, list_tugas, selesaikan_tugas, hapus_tugas
from utils.helpers import parse_deadline, format_deadline, deadline_to_db


async def cmd_tambah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = " ".join(context.args).strip()

    if not args:
        await update.message.reply_text(
            "❌ Format salah!\n"
            "Gunakan: `/tambah Nama Tugas | DD/MM/YYYY HH:MM | Mata Kuliah`\n"
            "Mata kuliah boleh dikosongkan.",
            parse_mode="Markdown",
        )
        return

    bagian = [b.strip() for b in args.split("|")]
    if len(bagian) < 2:
        await update.message.reply_text(
            "❌ Pisahkan nama tugas dan deadline dengan `|`\n"
            "Contoh: `/tambah UTS | 25/12/2024 08:00`",
            parse_mode="Markdown",
        )
        return

    nama_tugas   = bagian[0]
    deadline_raw = bagian[1]
    mata_kuliah  = bagian[2] if len(bagian) >= 3 else None

    dt = parse_deadline(deadline_raw)
    if dt is None:
        await update.message.reply_text(
            "❌ Format tanggal tidak dikenali.\n"
            "Gunakan `DD/MM/YYYY HH:MM` atau `DD/MM/YYYY`.",
            parse_mode="Markdown",
        )
        return

    task_id = tambah_tugas(user_id, nama_tugas, deadline_to_db(dt), mata_kuliah)
    mk_info = f" ({mata_kuliah})" if mata_kuliah else ""

    await update.message.reply_text(
        f"✅ Tugas berhasil ditambahkan!\n\n"
        f"📌 *{nama_tugas}*{mk_info}\n"
        f"🗓 Deadline: {format_deadline(deadline_to_db(dt))}\n"
        f"🆔 ID tugas: `{task_id}`",
        parse_mode="Markdown",
    )


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tugas_list = list_tugas(user_id)

    if not tugas_list:
        await update.message.reply_text("🎉 Tidak ada tugas aktif. Santai dulu!")
        return

    baris = ["📋 *Daftar Tugas Aktif:*\n"]
    for t in tugas_list:
        mk = f" _{t['mata_kuliah']}_" if t["mata_kuliah"] else ""
        baris.append(
            f"*[{t['id']}]* {t['nama_tugas']}{mk}\n"
            f"      📅 {format_deadline(t['deadline'])}\n"
        )

    await update.message.reply_text("\n".join(baris), parse_mode="Markdown")


async def cmd_selesai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "❌ Gunakan: `/selesai <id>`\nContoh: `/selesai 3`",
            parse_mode="Markdown",
        )
        return

    task_id = int(context.args[0])
    ok = selesaikan_tugas(task_id, user_id)

    if ok:
        await update.message.reply_text(f"✅ Tugas ID `{task_id}` ditandai selesai! 🎉", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Tugas ID `{task_id}` tidak ditemukan.", parse_mode="Markdown")


async def cmd_hapus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "❌ Gunakan: `/hapus <id>`\nContoh: `/hapus 3`",
            parse_mode="Markdown",
        )
        return

    task_id = int(context.args[0])
    ok = hapus_tugas(task_id, user_id)

    if ok:
        await update.message.reply_text(f"🗑 Tugas ID `{task_id}` berhasil dihapus.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Tugas ID `{task_id}` tidak ditemukan.", parse_mode="Markdown")
