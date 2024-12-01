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
        doctor = self.request.user.doctor if hasattr(self.request.user, 'doctor') else None
        if not self.request.user.is_staff and not doctor:
            raise PermissionDenied("You do not have permission to create an availability.")
        
        date = serializer.validated_data.get('date')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        # Verificar si ya existe una disponibilidad en el mismo rango de tiempo
        overlapping_availabilities = Availability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_availabilities.exists():
            raise PermissionDenied("This time slot is already occupied.")

        serializer.save(doctor=doctor)

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.doctor != self.request.user.doctor:
            raise PermissionDenied("You do not have permission to edit this availability.")
        
        date = serializer.validated_data.get('date')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        # Verificar si ya existe una disponibilidad en el mismo rango de tiempo
        overlapping_availabilities = Availability.objects.filter(
            doctor=serializer.instance.doctor,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(id=serializer.instance.id)

        if overlapping_availabilities.exists():
            raise PermissionDenied("This time slot is already occupied.")

        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.doctor != self.request.user.doctor:
            raise PermissionDenied("You do not have permission to delete this availability.")
        instance.delete()