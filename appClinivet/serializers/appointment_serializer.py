from rest_framework import serializers
from ..models.appointment import Appointment
from ..models.availability import Availability

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'availability', 'reason', 'invoice', 'status']
        read_only_fields = ['invoice', 'status']

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
        
        # Crear la cita
        appointment = Appointment.objects.create(**validated_data)
        return appointment

    def update(self, instance, validated_data):
        # Aquí puedes agregar lógica adicional si es necesario
        return super().update(instance, validated_data)