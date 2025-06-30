import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import requests
from bs4 import BeautifulSoup
from datetime import time

# ——— LOGOWANIE ———
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ——— Wczytaj .env ———
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# ——— HANDLERY ———

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Cześć, jestem Bon Assistant — Twój wirtualny partner sprzedażowy.\n\n"
        "Dostępne komendy:\n"
        "• /fuel — analiza kosztów paliwa\n"
        "• /news — najnowsze wiadomości TSL\n"
        "• /training — oferta szkoleń\n"
        "• /buy — przejdź do zakupu\n"
    )

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛽ Raport paliwowy:\n"
        "• Średni koszt paliwa: 6,12 PLN/l\n"
        "• Trend: wzrost o 2% w ciągu tygodnia\n\n"
        "Porównaj ceny: https://bonabanco.com/fuel"
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://businessinsider.com.pl")
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("h2.entry-title a")[:3]
        lines = ["📰 Najnowsze wiadomości TSL:"]
        for a in items:
            title = a.get_text(strip=True)
            href = a["href"]
            lines.append(f"• {title}\n  {href}")
        text = "\n".join(lines)
    except Exception as e:
        logger.error("Błąd pobierania news: %s", e)
        text = "❌ Nie udało się pobrać wiadomości."
    await update.message.reply_text(text)

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Oferta szkoleń TSL:\n"
        "– Indywidualny program motywacyjny\n"
        "– Wsparcie 24/7 przez ekspertów\n"
        "– Bonus: darmowa konsultacja onboardingowa\n\n"
        "Wpisz /buy aby przejść do zakupu 💪"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Zakup: https://bonabanco.com")

# ——— RAPORT RANO ———

async def morning_report(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="🌅 Dobry poranek! Oto Twój codzienny raport TSL.",
    )

# ——— MAIN ———

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # rejestracja komend
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy", buy))

    # ustawienie JobQueue dla codziennego raportu o 09:00
    jq = app.job_queue
    jq.run_daily(morning_report, time(hour=9, minute=0))

    # uruchamiamy polling
    app.run_polling()

if __name__ == "__main__":
    main()

