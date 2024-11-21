from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.appointment import Appointment
from ..serializers.appointment_serializer import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]