from os import getenv
from dotenv import load_dotenv

load_dotenv()

# ---- अनिवार्य वेरिएबल्स (डिफ़ॉल्ट मान आपके दिए गए हैं) ----
API_ID = int(getenv("API_ID", "34422904"))
API_HASH = getenv("API_HASH", "7e0002469784f47fc08a6b3d93d7ebed")
BOT_TOKEN = getenv("BOT_TOKEN", "863839853AAGd0NJg0MEGbY2Zx7d1RHF8z6gaZ5PVo4")  # ✅ कोट्स लगाएँ

# ---- वैकल्पिक वेरिएबल्स ----
OWNER_ID = int(getenv("OWNER_ID", "5349573682"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5349573682").split()))
