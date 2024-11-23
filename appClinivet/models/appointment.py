from django.db import models
from .pet import Pet
from .availability import Availability
from .invoice import Invoice

class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)
    pet = models.ForeignKey(Pet, related_name='appointments', on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, related_name='appointments', on_delete=models.CASCADE)
    reason = models.CharField('Reason', max_length=255)
    invoice = models.OneToOneField(Invoice, related_name='appointment', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.availability.date} at {self.availability.start_time}"