import os, subprocess
import datetime
import time

from flask import Flask, request, abort
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

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

@app.route("/prepare", methods=['get', 'post'])
def prepare():
    data = request.get_json()
    if data["step"] == "save":
        last=data["date"]
        save_last_version = "svn cp -m '{}归档' svn://local.svn.badam.mobi/NinjaMustDie/ParkourUnityProject_release " \
                            "svn://local.svn.badam.mobi/NinjaMustDie/tag_HistoryVersion/" \
                            "ParkourUnityProject_release_{} ".format(last, last)
        # print(last,type(last))
        if last!="":
            pipe=subprocess.Popen(save_last_version,stdout=subprocess.PIPE,stdin=subprocess.PIPE,shell=True,bufsize=0)
            msg=pipe.stdout.read().decode("utf-8")
            pipe.kill()
            pipe.wait()
        else:
            return "日期读取失败,请到服务端查看日志!"
        time.sleep(3)
        reply="归档成功!\n"+"NinjaMustDie/tag_History/ParkourUnityProject_release_"+last
        print(reply)
        if "revision" in msg:
            return reply
        else:
            return "归档出现异常,请到服务端查看日志!"
    elif data["step"] == "delete":
        pipe = subprocess.Popen(delete_last_release, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, bufsize=0)
        msg = pipe.stdout.read().decode("gbk")
        print(msg, type(msg))
        pipe.kill()
        pipe.wait()
        return (msg)
    elif data["step"] == "create":
        pipe = subprocess.Popen(create_new_release, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                                bufsize=0)
        msg = pipe.stdout.read().decode("gbk")
        print(msg, type(msg))
        pipe.kill()
        pipe.wait()
        return (msg)
    elif data["step"] == "test":
        s="d: && cd D:/PARKOR"
        try:
            pipe=subprocess.Popen(s,stdout=subprocess.PIPE,stdin=subprocess.PIPE,shell=True,bufsize=0)
            msg=pipe.stdout.read()
            return msg
        except Exception:
            return "运行异常"







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
