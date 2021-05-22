from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from emoji import emojize

BUTTON1_HELP = f"Помощь 🆘"
BUTTON2_COUNT = f"Количество сообщений 🔢"
BUTTON3_TIMER = f"Таймер {emojize(':alarm_clock:')}"
BUTTON4_QUOTE = f"Цитата {emojize(':speech_balloon:')}"
BUTTON5_SETTINGS = f"Настройки {emojize(':wrench:')}"

TIMER_BUTTON1_EDIT = "timer_button1_edit"
TIMER_BUTTON2_SAVE = "timer_button2_save"
TIMER_BUTTON3_CANCEL = "timer_button3_cancel"
SETTINGS_BUTTON1_ADD = "settings_button1_add"
SETTINGS_BUTTON2_SHOW = "settings_button2_show"
SETTINGS_BUTTON3_OPEN = "settings_button4_OPEN"
SETTINGS_BUTTON4_CLOSE = "settings_button4_close"
SETTINGS_BUTTON5_BACK = "settings_button5_back"

TITLES = {
    TIMER_BUTTON1_EDIT: f"Выбрать {emojize(':pencil:')}",
    TIMER_BUTTON2_SAVE: "Сохранить ✅",
    TIMER_BUTTON3_CANCEL: "Отменить ❎",
    SETTINGS_BUTTON1_ADD: f"Добавить дедлайн 🔜",
    SETTINGS_BUTTON2_SHOW: f"Просмотр всех дедлайнов 🗒",
    SETTINGS_BUTTON3_OPEN: f"Текущие дедлайны 🔓",
    SETTINGS_BUTTON4_CLOSE: f"Закрытые дедлайны 🔒",
    SETTINGS_BUTTON5_BACK: f"Назад ⬅",

}


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


def get_base_inline_keyboard_timer():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[TIMER_BUTTON1_EDIT], callback_data=TIMER_BUTTON1_EDIT),
        ],
        [
            InlineKeyboardButton(TITLES[TIMER_BUTTON2_SAVE], callback_data=TIMER_BUTTON2_SAVE),
        ],
        [
            InlineKeyboardButton(TITLES[TIMER_BUTTON3_CANCEL], callback_data=TIMER_BUTTON3_CANCEL),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_keyboard_settings1():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[SETTINGS_BUTTON1_ADD], callback_data=SETTINGS_BUTTON1_ADD),
        ],
        [
            InlineKeyboardButton(TITLES[SETTINGS_BUTTON2_SHOW], callback_data=SETTINGS_BUTTON2_SHOW),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_keyboard_settings2():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[SETTINGS_BUTTON3_OPEN], callback_data=SETTINGS_BUTTON3_OPEN),
        ],
        [
            InlineKeyboardButton(TITLES[SETTINGS_BUTTON4_CLOSE], callback_data=SETTINGS_BUTTON4_CLOSE),
        ],
        [
            InlineKeyboardButton(TITLES[SETTINGS_BUTTON5_BACK], callback_data=SETTINGS_BUTTON5_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(update: Update, chat_data=None, **kwargs):
    """обработчик всех кнопок со всех клавиатур"""
    query = update.callback_query
    data = query.data
    if data == TIMER_BUTTON1_EDIT:
        query.edit_message_text(
            text='edit',
            reply_markup=get_base_inline_keyboard_timer(),
        )
    elif data == TIMER_BUTTON2_SAVE:
        query.edit_message_text(
            text='save',
            reply_markup=get_base_inline_keyboard_timer(),
        )
    elif data == TIMER_BUTTON3_CANCEL:
        query.edit_message_text(
            text='cancel',
            reply_markup=get_base_inline_keyboard_timer(),
        )
    elif data == SETTINGS_BUTTON1_ADD:
        query.edit_message_text(
            text='add',
            reply_markup=get_keyboard_settings1(),
        )
    elif data == SETTINGS_BUTTON2_SHOW:
        query.edit_message_text(
            text='Выберите действие:',
            reply_markup=get_keyboard_settings2(),
        )
    elif data == SETTINGS_BUTTON3_OPEN:
        query.edit_message_text(
            text='open',
            reply_markup=get_keyboard_settings2(),
        )
    elif data == SETTINGS_BUTTON4_CLOSE:
        query.edit_message_text(
            text='close',
            reply_markup=get_keyboard_settings2(),
        )
    elif data == SETTINGS_BUTTON5_BACK:
        query.edit_message_text(
            text='back',
            reply_markup=get_keyboard_settings1(),
        )
