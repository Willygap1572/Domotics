import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    source, message = msg.payload.decode().split(';')
    print("[Received]: \n\t" + "Theme: " + msg.topic + "\n\t" + "From: " + source + "\n\t" + "Message: " + message)
    
if __name__ == '__main__':
    # creamos el cliente
    client = mqtt.Client()
    # indicamos las funciones de callback
    client.on_message = on_message
    # nos conectamos al broker
    client.connect(host='localhost', port=1883)
    client.subscribe('redes2/2391/1/controler')
    
    # publicamos un mensaje
    print("[Sending]: \n\t" + "Theme: redes2/2391/1/sensor/1" + "\n\t" + "Message " + "ShutDown")
    client.publish('redes2/2391/1/sensor/1', 'redes2/2391/1/controler;ShutDown')
    # bucle de espera de mensajes
    client.loop_forever()
        