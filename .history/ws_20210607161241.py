from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@sock.route('/reverse')
def reverse(ws):
   while True:
       text =  ws.receive()
       ws.send(text[::-1])
       ws.


if __name__ == '__main__':
    app.run(debug=True)