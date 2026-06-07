from django.db.models import Q
from apps.bookings.models import Booking, BookingStatus
from core.exceptions import OverlapError

ACTIVE_STATUSES = (BookingStatus.PENDING, BookingStatus.APPROVED, BookingStatus.ACTIVE)

class AvailabilityService:
    @staticmethod
    def has_overlap(vehicle_id, start_at, end_at, exclude_booking_id=None):
        qs = Booking.objects.filter(
            vehicle_id=vehicle_id,
            status__in=ACTIVE_STATUSES,
        ).filter(Q(start_at__lt=end_at) & Q(end_at__gt=start_at))
        if exclude_booking_id:
            qs = qs.exclude(id=exclude_booking_id)
        return qs.exists()

    @staticmethod
    def ensure_available(vehicle_id, start_at, end_at, exclude_booking_id=None):
        if AvailabilityService.has_overlap(vehicle_id, start_at, end_at, exclude_booking_id):
            raise OverlapError()
