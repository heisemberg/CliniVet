from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.availability import Availability
from ..serializers.availability_serializer import AvailabilitySerializer
from ..permissions import IsDoctorOrAdmin

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def perform_create(self, serializer):
        if not self.request.user.is_staff and not hasattr(self.request.user, 'doctor'):
            raise PermissionDenied("You do not have permission to create an availability.")
        serializer.save(doctor=self.request.user.doctor)

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.doctor != self.request.user.doctor:
            raise PermissionDenied("You do not have permission to edit this availability.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.doctor != self.request.user.doctor:
            raise PermissionDenied("You do not have permission to delete this availability.")
        instance.delete()