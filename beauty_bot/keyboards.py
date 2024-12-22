from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.models import Specialist, Procedure
from funcs import is_free_time
import datetime
from datetime import time



def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝  Записаться через салон  ", callback_data="salon")],
        [InlineKeyboardButton("🖊️  Записаться через мастера", callback_data="master")],
        [InlineKeyboardButton("📞 Позвонить администратору", callback_data="call_admin")],

    ]
    return InlineKeyboardMarkup(keyboard)


def get_master_keyboard():
    masters = Specialist.objects.all()
    keyboard = []
    for master in masters:
        keyboard.append([InlineKeyboardButton(f"‍👩‍{master.name} ", callback_data=f"master_{master.id}")])
    return InlineKeyboardMarkup(keyboard)


def get_date_keyboard():
    keyboard = []
    today = datetime.datetime.now()
    end_date = today + datetime.timedelta(days=4)
    dates = [today + datetime.timedelta(days=x) for x in range((end_date - today).days + 1)]
    formatted_dates = [date.strftime('%d-%m-%Y') for date in dates]
    k = 1
    for date in formatted_dates:
        keyboard.append([InlineKeyboardButton(f"{date} ", callback_data=f"date_{k}")])
        k += 1
    return InlineKeyboardMarkup(keyboard)


def get_salon_keyboard():
    keyboard = [
        [InlineKeyboardButton("‍🏠 Салон 'Челка' ", callback_data="salon_1"),
         InlineKeyboardButton("🏠 Салон 'Стиляга' ", callback_data="salon_2"),
         InlineKeyboardButton("🏠 Салон 'Гармония' ", callback_data="salon_3")],
        [InlineKeyboardButton("🏠 Салон 'Элеганс' ", callback_data="salon_4"),
         InlineKeyboardButton("🏠 Салон 'Краса' ", callback_data="salon_5"),
         InlineKeyboardButton("🏠 Салон 'Стиль' ", callback_data="salon_6")]

    ]
    return InlineKeyboardMarkup(keyboard)


def get_procedure_keyboard():
    keyboard = []
    procedures = Procedure.objects.all()
    for procedure in procedures:
        keyboard.append([InlineKeyboardButton(f"{procedure.name} ", callback_data=f"procedure_{procedure.id}")])
    return InlineKeyboardMarkup(keyboard)


def get_time_slots_keyboard(chat_id):
    from handlers import USER_DATA
    try:
        # Получаем мастера из базы данных
        specialist_id = USER_DATA[chat_id].get('master', [])[-1]
        specialist = Specialist.objects.get(id=specialist_id)

        # Получаем дату и преобразуем её в объект date
        raw_date = USER_DATA[chat_id].get('date')
        date = datetime.strptime(raw_date, "%Y-%m-%d").date()

        # Проверяем доступные временные интервалы
        is_available = is_free_time(specialist, date)  # Должна возвращать словарь {время: доступно/нет}

        # Создаем кнопки для свободных временных интервалов
        keyboard = []
        for time_interval, available in is_available.items():
            if available:  # Если время доступно
                keyboard.append([
                    InlineKeyboardButton(
                        text=f"{time_interval}",
                        callback_data=f"time_{time_interval}"
                    )
                ])

        # Возвращаем объект клавиатуры
        return InlineKeyboardMarkup(keyboard)

    except ValueError as e:
        print(f"Ошибка преобразования даты: {e}")
    except Specialist.DoesNotExist:
        print(f"Мастер с id {specialist_id} не найден.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return InlineKeyboardMarkup([[]])  # Возвращаем пустую клавиатуру в случае ошибки


def get_confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("Подтвердить запись", callback_data="confirm_booking")]
    ]
    return InlineKeyboardMarkup(keyboard)
