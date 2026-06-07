import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class VendorType(models.TextChoices):
    INDIVIDUAL = 'INDIVIDUAL', 'Individual'
    COMPANY = 'COMPANY', 'Company'

class VendorMemberRole(models.TextChoices):
    MANAGER = 'MANAGER', 'Manager'
    STAFF = 'STAFF', 'Staff'

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=VendorType.choices)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='owned_vendors'
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['type']), models.Index(fields=['owner_user'])]

    def clean(self):
        if self.type == VendorType.INDIVIDUAL and self.owner_user_id is None:
            raise ValidationError('Individual vendor requires owner_user.')

    def __str__(self):
        return f'{self.name} ({self.type})'

class VendorMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='vendor_memberships')
    role = models.CharField(max_length=20, choices=VendorMemberRole.choices,
                            default=VendorMemberRole.STAFF)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vendor','user'], name='uniq_vendor_member'),
        ]
        indexes = [models.Index(fields=['vendor']), models.Index(fields=['user'])]

    def clean(self):
        if self.vendor.type != VendorType.COMPANY:
            raise ValidationError('Only COMPANY vendors can have members.')
