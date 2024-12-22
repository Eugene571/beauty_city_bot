from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.models import Procedure
from datetime import datetime
from keyboards import (
    get_main_menu_keyboard,
    get_salon_keyboard,
    get_procedure_keyboard,
    get_time_slots_keyboard,
    get_date_keyboard,
    get_master_keyboard
)

USER_DATA = {}

PROCEDURE_TRANSLATIONS = {
    "cut": "Стрижка",
    "manicure": "Маникюр",
    "pedicure": "Педикюр",
    "color": "Окрашивание волос",
    "facial": "Уход за лицом",
    "waxing": "Эпиляция",
    "massage": "Массаж"
}

PROCEDURE_PRICES = {
    "Стрижка": 1000,
    "Маникюр": 1500,
    "Педикюр": 1200,
    "Окрашивание волос": 2500,
    "Уход за лицом": 2000,
    "Эпиляция": 800,
    "Массаж": 1800
}

SALONS = {
    "1": "Салон 'Челка'",
    "2": "Салон 'Стиляга'",
    "3": "Салон 'Гармония'",
    "4": "Салон 'Элеганс'",
    "5": "Салон 'Краса'",
    "6": "Салон 'Стиль'"
}

MASTERS = {
    "1": "Ольга Смирнова",
    "2": "Надежда Литвина",
    "3": "Лариса Новикова",
    "4": "Светлана Ларина",
    "5": "Любовь Макеева",
    "6": "Татьяна Смелова"
}


def format_procedure_prices(prices):
    message = "Цены на процедуры:\n\n"
    for procedure, price in prices.items():
        message += f"- {procedure}: {price} рублей\n"
    return message.strip()


def button_handler(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    if query.data == "agree":
        USER_DATA[chat_id] = {"agreed": True}
        message = "Спасибо! Выберите, как вы хотите записаться:"
        reply_markup = get_main_menu_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data == "show_prices":
        message = format_procedure_prices(PROCEDURE_PRICES)
        context.bot.send_message(chat_id=chat_id, text=message)

    elif query.data == "disagree":
        context.bot.send_message(chat_id=chat_id, text="К сожалению, вы не можете продолжить без согласия.")

    elif query.data == "salon":
        message = "Выберите салон:"
        reply_markup = get_salon_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("salon_"):
        salon_id = query.data.split("_")[1]
        USER_DATA[chat_id]["salon"] = salon_id
        message = "Вы выбрали салон. Что хотите сделать дальше?"
        keyboard = [
            [InlineKeyboardButton("🖋 Хочу записаться", callback_data="choose_procedure")],
            [InlineKeyboardButton("📈 Интересно узнать цены", callback_data="show_prices")],
            [InlineKeyboardButton("🔙 Назад", callback_data="salon")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data == "choose_procedure":
        message = "Выберите процедуру:"
        reply_markup = get_procedure_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("procedure_"):
        procedure_id = query.data.split("_")
        USER_DATA[chat_id]["procedure"] = procedure_id
        procedure_name = Procedure.objects.get(id=procedure_id[-1])
        message = f"Вы выбрали процедуру '{procedure_name}'. Что хотите сделать дальше?"
        keyboard = [
            [InlineKeyboardButton("✏️ Хочу записаться на удобное время", callback_data="choose_time")],
            [InlineKeyboardButton("📉 Интересно узнать цены", callback_data="show_prices")],
            [InlineKeyboardButton("🔙 Назад", callback_data="choose_procedure")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data == "choose_time":
        message = "Выберите дату для записи:"
        reply_markup = get_date_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("time_"):
        time_slot = query.data.split("_")[1]
        USER_DATA[chat_id]["time"] = time_slot
        message = "Введите ваш номер телефона для подтверждения записи."
        context.bot.send_message(chat_id=chat_id, text=message)

    elif query.data == "master":
        message = "Выберите мастера:"
        reply_markup = get_master_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("master_"):
        master_id = query.data.split("_")
        USER_DATA[chat_id]["master"] = master_id
        message = "Вы выбрали мастера. Теперь выберите процедуру:"
        reply_markup = get_procedure_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("date_"):
        raw_date = query.data.split("_")[1]
        date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        USER_DATA[chat_id]["date"] = date
        message = "Выберите время для записи:"
        reply_markup = get_time_slots_keyboard(chat_id)
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("time_"):
        time_slot = query.data.split("_")[1]
        USER_DATA[chat_id]["time"] = time_slot
        message = "Введите ваш номер телефона для подтверждения записи."
        context.bot.send_message(chat_id=chat_id, text=message)

    elif query.data == "call_admin":
        message = "Вы можете позвонить нашему менеджеру по номеру:\n +7 (123) 456-78-90"
        context.bot.send_message(chat_id=chat_id, text=message)


def phone_handler(update, context):
    global confirmation_message
    chat_id = update.message.chat_id
    phone = update.message.text
    USER_DATA[chat_id]["phone"] = phone

    procedure = USER_DATA[chat_id]["procedure"]
    time_slot = USER_DATA[chat_id]["time"]
    date = USER_DATA[chat_id].get("date", "Неизвестная дата")
    procedure_russian = PROCEDURE_TRANSLATIONS.get(procedure, procedure)

    if "salon" in USER_DATA[chat_id] and "master" not in USER_DATA[chat_id]:
        salon_id = USER_DATA[chat_id]["salon"]
        salon_name = SALONS.get(salon_id, "Неизвестный салон")
        confirmation_message = (
            "✅ Спасибо! Ваша запись подтверждена.\n\n"
            f"Салон: '{salon_name}'\n"
            f"Процедура: {procedure_russian}\n"
            f"Дата: {date}\n"
            f"Время: {time_slot}\n"
            f"Телефон: {phone}\n\n"
            "Ждём вас в назначенное время!\n"
        )
    elif "master" in USER_DATA[chat_id]:
        master_id = USER_DATA[chat_id]["master"]
        master_name = MASTERS.get(master_id, "Неизвестный мастер")
        confirmation_message = (
            "✅ Спасибо! Ваша запись подтверждена.\n\n"
            f"Мастер: {master_name}\n"
            f"Процедура: {procedure_russian}\n"
            f"Дата: {date}\n"
            f"Время: {time_slot}\n"
            f"Телефон: {phone}\n\n"
            "Ждём вас в назначенное время!\n"
        )

    context.bot.send_message(chat_id=chat_id, text=confirmation_message)
