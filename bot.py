#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 1. Załaduj .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Musisz ustawić BOT_TOKEN i CHAT_ID w zmiennych środowiskowych!")

# 2. Parsuj CHAT_ID
CHAT_ID = int(CHAT_ID)

# 3. Import command handlerów
from modules.fuel    import fuel_handler
from modules.news    import news_handler
from modules.training import training_handler

# 4. Definicja /start
async def start_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Cześć, {update.effective_user.first_name}! Bot działa. 🟢"
    )

# 5. Fallback na nieznane komendy
async def unknown_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nie znam tej komendy.")

# 6. Budujemy aplikację
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",    start_handler))
app.add_handler(CommandHandler("fuel",     fuel_handler))
app.add_handler(CommandHandler("news",     news_handler))
app.add_handler(CommandHandler("training", training_handler))
app.add_handler(CommandHandler(None,       unknown_handler))

# 7. Scheduler (jeśli potrzebny)
scheduler = AsyncIOScheduler()
scheduler.start()

print("🔄 Uruchamiam bota i scheduler…")
app.run_polling()

