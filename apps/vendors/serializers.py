from rest_framework import serializers
from .models import Vendor, VendorMember, VendorType

class VendorSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner_user.email')
    owner_name = serializers.ReadOnlyField(source='owner_user.full_name')

    class Meta:
        model = Vendor
        fields = ('id','type','name','description','owner_user','owner_email','owner_name','is_verified','created_at')
        read_only_fields = ('id','is_verified','created_at','owner_user')

class VendorMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMember
        fields = ('id','vendor','user','role','created_at')
        read_only_fields = ('id','created_at')

    def validate(self, attrs):
        vendor = attrs.get('vendor')
        if vendor and vendor.type != VendorType.COMPANY:
            raise serializers.ValidationError('Only COMPANY vendors can have members.')
        return attrs
