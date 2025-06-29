#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ——— 1. Załaduj .env i weź token/chat_id —————————————
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić BOT_TOKEN i CHAT_ID w .env")

CHAT_ID = int(CHAT_ID)

# ——— 2. Logger ——————————————————————————————————————
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ——— 3. Handlery komend ————————————————————————————
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "tam"
    await update.message.reply_text(f"Cześć, {user}! Bot działa. 🟢")

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tutaj Twoja logika
    await update.message.reply_text("Fuel – tu wprowadź swoją logikę.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("News – tu wprowadź swoją logikę.")

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Training – tu wprowadź swoją logikę.")

# ——— 4. Obsługa konfliktu getUpdates ———————————————
# Telegram wyrzuca Conflict, gdy działają dwa pollery na raz.
# Otoczmy run_polling() blokiem try/except, by kontener się nie wyłączył.

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Rejestracja komend
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel",  fuel))
    app.add_handler(CommandHandler("news",  news))
    app.add_handler(CommandHandler("training", training))

    # Scheduler (przykład – odpala co dzień o 8:00)
    sched = BackgroundScheduler()
    def daily_job():
        bot = Bot(BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=f"Przypomnienie: {datetime.now()}")
    sched.add_job(daily_job, "cron", hour=8, minute=0)
    sched.start()

    # Uruchamiamy polling, łapiemy Conflict, ale nie przerywamy
    try:
        logger.info("🔄 Uruchamiam bota (polling)...")
        await app.run_polling()
    except Exception as e:
        if "Conflict" in str(e):
            logger.warning("⚠ Konflikt getUpdates, ignoruję i kontynuuję.")
            await app.run_polling()
        else:
            raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

