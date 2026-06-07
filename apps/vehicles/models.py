import uuid
from django.db import models
from apps.vendors.models import Vendor

class VehicleStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    year = models.PositiveSmallIntegerField()
    license_plate = models.CharField(max_length=32, unique=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=VehicleStatus.choices,
                              default=VehicleStatus.DRAFT)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['vendor']),
            models.Index(fields=['status']),
            models.Index(fields=['make','model']),
        ]

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate})'

class VehicleImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicles/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['vehicle'])]

class VehicleAvailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=['vehicle','start_date','end_date'])]
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gte=models.F('start_date')),
                                   name='availability_valid_range'),
        ]

class FavoriteVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='favorites')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','vehicle'], name='uniq_fav'),
        ]
