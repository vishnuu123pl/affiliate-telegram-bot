import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "5250059606:AAHmu7ZfuXzOmvjS6SHoNcx8nER4-d4xUkY"

AMAZON_TAG = "fastdeals0ee-21"

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if "amazon" in text or "amzn.in" in text:

        if "?" in text:
            link = text + f"&tag={AMAZON_TAG}"
        else:
            link = text + f"?tag={AMAZON_TAG}"

        await update.message.reply_text(
            f"✅ Amazon Affiliate Link Created\n\n{link}"
        )

    else:
        await update.message.reply_text(
            "❌ Send an Amazon link."
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, convert)
)

print("Bot Running...")

app.run_polling()
