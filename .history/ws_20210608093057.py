from flask import Flask
from flask_sock import Sock
import time

app = Flask(__name__)
sock = Sock(app)



import threading

BROKER = 'io.adafruit.com'
USER = 'khanhdk0000'
PASSWORD = 'aio_FfID10QWNVSKUC2j15nLtOSeckin'
TOPIC = 'khanhdk0000/feeds/light'

res = '"id":"13","name":"LIGHT","data":"0","unit":""'


def mqttGet(user, password,topic):
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
        global res
        message = str(message.payload.decode("utf-8"))
        print(message)
        res = message

    client = mqtt.Client()
    client.username_pw_set(username=user,password=password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect(BROKER, 1883, 60)
    client.subscribe(topic)
    # client.publish("khanhdk0000/feeds/light", "123456779")
    client.loop_forever()

t1 = threading.Thread(target=mqttGet, name=mqttGet, args=(USER, PASSWORD,TOPIC))
t1.start()


i = 0
@sock.route('/reverse')
def reverse(ws):
    while True:
        global i
        time.sleep(3)
        i += 1
        ws.send(i)
        
       


if __name__ == '__main__':
    app.run(debug=True)