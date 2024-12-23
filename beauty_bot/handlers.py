from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.models import Procedure, Appointment
from datetime import datetime
from datetime import timedelta
from keyboards import (
    get_main_menu_keyboard,
    get_salon_keyboard,
    get_procedure_keyboard,
    get_time_slots_keyboard,
    get_date_keyboard,
    get_master_keyboard
)

USER_DATA = {}


def format_procedure_prices():
    procedures = Procedure.objects.all()
    message = "Цены на процедуры:\n\n"
    for procedure in procedures:
        message += f"- 🌺{procedure.name}: {procedure.price} рублей\n"
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
        message = format_procedure_prices()
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
        procedure_id = query.data.split("_")[-1]
        USER_DATA[chat_id]["procedure"] = procedure_id
        procedure_name = Procedure.objects.get(id=procedure_id).name
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

        try:
            # Извлекаем дату и время из callback_data
            _, raw_date, raw_time = query.data.split("_")
            USER_DATA[chat_id]["date"] = raw_date
            # Преобразуем строку времени в объект time
            time_obj = datetime.strptime(raw_time, "%H:%M").time()
            USER_DATA[chat_id]["time"] = time_obj
            USER_DATA[chat_id]["start_time"] = time_obj
            # Вычисляем end_time
            end_datetime = datetime.combine(datetime.today(), time_obj) + timedelta(hours=1)
            USER_DATA[chat_id]["end_time"] = end_datetime.time()

            # Сообщение с подтверждением времени
            message = f"Вы выбрали дату {raw_date} и время {raw_time}. Введите ваш номер телефона для подтверждения записи."
            context.bot.send_message(chat_id=chat_id, text=message)
        except ValueError as e:
            context.bot.send_message(chat_id=chat_id, text="Произошла ошибка при выборе времени. Попробуйте снова.")
            print(f"Ошибка обработки времени: {e}")

    elif query.data == "master":
        message = "Выберите мастера:"
        reply_markup = get_master_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("master_"):
        master_id = query.data.split("_")[-1]
        USER_DATA[chat_id]["master"] = master_id
        message = "Вы выбрали мастера. Теперь выберите процедуру:"
        reply_markup = get_procedure_keyboard()
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data.startswith("date_"):
        # Извлекаем выбранную дату
        raw_date = query.data.split("_")[1]  # Получаем дату из callback_data
        USER_DATA[chat_id]["date"] = raw_date  # Сохраняем дату как строку в формате 'YYYY-MM-DD'
        # Предлагаем выбрать время
        message = f"Вы выбрали дату: {raw_date}. Теперь выберите удобное время:"
        reply_markup = get_time_slots_keyboard(chat_id)  # Генерация клавиатуры для времени
        context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    elif query.data == "call_admin":
        message = "Вы можете позвонить нашему менеджеру по номеру:\n +7 (123) 456-78-90"
        context.bot.send_message(chat_id=chat_id, text=message)


def phone_handler(update, context):
    chat_id = update.message.chat_id
    phone = update.message.text
    USER_DATA[chat_id]["phone"] = phone

    # Save appointment in the database
    salon_id = USER_DATA[chat_id].get("salon")
    specialist_id = USER_DATA[chat_id].get("master")
    procedure_id = USER_DATA[chat_id].get("procedure")
    date = USER_DATA[chat_id].get("date")
    time = USER_DATA[chat_id].get("time")
    start_time = USER_DATA[chat_id].get("start_time")
    end_time = USER_DATA[chat_id].get("end_time")

    appointment = Appointment.objects.create(
        salon_id=salon_id,
        specialist_id=specialist_id,
        procedure_id=procedure_id,
        date=date,
        time=time,
        client_name=update.message.chat.first_name,
        client_phone=phone,
        start_time=start_time,
        end_time=end_time
    )

    context.bot.send_message(chat_id=chat_id, text="✅ Спасибо! Ваша запись подтверждена.")

