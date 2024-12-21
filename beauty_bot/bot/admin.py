from django.contrib import admin
from .models import Salon, Schedule, Specialist, Client, Booking, Procedure

admin.site.register(Schedule)


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'price')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone')
    search_fields = ('name', 'specialization', 'phone')


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'opening_time', 'closing_time')
    search_fields = ('name', 'phone')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'loyalty_points')
    search_fields = ('name', 'phone_number', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'schedule', 'procedure', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'schedule__date')
    search_fields = ('client__name', 'client__phone_number')
