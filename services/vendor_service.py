from django.db import transaction
from apps.vendors.models import Vendor, VendorMember, VendorType

class VendorService:
    @staticmethod
    @transaction.atomic
    def create_vendor(owner, serializer):
        vendor = serializer.save(owner_user=owner)
        vendor.full_clean()
        return vendor

    @staticmethod
    @transaction.atomic
    def add_member(vendor: Vendor, user, role):
        if vendor.type != VendorType.COMPANY:
            raise ValueError('Only COMPANY vendors can have members.')
        member, _ = VendorMember.objects.get_or_create(
            vendor=vendor, user=user, defaults={'role': role}
        )
        return member
