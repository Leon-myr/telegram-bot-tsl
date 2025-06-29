#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Załaduj zmienne z .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

# 2. Walidacja
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić zmienne środowiskowe BOT_TOKEN i CHAT_ID")

# Chat ID musi być liczbą
CHAT_ID = int(CHAT_ID)

# 3. Inicjalizacja bota
bot = Bot(token=BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 4. Przykładowy handler komendy /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "użytkowniku"
    await update.message.reply_text(f"Cześć, {user}! Bot jest uruchomiony. 🟢")

app.add_handler(CommandHandler("start", start_handler))

# 5. Inicjalizacja BlockingScheduler
sched = BlockingScheduler()

# 6. Przykładowe zadanie: co godzinę wysyłaj wiadomość
@sched.scheduled_job("interval", hours=1)
def hourly_reminder():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    bot.send_message(
        chat_id=CHAT_ID,
        text=f"⏰ Przypomnienie! Aktualny czas: {now}"
    )

if __name__ == "__main__":
    # 7. Uruchomienie bota pollingiem (w tle)
    #    + scheduler (blokuje wątek)
    print("🔄 Uruchamiam Bot + Scheduler...")
    app_task = app.run_polling(poll_interval=3.0, stop_signals=None, allowed_updates=None, clean=False)
    # 8. Start schedulera (blokuje program)
    sched.start()

