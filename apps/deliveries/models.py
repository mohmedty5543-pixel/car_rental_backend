import uuid
from django.db import models
from apps.bookings.models import Booking

class DeliveryStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_TRANSIT = 'IN_TRANSIT', 'In transit'
    DELIVERED = 'DELIVERED', 'Delivered'
    RETURNED = 'RETURNED', 'Returned'
    CANCELLED = 'CANCELLED', 'Cancelled'

class DeliveryType(models.TextChoices):
    PICKUP = 'PICKUP', 'Pickup'
    DROPOFF = 'DROPOFF', 'Dropoff'

class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='delivery')
    type = models.CharField(max_length=20, choices=DeliveryType.choices)
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices,
                              default=DeliveryStatus.PENDING)
    address = models.CharField(max_length=512)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
