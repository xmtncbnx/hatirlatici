import asyncio
import schedule
import time
import threading
from datetime import datetime
import pytz
from telegram import Bot
from config import BOT_TOKEN, CHAT_ID

bot = Bot(token=BOT_TOKEN)
TZ  = pytz.timezone("Europe/Istanbul")

# ─────────────────────────────────────────
# MESAJ GÖNDERME
# ─────────────────────────────────────────
def send(msg: str):
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="HTML"))

# ─────────────────────────────────────────
# SINAV HATIRLATICILARI  (tek seferlik)
# ─────────────────────────────────────────
EXAMS = [
    # (tarih_str,        saat,    ders,                                    salon)
    ("2026-05-11", "20:00", "Finansal Yönetim (YBS208)",              "M1"),
    ("2026-05-12", "11:15", "Finansal Yönetim (YBS208)",              "M1"),

    ("2026-05-13", "20:00", "Bilişim Hukuku ve Etiği (YBS462)",       "D13"),
    ("2026-05-14", "11:15", "Bilişim Hukuku ve Etiği (YBS462)",       "D13"),
    ("2026-05-14", "15:00", "Kurumsal Kaynak Planlaması (YBS304)",    "M1"),

    ("2026-05-14", "20:00", "Güvenlik Mimarisi Tasarımı (YBS302)",    "D1"),
    ("2026-05-15", "14:00", "Güvenlik Mimarisi Tasarımı (YBS302)",    "D1"),

    ("2026-05-20", "20:00", "Süreç Yönetimi ve Dijital Dönüşüm (YBS312)", "D4/D5/D7"),
    ("2026-05-21", "17:00", "Süreç Yönetimi ve Dijital Dönüşüm (YBS312)", "D4/D5/D7"),

    ("2026-05-21", "20:00", "Mesleki Etik (YBS140)",                  "M3/M4"),
    ("2026-05-22", "11:15", "Mesleki Etik (YBS140)",                  "M3/M4"),
]

def check_exam_reminders():
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    for tarih, saat, ders, salon in EXAMS:
        hedef = f"{tarih} {saat}"
        if now == hedef:
            send(
                f"📚 <b>SINAV HATIRLATICI</b>\n\n"
                f"📖 <b>{ders}</b>\n"
                f"🕐 {tarih} — {saat[:2]}:{saat[3:]}\n"
                f"📍 Salon: {salon}"
            )

# ─────────────────────────────────────────
# PROTOKOL HATIRLATICILARI (tekrarlayan)
# ─────────────────────────────────────────
def sabah_takviye():
    send(
        "🌅 <b>SABAH TAKVİYELERİ</b>\n\n"
        "✅ Omega-3 — 2g\n"
        "✅ Kreatin — 5g\n\n"
        "💪 Günaydın!"
    )

def l_theanine():
    send(
        "⚡ <b>TAKVİYE ZAMANI</b>\n\n"
        "✅ L-Theanine — 200mg\n"
        "✅ Kafein — 100mg"
    )

def zma():
    send(
        "🌙 <b>GECE TAKVİYESİ</b>\n\n"
        "✅ ZMA — al ve uyu!\n"
        "😴 İyi geceler."
    )

def testosteron():
    now = datetime.now(TZ)
    if now.weekday() == 2:  # 2 = Çarşamba
        send(
            "💉 <b>TESTOSTERON GÜNÜ</b>\n\n"
            "🧬 Testosteron Enanthate — 200mg\n"
            "📅 Haftalık doz — Çarşamba"
        )

def sabah_kos():
    send(
        "🏃 <b>SABAH KOŞUSU</b>\n\n"
        "⏱ Hedef: 20–30 dakika\n"
        "Haydi çık dışarı! 🌤"
    )

# ─────────────────────────────────────────
# SCHEDULE KURULUMU
# ─────────────────────────────────────────
def setup_schedule():
    # Protokol
    schedule.every().day.at("08:00").do(sabah_takviye)
    schedule.every().day.at("07:30").do(sabah_kos)
    schedule.every().day.at("09:30").do(l_theanine)
    schedule.every().day.at("22:00").do(zma)
    schedule.every().wednesday.at("09:00").do(testosteron)

    # Sınav kontrolü — her dakika çalışır
    schedule.every(1).minutes.do(check_exam_reminders)

# ─────────────────────────────────────────
# ANA DÖNGÜ
# ─────────────────────────────────────────
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    print("✅ Bot başlatıldı...")
    send("🤖 <b>Reminder Bot aktif!</b>\nSınav ve protokol hatırlatıcıları çalışıyor.")
    setup_schedule()
    run_schedule()