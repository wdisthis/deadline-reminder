from datetime import datetime
import pytz
from config import TIMEZONE

TZ = pytz.timezone(TIMEZONE)


def now_local() -> datetime:
    return datetime.now(TZ)


def parse_deadline(teks: str) -> datetime | None:
    """
    Terima format:
      - DD/MM/YYYY HH:MM  → '25/12/2024 23:59'
      - DD/MM/YYYY        → '25/12/2024'  (default jam 23:59)
    Kembalikan datetime tz-aware, atau None jika format salah.
    """
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(teks.strip(), fmt)
            if fmt == "%d/%m/%Y":
                dt = dt.replace(hour=23, minute=59)
            return TZ.localize(dt)
        except ValueError:
            continue
    return None


def format_deadline(deadline_str: str) -> str:
    """Ubah 'YYYY-MM-DD HH:MM' (format DB) ke tampilan ramah."""
    try:
        dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        dt = TZ.localize(dt)
        selisih = dt - now_local()
        total_jam = selisih.total_seconds() / 3600

        if total_jam < 0:
            sisa = "⚠️ SUDAH LEWAT"
        elif total_jam < 1:
            menit = int(selisih.total_seconds() / 60)
            sisa = f"⏰ {menit} menit lagi"
        elif total_jam < 24:
            sisa = f"🔴 {int(total_jam)} jam lagi"
        elif total_jam < 48:
            sisa = f"🟠 besok ({int(total_jam)} jam lagi)"
        else:
            hari = int(total_jam / 24)
            sisa = f"🟢 {hari} hari lagi"

        return f"{dt.strftime('%d/%m/%Y %H:%M')} — {sisa}"
    except Exception:
        return deadline_str


def deadline_to_db(dt: datetime) -> str:
    """Konversi datetime ke format penyimpanan DB."""
    return dt.strftime("%Y-%m-%d %H:%M")
