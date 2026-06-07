from django.contrib import admin
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user','vehicle','status','type','start_at','end_at','total_amount')
    list_filter = ('status','type')
    search_fields = ('user__email','vehicle__license_plate')
    raw_id_fields = ('user','vehicle','driver')
    date_hierarchy = 'start_at'
