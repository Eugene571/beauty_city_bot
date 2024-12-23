import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_bot.settings')
django.setup()
from datetime import time
from bot.models import Schedule, Specialist, Appointment


def is_free_time(specialist, date):
    time_intervals = [time(hour, 0) for hour in range(10, 19)]  # Временные интервалы с 10 до 18
    schedules = Appointment.objects.filter(specialist=specialist, date=date)
    availability = {interval: True for interval in time_intervals}  # По умолчанию все интервалы свободны

    for schedule in schedules:
        for interval in time_intervals:
            if schedule.start_time <= interval < schedule.end_time:
                availability[interval] = False  # Если время занято, ставим False

    return availability


if __name__ == '__main__':
    availability = is_free_time(37, '2024-12-22')
    print(availability)
