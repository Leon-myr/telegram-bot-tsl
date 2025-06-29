import os
from docx import Document
from striprtf.striprtf import rtf_to_text
from telegram import Update
from telegram.ext import ContextTypes

# Ścieżki do plików w katalogu głównym:
RTF1 = "Sales 1.rtf"
RTF2 = "Sales 2.rtf"
DOCX = "Zagadnienia na egzamin dyplomowy - opracowanie.docx"

async def training_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1) RTF1
    with open(RTF1, encoding="utf-8", errors="ignore") as f:
        text1 = rtf_to_text(f.read())
    # 2) RTF2
    with open(RTF2, encoding="utf-8", errors="ignore") as f:
        text2 = rtf_to_text(f.read())
    # 3) DOCX
    doc = Document(DOCX)
    text3 = "\n".join(p.text for p in doc.paragraphs)

    # Wyślij obcięte fragmenty
    await update.message.reply_text("📄 *Sales 1:*\n" + text1[:500], parse_mode="Markdown")
    await update.message.reply_text("📄 *Sales 2:*\n" + text2[:500], parse_mode="Markdown")
    await update.message.reply_text("📄 *Zagadnienia:*\n" + text3[:500], parse_mode="Markdown")

