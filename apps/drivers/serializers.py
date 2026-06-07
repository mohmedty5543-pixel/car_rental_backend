from rest_framework import serializers
from .models import Driver
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id','vendor','full_name','license_number','is_active','created_at')
        read_only_fields = ('id','created_at')
