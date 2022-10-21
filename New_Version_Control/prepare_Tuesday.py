import time

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import subprocess

app = Flask(__name__)

CORS(app, cors_allowed_origins="*")

socketio = SocketIO(app, cors_allowed_origins='*')
# today = datetime.date.today()
# long = str(today)
# timelist = long.split("-")
# short = timelist[1] + timelist[2]
# lastint = int(short) - 14
# last = str(lastint)


# print(last)

delete_last_release = "svn delete svn://local.svn.badam.mobi/NinjaMustDie/ParkourUnityProject_release -m " \
                      "'release_Unity_project_branch_delete' "
create_new_release = "svn cp -m 'release_Unity_project_branch_create'" \
                     " svn://local.svn.badam.mobi/NinjaMustDie/ParkourUnityProject " \
                     "svn://local.svn.badam.mobi/NinjaMustDie/ParkourUnityProject_release"


@socketio.on('connect')
def start_connect():
    print("Auto Connected")
    emit("connected", "Auto connected")


@socketio.on('emit')
def prepare(data):
    if data["step"] == "start":
        print(data)
        pipe = subprocess.Popen("ping www.baidu.com -n 100", stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                bufsize=0)
        i = 1
        while True:
            line = pipe.stdout.readline().decode("gbk")
            if line != "":
                emit("emit", line)
                print(line)
                i = i + 1
                i = i + 1
                time.sleep(0.1)
            else:
                print("终止空字符串")
                break
    elif data["step"] == "save":
        last = data["date"]
        lines=""
        save_last_version = "svn cp -m '{}归档' svn://local.svn.badam.mobi/NinjaMustDie/ParkourUnityProject_release " \
                            "svn://local.svn.badam.mobi/NinjaMustDie/tag_HistoryVersion/" \
                            "ParkourUnityProject_release_{} ".format(last, last)
        # print(last,type(last))
        if last != "":
            pipe = subprocess.Popen(save_last_version, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                                    bufsize=0)
            i = 1
            while True:
                line = pipe.stdout.readline().decode("gbk")
                lines=lines+line
                if line != "":
                    emit("emit", line)
                    print(line)
                    i = i + 1
                    time.sleep(0.1)
                else:
                    print("终止空字符串")
                    break
        else:
            return "日期读取失败,请到服务端查看日志!"
        time.sleep(3)
        reply = "归档成功!\n" + "NinjaMustDie/tag_History/ParkourUnityProject_release_" + last
        print(reply)
        if "revision" in lines:
            emit("emit",reply)
        else:
            emit("emit","归档出现异常,请到服务端查看日志!")
    elif data["step"] == "delete":
        pipe = subprocess.Popen(delete_last_release, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                                bufsize=0)
        i = 1
        while True:
            line = pipe.stdout.readline().decode("gbk")
            if line != "":
                emit("emit", line)
                print(line)
                i = i + 1
                time.sleep(0.1)
            else:
                print("终止空字符串")
                break
    elif data["step"] == "create":
        pipe = subprocess.Popen(create_new_release, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                                bufsize=0)
        i = 1
        while True:
            line = pipe.stdout.readline().decode("gbk")
            if line != "":
                emit("emit", line)
                print(line)
                i = i + 1
                time.sleep(0.1)
            else:
                print("终止空字符串")
                break
    elif data["step"] == "test":
        pass  #留给testhttp的接口

    else:
        print("pipe未启动")
        emit("emit", "检查启动参数是否正确")


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
