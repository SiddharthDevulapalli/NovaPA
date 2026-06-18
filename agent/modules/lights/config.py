import os
from dotenv import load_dotenv

load_dotenv()

KASA_EMAIL = os.getenv("KASA_EMAIL", "")
KASA_PASSWORD = os.getenv("KASA_PASSWORD", "")
KASA_CLOUD_URL = "https://wap.tplinkcloud.com"
TERMINAL_UUID = "personal-assistant-agent"
REQUEST_TIMEOUT = 10
