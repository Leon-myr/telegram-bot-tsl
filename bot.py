#!/usr/bin/env python3
import os
import logging
import time
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from telegram.error import Conflict
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Update
)

# ————— Logger —————
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ————— 1. Load .env —————
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Ustaw BOT_TOKEN i CHAT_ID w .env")
CHAT_ID = int(CHAT_ID)

# ————— 2. Handlery —————
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "użytkowniku"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Cześć, {user}! Bot działa. 🟢"
    )

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# ————— 3. Scheduler job —————
def scheduled_job():
    now = datetime.now().strftime("%H:%M")
    Bot(BOT_TOKEN).send_message(
        chat_id=CHAT_ID,
        text=f"⏰ Przypomnienie! Jest {now}."
    )

# ————— 4. Main —————
def main():
    # zbuduj aplikację
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # **Usuń ewentualne webhooks** (by nie miksować trybów)
    try:
        app.bot.delete_webhook(drop_pending_updates=True)
        logger.info("🗑️ Webhook usunięty")
    except Exception:
        logger.debug("🔇 Nie udało się usunąć webhook (być może nie było)")

    # zarejestruj komendy
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("fuel",     fuel))
    app.add_handler(CommandHandler("news",     news))
    app.add_handler(CommandHandler("training", training))

    # uruchom scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, "cron", hour=9, minute=0)
    scheduler.start()
    logger.info("🔄 Scheduler uruchomiony w tle")

    # uruchom polling w pętli, obsłuż Conflict
    while True:
        try:
            logger.info("🔄 Start polling (drop_pending_updates=True)…")
            app.run_polling(
                poll_interval=3.0,
                drop_pending_updates=True
            )
            break  # zakończ, jeśli run_polling zwróci normalnie
        except Conflict:
            logger.warning("⚠️ Conflict: inny getUpdates w toku, czekam 5s i retry…")
            time.sleep(5)
        except Exception as e:
            logger.error(f"❌ Nieoczekiwany błąd: {e}, wychodzę.")
            break

if __name__ == "__main__":
    main()

