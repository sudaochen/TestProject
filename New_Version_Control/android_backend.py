import os
import subprocess
import time

from flask import Flask, request
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

basic_path = "cd /Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release"
upload_1_script = "python upload_util.py --platform=Android --action=upload_to_svn --source=web"
upload_2_script = "python upload_util.py --platform=Android --action=upload_to_svn_2 --source=web"
remote_1_script = "python upload_util.py --platform=Android --action=upload_to_remote --source=web"
remote_2_script = "python upload_util.py --platform=Android --action=upload_to_remote_2 --source=web"
check_script = "python upload_util.py --platform=Android --action=asset_check --source=web"
unzip_script = "python upload_util.py --platform=Android --action=unzip --source=web"
temp_1_script = "python upload_util.py --platform=Android --action=upload_global_info_temp --source=web"
temp_2_script = "python upload_util.py --platform=Android --action=upload_global_info_temp_2 --source=web"
maintain_script = "python upload_util.py --platform=Android --action=open_maintain --source=web"
maintain_2_script = "python upload_util.py --platform=Android --action=open_maintain_2 --source=web"

global_script = "python upload_util.py --platform=Android --action=upload_global_info --source=web"
global_2_script = "python upload_util.py --platform=Android --action=upload_global_info_2 --source=web"


@app.route("/main", methods=["get", "post"])
def operate():

    data = request.get_json()
    if data["step"] == "upload_to_svn_1":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_to_svn --source=web",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg=pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()

        print(msg)
        return msg

    if data["step"] == "upload_to_svn_2":

        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_to_svn_2 --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg

    elif data["step"] == "upload_to_remote":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_to_remote --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg
    elif data["step"] == "upload_to_remote_2":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_to_remote_2 --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg



    elif data["step"] == "asset_check":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=asset_check --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg

    elif data["step"] == "unzip":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=unzip --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg
    elif data["step"] == "temp_1":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_global_info_temp --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg
    elif data["step"] == "temp_2":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_global_info_temp_2 --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg

    # 以下为周四时使用
    # 开维护
    elif data["step"] == 'maintain':
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=open_maintain --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg
    elif data["step"] == 'maintain_2':
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=open_maintain_2 --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg



    # 发正式patch
    elif data["step"] == "global_1":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_global_info --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg
    # 发正式patch
    elif data["step"] == "global_2":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_global_info_2 --source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg





    elif data["step"] == "test":
        pipe = subprocess.Popen("python upload_util.py --platform=Android --action=upload_to_svn--source=web ",
                                cwd="/Users/guangyi/NinjaMustDie/Tools/depoly_asset_bundle_release",
                                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        msg = pipe.stdout.read().decode("utf-8")
        pipe.kill()
        pipe.wait()
        print(msg)
        return msg



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


