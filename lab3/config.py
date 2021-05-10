import ujson
import logging


logging.basicConfig(level=logging.INFO)

TOKEN = "1866001433:AAEBrJh0xKjxgrJWlA3wZ5N8aoSGtxmlNFk"
BOT_VERSION = 0.1
# База данных хранит выбранные юзером лиги
BOT_DB_NAME = "users_deadlines"
# Тестовые данные поддерживаемых лиг
BOT_DEADLINES = {
    "1": "ИСП лаб 1",
    "2": "МЧА лаб 1",
    "3": "ООП курсач",
}
# Флаги для сообщений, emoji-код
BOT_DEADLINES_FLAGS = {
    "1": ":grimacing:",
    "2": ":wink:",
    "3": ":rage:",
}

# Данные redis-клиента
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# По умолчанию пароля нет. Он будет на сервере
REDIS_PASSWORD = None
