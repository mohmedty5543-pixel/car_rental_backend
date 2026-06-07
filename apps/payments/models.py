import uuid
from django.db import models
from apps.bookings.models import Booking

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PAID = 'PAID', 'Paid'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'

class PaymentMethod(models.TextChoices):
    CARD = 'CARD', 'Card'
    CASH = 'CASH', 'Cash'
    WALLET = 'WALLET', 'Wallet'
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank transfer'

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices,
                              default=PaymentStatus.PENDING)
    reference = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['booking']), models.Index(fields=['status'])]
