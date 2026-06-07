from django.db.models import Q

from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.users.models import UserRole
from .models import Vendor, VendorMember
from .serializers import VendorSerializer, VendorMemberSerializer
from services.vendor_service import VendorService

from core.permissions import (
    IsVendorOwnerOrStaff,
    IsVendorStaffOrAdmin
)


# =====================================================
# VENDOR VIEWSET
# =====================================================
class VendorViewSet(viewsets.ModelViewSet):
    """
    Vendor CRUD (multi-tenant safe)
    """

    serializer_class = VendorSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ("type", "is_verified", "owner_user")
    search_fields = ("name", "description")
    ordering_fields = ("created_at", "name")

    # NOTE: queryset is overridden by get_queryset for security
    queryset = Vendor.objects.all()

    def get_permissions(self):
        """
        Permission rules:
        - CREATE: only STAFF or ADMIN
        - UPDATE/DELETE: owner or staff
        - LIST/RETRIEVE: authenticated users
        """

        if self.action == "create":
            return [IsVendorStaffOrAdmin()]

        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsVendorOwnerOrStaff()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Force owner = request.user (prevents spoofing)
        """
        VendorService.create_vendor(
            owner=self.request.user,
            serializer=serializer,
        )

    def get_queryset(self):
        """
        SECURITY:
        - ADMIN sees all vendors
        - USER sees only:
            - vendors they own
            - vendors they are members of
        - Safe methods (list/retrieve) are open to all authenticated users
        """

        user = self.request.user

        if not user.is_authenticated:
            return Vendor.objects.none()

        if getattr(user, "role", None) == "ADMIN":
            return Vendor.objects.all()

        if self.action in ("list", "retrieve"):
            return Vendor.objects.all()

        return Vendor.objects.filter(
            Q(owner_user=user) |
            Q(members__user=user)
        ).distinct()


# =====================================================
# VENDOR MEMBER VIEWSET
# =====================================================
class VendorMemberViewSet(viewsets.ModelViewSet):
    """
    Manage vendor team members
    """

    serializer_class = VendorMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = VendorMember.objects.select_related("vendor", "user")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("vendor", "user", "role")

    def get_queryset(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            return VendorMember.objects.none()

        if getattr(user, 'role', None) == UserRole.ADMIN:
            return self.queryset

        return VendorMember.objects.filter(
            Q(vendor__owner_user=user) |
            Q(vendor__members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Only vendor owner or admin can add members
        """

        vendor = serializer.validated_data["vendor"]
        user = self.request.user

        is_owner = vendor.owner_user_id == user.id
        is_admin = getattr(user, "role", None) == "ADMIN"

        if not (is_owner or is_admin):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only vendor owner or admin can add members."
            )

        serializer.save()