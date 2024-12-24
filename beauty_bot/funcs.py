import os
from datetime import time

import django

from bot.models import Appointment, Specialist, Salon

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_bot.settings')
django.setup()


def is_free_time(entity_type, entity_id, date):
    # Временные интервалы с 10 до 18
    time_intervals = [time(hour, 0) for hour in range(10, 19)]
    availability = {interval: True for interval in time_intervals}  # Все интервалы по умолчанию свободны

    # Формируем фильтр для базы данных
    schedules = []

    if entity_type == "salon":
        try:
            salon = Salon.objects.get(id=entity_id)
            schedules = Appointment.objects.filter(salon=salon, date=date)
        except Salon.DoesNotExist:
            print(f"Ошибка: салон с id {entity_id} не найден.")
            return availability

    elif entity_type == "master":
        try:
            specialist = Specialist.objects.get(id=entity_id)
            schedules = Appointment.objects.filter(specialist=specialist, date=date)
        except Specialist.DoesNotExist:
            print(f"Ошибка: мастер с id {entity_id} не найден.")
            return availability

    # Проверяем занятость временных интервалов
    for schedule in schedules:
        for interval in time_intervals:
            if schedule.start_time <= interval < schedule.end_time:
                availability[interval] = False  # Отмечаем интервал как занятый

    return availability
