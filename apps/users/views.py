from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserReadSerializer,
    UserRegisterSerializer,
    ChangePasswordSerializer,
    DeleteAccountSerializer,
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserReadSerializer
    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data.get("password")
        if not user.check_password(password):
            return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import viewsets
from rest_framework.decorators import action
from apps.users.permissions import IsAdmin
from apps.vendors.models import Vendor
from apps.vendors.serializers import VendorSerializer
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingReadSerializer
from .serializers import AdminUserRoleUpdateSerializer, AdminVendorVerifySerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def delete_account(self, request):
        """
        Allow users to delete their own account.
        Requires password confirmation.
        """
        serializer = DeleteAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data.get("password")
        if not user.check_password(password):
            return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"detail": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserReadSerializer
    permission_classes = [IsAdmin]


class AdminVendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all().order_by('-created_at')
    serializer_class = VendorSerializer
    permission_classes = [IsAdmin]


class AdminBookingListView(generics.ListAPIView):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingReadSerializer
    permission_classes = [IsAdmin]


class AdminUserRoleUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserRoleUpdateSerializer
    permission_classes = [IsAdmin]


class AdminUserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAdmin]


class AdminVendorVerifyView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorVerifySerializer
    permission_classes = [IsAdmin]

