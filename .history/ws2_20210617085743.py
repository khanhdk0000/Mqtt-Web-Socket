import sys
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