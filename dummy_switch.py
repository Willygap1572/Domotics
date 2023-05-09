import paho.mqtt.client as mqtt
import random
import json


class Switch():

    def __init__(self, aid, host, port, fail, name=None, state=False):
        self.aid = aid
        if name is None:
            self.name = "Switch" + str(aid)
        else:
            self.name = name
        self.theme = "redes2/2391/1/switch/" + str(aid)
        self.state = int(state)
        self.broker_host = host
        self.port = port
        self.fail = fail
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host=host, port=port)
        self.client.subscribe(self.theme)
        switch_dict = self.switch_to_dict()
        switch_dict['message'] = 'off'
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + 'off')
        self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))

    def switch_to_dict(self):
        switch_dict = {
            'aid': self.aid,
            'name': self.name,
            'theme': self.theme,
            'state': self.state,
            'broker_host': self.broker_host,
            'port': self.port,
            'fail': self.fail
        }
        return switch_dict

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode())
        source = message['theme']
        message = message['message']
        print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + message)
        if message == "toggle":
            self.toggle_state()
        elif message == 'on':
            self.set_on()
        elif message == 'off':
            self.set_off()

    def set_on(self):
        if random.random() > self.fail:
            self.state = 1
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'on'
            print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + 'on')
            self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))
        else:
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'Failure'
            print("[FAIL] El interruptor " + str(self.aid) + " ha fallado")
            self.client.publish("redes2/2391/1/controler", self.theme + ';' + f"Switch {self.aid} failed")

    def set_off(self):
        if random.random() > self.fail:
            self.state = 0
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'off'
            print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + 'off')
            self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))
        else:
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'Faliure'
            print("[FAIL] El interruptor " + str(self.aid) + " ha fallado")
            self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))

    def toggle_state(self):
        if random.random() > self.fail:
            self.state = int(not bool(self.state))
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'off' if self.state == 0 else 'on'
            print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + switch_dict['message'])
            self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))
        else:
            switch_dict = self.switch_to_dict()
            switch_dict['message'] = 'Faliure'
            print("[FAIL] El interruptor " + str(self.aid) + " ha fallado")
            self.client.publish("redes2/2391/1/controler", json.dumps(switch_dict))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Simula un interriptor que se comunica con un controlador mediante MQTT Mosquitto', usage='%(prog)s [options] id')
    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    parser.add_argument('--probability', '-P', type=float, default=0.3, help='Probabilidad de fallo')
    parser.add_argument('id', type=int, help='Id del interruptor')
    args = parser.parse_args()
    if not args.id:
        print("[FAIL] Usage: " + parser.usage)
        exit(1)
    switch = Switch(aid=args.id, host=args.host, port=args.port, fail=args.probability)
    try:
        switch.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        data = switch.switch_to_dict()
        data['message'] = "ShutDown"
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + str(data['message']))
        switch.client.publish("redes2/2391/1/controler", json.dumps(data))
        switch.client.disconnect()
        exit(0)
    exit(0)