import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admins = [
    868136575, 641660459
]

ip = os.getenv("ip")
path_to_db = os.path.join('data', 'news_database.db')

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
