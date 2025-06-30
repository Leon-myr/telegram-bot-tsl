import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
from datetime import time

# Logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Cześć! Jestem Bon Assistant.\n\n"
        "Komendy:\n"
        "/fuel — analiza kosztów paliwa⛽\n"
        "/news — najnowsze wiadomości📰\n"
        "/training — oferta szkoleń🎓\n"
        "/buy — przejdź do zakupu🛒"
    )

# /fuel
async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛽ Średni koszt paliwa: 6,12 PLN/l\n"
        "Trend: +2% tydzień do tygodnia\n"
        "Porównaj: https://bonabanco.com/fuel"
    )

# /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://businessinsider.com.pl")
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("h2.entry-title a")[:3]
        text = "📰 Najnowsze TSL:\n" + "\n".join(
            f"• {a.get_text(strip=True)}\n  {a['href']}" for a in items
        )
    except Exception as e:
        logger.error("News fetch error: %s", e)
        text = "❌ Nie udało się pobrać wiadomości."
    await update.message.reply_text(text)

# /training
async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Oferta szkoleń TSL:\n"
        "– Program motywacyjny\n"
        "– Wsparcie 24/7\n"
        "– Darmowa konsultacja\n\n"
        "Wpisz /buy aby przejść do zakupu."
    )

# /buy
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 👉 https://bonabanco.com")

# Poranny raport o 09:00
async def morning_report(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=int(CHAT_ID),
        text="🌅 Dzień dobry! Twój poranny raport TSL."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Rejestracja komend
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy", buy))

    # JobQueue: codziennie o 09:00
    jq = app.job_queue
    jq.run_daily(morning_report, time(hour=9, minute=0))

    # Start
    app.run_polling()

if __name__ == "__main__":
    main()

