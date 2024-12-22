
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_bot.settings')
django.setup()

from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from handlers import button_handler, phone_handler

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')

SUBSCRIBE, GET_USERNAME, CHOOSE_SPEAKER, ASK_QUESTION = range(4)


def start(update, context):
    chat_id = update.effective_chat.id
    message = ("Здравствуйте! Перед началом записи, ознакомьтесь с политикой обработки персональных данных: "
               "[PDF](https://clck.ru/3FKLhp).\n\n"
               "Если вы согласны, нажмите \"Согласен\". Иначе, нажмите \"Не согласен\".")

    keyboard = [
        [InlineKeyboardButton("✅ Согласен", callback_data="agree"),
         InlineKeyboardButton("❌ Не согласен", callback_data="disagree")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode="Markdown")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, phone_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
