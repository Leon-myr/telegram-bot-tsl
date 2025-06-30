#!/usr/bin/env python3
import os
import logging
import pandas as pd
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# 1️⃣ Załaduj zmienne z .env
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

# — Handlery komend —

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
        "• /analiza — analiza Twoich danych 🔍\n"
        "• /koszyk — podsumowanie koszyka 🛒\n"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⛽ *Raport paliwowy*\n"
        "• Średni koszt paliwa: _6,12 PLN/l_\n"
        "• Trend: wzrost o 2% w ciągu tygodnia\n\n"
        "Porównaj ceny: https://twoja-firma.pl/fuel"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📰 *Najnowsze wieści ze świata biznesu:*\n"
        "1. 🚚 Rynek TSL rośnie o 5% QoQ\n"
        "2. 📦 Nowe regulacje faktoringowe w UE\n"
        "3. 🤖 AI w logistyce: case study XYZ\n\n"
        "Pełne raporty: https://twoja-firma.pl/news"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💼 *Oferta szkoleń sprzedażowych:*\n"
        "– *SPIN Selling*: techniki skutecznego zamykania\n"
        "– *Negocjacje integracyjne*: budowanie relacji\n"
        "– *Obsługa klienta*: legendarna jakość wg Blancharda\n\n"
        "👉 Wpisz /buy, aby odebrać kod rabatowy 10%!"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛒 *Gotowy na rozwój biznesu?*\n\n"
        "1. Wejdź: https://twoja-firma.pl/buy\n"
        "2. Kod rabatowy: _BON10_\n"
        "3. Start już dziś!\n\n"
        "Masz pytania? support@twoja-firma.pl"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# 3️⃣ Nowe komendy:

async def analiza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Analiza Twoich danych jest w toku…\n"
        "Wkrótce dostaniesz kompleksowy raport!",
        parse_mode=ParseMode.MARKDOWN
    )

async def koszyk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        df = pd.read_csv("basket.csv")
        lines = ["🛒 *Twój koszyk:*"]
        for _, row in df.iterrows():
            lines.append(f"– {row['item']}: {row['quantity']} szt.")
        msg = "\n".join(lines)
    except Exception as e:
        msg = f"⚠️ Nie udało się wczytać koszyka: {e}"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# 4️⃣ Scheduler na 09:00 codziennie
def scheduled_message():
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "⏰ *Dzienna dawka wiedzy*: nowe materiały już czekają!\n"
            "Kod BON10 na szkolenia."
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Rejestracja handlers
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("fuel",     fuel))
    app.add_handler(CommandHandler("news",     news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy",      buy))
    app.add_handler(CommandHandler("analiza",  analiza))
    app.add_handler(CommandHandler("koszyk",   koszyk))

    # Scheduler
    sched = BackgroundScheduler()
    sched.add_job(scheduled_message, "cron", hour=9, minute=0, id="daily_know")
    sched.start()

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()

