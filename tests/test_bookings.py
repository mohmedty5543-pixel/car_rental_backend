import pytest
from datetime import timedelta
from django.utils import timezone
from apps.users.models import User, UserRole
from apps.vendors.models import Vendor, VendorType
from apps.vehicles.models import Vehicle, VehicleStatus
from services.booking_service import BookingService
from core.exceptions import OverlapError

@pytest.mark.django_db
def test_create_and_overlap():
    owner = User.objects.create_user(email='o@e.com', password='pw12345678')
    customer = User.objects.create_user(email='c@e.com', password='pw12345678')
    vendor = Vendor.objects.create(type=VendorType.INDIVIDUAL, name='V', owner_user=owner)
    v = Vehicle.objects.create(vendor=vendor, make='A', model='B', year=2020,
                               license_plate='X1', daily_rate=100,
                               status=VehicleStatus.ACTIVE)
    now = timezone.now()
    b = BookingService.create_request(customer, v, now + timedelta(days=1),
                                      now + timedelta(days=3))
    assert b.total_amount > 0
    with pytest.raises(OverlapError):
        BookingService.create_request(customer, v, now + timedelta(days=2),
                                      now + timedelta(days=4))


@pytest.mark.django_db
def test_booking_list_visibility(api):
    owner = User.objects.create_user(
        email='owner@example.com',
        password='pw12345678',
        full_name='Owner',
        role=UserRole.VENDOR_OWNER,
    )
    customer = User.objects.create_user(
        email='customer@example.com',
        password='pw12345678',
        full_name='Customer',
        role=UserRole.CUSTOMER,
    )
    admin = User.objects.create_user(
        email='admin@example.com',
        password='pw12345678',
        full_name='Admin',
        role=UserRole.ADMIN,
    )
    vendor = Vendor.objects.create(type=VendorType.COMPANY, name='Vendor Co', owner_user=owner)
    vehicle = Vehicle.objects.create(
        vendor=vendor,
        make='Make',
        model='Model',
        year=2024,
        license_plate='XXX-1234',
        daily_rate=100,
        status=VehicleStatus.ACTIVE,
    )
    now = timezone.now()
    booking = BookingService.create_request(customer, vehicle, now + timedelta(days=1), now + timedelta(days=2))

    def get_items(response):
        data = response.json()
        return data['results'] if isinstance(data, dict) and 'results' in data else data

    api.force_authenticate(user=customer)
    response = api.get('/api/bookings/')
    assert response.status_code == 200
    assert any(item['id'] == str(booking.id) for item in get_items(response))

    api.force_authenticate(user=owner)
    response = api.get('/api/bookings/')
    assert response.status_code == 200
    assert any(item['id'] == str(booking.id) for item in get_items(response))

    api.force_authenticate(user=admin)
    response = api.get('/api/bookings/')
    assert response.status_code == 200
    assert any(item['id'] == str(booking.id) for item in get_items(response))

    another_user = User.objects.create_user(
        email='other@example.com',
        password='pw12345678',
        full_name='Other',
        role=UserRole.CUSTOMER,
    )
    api.force_authenticate(user=another_user)
    response = api.get('/api/bookings/')
    assert response.status_code == 200
    assert get_items(response) == []
