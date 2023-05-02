import paho.mqtt.client as mqtt
import random

class Switch():
    def __init__(self, id, host, port, fail, state=False):
        self.id = id
        self.theme = "redes2/2391/1/switch/" + str(id)
        self.state = state
        self.broker_host = host
        self.port = port
        self.fail = fail
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host=host, port=port)
        self.client.subscribe(self.theme)
        

    def on_message(self, client, userdata, msg):
        source, message = msg.payload.decode().split(';')
        print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + message)
        if message == "toggle":
            self.toggle_state()

    def get_state(self):
        return self.state

    def toggle_state(self):
        if random.random() > self.fail:
            self.state = not self.state
            print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + ("on" if self.state else "off"))
            self.client.publish("redes2/2391/1/controler", self.theme + ';' + ("on" if self.state else "off"))
        else:
            print("[FAIL] El interruptor " + str(self.id) + " ha fallado")
            self.client.publish("redes2/2391/1/controler", self.theme + ';' + f"Toggle Switch {self.id} failed")

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
    switch = Switch(id=args.id, host=args.host, port=args.port, fail=args.probability)
    switch.client.loop_forever()
    exit(0)