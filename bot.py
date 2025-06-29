#!/usr/bin/env python3
import os
import logging
import telegram
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ————— konfiguracja logowania —————
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ————— 1. Załaduj zmienne z .env —————
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

# ————— 2. Walidacja —————
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError(
        "❌ Musisz ustawić BOT_TOKEN i CHAT_ID w .env"
    )
CHAT_ID = int(CHAT_ID)

# ————— 3. Handlery komend —————
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "User"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Cześć, {user}! Bot działa. 🟢"
    )

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # przykład odpowiedzi
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⛽ Sprawdzam ceny paliw..."
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📰 Oto najnowsze wiadomości..."
    )

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🏋️ Rozpoczynam trening..."
    )

# ————— 4. (opcjonalnie) Funkcja schedulera —————
def scheduled_job():
    # wysyłka przypomnienia o ustalonej godzinie
    now = datetime.now().strftime("%H:%M")
    telegram.Bot(BOT_TOKEN).send_message(
        chat_id=CHAT_ID,
        text=f"⏰ Przypomnienie! Jest {now}."
    )

# ————— 5. Main: zbuduj aplikację, zarejestruj handlery i schedulera —————
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # rejestracja komend
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("fuel",     fuel))
    app.add_handler(CommandHandler("news",     news))
    app.add_handler(CommandHandler("training", training))

    # uruchom BackgroundScheduler
    scheduler = BackgroundScheduler()
    # np. codziennie o 9:00
    scheduler.add_job(scheduled_job, "cron", hour=9, minute=0)
    scheduler.start()
    logger.info("🔄 Scheduler uruchomiony w tle")

    # ————— 6. Start polling z obsługą konflików —————
    try:
        logger.info("🔄 Uruchamiam bota (run_polling)…")
        app.run_polling(poll_interval=3.0, stop_signals=None, allowed_updates=None)
    except telegram.error.Conflict:
        logger.warning("⚠️ Conflict: inny polling jest w toku – ignoruję.")

if __name__ == "__main__":
    main()

