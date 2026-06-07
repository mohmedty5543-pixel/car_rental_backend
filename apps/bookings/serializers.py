from rest_framework import serializers
from .models import Booking

class BookingReadSerializer(serializers.ModelSerializer):
    with_driver = serializers.SerializerMethodField()
    driver_name = serializers.SerializerMethodField()
    user_email = serializers.ReadOnlyField(source='user.email')
    user_name = serializers.ReadOnlyField(source='user.full_name')
    vehicle_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            'id',
            'user',
            'user_email',
            'user_name',
            'vehicle',
            'vehicle_name',
            'driver',
            'driver_name',
            'type',
            'status',
            'start_at',
            'end_at',
            'total_amount',
            'created_at',
            'with_driver',
        )
        read_only_fields = fields

    def get_vehicle_name(self, obj):
        return f"{obj.vehicle.make} {obj.vehicle.model}"

    def get_with_driver(self, obj):
        return obj.type == 'WITH_DRIVER'

    def get_driver_name(self, obj):
        return obj.driver.full_name if obj.driver else None

class BookingWriteSerializer(serializers.ModelSerializer):
    with_driver = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Booking
        fields = ('id','vehicle','driver','type','start_at','end_at', 'with_driver')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if attrs['end_at'] <= attrs['start_at']:
            raise serializers.ValidationError('end_at must be after start_at')
        
        # Pop with_driver if sent in payload and map to type choice field
        with_driver = attrs.pop('with_driver', None)
        if with_driver is not None:
            attrs['type'] = 'WITH_DRIVER' if with_driver else 'SELF_DRIVE'
            
        return attrs
