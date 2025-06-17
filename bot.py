from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Twój chat_id jako zmienna środowiskowa

# 🔔 Funkcja do przypomnienia
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    message = "🧠 Przypomnienie: Sprawdź nowych klientów lub zaległe działania!"
    await context.bot.send_message(chat_id=CHAT_ID, text=message)

# 🟢 Funkcja reagująca na /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć Chodakowski! 💼 Twój bot działa!")

# 🔧 Konfiguracja bota
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 🔁 Harmonogram codziennego przypomnienia o 9:00
scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: app.create_task(send_reminder(ContextTypes.DEFAULT_TYPE())),
    trigger='cron',
    hour=9,
    minute=0
)
scheduler.start()

# ➕ Komendy
app.add_handler(CommandHandler("start", start))

print("✅ Bot uruchomiony – możesz pisać do niego na Telegramie.")
app.run_polling()



