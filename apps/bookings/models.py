import uuid
from django.db import models
from django.conf import settings
from apps.vehicles.models import Vehicle
from apps.drivers.models import Driver

class BookingStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    CANCELLED = 'CANCELLED', 'Cancelled'
    ACTIVE = 'ACTIVE', 'Active'
    COMPLETED = 'COMPLETED', 'Completed'

class BookingType(models.TextChoices):
    SELF_DRIVE = 'SELF_DRIVE', 'Self drive'
    WITH_DRIVER = 'WITH_DRIVER', 'With driver'

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='bookings')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='bookings')
    type = models.CharField(max_length=20, choices=BookingType.choices,
                            default=BookingType.SELF_DRIVE)
    status = models.CharField(max_length=20, choices=BookingStatus.choices,
                              default=BookingStatus.PENDING)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['vehicle']),
            models.Index(fields=['status']),
            models.Index(fields=['start_at','end_at']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(end_at__gt=models.F('start_at')),
                                   name='booking_valid_range'),
        ]
