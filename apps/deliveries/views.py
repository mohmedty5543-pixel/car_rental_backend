from django.db.models import Q

from rest_framework import viewsets, permissions
from apps.users.models import UserRole
from core.permissions import IsVendorOwnerOrStaff
from .models import Delivery
from .serializers import DeliverySerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.select_related('booking')
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwnerOrStaff]
    filterset_fields = ('status','type','booking')

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'role', None) == UserRole.ADMIN:
            return Delivery.objects.select_related('booking')

        return Delivery.objects.select_related('booking').filter(
            Q(booking__vehicle__vendor__owner_user=user) |
            Q(booking__vehicle__vendor__members__user=user) |
            Q(booking__user=user)
        ).distinct()
