from flask import Flask, jsonify, request
from flask_sock import Sock
import time
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




resLight = '"id":"13","name":"LIGHT","data":"0","unit":""'
prevLight = resLight

resTemp = '"id":"7","name":"SOUND","data":"0","unit":""'
prevTemp = resTemp

resSound = '"id":"12","name":"TEMP-HUMID","data":"0","unit":""'
prevSound = resSound



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
        
        if device == LIGHT:
            global resLight
            message = str(message.payload.decode("utf-8"))
            print(message)
            resLight = message
        elif device == TEMP:
            global resTemp
            message = str(message.payload.decode("utf-8"))
            print(message)
            resTemp = message
        elif device == SOUND:
            global resSound
            message = str(message.payload.decode("utf-8"))
            print(message)
            resSound = message

    client = mqtt.Client(client_id=str(random.randint(0,1000)))
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect(BROKER, 1883, 60)
    client.subscribe(topic)
    client.loop_forever()

t1 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + LIGHT, LIGHT))
t1.start()

t2 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + TEMP, TEMP))
t2.start()

t3 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + SOUND, SOUND))
t3.start()

t4 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + BUZZER, BUZZER))
t4.start()


t4 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC + SOUND, SOUND))
t4.start()


def mqttPost(topic, user, password,payload):
    import paho.mqtt.publish as publish
    publish.single(topic,hostname="io.adafruit.com",auth={"username":user, "password":password},payload = payload)


@sock.route('/light')
def light(ws):
    global resLight, prevLight
    while True:
        if prevLight == resLight:
            continue
        else:
            ws.send(resLight)
            prevLight = resLight

@sock.route('/sound')
def sound(ws):
    global resSound, prevSound
    while True:
        if prevSound == resSound:
            continue
        else:
            ws.send(resSound)
            prevSound = resSound

@sock.route('/temp')
def temp(ws):
    global resTemp, prevTemp
    while True:
        if prevTemp == resTemp:
            continue
        else:
            ws.send(resTemp)
            prevTemp = resTemp



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
    app.run(debug=True)