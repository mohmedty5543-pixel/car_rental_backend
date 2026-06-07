import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    VENDOR_OWNER = 'VENDOR_OWNER', 'Vendor owner'
    VENDOR_STAFF = 'VENDOR_STAFF', 'Vendor staff'
    ADMIN = 'ADMIN', 'Admin'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('role', UserRole.ADMIN)
        return self.create_user(email, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [models.Index(fields=['role'])]

    def save(self, *args, **kwargs):
        if self.role == UserRole.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role in [UserRole.CUSTOMER, UserRole.VENDOR_OWNER, UserRole.VENDOR_STAFF]:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from django.db import transaction
        from apps.payments.models import Payment
        from apps.bookings.models import Booking
        from apps.vehicles.models import Vehicle
        from apps.vendors.models import Vendor, VendorMember

        with transaction.atomic():
            Payment.objects.filter(booking__user=self).delete()
            Payment.objects.filter(booking__vehicle__vendor__owner_user=self).delete()
            Booking.objects.filter(user=self).delete()
            Booking.objects.filter(vehicle__vendor__owner_user=self).delete()
            Vehicle.objects.filter(vendor__owner_user=self).delete()
            VendorMember.objects.filter(user=self).delete()
            VendorMember.objects.filter(vendor__owner_user=self).delete()
            Vendor.objects.filter(owner_user=self).delete()
            return super().delete(*args, **kwargs)

    def __str__(self):
        return self.email
