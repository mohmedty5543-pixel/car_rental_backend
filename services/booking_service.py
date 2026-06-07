from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.bookings.models import Booking, BookingStatus, BookingType
from apps.vehicles.models import Vehicle
from apps.drivers.models import Driver
from core.exceptions import InvalidTransition
from services.availability_service import AvailabilityService
from services.notification_service import NotificationService

class BookingService:
    @staticmethod
    def _compute_total(vehicle: Vehicle, start_at, end_at, type=BookingType.SELF_DRIVE) -> Decimal:
        delta = end_at - start_at
        days = max(1, int((delta + timedelta(hours=23)).days))
        base_total = (vehicle.daily_rate or Decimal('0')) * days
        if type == BookingType.WITH_DRIVER:
            base_total += Decimal('50.00') * days
        return base_total

    @staticmethod
    @transaction.atomic
    def create_request(user, vehicle, start_at, end_at, type=BookingType.SELF_DRIVE,
                       driver=None):
        AvailabilityService.ensure_available(vehicle.id, start_at, end_at)
        total = BookingService._compute_total(vehicle, start_at, end_at, type=type)
        booking = Booking.objects.create(
            user=user, vehicle=vehicle, driver=driver,
            type=type, start_at=start_at, end_at=end_at,
            total_amount=total, status=BookingStatus.PENDING,
        )
        NotificationService.notify(
            user=vehicle.vendor.owner_user,
            title='New booking request',
            body=f'Booking {booking.id} pending approval',
        )
        return booking

    @staticmethod
    @transaction.atomic
    def approve(booking: Booking, actor):
        if booking.status != BookingStatus.PENDING:
            raise InvalidTransition()
        AvailabilityService.ensure_available(
            booking.vehicle_id, booking.start_at, booking.end_at,
            exclude_booking_id=booking.id,
        )
        booking.status = BookingStatus.APPROVED
        booking.save(update_fields=['status','updated_at'])
        NotificationService.notify(booking.user, 'Booking approved',
                                   f'Booking {booking.id} approved')
        return booking

    @staticmethod
    @transaction.atomic
    def reject(booking: Booking, actor):
        if booking.status != BookingStatus.PENDING:
            raise InvalidTransition()
        booking.status = BookingStatus.REJECTED
        booking.save(update_fields=['status','updated_at'])
        NotificationService.notify(booking.user, 'Booking rejected',
                                   f'Booking {booking.id} rejected')
        return booking

    @staticmethod
    @transaction.atomic
    def cancel(booking: Booking, actor):
        if booking.status in (BookingStatus.COMPLETED, BookingStatus.CANCELLED):
            raise InvalidTransition()
        booking.status = BookingStatus.CANCELLED
        booking.save(update_fields=['status','updated_at'])
        return booking

    @staticmethod
    @transaction.atomic
    def complete(booking: Booking, actor):
        if booking.status not in (BookingStatus.APPROVED, BookingStatus.ACTIVE):
            raise InvalidTransition()
        booking.status = BookingStatus.COMPLETED
        booking.save(update_fields=['status','updated_at'])
        return booking

    @staticmethod
    @transaction.atomic
    def assign_driver(booking: Booking, driver_id):
        driver = get_object_or_404(Driver, pk=driver_id, vendor=booking.vehicle.vendor)
        booking.driver = driver
        booking.type = BookingType.WITH_DRIVER
        booking.save(update_fields=['driver','type','updated_at'])
        return booking
