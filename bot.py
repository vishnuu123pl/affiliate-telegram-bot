import os
import requests
from urllib.parse import *

from telegram import Update
from telegram.ext import *

BOT_TOKEN = os.getenv("BOT_TOKEN")
AMAZON_TAG = os.getenv("AMAZON_TAG")


def expand_url(url):
    try:
        r = requests.get(
            url,
            allow_redirects=True,
            timeout=10
        )
        return r.url
    except:
        return url


def make_affiliate(url, tag):

    if not tag:
        return url

    parsed = urlparse(url)

    query = parse_qs(parsed.query)

    remove_keys = [
        "tag",
        "linkCode",
        "linkId",
        "ref_",
        "ascsubtag"
    ]

    for k in remove_keys:
        query.pop(k, None)

    query["tag"] = [tag]

    return urlunparse(
        parsed._replace(
            query=urlencode(
                query,
                doseq=True
            )
        )
    )


async def convert(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # FIXED CRASH
    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text.strip()

    words = text.split()

    modified = []

    changed = False

    for item in words:

        if "http" in item:

            expanded = expand_url(item)

            if (
                "amazon." in expanded
                or "amzn." in expanded
            ):

                aff = make_affiliate(
                    expanded,
                    AMAZON_TAG
                )

                modified.append(aff)

                changed = True

            else:
                modified.append(item)

        else:
            modified.append(item)

    if changed:

        await update.message.reply_text(
            "✅ Converted\n\n" +
            " ".join(modified)
        )

    else:

        await update.message.reply_text(
            "❌ No supported link found."
        )


app = ApplicationBuilder().token(
    BOT_TOKEN
).build()

app.add_handler(
    MessageHandler(
        filters.ALL,
        convert
    )
)

print("Bot Running...")

app.run_polling()
        await update.message.reply_text(
            "❌ No supported link found."
        )

app = ApplicationBuilder().token(
    BOT_TOKEN
).build()

app.add_handler(
    MessageHandler(
        filters.TEXT,
        convert
    )
)

app.run_polling()
