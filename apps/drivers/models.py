import uuid
from django.db import models
from apps.vendors.models import Vendor

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='drivers')
    full_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [models.Index(fields=['vendor']), models.Index(fields=['is_active'])]
    def __str__(self):
        return self.full_name
