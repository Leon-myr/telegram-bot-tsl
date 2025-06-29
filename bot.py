import os, asyncio
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = int(os.getenv("CHAT_ID"))

async def morning_message():
    now = datetime.now(pytz.timezone("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S")
    text = f"🚀 Dzień dobry Chodakowski!\nDzisiaj jest {now}\n– Przypomnienie o analizie klientów i rynku."
    await Bot(BOT_TOKEN).send_message(chat_id=CHAT_ID, text=text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć Chodakowski! Bot 24/7 🚀")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # 7:40 CET = 5:40 UTC
    sched = AsyncIOScheduler(timezone="Europe/Warsaw")
    sched.add_job(lambda: asyncio.create_task(morning_message()),
                  "cron", hour=7, minute=40)
    sched.start()

    print("✅ Bot + scheduler uruchomione")
    app.run_polling()

