import time
import random

import threading

BROKER = 'io.adafruit.com'
USER = 'khanhdk0000'
PASSWORD = 'aio_FfID10QWNVSKUC2j15nLtOSeckin'

TOPIC = 'khanhdk0000/feeds/'
LIGHT = 'light'
SOUND = 'sound'
TEMP = 'temp'
LCD = 'iot_led'
BUZZER = 'buzzer'


def mqttGet(user, password,topic,device):
    import paho.mqtt.client as mqtt
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


    client = mqtt.Client(transport="websockets")
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_soc


    client.connect(BROKER, 2000, 60)
    client.subscribe(topic)
    client.loop_forever()

mqttGet(USER, PASSWORD,TOPIC + LIGHT, LIGHT)