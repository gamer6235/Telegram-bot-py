import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Please add it to the .env file.")

# Terabox Resolve API
RESOLVE_API = "https://terabox-api-ksit.onrender.com/api/resolve"

# Temporary download directory
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Maximum Telegram upload size (1.5 GB)
MAX_UPLOAD_SIZE = 1610612736

# Progress update interval (seconds)
PROGRESS_UPDATE_INTERVAL = 2

# HTTP timeouts (seconds)
CONNECT_TIMEOUT = 30
READ_TIMEOUT = 300

# Supported Terabox Domains
SUPPORTED_DOMAINS = (
    "terabox.com",
    "terabox.app",
    "1024terabox.com",
    "teraboxshare.com",
    "teraboxlink.com",
    "terasharefile.com",
    "terafileshare.com",
    "terasharelink.com",
    "teraboxapp.com",
    "nephobox.com",
    "4funbox.com",
    "mirrobox.com",
    "momerybox.com",
)
