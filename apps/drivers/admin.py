from django.contrib import admin
from .models import Driver
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name','vendor','license_number','is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name','license_number')
    raw_id_fields = ('vendor',)
