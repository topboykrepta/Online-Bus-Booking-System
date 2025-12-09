from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'origin', 'destination', 'depart_time', 'seats', 'price')
    list_filter = ('origin', 'destination')

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'trip', 'route', 'price', 'paid', 'created_at')
    list_filter = ('paid', 'trip', 'route')
    search_fields = ('name', 'phone', 'id_number')
    readonly_fields = ('luggage_fee',)
