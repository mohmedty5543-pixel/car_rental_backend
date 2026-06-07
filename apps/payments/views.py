from rest_framework import viewsets, decorators, response
from .models import Payment
from .serializers import PaymentSerializer
from services.payment_service import PaymentService

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('booking')
    serializer_class = PaymentSerializer
    filterset_fields = ('booking','status','method')

    def perform_create(self, serializer):
        p = PaymentService.create_payment(**serializer.validated_data)
        serializer.instance = p

    @decorators.action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        p = PaymentService.mark_paid(self.get_object())
        return response.Response(PaymentSerializer(p).data)

    @decorators.action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        p = PaymentService.refund(self.get_object())
        return response.Response(PaymentSerializer(p).data)
