from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import (
    RegisterView,
    MeView,
    ChangePasswordView,
    DeleteAccountView,
    UserViewSet,
    AdminUserListView,
    AdminVendorListView,
    AdminBookingListView,
    AdminUserRoleUpdateView,
    AdminUserDeleteView,
    AdminVendorVerifyView,
)
from apps.vendors.views import VendorViewSet, VendorMemberViewSet
from apps.vehicles.views import (
    VehicleViewSet, VehicleImageViewSet, VehicleAvailabilityViewSet,
    FavoriteVehicleViewSet,
)
from apps.bookings.views import BookingViewSet
from apps.payments.views import PaymentViewSet
from apps.deliveries.views import DeliveryViewSet
from apps.reviews.views import ReviewViewSet
from apps.drivers.views import DriverViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('vendors', VendorViewSet)
router.register('vendor-members', VendorMemberViewSet)
router.register('vehicles', VehicleViewSet, basename='vehicles')
router.register('vehicle-images', VehicleImageViewSet)
router.register('vehicle-availability', VehicleAvailabilityViewSet)
router.register('favorites', FavoriteVehicleViewSet, basename='favorites')
router.register('bookings', BookingViewSet)
router.register('payments', PaymentViewSet)
router.register('deliveries', DeliveryViewSet)
router.register('reviews', ReviewViewSet)
router.register('drivers', DriverViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/vendors/', AdminVendorListView.as_view(), name='admin_vendors'),
    path('admin/bookings/', AdminBookingListView.as_view(), name='admin_bookings'),
    path('admin/users/<uuid:pk>/role/', AdminUserRoleUpdateView.as_view(), name='admin_user_role'),
    path('admin/users/<uuid:pk>/', AdminUserDeleteView.as_view(), name='admin_user_delete'),
    path('admin/vendors/<uuid:pk>/verify/', AdminVendorVerifyView.as_view(), name='admin_vendor_verify'),
    path('', include(router.urls)),
]

