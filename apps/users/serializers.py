from rest_framework import serializers
from .models import User

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','phone','full_name','role','is_active','is_staff','is_superuser','created_at')
        read_only_fields = ('id', 'role', 'is_active', 'is_staff', 'is_superuser', 'created_at')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ('id','email','password','phone','full_name','role')
        read_only_fields = ('id',)
    def create(self, validated):
        password = validated.pop('password')
        user = User(**validated)
        user.set_password(password)
        user.save()
        return user

class AdminUserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('role',)
        extra_kwargs = {
            'role': {'required': True}
        }

from apps.vendors.models import Vendor

class AdminVendorVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('is_verified',)
        extra_kwargs = {
            'is_verified': {'required': True}
        }

