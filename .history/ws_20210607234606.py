from flask import Flask
from flask_sock import Sock
import time

app = Flask(__name__)
sock = Sock(app)

i = 0
@sock.route('/reverse')
def reverse(ws):
    while True:
        global i
        time.sleep(3)
        i += 1
        ws.send(i)
        ws.
       


if __name__ == '__main__':
    app.run(debug=True)