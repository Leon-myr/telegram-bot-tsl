import os
import html
import requests
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

def fetch_headlines(url, selector="h2.entry-title a"):
    r = requests.get(url, timeout=5); r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for a in soup.select(selector)[:5]:
        t = a.get_text(strip=True)
        h = a.get("href")
        if h and t:
            if h.startswith("/"):
                h = requests.compat.urljoin(url, h)
            out.append((html.escape(t), h))
    return out

def fetch_fuel_price():
    url = "https://www.orlen.pl/pl/dla-biznesu/hurtowe-ceny-paliw"
    r = requests.get(url, timeout=5); r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    cell = soup.select_one(".table__cell--value")
    return cell.get_text(strip=True) if cell else "–"

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Witaj! Oto komendy:\n"
        "/start      – to menu\n"
        "/help       – lista komend\n"
        "/fuel       – cena hurtowa paliwa\n"
        "/news       – najnowsze newsy TSL\n"
        "/buy        – link do zakupu\n"
        "/training   – plan treningowy sprzedażowy\n"
        "/materials  – Twoje materiały sprzedażowe\n"
    )
    await update.message.reply_text(text)

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n/help\n/fuel\n/news\n/buy\n/training\n/materials"
    )

async def fuel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    price = fetch_fuel_price()
    await update.message.reply_text(f"⛽ Hurtowa cena paliwa: {price}")

NEWS_SOURCES = {
    "Business Insider PL":   "https://businessinsider.com.pl/biznes",
    "TransInfo":             "https://transinfo.pl",
    "Logistyka.net.pl":      "https://www.logistyka.net.pl/aktualnosci",
    "BonaBanco (TSL news)":  "https://bonabanco.com",
}
async def news(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lines = ["📰 *Najnowsze wiadomości TSL:*"]
    for name, url in NEWS_SOURCES.items():
        lines.append(f"\n*{name}*")
        try:
            for t, l in fetch_headlines(url):
                lines.append(f"• [{t}]({l})")
        except:
            lines.append("❌ błąd pobierania")
    await update.message.reply_markdown_v2("\n".join(lines))

async def buy(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    btn = InlineKeyboardButton("Kup teraz", url="https://bonabanco.com")
    kb = InlineKeyboardMarkup([[btn]])
    await update.message.reply_text("Kliknij:", reply_markup=kb)

async def training(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    steps = [
        "1️⃣ Poznaj klienta",
        "2️⃣ Wywołaj potrzebę",
        "3️⃣ Rozwiej obiekcje",
        "4️⃣ Zaproponuj wartość",
        "5️⃣ Zamknij sprzedaż",
    ]
    await update.message.reply_text("\n".join(steps))

async def materials(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    for fn in os.listdir("sales_materials"):
        path = os.path.join("sales_materials", fn)
        await ctx.bot.send_document(chat_id, open(path, "rb"))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_cmd))
    app.add_handler(CommandHandler("fuel",  fuel))
    app.add_handler(CommandHandler("news",  news))
    app.add_handler(CommandHandler("buy",   buy))
    app.add_handler(CommandHandler("training", training))
    app.add_handler(CommandHandler("materials", materials))
    print("🚀 Bot wystartował")
    app.run_polling()

if __name__ == "__main__":
    main()

