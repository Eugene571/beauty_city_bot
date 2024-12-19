from django.contrib import admin
from .models import Salon, Schedule, Specialist, Client, Booking

admin.site.register(Salon)
admin.site.register(Schedule)
admin.site.register(Specialist)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'loyalty_points')
    search_fields = ('name', 'phone_number', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'schedule', 'procedure', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'schedule__date')
    search_fields = ('client__name', 'client__phone_number')
