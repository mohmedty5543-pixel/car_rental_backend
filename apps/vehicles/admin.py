from django.contrib import admin
from .models import Vehicle, VehicleImage, VehicleAvailability, FavoriteVehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make','model','year','license_plate','vendor','status','daily_rate')
    list_filter = ('status','make','year')
    search_fields = ('make','model','license_plate','vendor__name')
    raw_id_fields = ('vendor',)

admin.site.register(VehicleImage)
admin.site.register(VehicleAvailability)
admin.site.register(FavoriteVehicle)
