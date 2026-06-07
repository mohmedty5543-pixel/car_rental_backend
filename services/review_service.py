from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.reviews.models import Review
from apps.bookings.models import BookingStatus

class ReviewService:
    @staticmethod
    @transaction.atomic
    def create_review(user, booking, rating, comment=''):
        if booking.status != BookingStatus.COMPLETED:
            raise ValidationError('Can only review completed bookings.')
        if booking.user_id != user.id:
            raise ValidationError('Only the booking user can review.')
        if hasattr(booking, 'review'):
            raise ValidationError('Review already exists for this booking.')
        return Review.objects.create(
            booking=booking, user=user, rating=rating, comment=comment,
        )
