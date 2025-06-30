import os
import logging
from dotenv import load_dotenv
from telegram import __version__ as TG_VER, Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- LOGOWANIE ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Wczytaj .env ---
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# --- HANDLERY ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "👋 Cześć!\n"
        "Jestem Bon Assistant, Twój wirtualny partner sprzedażowy.\n\n"
        "Dostępne komendy:\n"
        "• /fuel — analiza kosztów paliwa\n"
        "• /news — najnowsze wiadomości TSL\n"
        "• /training — oferta szkoleń\n"
        "• /buy — przejdź do zakupu\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # przykładowe statyczne dane; tu możesz podpiąć CSV lub API
    txt = (
        "⛽ Raport paliwowy:\n"
        "• Średni koszt paliwa: 6,12 PLN/l\n"
        "• Trend: wzrost o 2% w ciągu tygodnia\n"
        "\nPorównaj ceny: https://bonabanco.com/fuel"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # przykładowe skrobanie Business Insider TSL
    try:
        resp = requests.get("https://businessinsider.com.pl")
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("h2.entry-title a")[:3]
        lines = ["📰 Najnowsze wiadomości TSL:"]
        for a in items:
            lines.append(f"• {a.get_text().strip()} — {a['href']}")
        msg = "\n".join(lines)
    except Exception as e:
        logger.error("Błąd podczas fetchowania newsów: %s", e)
        msg = "❌ Nie udało się pobrać aktualności."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "🎓 Oferta szkoleń TSL:\n"
        "– Indywidualny program motywacyjny\n"
        "– Wsparcie 24/7 przez ekspertów\n"
        "– Bonus: darmowa konsultacja onboardingowa\n\n"
        "Wpisz /buy aby przejść do zakupu 💪"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "🛒 Aby kupić, wejdź na: https://bonabanco.com"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)

# --- RUN SCHEDULERA (przykład: codziennie 9:00 wysyłka do CHAT_ID) ---
def schedule_jobs(app):
    sched = AsyncIOScheduler()
    async def daily_report():
        await app.bot.send_message(chat_id=CHAT_ID, text="🌅 Dobry poranek! Raport TSL:")
    sched.add_job(daily_report, "cron", hour=9, minute=0)
    sched.start()
    logger.info("Scheduler uruchomiony")

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # rejestracja handlerów
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy", buy))

    # uruchom scheduler
    schedule_jobs(app)

    # start
    await app.initialize()
    await app.start()
    logger.info("Bot wystartował")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

