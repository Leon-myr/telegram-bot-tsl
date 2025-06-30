#!/usr/bin/env python3
import os, logging, pandas as pd
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- 1. ENV ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Ustaw BOT_TOKEN i CHAT_ID w ENV")
CHAT_ID = int(CHAT_ID)

# --- 2. Logging ---
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

# --- 3. Handlery ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Partnerze"
    msg = (
        f"👋 Cześć, {user}!\n"
        "*Bon Assistant* – Twój wirtualny partner sprzedażowy.\n\n"
        "Dostępne komendy:\n"
        "• /fuel — raport paliwowy ⛽\n"
        "• /news — wiadomości 📰\n"
        "• /training — szkolenia 💼\n"
        "• /buy — kup teraz 🛒\n"
        "• /analiza — analiza danych 🔍\n"
        "• /koszyk — twój koszyk 🛒\n"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⛽ *Raport paliwowy*\n"
        "• Średni koszt: _6,12 PLN/l_\n"
        "• Trend: +2% 🆙\n\n"
        "Porównaj: https://twoja-firma.pl/fuel"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 *Najnowsze z TSL:*\n"
        "1. 🚚 +5% QoQ\n"
        "2. 📦 Regulacje UE\n"
        "3. 🤖 AI w logistyce\n\n"
        "Pełne: https://twoja-firma.pl/news"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "💼 *Oferta szkoleń:*\n"
        "– SPIN Selling\n"
        "– Negocjacje\n"
        "– Obsługa klienta\n\n"
        "Wpisz /buy, by kupić!"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🛒 *Zamów teraz*\n"
        "1. Wejdź: https://twoja-firma.pl/buy\n"
        "2. Kod: _BON10_\n"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def analiza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Analiza w toku…", parse_mode=ParseMode.MARKDOWN)

async def koszyk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        df = pd.read_csv("basket.csv")
        lines = ["🛒 *Twój koszyk:*"]
        for _, r in df.iterrows():
            lines.append(f"– {r['item']}: {r['quantity']} szt.")
        text = "\n".join(lines)
    except Exception as e:
        text = f"⚠️ Błąd: {e}"
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# --- 4. Scheduler 09:00 ---
def scheduled_message():
    Bot(token=BOT_TOKEN).send_message(
        chat_id=CHAT_ID,
        text="⏰ *Daily Tip*: sprawdź nowe materiały!",
        parse_mode=ParseMode.MARKDOWN,
    )

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    for cmd, fn in [
        ("start", start), ("fuel", fuel), ("news", news),
        ("training", training), ("buy", buy),
        ("analiza", analiza), ("koszyk", koszyk),
    ]:
        app.add_handler(CommandHandler(cmd, fn))

    sched = BackgroundScheduler()
    sched.add_job(scheduled_message, "cron", hour=9, minute=0)
    sched.start()

    app.run_polling()

if __name__ == "__main__":
    main()

