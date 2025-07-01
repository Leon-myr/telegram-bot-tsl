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
    cel = soup.select_one("td.cennik-table__cell.cennik-table__cell--value")
    if cel:
        return cel.get_text(strip=True)
    lbl = soup.find("td", string=lambda t: "Pb95" in t if t else False)
    if lbl and lbl.find_next_sibling("td"):
        return lbl.find_next_sibling("td").get_text(strip=True)
    return "brak danych"

SOURCES = {
    "Business Insider PL": ("https://businessinsider.com.pl/biznes", "article h3 a"),
    "TransInfo": ("https://transinfo.pl", ".td-module-thumb a"),
    "Logistyka.net.pl": ("https://www.logistyka.net.pl/aktualnosci", ".itemFullTitle a"),
    "BonaBanco": ("https://bonabanco.com", ".jeg_post_title a"),
}

def fetch_headlines(name):
    url, sel = SOURCES[name]
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for a in soup.select(sel)[:5]:
        t = a.get_text(strip=True)
        h = a.get("href")
        if h and t:
            if h.startswith("/"):
                h = requests.compat.urljoin(url, h)
            out.append((html.escape(t), h))
    return out

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Witaj! /help lista komend")

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start\n/help\n/fuel\n/news\n/buy\n/training\n/materials")

async def fuel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    price = fetch_fuel_price()
    await update.message.reply_text(f"⛽ Cena hurtowa paliwa: {price}")

async def news(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lines = ["📰 Najnowsze wiadomości TSL:"]
    for name in SOURCES:
        lines.append(f"\n{name}:")
        try:
            for t, l in fetch_headlines(name):
                lines.append(f"• {t}  |  {l}")
        except:
            lines.append("• błąd pobierania")
    await update.message.reply_text("\n".join(lines))

async def buy(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Przejdź do zakupu: https://bonabanco.com")

async def training(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    plan = [
        "1 Poznaj klienta",
        "2 Wywołaj potrzebę",
        "3 Rozwiej obiekcje",
        "4 Zaproponuj wartość",
        "5 Zamknij sprzedaż"
    ]
    await update.message.reply_text("\n".join(plan))

async def materials(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    folder = "sales_materials"
    for fn in os.listdir(folder):
        path = os.path.join(folder, fn)
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

