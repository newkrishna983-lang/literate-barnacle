import os
import logging

logging.basicConfig(level=logging.INFO)

# ---- Environment Variables (डिफ़ॉल्ट मान आपके दिए गए) ----
API_ID = int(os.getenv("API_ID", 34422904))
API_HASH = os.getenv("API_HASH", "7e0002469784f47fc08a6b3d93d7ebed")
BOT_TOKEN = os.getenv("BOT_TOKEN", "863839853AAGd0NJg0MEGbY2Zx7d1RHF8z6gaZ5PVo4")
OWNER_ID = int(os.getenv("OWNER_ID", 5349573682))

# SUDO_USERS – स्पेस या कॉमा से अलग IDs
sudo_raw = os.getenv("SUDO_USERS", "5349573682")
SUDO_USERS = []
if sudo_raw:
    for part in sudo_raw.replace(",", " ").split():
        try:
            SUDO_USERS.append(int(part))
        except ValueError:
            pass

# Log कि सब ठीक है (लेकिन टोकन पूरा न दिखाएँ)
logging.info("✅ Environment variables loaded.")
logging.info(f"API_ID: {API_ID}")
logging.info(f"OWNER_ID: {OWNER_ID}")
logging.info(f"SUDO_USERS: {SUDO_USERS}")
