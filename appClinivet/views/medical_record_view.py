from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.medical_record import MedicalRecord
from ..serializers.medical_record_serializer import MedicalRecordSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]