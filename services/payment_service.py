from django.db import transaction
from apps.payments.models import Payment, PaymentStatus
from core.exceptions import InvalidTransition

class PaymentService:
    @staticmethod
    @transaction.atomic
    def create_payment(booking, amount, method, reference=''):
        return Payment.objects.create(
            booking=booking, amount=amount, method=method,
            status=PaymentStatus.PENDING, reference=reference,
        )

    @staticmethod
    @transaction.atomic
    def mark_paid(payment: Payment):
        if payment.status != PaymentStatus.PENDING:
            raise InvalidTransition()
        payment.status = PaymentStatus.PAID
        payment.save(update_fields=['status','updated_at'])
        return payment

    @staticmethod
    @transaction.atomic
    def refund(payment: Payment):
        if payment.status != PaymentStatus.PAID:
            raise InvalidTransition()
        payment.status = PaymentStatus.REFUNDED
        payment.save(update_fields=['status','updated_at'])
        return payment
