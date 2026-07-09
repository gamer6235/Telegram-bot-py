import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from telegram import Update

from config import BOT_TOKEN
from handlers.message import handle_message


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("terabox-bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me any Terabox link.\n\n"
        "I'll download and upload files up to 1.5 GB.\n"
        "Larger files will be returned as a download button."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Just send a supported Terabox link.\n\n"
        "Supported domains:\n"
        "- terabox.com\n"
        "- terabox.app\n"
        "- 1024terabox.com\n"
        "- teraboxshare.com\n"
        "- teraboxlink.com\n"
        "- terasharefile.com\n"
        "- terafileshare.com\n"
        "- terasharelink.com"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    logger.info("Bot Started")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
