import os
import html
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_fuel_price():
    url = "https://www.orlen.pl/pl/dla-biznesu/hurtowe-ceny-paliw"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    cell = soup.select_one("td.cennik-table__cell--value")
    if cell:
        return cell.get_text(strip=True)
    return "brak danych"

NEWS_SOURCES = [
    ("Business Insider PL", "https://businessinsider.com.pl/biznes", "article h3 a"),
    ("TransInfo", "https://transinfo.pl", ".td-module-thumb a"),
    ("Logistyka.net.pl", "https://www.logistyka.net.pl/aktualnosci", ".itemFullTitle a"),
    ("BonaBanco", "https://bonabanco.com", ".jeg_post_title a"),
]

def fetch_headlines(name, url, selector):
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    headlines = []
    for a in soup.select(selector)[:5]:
        text = a.get_text(strip=True)
        href = a.get("href")
        if href and text:
            if href.startswith("/"):
                href = requests.compat.urljoin(url, href)
            headlines.append((html.escape(text), href))
    return headlines

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Witaj! Wyślij /help aby zobaczyć komendy")

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start\n/help\n/fuel\n/news\n/buy\n/training\n/materials")

async def fuel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    price = fetch_fuel_price()
    await update.message.reply_text(f"⛽ Cena hurtowa paliwa: {price}")

async def news(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    parts = ["📰 Najnowsze wiadomości TSL:"]
    for name, url, sel in NEWS_SOURCES:
        parts.append(f"\n<b>{name}</b>")
        try:
            for text, link in fetch_headlines(name, url, sel):
                parts.append(f'<a href="{link}">{text}</a>')
        except:
            parts.append("błąd pobierania")
    await update.message.reply_text("\n".join(parts), parse_mode="HTML", disable_web_page_preview=True)

async def buy(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Przejdź do zakupu: https://bonabanco.com")

async def training(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    plan = [
        "1. Poznaj klienta",
        "2. Wywołaj potrzebę",
        "3. Rozwiej obiekcje",
        "4. Zaproponuj wartość",
        "5. Zamknij sprzedaż",
    ]
    await update.message.reply_text("\n".join(plan))

async def materials(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    for fn in sorted(os.listdir("sales_materials")):
        path = os.path.join("sales_materials", fn)
        await ctx.bot.send_document(chat_id, open(path, "rb"))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("materials", materials))
    print("🚀 Bot wystartował")
    app.run_polling()

if __name__ == "__main__":
    main()

