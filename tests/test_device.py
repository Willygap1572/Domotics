import paho.mqtt.client as mqtt
import json


class TestDevices:

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
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Tester de los dummies, se queda a la escucha de todos los mensajes', usage='%(prog)s [options] id')
    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    args = parser.parse_args()
    test = TestDevices(host=args.host, port=args.port)
    try:
        test.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        exit(0)