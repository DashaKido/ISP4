import random

from django.core.management.base import BaseCommand
from django.conf import settings
from logging import getLogger
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
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
        reply_text1 = "Даже не знаю, что ответить."
        reply_text2 = "Очень интересно."
        reply_text3 = "Может напишете что-то еще?"
        reply_text4 = "После такого даже не хочется с вами говорить."
        reply_text5 = "Скучно с вами."
        reply_text6 = "А с вами интересно."
        reply_text7 = "Что?"
        reply_text8 = "Повторите?"
        reply_text9 = "Буду знать."
        reply_text10 = "Если что, то я все записываю."
        reply_text11 = "Вы прекрасный собеседник."
        seq = [reply_text1, reply_text2, reply_text3, reply_text4,
               reply_text5, reply_text6, reply_text7, reply_text8,
               reply_text9, reply_text10, reply_text11]
        reply_text = random.choice(seq)
        update.message.reply_text(
            text=reply_text,
        )


@log_errors
def do_settings(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Выберите действие:',
        reply_markup=get_keyboard_settings1(),
    )


@log_errors
def do_timer(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Выберите действие:',
        reply_markup=get_base_inline_keyboard_timer(),
    )


@log_errors
def do_quote(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Пока просто текст, но скоро что-то будет...',
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
        reply_markup=get_base_reply_keyboard(),
    )


@log_errors
def do_help(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="""
Привет! Я помогу тебе с отслеживанием твоих дедлайнов.
- Я могу рассчитать хорошую тактику для успешной сдачи любого задания в срок.
- Я могу быть таймером для интенсивного занятия (например 45 минут работы/15 минут отдыха).
- Так же могу посчитать количество сообщений в этом чате.
- Если тебе стало грустно, то я попробую подбодрить тебя цитатой.

Просто выбери что-то из меню ниже и посмотри, что получится 😉.
        """,
        reply_markup=get_base_reply_keyboard(),
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
        start_handler = CommandHandler('start', do_start)
        updater.dispatcher.add_handler(start_handler)
        count_handler = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(count_handler)
        help_handler = CommandHandler('help', do_help)
        updater.dispatcher.add_handler(help_handler)
        timer_handler = CommandHandler('timer', do_timer)
        updater.dispatcher.add_handler(timer_handler)
        quote_handler = CommandHandler('quote', do_quote)
        updater.dispatcher.add_handler(quote_handler)
        settings_handler = CommandHandler('settings', do_settings)
        updater.dispatcher.add_handler(settings_handler)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        timer_button_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
        updater.dispatcher.add_handler(timer_button_handler)
        settings_button_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
        updater.dispatcher.add_handler(settings_button_handler)
        # 3 -- запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
