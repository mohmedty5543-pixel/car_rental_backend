from django.db.models import Q

from rest_framework import viewsets, permissions
from apps.users.models import UserRole
from core.permissions import IsVendorOwnerOrStaff
from .models import Driver
from .serializers import DriverSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('vendor')
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwnerOrStaff]
    filterset_fields = ('vendor','is_active')
    search_fields = ('full_name','license_number')

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'role', None) == UserRole.ADMIN:
            return Driver.objects.select_related('vendor')

        return Driver.objects.select_related('vendor').filter(
            Q(vendor__owner_user=user) |
            Q(vendor__members__user=user)
        ).distinct()
