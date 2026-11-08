from django.contrib import admin
from .models import Parking


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'accessible_spaces', 'paid', 'open_24h']
    list_filter = ['paid', 'open_24h']
    search_fields = ['name', 'address']
