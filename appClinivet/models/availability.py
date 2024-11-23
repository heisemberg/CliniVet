from django.db import models
from .doctor import Doctor

class Availability(models.Model):
    id = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, related_name='availabilities', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_occupied = models.BooleanField(default=False)  # Campo para indicar si la disponibilidad está ocupada

    def __str__(self):
        return f"Availability for Dr. {self.doctor.last_name} on {self.date} from {self.start_time} to {self.end_time}"