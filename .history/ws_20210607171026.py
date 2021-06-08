from flask import Flask
from flask_sock import Sock
import time

app = Flask(__name__)
sock = Sock(app)

i = 0
@sock.route('/reverse')
def reverse(ws):
    while True:
    #    text =  ws.receive()
    #    ws.send(text[::-1])
        time.sleep(3)
        i += 1
        ws.send(1)
       


if __name__ == '__main__':
    app.run(debug=True)