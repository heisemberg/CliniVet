from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.medical_record import MedicalRecord
from ..serializers.medical_record_serializer import MedicalRecordSerializer
from ..permissions import IsDoctorOrAdmin, IsAdminOrReadOnly

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.all()
        if hasattr(user, 'doctor'):
            return MedicalRecord.objects.filter(doctor=user.doctor)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_staff and not hasattr(self.request.user, 'doctor'):
            raise PermissionDenied("You do not have permission to create a medical record.")
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this medical record.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this medical record.")
        instance.delete()