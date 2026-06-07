from django.contrib import admin
from .models import Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','booking','user','rating','created_at')
    list_filter = ('rating',)
    raw_id_fields = ('booking','user')
