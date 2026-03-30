import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    try:
        response = requests.post(GEMINI_URL, json=payload)
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = "Kuch error aa gaya, thodi der baad try karo!"
    
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot chal raha hai...")
    app.run_polling()
