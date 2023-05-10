import paho.mqtt.client as mqtt
import json
import os
import django
import datetime
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'practica3.settings')
django.setup()

from domotics.models import Switch, Sensor, Clock, Rule, Activator
from domotics.constants import *


class Controller:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.theme = "redes2/2391/1/controler"
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host=host, port=port)
        self.client.subscribe(self.theme)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        source = data['theme']
        message = data['message']
        print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + str(message))
        if "switch" in data['theme']:
            if message == "ShutDown":
                try:
                    Rule.objects.filter(switch=data['aid']).delete()
                    Rule.objects.filter(activator=data['aid']).delete()
                    Switch.objects.get(aid=data['aid']).delete()
                except:
                    pass
            else:
                switch, created = Switch.objects.get_or_create(aid=data['aid'], broker_host=data['broker_host'], port=data['port'], fail=data['fail'], name=data['name'])
                switch.state = data['state']    
                switch.save()
                self.apply_rules(switch)
        if "sensor" in data['theme']:
            if message == "ShutDown":
                try:
                    Rule.objects.filter(activator=data['aid']).delete()
                    Sensor.objects.get(aid=data['aid']).delete()
                except:
                    pass
            else:
                sensor, created = Sensor.objects.get_or_create(aid=data['aid'], broker_host=data['broker_host'], port=data['port'], name=data['name'], increment=data['increment'], min=data['min'], max=data['max'], interval=data['interval'])
                sensor.state = data['state']
                sensor.save()
                self.apply_rules(sensor)
        if "clock" in data['theme']:
            if message == "ShutDown":
                try:
                    Rule.objects.filter(activator=data['aid']).delete()
                    Clock.objects.get(aid=data['aid']).delete()
                except:
                    pass
            else:
                clock, created = Clock.objects.get_or_create(aid=data['aid'], broker_host=data['broker_host'], port=data['port'], name=data['name'], time=data['time'], increment=data['increment'], rate=data['rate'])
                clock.state = data['state']
                clock.save()
                self.apply_rules(clock)
        

    def apply_rules(self, activator):
        rules = Rule.objects.filter(activator=activator)
        for rule in rules:
            if "sensor" in rule.activator.theme:
                self.sensor_rule(rule)
            if "clock" in rule.activator.theme:
                self.clock_rule(rule)
            if "switch" in rule.activator.theme:
                self.switch_rule(rule)
        
    def sensor_rule(self, rule):
        activator = Sensor.objects.get(theme=rule.activator.theme)
        switch = Switch.objects.get(theme=rule.switch.theme)
        if rule.type == GREATER:
            if int(activator.state) > int(rule.threshold) and int(switch.state) == 0:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif int(activator.state) < int(rule.threshold) and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
        elif rule.type == LOWER:
            if int(activator.state) < int(rule.threshold) and int(switch.state) == 0:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif int(activator.state) > int(rule.threshold) and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))

    def clock_rule(self, rule):
        activator = Clock.objects.get(theme=rule.activator.theme)
        switch = Switch.objects.get(theme=rule.switch.theme)
        threshold = datetime.datetime.strptime(rule.threshold, "%H:%M:%S")
        activator_state = datetime.datetime.strptime(activator.state, "%H:%M:%S")
        if rule.type == GREATER:
            if activator_state > threshold and int(switch.state) == 0: 
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif activator_state < threshold and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
        elif rule.type == LOWER:
            if activator_state < threshold and int(switch.state) == 0:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif activator_state > threshold and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))

    def switch_rule(self, rule):
        activator = Switch.objects.get(theme=rule.activator.theme)
        switch = Switch.objects.get(theme=rule.switch.theme)
        if rule.type == GREATER:
            if int(activator.state) == int(rule.threshold) and int(switch.state) == 0:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif int(activator.state) != int(rule.threshold) and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
        elif rule.type == LOWER:
            if int(activator.state) != int(rule.threshold) and int(switch.state) == 0:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'on'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))
            elif int(activator.state) == int(rule.threshold) and int(switch.state) == 1:
                message = {
                    'theme': 'redes2/2391/1/controler',
                    'message': 'off'
                }
                print("[Sending]: \n\t" + rule.switch.theme + "\n\t" + "Message: " + message['message'])
                controller.client.publish(rule.switch.theme, json.dumps(message))

    def clean_all(self):
        Sensor.objects.all().delete()
        Clock.objects.all().delete()
        Switch.objects.all().delete()
        Rule.objects.all().delete()
        print("[Clean]: All objects deleted")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simula un interriptor que se comunica con un controlador mediante MQTT Mosquitto', usage='%(prog)s [options] id')
    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    args = parser.parse_args()

    controller = Controller(host=args.host, port=args.port)
    try:
        controller.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        controller.clean_all()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)