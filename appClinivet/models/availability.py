from django.db import models
from .doctor import Doctor

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='availabilities', on_delete=models.CASCADE)
    date = models.DateField('Date')
    start_time = models.TimeField('Start Time')
    end_time = models.TimeField('End Time')

    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')