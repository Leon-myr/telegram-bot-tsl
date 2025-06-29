#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 1. Załaduj .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

# 2. Walidacja
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić zmienne BOT_TOKEN i CHAT_ID w bot_env/.env")

CHAT_ID = int(CHAT_ID)

# 3. Funkcje handlerów
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Cześć, {update.effective_user.first_name}! Bot działa. 🟢")

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tu Twój kod fetchujący ceny paliw
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Aktualne ceny paliw: ...")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tu Twój kod fetchujący newsy
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Najnowsze wiadomości: ...")

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tu Twój kod fetchujący trening
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Plan treningu: ...")

# 4. Scheduler – przykładowa funkcja wysyłająca przypomnienie
def scheduled_job():
    import telegram
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID,
                     text=f"📅 Przypomnienie: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 5. Budowa aplikacji
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # zarejestruj command handlery
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))

    # uruchom scheduler w tle
    sched = BackgroundScheduler()
    sched.add_job(scheduled_job, "interval", hours=1)  # co godzinę
    sched.start()

    # Start polling
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

