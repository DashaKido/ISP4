from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from config import BOT_DEADLINES, BOT_DEADLINES_FLAGS, MINUTE
from database import cache, database as db
from app.dialogs import msg


MAIN_KB = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).row(
    KeyboardButton(msg.btn_online),
    KeyboardButton(msg.btn_config)
)

CONFIG_KB = InlineKeyboardMarkup().row(
    InlineKeyboardButton(msg.btn_back, callback_data='main_window'),
    InlineKeyboardButton(msg.config_btn_edit, callback_data='edit_config#')
).add(InlineKeyboardButton(msg.config_btn_delete, callback_data='delete_config'))


def deadlines_kb(active_deadlines: list, offset: int = 0):
    kb = InlineKeyboardMarkup()
    deadline_keys = list(BOT_DEADLINES.keys())[0+offset:5+offset]
    for dl_id in deadline_keys:
        if dl_id in active_deadlines:
            kb.add(InlineKeyboardButton(
                f"{emojize(':white_heavy_check_mark:')} {BOT_DEADLINES[dl_id]}",
                callback_data=f'del_deadline_#{offset}#{dl_id}'
            ))
        else:
            kb.add(InlineKeyboardButton(
                BOT_DEADLINES[dl_id],
                callback_data=f'add_deadline_#{offset}#{dl_id}'
            ))
    kb.row(
        InlineKeyboardButton(
            msg.btn_back if offset else msg.btn_go,
            callback_data='edit_config#0' if offset else 'edit_config#5'),
        InlineKeyboardButton(msg.btn_save, callback_data='save_config')
    )
    return kb


def results_kb(deadlines: list):
    params = [f'#{dl}' for dl in deadlines]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        msg.update_results,
        callback_data=f"update_results{''.join(params)}"
    ))
    return kb


async def get_deadline_ids(user_id: str) -> list:
    """Функция получает id дедлайнов пользователя в базе данных"""
    deadlines = cache.lrange(f'u{user_id}', 0, -1)
    if deadlines is None:
        deadlines = await db.select_users(user_id)
        if deadlines is not None:
            deadlines = deadlines.split(",")
            [cache.lpush(f'u{user_id}', dl_id) for dl_id in deadlines]
        else:
            return []
    return deadlines


async def get_deadline_names(ids: list) -> str:
    """Функция собирает сообщение с названиями дедлайнов из id"""
    deadlines_text = ""
    for i, dl_id in enumerate(ids, start=1):
        if i != 1:
            deadlines_text += "\n"
        deadlines_text += msg.deadline_row.format(
            i=i,
            flag=emojize(BOT_DEADLINES_FLAGS.get(dl_id, "-")),
            name=BOT_DEADLINES.get(dl_id, "-")
        )
    return deadlines_text


def update_deadlines(user_id: str, data: str):
    """Функция добаляет или удаляет id дедлайна для юзера"""
    deadline_id = data.split("#")[-1]  # data ~ add_deadline_#5#345
    if data.startswith("add"):
        cache.lpush(f'u{user_id}', deadline_id)
    else:
        cache.lrem(f'u{user_id}', 0, deadline_id)


async def generate_results_answer(ids: list) -> str:
    """Функция создaет сообщение для вывода результатов задач"""
    results = await get_last_results(ids)
    if results:
        text_results = results_to_text(results)
        return msg.results.format(tasks=text_results)
    else:
        return msg.no_results


def ids_to_key(ids: list) -> str:
    """Стандартизация ключей для хранения задач"""
    ids.sort()
    return ','.join(ids)


async def parse_matches(ids: list) -> list:
    """Функция получения задач по API"""
    # логику напишем в следующей части
    return []


async def get_last_results(deadline_ids: list) -> list:
    dl_key = ids_to_key(deadline_ids)
    last_results = cache.jget(dl_key)
    if last_results is None:
        last_results = await parse_matches(deadline_ids)
        if last_results:
            # добавляем новые задачи, если они есть
            cache.jset(dl_key, last_results, MINUTE)
    return last_results


def results_to_text(matches: list) -> str:
    """
    Функция генерации сообщения с задачами
    """
    # логику напишем в следующей части
    ...
