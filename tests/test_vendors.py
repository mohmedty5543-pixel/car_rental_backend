import pytest

from apps.users.models import UserRole, User
from apps.vendors.models import Vendor, VendorMember, VendorType


@pytest.mark.django_db
def test_vendor_list_includes_member_vendors(api):
    owner = User.objects.create_user(
        email='owner@example.com',
        password='pw12345678',
        full_name='Owner',
        role=UserRole.VENDOR_OWNER,
    )
    member = User.objects.create_user(
        email='member@example.com',
        password='pw12345678',
        full_name='Member',
        role=UserRole.VENDOR_STAFF,
    )
    other_user = User.objects.create_user(
        email='other@example.com',
        password='pw12345678',
        full_name='Other',
        role=UserRole.CUSTOMER,
    )

    vendor = Vendor.objects.create(
        type=VendorType.COMPANY,
        name='Test Vendor',
        owner_user=owner,
    )
    VendorMember.objects.create(vendor=vendor, user=member)

    api.force_authenticate(user=member)
    response = api.get('/api/vendors/')
    assert response.status_code == 200
    assert any(item['id'] == str(vendor.id) for item in response.json())

    api.force_authenticate(user=other_user)
    response = api.get('/api/vendors/')
    assert response.status_code == 200
    assert response.json() == []
