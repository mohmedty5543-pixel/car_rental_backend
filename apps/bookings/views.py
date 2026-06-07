from django.db.models import Q
from rest_framework import viewsets, status, decorators, response
from apps.users.models import UserRole
from .models import Booking
from .serializers import BookingReadSerializer, BookingWriteSerializer
from services.booking_service import BookingService

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('user','vehicle','driver')
    filterset_fields = ('status','type','vehicle','user')
    ordering_fields = ('created_at','start_at')

    def get_queryset(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            return Booking.objects.none()

        if getattr(user, 'role', None) == UserRole.ADMIN:
            return Booking.objects.select_related('user', 'vehicle', 'driver')

        return Booking.objects.filter(
            Q(user=user) |
            Q(vehicle__vendor__owner_user=user) |
            Q(vehicle__vendor__members__user=user)
        ).select_related('user', 'vehicle', 'driver').distinct()

    def get_serializer_class(self):
        return BookingWriteSerializer if self.action in ('create','update','partial_update')             else BookingReadSerializer

    def perform_create(self, serializer):
        booking = BookingService.create_request(
            user=self.request.user, **serializer.validated_data
        )
        serializer.instance = booking

    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        b = BookingService.approve(self.get_object(), actor=request.user)
        return response.Response(BookingReadSerializer(b).data)

    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        b = BookingService.reject(self.get_object(), actor=request.user)
        return response.Response(BookingReadSerializer(b).data)

    @decorators.action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        b = BookingService.cancel(self.get_object(), actor=request.user)
        return response.Response(BookingReadSerializer(b).data)

    @decorators.action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        b = BookingService.complete(self.get_object(), actor=request.user)
        return response.Response(BookingReadSerializer(b).data)

    @decorators.action(detail=True, methods=['post'], url_path='assign-driver')
    def assign_driver(self, request, pk=None):
        driver_id = request.data.get('driver_id')
        b = BookingService.assign_driver(self.get_object(), driver_id=driver_id)
        return response.Response(BookingReadSerializer(b).data)
