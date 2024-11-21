from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.availability import Availability
from ..serializers.availability_serializer import AvailabilitySerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]