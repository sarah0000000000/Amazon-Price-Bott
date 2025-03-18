import os
from dotenv import load_dotenv

load_dotenv()

SETTINGS = {
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_ASSOCIATE_TAG": os.getenv("AWS_ASSOCIATE_TAG"),
}

ROTATING_PROXY_LIST = [
    "http://proxy1:port",
    "http://proxy2:port",
    "http://proxy3:port",
]

DOWNLOAD_DELAY = 2  # 2 secondes entre les requêtes