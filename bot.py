#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# 1. Załaduj zmienne z .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić BOT_TOKEN i CHAT_ID w .env")
CHAT_ID = int(CHAT_ID)

# 2. Konfiguracja logowania
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 3. Definicja handlerów
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "tam"
    await update.message.reply_text(f"Cześć, {user}! Bot działa. 🟢")

async def fuel(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Tutaj display fuel data…")

async def news(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 Najnowsze wiadomości…")

async def training(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏋️ Plan treningowy…")

# 4. Funkcja główna (synchroniczna)
def main():
    # zbuduj aplikację
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # zarejestruj komendy
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel",  fuel))
    app.add_handler(CommandHandler("news",  news))
    app.add_handler(CommandHandler("training", training))

    # ustaw scheduler
    sched = BackgroundScheduler()
    def daily_job():
        Bot(BOT_TOKEN).send_message(
            chat_id=CHAT_ID,
            text=f"🔔 Przypomnienie dnia: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    sched.add_job(daily_job, "cron", hour=8, minute=0)
    sched.start()

    # uruchom polling
    try:
        logger.info("🔄 Uruchamiam bota (polling)...")
        app.run_polling()
    except Exception as e:
        if "Conflict" in str(e):
            logger.warning("⚠ Konflikt getUpdates – retry")
            app.run_polling()
        else:
            raise

# 5. Entry point
if __name__ == "__main__":
    main()

