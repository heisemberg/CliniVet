from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.appointment import Appointment
from ..serializers.appointment_serializer import AppointmentSerializer
from ..permissions import IsOwnerOrDoctorOrAdmin

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrDoctorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        if hasattr(user, 'doctor'):
            return Appointment.objects.filter(availability__doctor=user.doctor)
        return Appointment.objects.filter(pet__owner=user.client)