from rest_framework import permissions
from apps.users.models import UserRole
from apps.vendors.models import Vendor, VendorMember, VendorMemberRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsVendorStaffOrAdmin(permissions.BasePermission):
    """
    Allow only STAFF or ADMIN to create/manage vendors.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in (UserRole.ADMIN, UserRole.VENDOR_STAFF, UserRole.VENDOR_OWNER)


class IsVendorOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission:
    - owner_user
    - OR vendor members (STAFF/MANAGER)
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if not user or not user.is_authenticated:
            return False

        vendor = obj if isinstance(obj, Vendor) else getattr(obj, "vendor", None)

        if vendor is None:
            return False

        # ✅ Owner full access
        if vendor.owner_user_id == user.id:
            return True

        # ✅ Admin full access
        if getattr(user, 'role', None) == UserRole.ADMIN:
            return True

        return VendorMember.objects.filter(
            vendor=vendor,
            user=user,
            role__in=[VendorMemberRole.STAFF, VendorMemberRole.MANAGER]
        ).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Generic ownership permission.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        owner = getattr(obj, "user", None) or getattr(obj, "owner_user", None)
        return owner == user