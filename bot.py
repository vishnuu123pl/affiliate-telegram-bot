import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from telegram import Update
from telegram.ext import *

BOT_TOKEN = os.getenv("BOT_TOKEN")
AMAZON_TAG = os.getenv("AMAZON_TAG")

def expand_url(url):
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return url

def make_affiliate(url, tag):

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    query["tag"] = [tag]

    return urlunparse(
        parsed._replace(
            query=urlencode(query, doseq=True)
        )
    )

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    urls = text.split()

    output = []

    for item in urls:

        if "http" in item:

            expanded = expand_url(item)

            if "amazon." in expanded or "amzn." in expanded:

                aff = make_affiliate(expanded, AMAZON_TAG)

                output.append(aff)

    if output:

        await update.message.reply_text(
            "✅ Amazon Affiliate Link Created\n\n" +
            "\n".join(output)
        )

    else:

        await update.message.reply_text(
            "❌ No supported link found."
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, convert)
)

app.run_polling()
