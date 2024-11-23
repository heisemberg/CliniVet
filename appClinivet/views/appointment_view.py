from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from ..models.appointment import Appointment
from ..models.availability import Availability
from ..serializers.appointment_serializer import AppointmentSerializer
from ..permissions import IsOwnerOrDoctorOrAdmin, IsAdminOrReadOnly

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrDoctorOrAdmin, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        if hasattr(user, 'doctor'):
            return Appointment.objects.filter(availability__doctor=user.doctor)
        return Appointment.objects.filter(client=user.client)

    def perform_create(self, serializer):
        availability = serializer.validated_data.get('availability')
        if not availability:
            raise PermissionDenied("Availability is required to create an appointment.")
        
        # Verificar que la disponibilidad no esté ocupada
        if availability.is_occupied:
            raise PermissionDenied("This availability slot is already booked.")
        
        # Ocupar la disponibilidad
        availability.is_occupied = True
        availability.save()
        
        serializer.save(client=self.request.user.client)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this appointment.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this appointment.")
        
        # Liberar la disponibilidad
        availability = instance.availability
        availability.is_occupied = False
        availability.save()
        
        instance.delete()