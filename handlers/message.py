from telegram import Update
from telegram.ext import ContextTypes

from config import SUPPORTED_DOMAINS
from services.resolver import resolve_link

import re


URL_PATTERN = re.compile(r"https?://[^\s]+")


def is_terabox_link(url: str) -> bool:
    url = url.lower()

    return any(domain in url for domain in SUPPORTED_DOMAINS)


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    text = update.message.text.strip()

    match = URL_PATTERN.search(text)

    if not match:
        await update.message.reply_text(
            "❌ Please send a valid Terabox link."
        )
        return

    url = match.group(0)

    if not is_terabox_link(url):
        await update.message.reply_text(
            "❌ Unsupported Terabox domain."
        )
        return

    status = await update.message.reply_text(
        "🔍 Resolving Terabox link..."
    )

    try:

        result = await resolve_link(url)

    except Exception as e:

        await status.edit_text(
            f"❌ {str(e)}"
        )

        return

    await status.edit_text(
        "✅ Link Resolved\n\n"
        f"📁 {result['filename']}"
    )

    # Downloader will be connected in the next step.
