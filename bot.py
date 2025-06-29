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
    ContextTypes
)

# ─── 1) Załaduj zmienne środowiskowe z .env ────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić zmienne środowiskowe BOT_TOKEN i CHAT_ID")
CHAT_ID = int(CHAT_ID)

# ─── 2) Konfiguracja logowania ──────────────────────────
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── 3) Handlery komend ─────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Użytkowniku"
    await update.message.reply_text(f"Cześć, {user}! Bot działa. 🟢")

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Tutaj display fuel data…")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 Najnowsze wiadomości…")

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Nasza oferta treningowa:\n"
        "– Indywidualny program motywacyjny\n"
        "– Wsparcie 24/7 przez ekspertów\n"
        "– Bonus: darmowa konsultacja onboardingowa\n"
        "\nWpisz /buy aby przejść do zakupu 💪"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Aby zakupić, wejdź na: https://twoja-firma.pl/kup")

# ─── 4) Funkcja wywoływana przez scheduler ──────────────
def scheduled_message():
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text="⏰ Przypomnienie: sprawdź naszą ofertę sprzedażową!"
    )

# ─── 5) Główna funkcja uruchamiająca aplikację ─────────
def main():
    # zbuduj aplikację
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # zarejestruj komendy
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("fuel",     fuel))
    app.add_handler(CommandHandler("news",     news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy",      buy))

    # uruchom scheduler (codziennie o 09:00)
    sched = BackgroundScheduler()
    sched.add_job(scheduled_message, "cron", hour=9, minute=0)
    sched.start()

    # uruchom polling
    app.run_polling()

if __name__ == "__main__":
    main()

