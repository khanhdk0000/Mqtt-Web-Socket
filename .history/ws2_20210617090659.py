import sys
import paho.mqtt.client as mqtt

BROKER = 'io.adafruit.com'
USER = 'khanhdk0000'
PASSWORD = 'aio_FfID10QWNVSKUC2j15nLtOSeckin'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0:
        print('good')
    else:
        print('no good')

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))


client = mqtt.Client()
client.username_pw_set(username=USER,password=password)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect(BROKER, 1883, 60)
client.subscribe(topic)
client.loop_forever()