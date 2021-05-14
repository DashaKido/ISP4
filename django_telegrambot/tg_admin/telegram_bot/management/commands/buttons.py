from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from emoji import emojize

BUTTON1_HELP = f"{emojize(':memo:')} Помощь"
BUTTON2_COUNT = f"{emojize(':clipboard:')} Количество сообщений"
BUTTON3_TIMER = f"{emojize(':alarm_clock:')} Таймер"
BUTTON4_QUOTE = f"{emojize(':speech_balloon:')} Цитата"
BUTTON5_SETTINGS = f"{emojize(':tools:')} Настройки"

def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON3_TIMER),
            KeyboardButton(BUTTON4_QUOTE),
        ],
        [
            KeyboardButton(BUTTON2_COUNT),
            KeyboardButton(BUTTON1_HELP),
        ],
        [
            KeyboardButton(BUTTON5_SETTINGS),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
