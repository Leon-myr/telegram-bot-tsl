#!/usr/bin/env python3
import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# —————————————————————————————————————————————
# 1. Załaduj .env i zmienne
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError(
        "❌ Musisz ustawić BOT_TOKEN i CHAT_ID w Railway Variables lub w .env"
    )
CHAT_ID = int(CHAT_ID)

# —————————————————————————————————————————————
# 2. Ustaw logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# —————————————————————————————————————————————
# 3. Definicje handlerów

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Cześć, {update.effective_user.first_name}! Bot działa. ✅"
    )

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # przykładowa odpowiedź
    await update.message.reply_text("Aktualne ceny paliw: …")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oto najnowsze wiadomości: …")

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Plan treningu na dziś: …")

# —————————————————————————————————————————————
# 4. Funkcja dla scheduler’a (przykład codziennego raportu)
async def daily_report():
    from telegram import Bot
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🕒 To jest Twój codzienny raport!"
    )

# —————————————————————————————————————————————
# 5. Budowa aplikacji i scheduler

async def main():
    # a) budowa bota
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    # b) rejestracja komend
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))

    # c) uruchom scheduler
    sched = AsyncIOScheduler()
    sched.add_job(
        daily_report,
        "cron", hour=8, minute=0,  # codziennie o 08:00
        id="daily_report"
    )
    sched.start()

    # d) start polling (tylko jeden raz, bez konfliktu)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

