from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@sock.@app.route('/route_name')
def method_name():
   pass