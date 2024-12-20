from django.db import models
from .pet import Pet
from .availability import Availability

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.BigAutoField(primary_key=True)
    pet = models.ForeignKey(Pet, related_name='appointments', on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, related_name='appointments', on_delete=models.CASCADE)
    reason = models.CharField('Reason', max_length=255)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.availability.date} at {self.availability.start_time}"