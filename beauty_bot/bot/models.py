from django.db import models


class Specialist(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя мастера")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name


class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название процедуры")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Salon(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название салона")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)
    opening_time = models.TimeField(verbose_name="Время открытия")
    closing_time = models.TimeField(verbose_name="Время закрытия")

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name="Салон", related_name="schedules")
    specialist = models.ForeignKey('Specialist', on_delete=models.CASCADE, verbose_name="Специалист", related_name="schedules")
    # задел для связки с моделью специалиста
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        unique_together = ('specialist', 'date', 'start_time')

    def __str__(self):
        return f"{self.specialist} - {self.date} ({self.start_time} - {self.end_time})"
