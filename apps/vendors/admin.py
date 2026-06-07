from django.contrib import admin
from .models import Vendor, VendorMember
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name','type','owner_user','is_verified','created_at')
    list_filter = ('type','is_verified')
    search_fields = ('name','owner_user__email')
    raw_id_fields = ('owner_user',)
@admin.register(VendorMember)
class VendorMemberAdmin(admin.ModelAdmin):
    list_display = ('vendor','user','role')
    list_filter = ('role',)
    raw_id_fields = ('vendor','user')
