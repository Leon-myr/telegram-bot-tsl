import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# -- HANDLERY --

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Użytkowniku"
    text = (
        f"👋 Cześć, {user}! Jestem Bon Assistant, Twój wirtualny partner sprzedażowy.\n\n"
        "Dostępne komendy:\n"
        "• /fuel — analiza kosztów paliwa ⛽\n"
        "• /news — najnowsze wiadomości 📰\n"
        "• /training — oferta szkoleń 💼\n"
        "• /buy — link do zakupu 🛒\n"
    )
    await update.message.reply_text(text)

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tu możesz podpiąć scrapowanie albo stałą odpowiedź
    await update.message.reply_text("⛽ Raport paliwowy:\n• Średni koszt: 6,12 PLN/l\n• Trend: +2% w tygodniu")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # tu możesz scrapować newsy
    await update.message.reply_text(
        "📰 Najnowsze z TSL:\n"
        "1. Rynek rośnie o 5% QoQ\n"
        "2. Nowe regulacje faktoringowe w UE\n"
        "3. AI w logistyce: case study XYZ"
    )

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💼 Nasza oferta szkoleniowa:\n"
        "– Indywidualny program motywacyjny\n"
        "– Wsparcie 24/7 przez ekspertów\n"
        "– Bonus: darmowa konsultacja onboardingowa"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👉 Przejdź do zakupu: https://bonabanco.com")

# -- START BOT’A --

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy", buy))

    app.run_polling()

if __name__ == "__main__":
    main()

