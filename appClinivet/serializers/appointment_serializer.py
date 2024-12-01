from rest_framework import serializers
from ..models.appointment import Appointment
from ..models.availability import Availability

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'availability', 'reason', 'invoice']

    def create(self, validated_data):
        availability = validated_data.get('availability')
        if not availability:
            raise serializers.ValidationError("Availability is required to create an appointment.")
        
        # Verificar que la disponibilidad no esté ocupada
        if availability.is_occupied:
            raise serializers.ValidationError("This availability slot is already booked.")
        
        # Ocupar la disponibilidad
        availability.is_occupied = True
        availability.save()
        
        appointment = Appointment.objects.create(**validated_data)
        return appointment