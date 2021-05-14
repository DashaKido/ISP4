from django.core.management.base import BaseCommand
from django.conf import settings
from logging import getLogger
from telegram import Bot
from telegram import Update
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.utils.request import Request
from .buttons import *
from telegram_bot.models import Message
from telegram_bot.models import Profile

logger = getLogger(__name__)


def log_errors(f):
    """декоратор для отладки событий от телеграма"""

    def inner(*args, **kwargs):
        try:
            logger.info(f"Обращение в функцию {f.__name__}")
            return f(*args, **kwargs)
        except Exception:
            logger.exception(f"Ошибка в обработчике {f.__name__}")
            raise

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == BUTTON1_HELP:
        return do_help(update=update, context=context)
    elif text == BUTTON2_COUNT:
        return do_count(update=update, context=context)
    elif text == BUTTON3_TIMER:
        return do_timer(update=update, context=context)
    elif text == BUTTON4_QUOTE:
        return do_quote(update=update, context=context)
    elif text == BUTTON5_SETTINGS:
        return do_settings(update=update, context=context)
    else:
        p, _ = Profile.objects.get_or_create(
            external_id=chat_id,
            defaults={
                'name': update.message.from_user.username,
            }
        )
        m = Message(
            profile=p,
            text=text,
        )
        m.save()
        reply_text = f"Ваш ID = {chat_id}\nMessage ID = {m.pk}\n{text}"
        update.message.reply_text(
            text=reply_text,
        )


@log_errors
def do_settings(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'Тут должны быть настройки дедлайнов, но их пока нет(',
    )


@log_errors
def do_timer(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'1..2..3.. я думаю',
    )


@log_errors
def do_quote(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'Пока просто текст, но скоро что-то будет...',
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Message.objects.filter(profile=p).count()
    update.message.reply_text(
        text=f'У вас {count} сообщений',
    )


@log_errors
def do_start(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(
        text=f'Привет {name}. Я помогу тебе с отслеживание твоих дедлайнов.',
    )


@log_errors
def do_help(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="""
Я помогу тебе с отслеживанием твоих дедлайнов.
Я могу помогу тебе рассчитать хорошую тактику для успешной сдачи любого задания в срок.
Так же я могу быть таймером для интенсивного занятия (45 минут работы/15 минут отдыха).
Если тебе стало грустно, то я попробую подбодрить тебя цитатой.
        """,
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 -- правильное подключение
        request = Request(
            connect_timeout=1.0,
            read_timeout=0.5,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())
        # 2 -- обработки
        updater = Updater(
            bot=bot,
            use_context=True,
            request_kwargs=settings.REQUEST_KWARGS,
        )
        message_handler3 = CommandHandler('start', do_start)
        updater.dispatcher.add_handler(message_handler3)
        message_handler2 = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler2)
        message_handler4 = CommandHandler('help', do_help)
        updater.dispatcher.add_handler(message_handler4)
        message_handler5 = CommandHandler('timer', do_timer)
        updater.dispatcher.add_handler(message_handler5)
        message_handler6 = CommandHandler('quote', do_quote)
        updater.dispatcher.add_handler(message_handler6)
        message_handler7 = CommandHandler('settings', do_settings)
        updater.dispatcher.add_handler(message_handler7)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
