from django.contrib import admin
from .models import Salon, Specialist, Client, Booking, Procedure, Appointment


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    search_fields = ('name', 'price', 'id')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone', 'id')
    search_fields = ('name', 'specialization', 'phone', 'id')


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
    list_display = ('client', 'procedure', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('client__name', 'client__phone_number')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('salon',
                    'specialist',
                    'procedure',
                    'client_name',
                    'client_phone',
                    'date',
                    'time',
                    'start_time',
                    'end_time')
