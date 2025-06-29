#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Załaduj zmienne
load_dotenv(dotenv_path="bot_env/.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić zmienne środowiskowe BOT_TOKEN i CHAT_ID")
CHAT_ID = int(CHAT_ID)

# 2. Import handlerów z modułów
from modules.fuel     import fuel_handler
from modules.news     import news_handler
from modules.training import training_handler

# 3. Definicja /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Witaj! Dostępne komendy:\n"
        "/fuel — ceny paliw\n"
        "/news — najnowsze wiadomości\n"
        "/training — materiały szkoleniowe"
    )

# 4. Zbuduj aplikację i zarejestruj komendy
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",    start_handler))
app.add_handler(CommandHandler("fuel",     fuel_handler))
app.add_handler(CommandHandler("news",     news_handler))
app.add_handler(CommandHandler("training", training_handler))

# 5. Scheduler (ASP Scheduler pod asyncio)
sched = AsyncIOScheduler()
# — przykład zadania codziennie o 08:00
sched.add_job(
    lambda: app.bot.send_message(chat_id=CHAT_ID, text="🌅 Dzienny raport gotowy!"),
    trigger="cron", hour=8, minute=0
)
sched.start()

# 6. Start bota
if __name__ == "__main__":
    print("🔄 Uruchamiam Bot + Scheduler...")
    app.run_polling()

