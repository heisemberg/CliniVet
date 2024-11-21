from django.db import models
from .pet import Pet

class MedicalRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    pet = models.ForeignKey(Pet, related_name='medical_records', on_delete=models.CASCADE)
    description = models.TextField('Description')
    date = models.DateTimeField('Date')
    weight = models.DecimalField('Weight (kg)', max_digits=5, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField('Temperature (°C)', max_digits=4, decimal_places=1, null=True, blank=True)
    diagnosis = models.TextField('Diagnosis', blank=True, null=True)
    treatment = models.TextField('Treatment', blank=True, null=True)
    next_appointment = models.DateTimeField('Next Appointment', null=True, blank=True)
    doctor = models.ForeignKey('Doctor', related_name='medical_records', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date']