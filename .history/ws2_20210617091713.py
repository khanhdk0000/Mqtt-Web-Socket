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

########################################################
resLight = '"id":"13","name":"LIGHT","data":"0","unit":""'
prevLight = resLight
timeLight, prevTimeLight = 0, 0

resTemp = '"id":"7","name":"SOUND","data":"0","unit":""'
prevTemp = resTemp
timeTemp, prevTimeTemp = 0, 0

resSound = '"id":"12","name":"TEMP-HUMID","data":"0","unit":""'
prevSound = resSound
timeSound, prevTimeSound = 0, 0

resBuzzer = '"id":"2","name":"SPEAKER","data":"0","unit":""'
prevBuzzer = resBuzzer
timeBuzzer, prevTimeBuzzer = 0, 0

resLCD = '"id":"3","name":"LCD","data":"0","unit":""'
prevLCD= resLCD
timeLCD, prevTimeLCD = 0, 0


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
        if device == LIGHT:
            global resLight, timeLight
            message = str(message.payload.decode("utf-8"))
            resLight = message
            timeLight += 1
        elif device == TEMP:
            global resTemp, timeTemp
            message = str(message.payload.decode("utf-8"))
            resTemp = message
            timeTemp += 1
        elif device == SOUND:
            global resSound, timeSound
            message = str(message.payload.decode("utf-8"))
            resSound = message
            timeSound += 1
        elif device == BUZZER:
            global resBuzzer, timeBuzzer
            message = str(message.payload.decode("utf-8"))
            resBuzzer = message
            timeBuzzer += 1
        elif device == LCD:
            global resLCD, timeLCD
            message = str(message.payload.decode("utf-8"))
            resLCD = message
            timeLCD += 1

    client = mqtt.Client(client_id=str(random.randint(0,1000)))
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect(BROKER, 1883, 60)
    client.subscribe(topic)
    client.loop_forever()