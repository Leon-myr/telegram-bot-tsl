import os
import csv
from datetime import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ───────────  Ładowanie konfiguracji  ───────────
load_dotenv()  
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# ───────────  Basket ───────────
def load_basket(path="basket.csv"):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def summarize_basket(path="basket.csv"):
    data = load_basket(path)
    total_value = sum(int(item["value"]) for item in data)
    total_limit = sum(int(item["limit"]) for item in data if item["status"]=="active")
    avg_usage = (total_value/total_limit*100) if total_limit else 0
    return "\n".join([
        "=== Podsumowanie koszyka ===",
        f"Suma wartości: {total_value}",
        f"Średnie wykorzystanie limitu: {avg_usage:.2f}%",
    ])

# ───────────  Handlery komend  ───────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Witaj! Komendy:\n"
        "/basket – podsumowanie koszyka\n"
        "/training – plan treningowy\n"
        "/buy – link do zakupu\n"
    )

async def basket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(summarize_basket("basket.csv"))

async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Plan treningowy:\n"
        "1. Poniedziałek – SPIN Selling\n"
        "2. Wtorek – Obsługa obiekcji\n"
        "3. Środa – Negocjacje integracyjne\n"
        "4. Czwartek – Rezonansowe liderstwo\n"
        "5. Piątek – Podsumowanie tygodnia"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kup tutaj: https://bonabanco.com")

async def daily_report(context: ContextTypes.DEFAULT_TYPE):
    text = "📊 Dzienny raport:\n\n" + summarize_basket("basket.csv")
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

# ───────────  Główna ───────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("basket", basket))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("buy", buy))
    jq = app.job_queue
    jq.run_daily(daily_report, time(hour=7, minute=40))
    app.run_polling()

if __name__ == "__main__":
    main()

