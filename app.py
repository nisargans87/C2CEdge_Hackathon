import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to FakeBreak!\n\n"
        "🔎 I am an AI news verification bot.\n\n"
        "Send me:\n"
        "🖼️ A news image\n"
        "📝 A news claim\n"
        "🔗 A news URL\n\n"
        "I will analyze the information and help verify it."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.reply_text(
        "📝 I received your message!\n\n"
        f"You sent:\n{text}\n\n"
        "🔎 Verification engine coming next..."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🖼️ Image received!\n\n"
        "🔎 I will analyze this news image next.\n"
        "The verification engine is being connected."
    )


def main():

    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is missing from .env")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(filters.PHOTO, handle_photo)
    )

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    print("FakeBreak bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()