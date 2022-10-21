import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import subprocess


app = Flask(__name__)

CORS(app, cors_allowed_origins="*")

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/flask_t")
def flask_t():
    return "Flask is also running"


@socketio.on('connect')
def start_connect():
    print("Auto Connected")

@socketio.on('ensureconnect')
def ensure_connect(message):
    print(message)


@socketio.on('message')
def handle_message(message):
    print(message)


@socketio.on('emit')
def handle_message(data):
    if data["step"]=="start":
        print(data)
        pipe=subprocess.Popen("ping www.baidu.com -n 100",stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                              bufsize=0)
        i=1
        while True:
            line=pipe.stdout.readline().decode("gbk")
            if line != "":
                emit("emit", line)
                print(line)
                i=i+1
                time.sleep(0.1)
            else:
                print("终止空字符串")
                break

    else:
        print("pipe未启动")
        emit("emit","检查启动参数是否正确")










if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)



