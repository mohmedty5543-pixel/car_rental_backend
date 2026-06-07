from django.contrib import admin
from .models import Delivery
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id','booking','type','status','fee')
    list_filter = ('status','type')
    raw_id_fields = ('booking',)
