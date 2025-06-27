import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="🧠 Przypomnienie: Sprawdź swoich klientów!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć Chodakowski! 💼 Bot działa!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Harmonogram przypomnienia codziennie o 9:00
scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: app.create_task(send_reminder(ContextTypes.DEFAULT_TYPE())),
    trigger='cron',
    hour=9,
    minute=0
)
scheduler.start()

app.add_handler(CommandHandler("start", start))

print("✅ Bot uruchomiony – możesz pisać do niego na Telegramie.")
app.run_polling()