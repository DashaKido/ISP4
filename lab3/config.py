import ujson
import logging


logging.basicConfig(level=logging.INFO)

TOKEN = "1866001433:AAEBrJh0xKjxgrJWlA3wZ5N8aoSGtxmlNFk"
BOT_VERSION = 0.2
# База данных хранит выбранные юзером дедлайны
BOT_DB_NAME = "users_deadlines"
# Тестовые данные поддерживаемых дедлайнов
BOT_DEADLINES = {
    "1": "ИСП",
    "2": "МЧА",
    "3": "ООП",
    "4": "Физика",
    "5": "Специально для Вани Стаселько)",
}
# Флаги для сообщений, emoji-код
BOT_DEADLINES_FLAGS = {
    "1": ":yellow_heart:",
    "2": ":green_heart:",
    "3": ":red_heart:",
    "4": ":blue_heart:",
    "5": ":blue_heart:",
}

# Данные redis-клиента
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# По умолчанию пароля нет. Он будет на сервере
REDIS_PASSWORD = None

MINUTE = 60
YEAR = 60*60*24*366

QUOTES_API_URL = "http://api.forismatic.com/api/1.0/"
