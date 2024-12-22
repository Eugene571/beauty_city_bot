from django.core.exceptions import ValidationError
from django.db import models


class Specialist(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя мастера")
    specialization = models.CharField(max_length=100, blank=True, verbose_name="Специализация")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    procedures = models.ManyToManyField('Procedure', blank=True, related_name="specialists", verbose_name="Процедуры")
    id = models.AutoField(primary_key=True, verbose_name='Персональный код мастера')

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name


class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название процедуры")
    price = models.FloatField(verbose_name="Цена")
    id = models.AutoField(primary_key=True, verbose_name='Код процедуры')

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
    specialist = models.ForeignKey('Specialist', on_delete=models.CASCADE, verbose_name="Специалист",
                                    related_name="schedules")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        unique_together = ('specialist', 'date', 'start_time')

    def __str__(self):
        return f"{self.specialist} - {self.date} ({self.start_time} - {self.end_time})"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала.")


class Client(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя клиента")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")
    email = models.EmailField(blank=True, null=True, verbose_name="Электронная почта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    loyalty_points = models.PositiveIntegerField(default=0, verbose_name="Бонусные баллы")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name or self.phone_number


class Booking(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='bookings', verbose_name="Клиент")
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='bookings',
                                 verbose_name="Расписание")
    procedure = models.ForeignKey('Procedure', on_delete=models.CASCADE, related_name='bookings',
                                  verbose_name="Процедура")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Ожидает'), ('confirmed', 'Подтверждена'), ('cancelled', 'Отменена')],
        default='pending',
        verbose_name="Статус записи"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('unpaid', 'Не оплачено'), ('paid', 'Оплачено')],
        default='unpaid',
        verbose_name="Статус оплаты"
    )
    feedback = models.TextField(blank=True, null=True, verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        unique_together = ('schedule', 'procedure', 'client')

    def __str__(self):
        return f"{self.procedure} для {self.client} ({self.schedule.date})"
