from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@sock.route('/route_name')
def method_name():
   pass