from pathlib import Path

from telegram import InputFile
from telegram.ext import ContextTypes


VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".webm",
    ".m4v",
}


def human_size(size: int) -> str:
    value = float(size)

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} PB"


async def upload_file(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    file_path: Path,
):
    """
    Upload a downloaded file to Telegram.
    """

    suffix = file_path.suffix.lower()
    file_size = file_path.stat().st_size

    caption = (
        f"📁 {file_path.name}\n\n"
        f"📦 {human_size(file_size)}"
    )

    with file_path.open("rb") as fp:

        telegram_file = InputFile(fp, filename=file_path.name)

        if suffix in VIDEO_EXTENSIONS:

            await context.bot.send_video(
                chat_id=chat_id,
                video=telegram_file,
                caption=caption,
                supports_streaming=True,
            )

        else:

            await context.bot.send_document(
                chat_id=chat_id,
                document=telegram_file,
                caption=caption,
          )
