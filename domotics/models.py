from django.db import models
from django.utils import timezone
import datetime
import uuid
from .constants import *


class Activator(models.Model):
    name = models.CharField(max_length=100, default=None)
    broker_host = models.CharField(max_length=100, default='redes2.ii.uam.es')
    theme = models.CharField(max_length=100, default='redes2/2391/1/')
    port = models.IntegerField(default=1883)
    state = models.CharField(max_length=255, default='N/A')


class Switch(Activator):
    
    aid = models.IntegerField(default=uuid.uuid4(), primary_key=True)
    fail = models.FloatField(default=0.3)

    def save(self, *args, **kwargs):
        self.name = f"Switch{str(self.aid)}"
        self.theme = f"redes2/2391/1/switch/{str(self.aid)}"
        super().save(*args, **kwargs)
    

class Sensor(Activator):
    
    aid = models.IntegerField(default=uuid.uuid4(), primary_key=True)
    min = models.IntegerField(default=20)
    max = models.IntegerField(default=30)
    interval = models.IntegerField(default=1)
    increment = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.name = f"Sensor{str(self.aid)}"
        self.theme = f"redes2/2391/1/sensor/{str(self.aid)}"
        super().save(*args, **kwargs)
    

class Clock(Activator):
    aid = models.IntegerField(default=uuid.uuid4() ,primary_key=True)
    time = models.CharField(max_length=255, default=datetime.datetime.now().strftime("%H:%M:%S"))
    increment = models.IntegerField(default=1)
    rate = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.name = f"Clock{str(self.aid)}"
        self.theme = f"redes2/2391/1/clock/{str(self.aid)}"
        super().save(*args, **kwargs)
    

class Rule(models.Model):
    CHOICES = {
        (GREATER, 'GREATER'),
        (LOWER, 'LOWER'),
    }

    activator = models.ForeignKey(Activator, on_delete=models.CASCADE)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='switch_rules')
    threshold = models.CharField(default=None, max_length=255)
    type = models.PositiveIntegerField(choices=CHOICES, default=1)
    description = models.CharField(max_length=255, default=None)