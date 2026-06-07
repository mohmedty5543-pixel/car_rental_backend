from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from services.review_service import ReviewService

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('booking','user')
    serializer_class = ReviewSerializer
    filterset_fields = ('booking','user','rating','booking__vehicle__vendor')

    def perform_create(self, serializer):
        r = ReviewService.create_review(user=self.request.user, **serializer.validated_data)
        serializer.instance = r
