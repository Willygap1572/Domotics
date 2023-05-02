import paho.mqtt.client as mqtt
import time
import datetime
import threading

flag = True

class Clock():
    def __init__(self, id, time, increment, rate, host, port):
        self.id = id
        self.theme = "redes2/2391/1/clock/" + str(id)
        self.broker_host = host
        self.port = port
        self.time = time
        self.increment = increment
        self.rate = rate
        self.state = self.time
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

    def get_state(self):
        return self.state

    def update_message(self):
        global flag
        while flag:
            self.state = (datetime.datetime.strptime(self.state, "%H:%M:%S") +
                           datetime.timedelta(seconds=self.increment)).strftime("%H:%M:%S")
            self.send_state()
            time.sleep(1/self.rate)

    def send_state(self):
        print("[Sending]: \n\t" + "Theme: redes2/2391/1/controler" + "\n\t" + "Message: " + str(self.state))
        self.client.publish("redes2/2391/1/controler", self.theme + ";" + str(self.state))


def checkTimeFormat(time):
    if (time.count(":") != 2 or len(time) != 8)\
      or (time.split(":")[0] > "23" or time.split(":")[1] > "59" or time.split(":")[2] > "59"):
        return False
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Simula un reloj que se comunica con un controlador mediante MQTT Mosquitto', usage='%(prog)s [options] id')

    parser.add_argument('--host', type=str, default="redes2.ii.uam.es", help='Host del broker MQTT')
    parser.add_argument('--port', '-p', type=int, default=1883, help='Puerto del broker MQTT')
    parser.add_argument('--time', '-t', type=str, default=datetime.datetime.now().strftime("%H:%M:%S"), help='Hora de inicio del reloj')
    parser.add_argument('--increment', '-i', type=int, default=1, help='Incremento de tiempo entre mensajes')
    parser.add_argument('--rate', '-r', type=int, default=1, help='Cantidad de mensajes por segundo')
    parser.add_argument('id', type=int, help='Id del reloj')
    args = parser.parse_args()
    if not args.id:
        print("[FAIL] Usage: " + parser.usage)
        exit(1)
    if checkTimeFormat(args.time) == False:
        print("[FAIL] Invalid time format")
        exit(1)
    try:
        
        clock = Clock(id=args.id, time=args.time, increment=args.increment, rate=args.rate, host=args.host, port=args.port)
        t = threading.Thread(target=clock.update_message)
        t.start()
        clock.client.loop_forever()
    except KeyboardInterrupt:
        print("[KeyboardInterrupt]: Stoping...")
        flag=False
        t.join()
        clock.client.disconnect()
        exit(0)