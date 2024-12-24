import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.models import Specialist, Procedure, Salon
from funcs import is_free_time


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

    for date in dates:
        formatted_date = date.strftime('%Y-%m-%d')  # Форматируем дату для использования в callback_data
        keyboard.append([
            InlineKeyboardButton(
                text=date.strftime('%d-%m-%Y'),  # Отображаемая дата для пользователя
                callback_data=f"date_{formatted_date}"  # Передаём фактическую дату в callback_data
            )
        ])
    return InlineKeyboardMarkup(keyboard)


def get_salon_keyboard():
    salons = Salon.objects.all()
    keyboard = []
    for salon in salons:
        keyboard.append([InlineKeyboardButton(f"🏠{salon.name} ", callback_data=f"salon_{salon.id}")])
    return InlineKeyboardMarkup(keyboard)


def get_procedure_keyboard():
    keyboard = []
    procedures = Procedure.objects.all()
    for procedure in procedures:
        keyboard.append([InlineKeyboardButton(f"{procedure.name} ", callback_data=f"procedure_{procedure.id}")])
    return InlineKeyboardMarkup(keyboard)


def get_time_slots_keyboard(chat_id):
    from handlers import USER_DATA
    keyboard = []
    try:
        raw_date = USER_DATA[chat_id].get('date')
        if not raw_date:
            print(f"Ошибка: дата отсутствует в USER_DATA для chat_id {chat_id}")
            return InlineKeyboardMarkup([])

        # Получаем идентификатор салона и мастера из USER_DATA
        salon_id = USER_DATA[chat_id].get('salon')
        specialist_id = USER_DATA[chat_id].get('master')

        # Если указан только салон
        if salon_id:
            try:
                salon = Salon.objects.get(id=int(salon_id))
            except Salon.DoesNotExist:
                print(f"Ошибка: салон с id {salon_id} не найден.")
                return InlineKeyboardMarkup([])

            # Преобразуем дату в объект date
            date = datetime.datetime.strptime(raw_date, "%Y-%m-%d").date()

            # Проверяем доступные временные интервалы для салона
            is_available = is_free_time(entity_type="salon", entity_id=salon.id, date=date)  # Проверка для салона
            print(f"Доступные временные интервалы для {salon.name} на {date}: {is_available}")

            # Добавляем кнопки для свободных временных интервалов
            for time_interval, available in is_available.items():
                if available:
                    time_str = time_interval.strftime("%H:%M")
                    callback_data = f"time_{raw_date}_{time_str}"  # Передаём дату и время
                    keyboard.append([InlineKeyboardButton(text=f"{time_str}", callback_data=callback_data)])

        # Если указан только мастер
        if specialist_id:
            try:
                specialist = Specialist.objects.get(id=int(specialist_id))
            except Specialist.DoesNotExist:
                print(f"Ошибка: мастер с id {specialist_id} не найден.")
                return InlineKeyboardMarkup([])

            # Преобразуем дату в объект date
            date = datetime.datetime.strptime(raw_date, "%Y-%m-%d").date()

            # Проверяем доступные временные интервалы для мастера
            is_available = is_free_time(entity_type="master", entity_id=specialist.id,
                                        date=date)  # Проверка для мастера
            print(f"Доступные временные интервалы для {specialist.name} на {date}: {is_available}")

            # Добавляем кнопки для свободных временных интервалов
            for time_interval, available in is_available.items():
                if available:
                    time_str = time_interval.strftime("%H:%M")
                    callback_data = f"time_{raw_date}_{time_str}"  # Передаём дату и время
                    keyboard.append([InlineKeyboardButton(text=f"{time_str}", callback_data=callback_data)])

        if not keyboard:
            print("Нет доступных временных интервалов.")
            return InlineKeyboardMarkup([])

        return InlineKeyboardMarkup(keyboard)

    except Exception as e:
        print(f"Ошибка в get_time_slots_keyboard: {e}")
        return InlineKeyboardMarkup([])


def get_confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("Подтвердить запись", callback_data="confirm_booking")]
    ]
    return InlineKeyboardMarkup(keyboard)
