from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models.medical_record import MedicalRecord
from ..models.appointment import Appointment
from ..models.availability import Availability
from ..serializers.medical_record_serializer import MedicalRecordSerializer
from ..permissions import IsDoctorOrAdmin

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.all()
        if hasattr(user, 'doctor'):
            return MedicalRecord.objects.filter(doctor=user.doctor)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff and not hasattr(user, 'doctor'):
            raise PermissionDenied("You do not have permission to create a medical record.")
        
        # Verificar que el médico tenga una cita asignada y esté disponible en la franja horaria correspondiente
        pet = serializer.validated_data.get('pet')
        date = serializer.validated_data.get('date')
        time = serializer.validated_data.get('time')
        
        try:
            appointment = Appointment.objects.get(pet=pet, availability__date=date, availability__start_time__lte=time, availability__end_time__gte=time, availability__doctor=user.doctor)
        except Appointment.DoesNotExist:
            raise PermissionDenied("You do not have an appointment assigned for this pet at the specified time.")
        
        try:
            availability = Availability.objects.get(doctor=user.doctor, date=date, start_time__lte=time, end_time__gte=time)
        except Availability.DoesNotExist:
            raise PermissionDenied("You are not available at the specified time.")
        
        serializer.save(doctor=user.doctor)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this medical record.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this medical record.")
        instance.delete()