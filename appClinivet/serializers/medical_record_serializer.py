from rest_framework import serializers
from ..models.medical_record import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'description', 'date', 'weight', 'temperature', 'diagnosis', 'treatment', 'next_appointment', 'doctor', 'client', 'pet']