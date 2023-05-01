from django.db import models
from django.utils import timezone

class Switch(models.Model):
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Sensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Clock(models.Model):
    name = models.CharField(max_length=100)
    time = models.TimeField(default=timezone.now().strftime('%H:%M:%S'), blank=True)
    def __str__(self):
        return self.name

