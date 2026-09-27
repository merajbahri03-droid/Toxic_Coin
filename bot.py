import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")
if not WEB_APP_URL or not WEB_APP_URL.startswith("https://"):
    raise RuntimeError("WEB_APP_URL must be a public HTTPS URL.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(
        "🎮 Play",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )]]
    await update.message.reply_text(
        "🪙 Welcome to Tap Coins!\n\n"
        "Tap to earn in-game coins, upgrade your power, and climb the leaderboard.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
