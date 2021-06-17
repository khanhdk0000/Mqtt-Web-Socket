from flask import Flask, jsonify, request
from flask_sock import Sock
import time
import paho.mqtt.client as mqtt
import random

app = Flask(__name__)
sock = Sock(app)



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

########
# USER = 'CSE_BBC'
# PASSWORD = 'aio_FfID10QWNVSKUC2j15nLtOSeckin'
# TOPIC = 'CSE_BBC/feeds/'

# USER1 = 'CSE_BBC1'
# PASSWORD1 = 'aio_FfID10QWNVSKUC2j15nLtOSeckin'
# TOPIC1 = 'CSE_BBC1/feeds/'


# LIGHT = 'bk-iot-light'
# SOUND = 'bk-iot-sound'
# TEMP = 'bk-iot-temp-humid' ## CSE_BBC
# LCD = 'bk-iot-lcd'        ## CSE_BBC
# BUZZER = 'bk-iot-speaker'  ## CSE_BBC

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

# client = mqtt.Client()
def firstMqtt(user, password):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        if rc == 0:
            print('good')
        else:
            print('no good')

    def on_disconnect(client, userdata, flags, rc=0):
        print("Disconnected result code " + str(rc))

    def on_message_light(client, userdata, message):
        print(message.payload.decode("utf-8"))
        global resLight, timeLight
        message = str(message.payload.decode("utf-8"))
        resLight = message
        timeLight += 1

    def on_message_temp(client, userdata, message):
        print(message.payload.decode("utf-8"))
        global resTemp, timeTemp
        message = str(message.payload.decode("utf-8"))
        resTemp = message
        timeTemp += 1

    ### topic message
    def on_message(mosq, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    client = mqtt.Client()
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.message_callback_add(TOPIC )


    client.connect(BROKER, 1883, 60)
    client.subscribe("khanhdk0000/feeds/#")
    client.loop_forever()

    


def mqttGet(user, password,topic,device):

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
    # global client
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect(BROKER, 1883, 60)
    client.subscribe(topic)
    client.loop_forever()

t1 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + LIGHT, LIGHT))
t1.setDaemon(True)
t1.start()

t2 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + TEMP, TEMP))
t2.setDaemon(True)
t2.start()

t3 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + SOUND, SOUND))
t3.setDaemon(True)
t3.start()

t4 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + BUZZER, BUZZER))
t4.setDaemon(True)
t4.start()

t5 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + LCD, LCD))
t5.setDaemon(True)
t5.start()


def mqttPost(topic, user, password,payload):
    import paho.mqtt.publish as publish
    publish.single(topic,hostname="io.adafruit.com",auth={"username":user, "password":password},payload = payload)


@sock.route('/light')
def light(ws):
    global resLight, prevLight, timeLight, prevTimeLight
    while True:
        if (prevLight == resLight) and (timeLight == prevTimeLight):
            continue
        else:
            ws.send(resLight)
            prevLight = resLight
            prevTimeLight = timeLight

@sock.route('/sound')
def sound(ws):
    global resSound, prevSound, timeSound, prevTimeSound
    while True:
        if (prevSound == resSound) and (timeSound == prevTimeSound):
            continue
        else:
            ws.send(resSound)
            prevSound = resSound
            prevTimeSound = timeSound

@sock.route('/temp')
def temp(ws):
    global resTemp, prevTemp, timeTemp, prevTimeTemp
    while True:
        if (prevTemp == resTemp) and (prevTimeTemp == timeTemp):
            continue
        else:
            ws.send(resTemp)
            prevTemp = resTemp
            prevTimeTemp = timeTemp

@sock.route('/buzzer')
def buzzer(ws):
    global resBuzzer, prevBuzzer,timeBuzzer, prevTimeBuzzer
    while True:
        if (prevBuzzer == resBuzzer) and (prevTimeBuzzer == timeBuzzer):
            continue
        else:
            ws.send(resBuzzer)
            prevBuzzer = resBuzzer
            prevTimeBuzzer = timeBuzzer

@sock.route('/lcd')
def lcd(ws):
    global resLCD, prevLCD, timeLCD, prevTimeLCD
    while True:
        if (prevLCD == resLCD) and (prevTimeLCD == timeLCD):
            continue
        else:
            ws.send(resLCD)
            prevLCD = resLCD
            prevTimeLCD = timeLCD


@app.route('/postlcd', methods=["POST"])
def postlcd():
    input_json = request.get_json(force=True)
    data = input_json['data']
    print('receive data', data)
    mqttPost(TOPIC+LCD, USER, PASSWORD, f'{{"id":"3", "name":"LCD", "data":"{data}", "unit":""}}')
    return 'yea: ' + data

@app.route('/postbuzzer', methods=["POST"])
def postbuzzer():
    input_json = request.get_json(force=True)
    data = input_json['data']
    print('receive data', data)
    mqttPost(TOPIC+BUZZER, USER, PASSWORD, f'{{"id":"2", "name":"SPEAKER", "data":"{data}", "unit":""}}')
    return 'yea: ' + data

if __name__ == '__main__':
    app.run()