from rest_framework import serializers
from .models import Delivery
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id','booking','type','status','address','fee','created_at')
        read_only_fields = ('id','created_at')
