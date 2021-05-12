from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


# def log_errors(f):
#     def inner(*args,**kwargs):
#         try:
#             return f(*args,**kwargs)
#         except Exception as e:
#             error_message = f'Произошла ошибка: {e}'
#             print(error_message)
#             raise e
#     return inner
# @log_errors
# def do_echo(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     text=update.message.text
#     reply_text= "Ваш ID = {}\n\n{}".format(chat_id,text)
#     update.message.reply_text(
#         text=reply_text,
#     )
class Command(BaseCommand):
    help = 'Телеграм-бот'
    can_import_settings = True
    def handle(self, *args, **options):
        from django.conf import settings
        #1-- правильное подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL,
        )
        print(bot.get_me())

        # # 2 -- обработки
        # updater = Updater(
        #     bot = bot,
        #     use_context=True,
        # )
        # message_hendler = MessageHandler(Filters.text, do_echo)
        # updater.dispatcher.add_handler(message_hendler)
        #
        # # 3 -- запустить бесконечную обработку входящих сообщений
        # updater.start_polling()
        # updater.idle()