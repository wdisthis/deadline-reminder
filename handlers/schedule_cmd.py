from telegram import Update
from telegram.ext import ContextTypes
from services.schedule import get_jadwal_msg
from datetime import datetime
from utils.helpers import TZ

async def cmd_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /jadwal."""
    now = datetime.now(TZ)
    hari_idx = now.weekday()
    
    pesan = get_jadwal_msg(hari_idx)
    await update.message.reply_text(pesan, parse_mode="Markdown")
