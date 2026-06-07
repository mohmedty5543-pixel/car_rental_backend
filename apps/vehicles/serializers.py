from rest_framework import serializers
from .models import Vehicle, VehicleImage, VehicleAvailability, FavoriteVehicle
from apps.vendors.models import Vendor

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ('id','vehicle','image','is_primary','created_at')
        read_only_fields = ('id','created_at')

class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAvailability
        fields = ('id','vehicle','start_date','end_date','is_available')
        read_only_fields = ('id',)
    def validate(self, attrs):
        if attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError('end_date must be >= start_date')
        return attrs

class VehicleVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'is_verified')

class VehicleSerializer(serializers.ModelSerializer):
    vendor_info = VehicleVendorSerializer(source='vendor', read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        fields = (
            'id',
            'vendor',
            'vendor_info',
            'make',
            'model',
            'year',
            'license_plate',
            'daily_rate',
            'status',
            'location',
            'images',
            'created_at',
        )
        read_only_fields = ('id','created_at','images','vendor_info')

class FavoriteVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteVehicle
        fields = ('id','user','vehicle','created_at')
        read_only_fields = ('id','user','created_at')
