from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Vehicle, VehicleImage, VehicleAvailability, FavoriteVehicle, VehicleStatus
from .serializers import (
    VehicleSerializer,
    VehicleImageSerializer,
    VehicleAvailabilitySerializer,
    FavoriteVehicleSerializer,
)
from apps.users.models import UserRole
from apps.vendors.models import VendorMember

from core.permissions import IsVendorOwnerOrStaff


# =========================
# 🚗 VEHICLE VIEWSET
# =========================
class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsVendorOwnerOrStaff]

    filterset_fields = ('vendor', 'status', 'make', 'model', 'year')
    search_fields = ('make', 'model', 'location', 'license_plate')
    ordering_fields = ('daily_rate', 'created_at', 'year')

    def get_queryset(self):
        queryset = Vehicle.objects.select_related('vendor').prefetch_related('images')
        if self.request.method in permissions.SAFE_METHODS:
            if self.request.user and self.request.user.is_authenticated:
                accessible_vendor_ids = list(self.request.user.owned_vendors.values_list('id', flat=True))
                accessible_vendor_ids += list(self.request.user.vendor_memberships.values_list('vendor_id', flat=True))
                if accessible_vendor_ids:
                    return queryset.filter(
                        Q(status=VehicleStatus.ACTIVE) | Q(vendor_id__in=accessible_vendor_ids)
                    )
            return queryset.filter(status=VehicleStatus.ACTIVE)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        vendor = serializer.validated_data.get('vendor')

        if not vendor:
            raise PermissionDenied("Vendor is required")

        # Admin can create vehicles for any vendor
        if getattr(user, 'role', None) == 'ADMIN':
            serializer.save()
            return

        # ownership check
        is_owner = vendor.owner_user_id == user.id

        # membership check
        is_member = vendor.members.filter(user=user).exists()

        print(f"DEBUG perform_create: user={user.email} (id={user.id}, role={getattr(user, 'role', None)})")
        print(f"DEBUG perform_create: vendor={vendor.name} (id={vendor.id}, owner_user_id={vendor.owner_user_id})")
        print(f"DEBUG perform_create: is_owner={is_owner}, is_member={is_member}")

        if not (is_owner or is_member):
            raise PermissionDenied(
                f"You are not allowed to create vehicles for this vendor. (Logged in: {user.email}, Vendor owner: {vendor.owner_user.email if vendor.owner_user else 'None'})"
            )

        serializer.save()


# =========================
# 🖼️ VEHICLE IMAGES
# =========================
class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwnerOrStaff]

    def perform_create(self, serializer):
        vehicle = serializer.validated_data.get('vehicle')
        user = self.request.user

        if not (
            vehicle.vendor.owner_user_id == user.id or
            vehicle.vendor.members.filter(user=user).exists()
        ):
            raise PermissionDenied("Not allowed")

        serializer.save()


# =========================
# 📅 AVAILABILITY
# =========================
class VehicleAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = VehicleAvailability.objects.all()
    serializer_class = VehicleAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwnerOrStaff]


# =========================
# ⭐ FAVORITES (CUSTOMER)
# =========================
class FavoriteVehicleViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteVehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteVehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)