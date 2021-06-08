from flask import Flask
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




resLight = '"id":"12","name":"LIGHT","data":"0","unit":""'
prevLight = resLight

resTemp = '"id":"13","name":"SOUND","data":"0","unit":""'
prevTemp = resTemp

resSound = '"id":"7","name":"TEMP-HUMID","data":"0","unit":""'
prevSound = resSound



def mqttLight(user, password,topic,device):
    import paho.mqtt.client as mqtt
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        if rc == 0:
            print('good')
        else:
            print('no good')

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

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
        elif device == TEMP:
            global resSound
            message = str(message.payload.decode("utf-8"))
            resS = message

    client = mqtt.Client()
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect(BROKER, 1883, 60)
    client.subscribe(topic)
    client.loop_forever()

t1 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC))
t1.start()




@sock.route('/reverse')
def reverse(ws):
    global res, prev
    while True:
        if prev == res:
            continue
        else:
            ws.send(res)
            prev = res
        
       


if __name__ == '__main__':
    app.run(debug=True)