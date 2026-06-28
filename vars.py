from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", 34422904))
API_HASH = getenv("API_HASH", 7e0002469784f47fc08a6b3d93d7ebed)
BOT_TOKEN = getenv("BOT_TOKEN", 8638398538:AAGd0NJuGoMEGbY2Zx7d1RHF8z6gaZ5PVo4)
OWNER_ID = int(getenv("OWNER_ID", 5349573682))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5349573682").split()))

