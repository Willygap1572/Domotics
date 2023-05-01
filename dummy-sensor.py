# clase Sensor que genera valores aleatorios entre min y max cada -m minutos y los publica en el tema redes2/2391/1/controler

import paho.mqtt.client as mqtt
import random
import time

flag = True

class Sensor():
    def __init__(self, id, min, max, interval, host="redes2.ii.uam.es", port=1883):
        self.id = id
        self.theme = "redes2/2391/1/sensor/" + str(id)
        self.broker_host = host
        self.port = port
        self.min = min
        self.max = max
        self.interval = interval
        self.state = 0
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host=host, port=port)
        self.client.subscribe(self.theme)

    def on_message(self, client, userdata, msg):
        global flag
        source, message = msg.payload.decode().split(';')
        print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + message)
        if message == "ShutDown":
            print("[ShutDown]: Shutting down...")
            flag=False
            exit(0)
            

    def __str__(self):
        return self.name

    def get_state(self):
        return self.state

    def update_message(self):
        global flag
        while flag:
        
            self.state = random.randint(self.min, self.max)
            self.send_state()
            time.sleep(self.interval)
    

    def send_state(self):
        self.state = random.randint(self.min, self.max)
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + str(self.state))
        self.client.publish("redes2/2391/1/controler", self.theme + ";" + str(self.state))

# hacer un main que reciba los argumentos y cree un sensor
# los argumentos son --interval, -min, -max, -host, -port, --increment

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Simula un sensor que se comunica con un controlador mediante MQTT Mosquitto', usage='%(prog)s [options] id')

    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    parser.add_argument('--interval', '-i', type=int, default=1, help='Intervalo de tiempo entre mensajes')
    parser.add_argument('--min', '-m', type=int, default=20, help='Valor mínimo del sensor')
    parser.add_argument('--max', '-M', type=int, default=30, help='Valor máximo del sensor')
    parser.add_argument('id', type=int, help='Id del sensor')
    args = parser.parse_args()
    if not args.id:
        print("[FAIL] Usage: " + parser.usage)
    try:
        sensor = Sensor(id=args.id, min=args.min, max=args.max, interval=args.interval, host=args.host, port=args.port)
        # crear un hilo para que se actualice el mensaje cada intervalo de tiempo
        import threading
        t = threading.Thread(target=sensor.update_message)
        t.start()
        sensor.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        flag = False
        t.join()
        sensor.client.disconnect()
        exit(0)