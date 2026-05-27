from telethon import TelegramClient, events
import requests
from urllib.parse import *

API_ID = 13305226
API_HASH = "8cde2475d6b0cb1162b89ebbac71a95d"

AMAZON_TAG = "fastdeals0ee-21"

SOURCE_CHANNELS = [
    -1003562125496
]

TARGET_CHANNEL = "@Fast_deals_online"

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

def make_affiliate(url):

    parsed = urlparse(url)

    query = parse_qs(parsed.query)

    query["tag"] = [AMAZON_TAG]

    return urlunparse(
        parsed._replace(
            query=urlencode(
                query,
                doseq=True
            )
        )
    )

client = TelegramClient(
    "affiliate_session",
    API_ID,
    API_HASH
)

@client.on(
    events.NewMessage(
        chats=SOURCE_CHANNELS
    )
)
async def handler(event):

    text = event.raw_text

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

                item = make_affiliate(
                    expanded
                )

                changed = True

        modified.append(item)

    if changed:

        final_msg = " ".join(modified)

        await client.send_message(
            TARGET_CHANNEL,
            final_msg,
            link_preview=False
        )

client.start()

print("Listening...")

client.run_until_disconnected()
