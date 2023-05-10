import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'practica3.settings')
django.setup()

from domotics.models import Switch, Sensor, Clock, Rule, Activator
from domotics.constants import *

if __name__ == '__main__':

    switch = Switch.objects.all().first()
    sensor = Sensor.objects.all().first()
    activator = Activator.objects.filter(theme=sensor.theme).first()
    Rule.objects.create(switch=switch, activator=activator, type=GREATER, threshold=25, description="Test rule")

