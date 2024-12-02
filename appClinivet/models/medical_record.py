from django.db import models
from .doctor import Doctor
from .client import Client
from .pet import Pet
from .appointment import Appointment

class MedicalRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField('Description')
    date = models.DateField('Date')
    weight = models.DecimalField('Weight', max_digits=5, decimal_places=2)
    temperature = models.DecimalField('Temperature', max_digits=4, decimal_places=1)
    diagnosis = models.TextField('Diagnosis')
    treatment = models.TextField('Treatment')
    next_appointment = models.DateField('Next Appointment', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, related_name='medical_records', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='medical_records', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, related_name='medical_records', on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, related_name='medical_records', on_delete=models.CASCADE)

    def __str__(self):
        return f"Medical Record for {self.pet.name} by {self.doctor.name} on {self.date}"