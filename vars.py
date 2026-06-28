import os
import sys
import logging

# लॉगिंग सेट करें
logging.basicConfig(level=logging.INFO)

def get_required_env(key):
    """अनिवार्य एनवायरनमेंट वेरिएबल पढ़ें – न मिलने पर एरर दिखाएँ"""
    value = os.getenv(key)
    if value is None or value.strip() == "":
        logging.error(f"❌ REQUIRED environment variable '{key}' is missing!")
        sys.exit(1)
    return value

# ---- अनिवार्य वेरिएबल्स (Render पर सेट करें) ----
API_ID = int(get_required_env("34422904"))
API_HASH = get_required_env("7e0002469784f47fc08a6b3d93d7ebed")  # ✅ string
BOT_TOKEN = get_required_env("8638398538:AAGd0NJuGoMEGbY2Zx7d1RHF8z6gaZ5PVo4)  # ✅ string

# ---- वैकल्पिक वेरिएबल्स (डिफ़ॉल्ट के साथ) ----
OWNER_ID = int(os.getenv("OWNER_ID", "5349573682"))
SUDO_USERS_RAW = os.getenv("SUDO_USERS", "5349573682")
SUDO_USERS = []
if SUDO_USERS_RAW:
    for part in SUDO_USERS_RAW.replace(",", " ").split():
        try:
            SUDO_USERS.append(int(part))
        except ValueError:
            logging.warning(f"Ignoring invalid sudo ID: {part}")

logging.info("✅ Environment variables loaded successfully.")
logging.info(f"API_ID: {API_ID}")
logging.info(f"OWNER_ID: {OWNER_ID}")
