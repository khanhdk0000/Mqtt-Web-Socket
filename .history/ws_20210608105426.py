from flask import Flask, jsonify, request
from flask_sock import Sock
import time

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
# TEMP = 'bk-iot-temp-humid'
# LCD = 'bk-iot-lcd'
# BUZZER = 'bk-iot-speaker'




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
            resLight = message
        elif device == TEMP:
            global resTemp
            message = str(message.payload.decode("utf-8"))
            resTemp = message
        elif device == SOUND:
            global resSound
            message = str(message.payload.decode("utf-8"))
            resSound = message

    client = mqtt.Client()
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



@app.route('/test2', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True)
     domain = input_json['data']
     
     return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)