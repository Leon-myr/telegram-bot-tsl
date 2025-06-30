#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# 1️⃣ Załaduj .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić BOT_TOKEN i CHAT_ID w .env")
CHAT_ID = int(CHAT_ID)

# 2️⃣ Konfiguracja logowania
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# — Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Partnerze"
    text = (
        f"👋 Cześć, {name}!\n"
        "Jestem *Bon Assistant*, Twój wirtualny partner sprzedażowy.\n\n"
        "Dostępne komendy:\n"
        "• /fuel — analiza kosztów paliwa ⛽\n"
        "• /news — najnowsze wiadomości 📰\n"
        "• /training — oferta szkoleń 💼\n"
        "• /buy — przejdź do zakupu 🛒\n"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# — Handler /fuel
async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⛽ *Raport paliwowy*\n"
        "• Średni koszt paliwa: _6,12 PLN/l_\n"
        "• Trend: wzrost o 2% w ciągu tygodnia\n\n"
        "Porównaj ceny: https://twoja-firma.pl/fuel"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# — Handler /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📰 *Najnowsze wieści ze świata biznesu:*\n"
        "1. 🚚 Rynek TSL rośnie o 5% QoQ\n"
        "2. 📦 Nowe regulacje faktoringowe w UE\n"
        "3. 🤖 AI w logistyce: case study XYZ\n\n"
        "Pełne raporty: https://twoja-firma.pl/news"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# — Handler /training
async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💼 *Oferta szkoleń sprzedażowych:*\n"
        "– *SPIN Selling*: techniki skutecznego zamykania\n"
        "– *Negocjacje integracyjne*: budowanie relacji\n"
        "– *Obsługa klienta*: legendarna jakość wg K. Blancharda\n\n"
        "✅ *Korzyści*:\n"
        "   • +20% wskaźnik konwersji\n"
        "   • 30 dni wsparcia eksperckiego\n"
        "   • Certyfikat ukończenia\n\n"
        "👉 Wpisz /buy, aby odebrać kod rabatowy 10%!"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# — Handler /buy
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛒 *Gotowy na rozwój biznesu?*\n\n"
        "1. Wejdź: https://twoja-firma.pl/buy\n"
        "2. Kod rabatowy _BON10_\n"
        "3. Start już dziś!\n\n"
        "Masz pytania? support@twoja-firma.pl"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# 3️⃣ Funkcja schedulera (codziennie 09:00)
def scheduled_message():
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "⏰ *Dzienna dawka wiedzy*: nowe materiały i kod _BON10_ na szkolenia!"
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

# — Główna funkcja
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ▪️ Rejestracja Komend
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("fuel",     fuel))
    app.add_handler(CommandHandler("news",     news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy",      buy))

    # ▪️ Scheduler
    sched = BackgroundScheduler()
    sched.add_job(scheduled_message, "cron", hour=9, minute=0)
    sched.start()

    # ▪️ Start polling
    app.run_polling()

if __name__ == "__main__":
    main()

