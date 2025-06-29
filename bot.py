import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cześć! Jestem Twoim osobistym asystentem sprzedaży 🚀")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
import asyncio
from datetime import datetime
from telegram import Bot

async def morning_message():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"🚀 Dzień dobry Chodakowski!\n"
        f"Dzisiaj jest {now}\n"
        f"- Przypominam o codziennej analizie klientów\n"
        f"- Za moment otrzymasz wiadomości z rynku i cenę paliwa\n\n"
        f"Działamy! 🔥"
    )
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Uruchom tylko jeśli skrypt wywoływany jest bezpośrednio (np. przez CRON)
if __name__ == "__main__":
    asyncio.run(morning_message())

