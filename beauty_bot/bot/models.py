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
    id = models.AutoField(primary_key=True, verbose_name='Код салона')

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self):
        return self.name


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
        unique_together = ('procedure', 'client')

    def __str__(self):
        return f"{self.procedure} для {self.client} ({self.schedule.date})"


class Appointment(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='appointments', null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=15)
    start_time = models.TimeField(verbose_name="Время начала",)
    end_time = models.TimeField(verbose_name="Время окончания",)
    # нужно добавить старт и энд для работы функции is_free_time

    class Meta:
        unique_together = ('specialist', 'date', 'time')

    def __str__(self):
        return f"{self.client_name} ({self.procedure.name})"
