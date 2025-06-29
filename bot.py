#!/usr/bin/env python3
import os
import threading
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- 1) Załaduj .env -----------------------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić zmienne środowiskowe BOT_TOKEN i CHAT_ID")

# Chat ID jako int
CHAT_ID = int(CHAT_ID)

# --- 2) Inicjalizacja bota ----------------------------
bot = Bot(token=BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()

# --- 3) Handler /start --------------------------------
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "użytkowniku"
    await update.message.reply_text(f"Cześć, {name}! Bot działa. 🟢")

app.add_handler(CommandHandler("start", start_handler))

# --- 4) Job co godzinę --------------------------------
def hourly_job():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    bot.send_message(chat_id=CHAT_ID, text=f"⏰ Przypomnienie! Teraz jest {now}")

sched = BackgroundScheduler()
sched.add_job(hourly_job, "interval", hours=1)
sched.start()

# --- 5) Start bota (polling) --------------------------
if __name__ == "__main__":
    print("🔄 Uruchamiam bota i scheduler w tle...")
    app.run_polling()  # <- bez dodatkowych argumentów

