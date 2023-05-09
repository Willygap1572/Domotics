import paho.mqtt.client as mqtt
import time
import json

flag = True


class Sensor():

    def __init__(self, aid, minim, maxim, interval, increment, host, port, state=None, name=None):
        self.aid = aid
        if name is None:
            self.name = "Sensor" + str(aid)
        else:
            self.name = name
        self.theme = "redes2/2391/1/sensor/" + str(aid)
        self.broker_host = host
        self.port = port
        self.min = minim
        self.max = maxim
        self.interval = interval
        self.increment = increment
        if state is None:
            self.state = self.min
        else:
            self.state = state
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host=host, port=port)
        self.client.subscribe(self.theme)

    def on_message(self, client, userdata, msg):
        global flag
        message = json.loads(msg.payload.decode())
        source = message['theme']
        message = message['message']
        print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + message)
        if message == "ShutDown":
            print("[ShutDown]: Shutting down...")
            flag=False
            exit(0)

    def get_sensor_dict(self):
        sensor_dict = {
            "aid": self.aid,
            "name": self.name,
            "theme": self.theme,
            "broker_host": self.broker_host,
            "port": self.port,
            "min": self.min,
            "max": self.max,
            "interval": self.interval,
            "increment": self.increment,
            "state": self.state
        }
        return sensor_dict


    def get_state(self):
        return self.state

    def update_message(self):
        global flag
        while flag:
            #self.state = random.randint(self.min, self.max)
            self.state = self.state + self.increment
            if self.state > self.max:
                self.state = self.min
            self.send_state()
            time.sleep(self.interval)

    def send_state(self):
        data = self.get_sensor_dict()
        data['message'] = self.state
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + str(self.state))
        self.client.publish("redes2/2391/1/controler", json.dumps(data))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Simula un sensor que se comunica con un controlador mediante MQTT Mosquitto', usage='%(prog)s [options] id')

    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    parser.add_argument('--interval', '-i', type=int, default=1, help='Intervalo de tiempo entre mensajes')
    parser.add_argument('--min', '-m', type=int, default=20, help='Valor mínimo del sensor')
    parser.add_argument('--max', '-M', type=int, default=30, help='Valor máximo del sensor')
    parser.add_argument('--increment', '-inc', type=int, default=1, help='Incremento del valor del sensor')
    parser.add_argument('id', type=int, help='Id del sensor')
    args = parser.parse_args()
    if not args.id:
        print("[FAIL] Usage: " + parser.usage)
        exit(1)
    sensor = Sensor(aid=args.id, minim=args.min, maxim=args.max, interval=args.increment, increment=args.increment, host=args.host, port=args.port)
    try:
        import threading
        t = threading.Thread(target=sensor.update_message)
        t.start()
        sensor.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        flag = False
        t.join()
        data = sensor.get_sensor_dict()
        data['message'] = "ShutDown"
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + str(data['message']))
        sensor.client.publish("redes2/2391/1/controler", json.dumps(data))
        sensor.client.disconnect()
        exit(0)